from django.http import HttpResponse
import datetime

from .utils import get_installed_packages


def test(request):
    now = datetime.datetime.now()
    deps = get_installed_packages()

    return HttpResponse('''<html>
<body>Hello world!<br/>
%s<br/>
path_info: <code>%s</code><br/>
path: <code>%s</code><br/>
deps: <code>%s</code>
</body>
</html>''' % (now, request.path_info, request.path, deps))
