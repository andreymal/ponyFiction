#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from django.utils.safestring import mark_safe
from django.conf import settings

from .typographus import typo
from .base import html_doc_to_string, html_doc_transform, transform_xslt_params
from .html import normalize_html, footnotes_to_html


empty_lines_re = re.compile(r'\n[\s\n]*\n')


def filter_html(text,
                tags = settings.ALLOWED_TAGS,
                attributes = settings.ALLOWED_ATTRIBUTES):
    doc = typo(text)
    doc = normalize_html(doc, convert_linebreaks = True)
    doc = _filter_html(doc,
        tags = tags,
        attributes = attributes
    )
    return doc

def filtered_html_property(name, filter_):
    def fn(self):
        try:
            return mark_safe(html_doc_to_string(filter_(getattr(self, name))))
        except Exception:
            import traceback, sys
            print >> sys.stderr, "filter_html", type(self), self.pk, name, filter_
            traceback.print_exc()
            return "#ERROR#"
    return property(fn)


_filter_transforms = {}   
@html_doc_transform
def _filter_html(doc, tags, attributes, **kw):
    key = repr((tags, attributes))
    
    if key not in _filter_transforms:
        filters = []
        filters.extend(tags)
        for tag, attrs in attributes.items():
            for attr in attrs:
                filters.append('%s/@%s' % (tag, attr))
        filters = '|'.join(filters)
        data = HTML_FILTER_TEMPLATE.replace('@FILTERS@', filters)
        
        from lxml import etree
        _filter_transforms[key] = etree.XSLT(etree.XML(data))
    filter_transform = _filter_transforms[key]
        
    kw = transform_xslt_params(kw)
    return filter_transform(doc, **kw).getroot()


HTML_FILTER_TEMPLATE = """<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:re="http://exslt.org/regular-expressions">

<xsl:template match="html | body | @FILTERS@">
    <xsl:apply-templates select="." mode="default-filters"/>
</xsl:template>

<xsl:template match="@*"/>

<xsl:template match="a/@href[not(re:match(.,'^((https?:)?/|#)'))]" mode="default-filters"/>

<xsl:template match="@*|node()" mode="default-filters">
    <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
</xsl:template>

</xsl:stylesheet>
"""
