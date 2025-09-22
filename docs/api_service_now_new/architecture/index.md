# Diagramas de Arquitetura

## Visão Geral

Esta seção apresenta diagramas detalhados da arquitetura do sistema `api_service_now_new`, mostrando como funcionam as atualizações das duas views principais e o disparo das threads.

## Arquitetura Geral do Sistema

```mermaid
graph TB
    subgraph "Cliente"
        A[Aplicação Cliente]
    end
    
    subgraph "Django Application"
        subgraph "API Layer"
            B[LoadIncidentsView]
            C[LoadConfigurationsView]
        end
        
        subgraph "Background Processing"
            D[Thread Pool Incidents]
            E[Thread Pool Configurations]
        end
        
        subgraph "Task Layer"
            F[LoadIncidentsOpened]
            G[LoadIncidentSla]
            H[LoadIncidentTask]
            I[LoadTaskTimeWorked]
            J[LoadContractSla]
            K[LoadGroups]
            L[LoadSysCompany]
            M[LoadSysUser]
            N[LoadCmdbCiNetworkLink]
        end
        
        subgraph "Data Layer"
            O[ServiceNow API]
            P[(Database)]
            Q[ServiceNowExecutionLog]
        end
    end
    
    A -->|POST /load-incidents/| B
    A -->|POST /load-configurations/| C
    
    B -->|Spawn Thread| D
    C -->|Spawn Thread| E
    
    B -->|HTTP 200 Immediate| A
    C -->|HTTP 200 Immediate| A
    
    D --> F
    D --> G  
    D --> H
    D --> I
    
    E --> J
    E --> K
    E --> L
    E --> M
    E --> N
    
    F --> O
    G --> O
    H --> O
    I --> O
    J --> O
    K --> O
    L --> O
    M --> O
    N --> O
    
    F --> P
    G --> P
    H --> P
    I --> P
    J --> P
    K --> P
    L --> P
    M --> P
    N --> P
    
    D --> Q
    E --> Q
```

## Fluxo LoadIncidentsView

### Sequência Completa

```mermaid
sequenceDiagram
    participant Client as Cliente HTTP
    participant View as LoadIncidentsView
    participant Thread as Background Thread
    participant Log as ExecutionLog
    participant T1 as LoadIncidentsOpened
    participant T2 as LoadIncidentSla
    participant T3 as LoadTaskTimeWorked
    participant T4 as LoadIncidentTask
    participant API as ServiceNow API
    participant DB as Database
    
    Note over Client,DB: Fase 1: Requisição e Resposta Imediata
    Client->>View: POST /load-incidents/
    Note over View: Parse data_inicio, data_fim
    View->>View: patch_requests_ssl()
    View->>Thread: Create daemon thread
    View-->>Client: HTTP 200 {"status": "accepted"}
    
    Note over Thread,DB: Fase 2: Execução Background
    Thread->>Log: Create execution log (status: running)
    
    par Execução Paralela (4 threads)
        Thread->>T1: Start LoadIncidentsOpened
        and
        Thread->>T2: Start LoadIncidentSla
        and  
        Thread->>T3: Start LoadTaskTimeWorked
        and
        Thread->>T4: Start LoadIncidentTask
    end
    
    par API Calls Simultâneas
        T1->>API: GET /incident (opened_at filter)
        and
        T2->>API: GET /task_sla (sys_created_on filter)
        and
        T3->>API: GET /time_worked (sys_created_on filter)
        and
        T4->>API: GET /incident_task (sys_created_on filter)
    end
    
    par Processamento de Dados
        API-->>T1: Incident data (paginated)
        T1->>T1: Transform to Polars DataFrame
        T1->>DB: DELETE + BULK INSERT
        and
        API-->>T2: SLA data (paginated) 
        T2->>T2: Transform to Polars DataFrame
        T2->>DB: DELETE + BULK INSERT
        and
        API-->>T3: Time worked data
        T3->>T3: Transform to Polars DataFrame
        T3->>DB: DELETE + BULK INSERT
        and
        API-->>T4: Task data
        T4->>T4: Transform to Polars DataFrame
        T4->>DB: DELETE + BULK INSERT
    end
    
    Note over Thread: Aguarda todas as threads (.join())
    Thread->>Log: Update execution log (status: success/error)
    Thread->>Thread: Complete
```

