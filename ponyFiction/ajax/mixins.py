# -*- coding: utf-8 -*-
from django.http.response import HttpResponse
from django.template.loader import render_to_string

class AJAXHTTPResponseMixin(object):
    """
    A mixin that can be used to render a template to AJAX response.
    """
    reponse_class = HttpResponse
    
    @property
    def template_name(self):
        return NotImplementedError
    
    def render_to_response(self, context, **response_kwargs):
        rendered = render_to_string(self.template_name, context_instance=context)
        return HttpResponse(rendered)