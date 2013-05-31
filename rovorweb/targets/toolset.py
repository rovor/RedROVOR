from django.http import HttpResponse
from django.views.generic import View

from mimeparse import best_match



class html_or_json(View):
    html_view = None
    json_view = None

    def dispatch(self,request, *args, **kwargs):
        '''determine appropriate content-type
        and dispatch to that method'''
        content_type = best_match({'text/html','application/json'},
                request.META['HTTP_ACCEPT'])
        if content_type == 'application/json' and self.json_view:
            return self.json_view(request,*args, **kwargs)
        elif content_type == 'text/html' and self.html_view:
            return self.html_view(request, *args, **kwargs)
        else:
            #not acceptable
            return HttpResponse(status_code=406)