### Detalhamento do Threading

```mermaid
graph TD
    subgraph "LoadIncidentsView._run_pipelines_in_background"
        A[Create ServiceNowExecutionLog]
        
        subgraph "Parallel Execution Block"
            B[Create Thread 1: LoadIncidentsOpened]
            C[Create Thread 2: LoadIncidentSla]
            D[Create Thread 3: LoadTaskTimeWorked] 
            E[Create Thread 4: LoadIncidentTask]
        end
        
        F[thread.start() for all threads]
        G[thread.join() for all threads]
        H[Update ExecutionLog with results]
    end
    
    A --> B
    A --> C
    A --> D
    A --> E
    
    B --> F
    C --> F
    D --> F
    E --> F
    
    F --> G
    G --> H
    
    style B fill:#e1f5fe
    style C fill:#e1f5fe
    style D fill:#e1f5fe
    style E fill:#e1f5fe
```

## Fluxo LoadConfigurationsView

### Sequência Completa

```mermaid
sequenceDiagram
    participant Client as Cliente HTTP
    participant View as LoadConfigurationsView
    participant Thread as Background Thread
    participant Log as ExecutionLog
    participant Batch1 as Batch 1 (3 threads)
    participant Batch2 as Batch 2 (2 threads)
    participant API as ServiceNow API
    participant DB as Database
    
    Note over Client,DB: Fase 1: Requisição e Resposta Imediata
    Client->>View: POST /load-configurations/
    View->>View: patch_requests_ssl()
    View->>Thread: Create daemon thread  
    View-->>Client: HTTP 200 {"status": "accepted"}
    
    Note over Thread,DB: Fase 2: Execução em Lotes
    Thread->>Log: Create execution log (status: running)
    
    Note over Thread: Batch 1: Máximo 3 threads simultâneas
    par Lote 1 (3 threads)
        Thread->>Batch1: LoadContractSla
        and
        Thread->>Batch1: LoadGroups
        and
        Thread->>Batch1: LoadSysCompany
    end
    
    par API Calls Lote 1
        Batch1->>API: GET /contract_sla
        and
        Batch1->>API: GET /sys_user_group
        and
        Batch1->>API: GET /sys_company
    end
    
    par Processamento Lote 1
        API-->>Batch1: Contract SLA data
        Batch1->>DB: UPSERT by sys_id
        and
        API-->>Batch1: Groups data
        Batch1->>DB: UPSERT by sys_id
        and
        API-->>Batch1: Company data
        Batch1->>DB: UPSERT by sys_id
    end
    
    Note over Thread: Aguarda conclusão do Lote 1
    
    Note over Thread: Batch 2: Próximas 2 tasks
    par Lote 2 (2 threads)
        Thread->>Batch2: LoadSysUser
        and
        Thread->>Batch2: LoadCmdbCiNetworkLink
    end
    
    par API Calls Lote 2
        Batch2->>API: GET /sys_user
        and
        Batch2->>API: GET /cmdb_ci_network_link
    end
    
    par Processamento Lote 2
        API-->>Batch2: User data
        Batch2->>DB: UPSERT by sys_id
        and
        API-->>Batch2: Network link data
        Batch2->>DB: UPSERT by sys_id
    end
    
    Note over Thread: Aguarda conclusão do Lote 2
    Thread->>Log: Update execution log (status: success/error)
    Thread->>Thread: Complete
```

### Estratégia de Lotes

```mermaid
graph TD
    subgraph "LoadConfigurationsView._run_pipelines_in_background"
        A[Create ServiceNowExecutionLog]
        B[tasks_to_run = 5 tasks]
        C[max_threads = 3]
        
        subgraph "Lote 1 (0:3)"
            D[LoadContractSla]
            E[LoadGroups] 
            F[LoadSysCompany]
        end
        
        G[Aguarda conclusão Lote 1]
        
        subgraph "Lote 2 (3:5)"
            H[LoadSysUser]
            I[LoadCmdbCiNetworkLink]
        end
        
        J[Aguarda conclusão Lote 2]
        K[Update ExecutionLog]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
    C --> F
    
    D --> G
    E --> G
    F --> G
    
    G --> H
    G --> I
    
    H --> J
    I --> J
    
    J --> K
    
    style D fill:#fff3e0
    style E fill:#fff3e0
    style F fill:#fff3e0
    style H fill:#e8f5e8
    style I fill:#e8f5e8
```

