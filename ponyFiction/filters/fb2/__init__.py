import lxml.etree as etree
from ..base import xslt_transform_loader


xslt_transform_function = xslt_transform_loader(__file__)


html_to_fb2 = xslt_transform_function('html-to-fb2.xslt')
_join_fb2_docs = xslt_transform_function('join-fb2-docs.xslt')

def join_fb2_docs(docs, **kw):
    doc = etree.Element('docs')
    doc.extend(docs)
    return _join_fb2_docs(doc, **kw)
