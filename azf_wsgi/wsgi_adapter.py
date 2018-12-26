from io import StringIO
import logging
from urllib.parse import urlparse
from wsgiref.headers import Headers
from wsgiref.handlers import read_environ

import azure.functions as func


class AzureFunctionsWsgi:
    "Convert between Azure Functions API and the WSGI protocol."
    def __init__(self, app, include_os_environ=True):
        self._app = app
        self._include_os_environ = include_os_environ
        self._req = None
        self._context = None

        self._status = None
        self._wsgi_headers = []
        self._azure_headers = None
        self._body = None
        self._errors = StringIO()
        self._environ = []

    def main(self, req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        self._req = req
        self._context = context

        self._get_body()
        self._setup_environ()

        buffer = [x for x in self._app(self._environ, self._start_response)]

        if self._errors.tell() > 0:
            self._errors.seek(0, 0)
            for line in self._errors.readline():
                logging.error(line)

        response_values = self._response_values()

        return func.HttpResponse(b''.join(buffer),
            headers=self._azure_headers,
            **response_values)

    def _get_body(self):
        body_encoding = 'utf-8' # default

        body_content_type = self._req.headers.get('Content-Type')
        if body_content_type and 'charset=' in body_content_type:
            header_parts = body_content_type.split(';')
            for part in header_parts:
                directive, value = part.split('=', maxsplit=1)
                if 'charset' in directive:
                    body_encoding = value
                    break

        self._body = self._req.get_body().decode(body_encoding)

    def _setup_environ(self):
        req_url = urlparse(self._req.url)
        port = req_url.port
        if not port:
            if req_url.scheme == 'https':
                port = 443
            else:
                port = 80

        environ = {
            'REQUEST_METHOD': self._req.method,
            'SCRIPT_NAME': '', # SCRIPT_NAME is always the root
            'PATH_INFO': req_url.path,
            'SERVER_NAME': req_url.hostname,
            'SERVER_PORT': str(port),
            'SERVER_PROTOCOL': 'HTTP/1.1', # TODO
            'SERVER_SOFTWARE': 'azure-functions',
            'wsgi.version': (1,0),
            'wsgi.url_scheme': req_url.scheme,
            'wsgi.input': StringIO(self._body),
            'wsgi.errors': self._errors,
            'wsgi.multithread': True,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'azure_functions.url': self._req.url,
            'azure_functions.function_directory': self._context.function_directory,
            'azure_functions.function_name': self._context.function_name,
            'azure_functions.invocation_id': self._context.invocation_id,
        }

        if req_url.query:
            environ['QUERY_STRING'] = req_url.query

        passthru_headers = ['Content-Type', 'Content-Length']
        for header_name in passthru_headers:
            if header_name in self._req.headers:
                environ[self._header_name(header_name)] = self._req.headers[header_name]

        for header, value in self._req.headers.items():
            environ['HTTP_' + self._header_name(header)] = str(value)

        if self._include_os_environ:
            environ.update(read_environ())

        self._environ = environ

    def _header_name(self, header_name):
        return header_name.replace('-', '_').upper()

    def _start_response(self, status, headers):
        self._status = status
        self._wsgi_headers = headers

    def _response_values(self):
        self._azure_headers = Headers(self._wsgi_headers)

        return {
            'status_code': int(self._status.split(' ')[0]),
            'mimetype': self._azure_headers.get('Content-Type', 'text/plain'),
            'charset': 'utf-8',
        }