## Gerenciamento de Threads

### Thread Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Created: threading.Thread()
    Created --> Started: thread.start()
    Started --> Running: Execute task
    Running --> API_Call: Paginate ServiceNow
    API_Call --> Processing: Transform data
    Processing --> Database: Upsert/Delete+Insert
    Database --> Completed: Task finished
    Database --> Error: Exception occurred
    Completed --> Joined: thread.join()
    Error --> Joined: thread.join()
    Joined --> [*]: Thread cleanup
    
    Running --> Running: Multiple API pages
    Processing --> Processing: Batch processing
```

### Thread Safety

```mermaid
graph TB
    subgraph "Thread Safety Mechanisms"
        A[Daemon Threads]
        B[Separate Error Lists]
        C[Separate Result Dicts]
        D[Database Transactions]
        E[Exception Isolation]
    end
    
    subgraph "Shared Resources"
        F[Database Connection Pool]
        G[ServiceNow API]
        H[ServiceNowExecutionLog]
    end
    
    subgraph "Risk Mitigation"
        I[Connection Pooling]
        J[API Rate Limiting]
        K[Atomic Transactions]
    end
    
    A --> I
    B --> E
    C --> E
    D --> K
    E --> K
    
    F --> I
    G --> J
    H --> K
    
    style A fill:#c8e6c9
    style D fill:#c8e6c9
    style E fill:#c8e6c9
```

## Pipeline de Dados

### ETL Flow per Task

```mermaid
flowchart TD
    subgraph "Extract Phase"
        A[Build ServiceNow Query]
        B[Get Field List from Model]
        C[Call paginate() function]
        D[Handle API Pagination]
        E[Collect All Records]
    end
    
    subgraph "Transform Phase" 
        F[Create Polars DataFrame]
        G[Flatten Reference Fields]
        H[Normalize Empty Strings to None]
        I[Add ETL Timestamps]
    end
    
    subgraph "Load Phase"
        J{Load Strategy}
        K[DELETE + INSERT<br/>Incidents Tasks]
        L[UPSERT by sys_id<br/>Configuration Tasks]
        M[Bulk Database Operations]
        N[Update Log Metrics]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    J --> L
    K --> M
    L --> M
    M --> N
    
    style F fill:#e3f2fd
    style M fill:#f3e5f5
```

### Data Flow Diagram

```mermaid
graph LR
    subgraph "ServiceNow"
        A[(incident table)]
        B[(task_sla table)]
        C[(sys_user_group table)]
        D[(sys_user table)]
    end
    
    subgraph "API Layer"
        E[REST API Calls]
        F[JSON Response]
        G[Pagination Handler]
    end
    
    subgraph "Processing"
        H[Polars DataFrame]
        I[Field Mapping]
        J[Data Validation]
        K[Reference Flattening]
    end
    
    subgraph "Database"
        L[(incident)]
        M[(incident_sla)]
        N[(groups)]
        O[(sys_user)]
        P[(execution_log)]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    
    E --> F
    F --> G
    G --> H
    
    H --> I
    I --> J
    J --> K
    
    K --> L
    K --> M
    K --> N
    K --> O
    K --> P
```

## Tratamento de Erros

### Error Handling Flow

```mermaid
flowchart TD
    subgraph "Task Level Errors"
        A[Task Execution Start]
        B{API Call Success?}
        C{Data Processing OK?}
        D{Database Save OK?}
        E[Task Success]
        F[Log Error in errors[] list]
        G[Continue Other Tasks]
    end
    
    subgraph "Thread Level Errors"  
        H[Aggregate All Task Results]
        I{Any Errors?}
        J[execution_log.status = 'success']
        K[execution_log.status = 'error']
        L[Save error_message]
    end
    
    A --> B
    B -->|No| F
    B -->|Yes| C
    C -->|No| F  
    C -->|Yes| D
    D -->|No| F
    D -->|Yes| E
    
    F --> G
    E --> G
    G --> H
    
    H --> I
    I -->|No| J
    I -->|Yes| K
    K --> L
    
    style F fill:#ffcdd2
    style K fill:#ffcdd2
    style L fill:#ffcdd2
