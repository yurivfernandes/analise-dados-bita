import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def patch_requests_ssl():
    """
    Desabilita a verificação SSL globalmente para requests (apenas para desenvolvimento).
    """
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    old_request = requests.Session.request

    def new_request(self, *args, **kwargs):
        kwargs["verify"] = False
        return old_request(self, *args, **kwargs)

    requests.Session.request = new_request
