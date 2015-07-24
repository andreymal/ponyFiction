# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from django.template import RequestContext, loader

def ajax_response(request, data, status=200, render_template=None, template_context=None):
    if render_template:
        template = loader.get_template(render_template)
        template_context = RequestContext(request, template_context or {})
        data = data.copy()
        data['html'] = template.render(template_context)
    return HttpResponse(json.dumps(data, ensure_ascii=False), status=status, content_type='application/json; charset=utf-8')