```

### Exception Isolation

```mermaid
graph TB
    subgraph "Main Thread"
        A[LoadIncidentsView.post()]
        B[Create Background Thread]
        C[Return HTTP 200]
    end
    
    subgraph "Background Thread"
        D[_run_pipelines_in_background]
        
        subgraph "Task Thread 1"
            E[LoadIncidentsOpened]
            F{Exception?}
            G[Add to errors[]]
        end
        
        subgraph "Task Thread 2"
            H[LoadIncidentSla]
            I{Exception?}
            J[Add to errors[]]
        end
        
        K[Collect All Results]
        L[Update ExecutionLog]
    end
    
    A --> B
    B --> C
    B --> D
    
    D --> E
    D --> H
    
    E --> F
    F -->|Yes| G
    H --> I  
    I -->|Yes| J
    
    G --> K
    J --> K
    K --> L
    
    style F fill:#ffab91
    style I fill:#ffab91
    style G fill:#ffcdd2
    style J fill:#ffcdd2
```

## Performance Characteristics

### Timing Diagram

```mermaid
gantt
    title Execution Timeline - LoadIncidentsView
    dateFormat X
    axisFormat %s
    
    section Main Thread
    HTTP Request Processing    :0, 1
    Create Background Thread   :1, 2
    Return HTTP 200           :2, 3
    
    section Background Thread
    Create ExecutionLog       :3, 5
    Spawn Parallel Tasks      :5, 7
    Wait for Completion       :7, 180
    Update ExecutionLog       :180, 185
    
    section Task Threads
    LoadIncidentsOpened       :7, 120
    LoadIncidentSla          :7, 150
    LoadTaskTimeWorked       :7, 90
    LoadIncidentTask         :7, 110
    
    section Database Operations
    Delete Old Records       :20, 25
    Bulk Insert New Records  :25, 60
    Update Execution Log     :180, 185
```

### Resource Utilization

```mermaid
graph LR
    subgraph "Resource Usage"
        subgraph "CPU"
            A[API Calls: Low]
            B[Data Transform: Medium]  
            C[DB Operations: High]
        end
        
        subgraph "Memory"
            D[Polars DataFrames: High]
            E[JSON Responses: Medium]
            F[Task Objects: Low]
        end
        
        subgraph "Network"
            G[ServiceNow API: High]
            H[Database: Medium]
        end
        
        subgraph "Database"
            I[Connection Pool: Medium]
            J[Transaction Locks: High]
            K[Disk I/O: High]
        end
    end
    
    style C fill:#ffcdd2
    style D fill:#ffcdd2
    style G fill:#ffcdd2
    style J fill:#ffcdd2
    style K fill:#ffcdd2
```

## Monitoramento e Observabilidade

### Metrics Collection

```mermaid
graph TD
    subgraph "Execution Metrics"
        A[Start Time]
        B[End Time] 
        C[Duration]
        D[Records Processed]
        E[Success/Error Status]
    end
    
    subgraph "Task Metrics"
        F[API Request Count]
        G[Database Operations]
        H[Error Messages]
        I[Performance Timings]
    end
    
    subgraph "System Metrics"
        J[Thread Count]
        K[Memory Usage]
        L[Database Connections]
        M[API Response Times]
    end
    
    subgraph "Storage"
        N[(ServiceNowExecutionLog)]
        O[Application Logs]
        P[System Metrics]
    end
    
    A --> N
    B --> N
    C --> N
    D --> N
    E --> N
    
    F --> O
    G --> O
    H --> O
    I --> O
    
    J --> P
    K --> P
    L --> P
    M --> P
```

Esta documentação fornece uma visão completa de como o sistema funciona, incluindo todos os diagramas detalhados da arquitetura, fluxo das views e gerenciamento de threads conforme solicitado.