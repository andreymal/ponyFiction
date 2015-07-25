#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template

from ponyFiction import context_processors

register = template.Library()

# это всё только для писем и 500.html


class ProjectSettings(template.Node):
    def render(self, context):
        context.update(context_processors.project_settings(None))
        return ''


@register.tag
def project_settings(parser, token):
    return ProjectSettings()
