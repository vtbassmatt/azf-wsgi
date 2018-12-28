import logging
import sys

import azure.functions as func

from azf_wsgi import AzureFunctionsWsgi

sys.path.insert(0, './dj_proj')
from django_on_azure.wsgi import application


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return AzureFunctionsWsgi(application).main(req, context)
