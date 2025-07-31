from django.db.models import Model


class MultiDBRouter:
    """
    Um roteador de banco de dados para direcionar as operações dos módulos dw_analytics e power_bi.
    """

    def db_for_read(self, model, **hints):
        """Direciona leituras das models para o banco correto."""
        if model._meta.app_label == "dw_analytics":
            return "dw_analytics"
        elif model._meta.app_label == "power_bi":
            return "power_bi"
        elif model._meta.app_label == "correios":
            return "correios"
        elif model._meta.app_label == "service_now":
            return "service_now"
        elif model._meta.app_label == "meraki_devices":
            return "default"
        elif model._meta.app_label == "api_service_now":
            return "api_service_now"
        return None

    def db_for_write(self, model, **hints):
        """Direciona escritas das models para o banco correto."""
        if model._meta.app_label == "dw_analytics":
            return "dw_analytics"
        elif model._meta.app_label == "power_bi":
            return "power_bi"
        elif model._meta.app_label == "correios":
            return "correios"
        elif model._meta.app_label == "service_now":
            return "service_now"
        elif model._meta.app_label == "meraki_devices":
            return "default"
        elif model._meta.app_label == "api_service_now":
            return "api_service_now"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Permite relações entre objetos do mesmo banco."""
        if obj1._state.db == obj2._state.db:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Direciona as migrações para o banco correto"""
        if app_label == "dw_analytics":
            return db == "dw_analytics"
        elif app_label == "power_bi":
            return db == "power_bi"
        elif app_label == "correios":
            return db == "correios"
        elif app_label == "service_now":
            return db == "service_now"
        elif app_label == "meraki_devices":
            return db == "default"
        elif app_label == "api_service_now":
            return db == "api_service_now"
        return True
