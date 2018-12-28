from django.http import HttpResponse
import datetime

# Create your views here.
def test(request):
    now = datetime.datetime.now()
    return HttpResponse('''<html>
<body>Hello world!<br/>
%s<br/>
path_info: <code>%s</code><br/>
path: <code>%s</code><br/>
</body>
</html>''' % (now, request.path_info, request.path))
