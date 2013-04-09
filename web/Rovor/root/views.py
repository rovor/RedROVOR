# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader

from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    template = loader.get_template('root/index.html')
    context = Context()
    return HttpResponse(template.render(context))
