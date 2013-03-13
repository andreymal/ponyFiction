from lxml import etree
from ..base import xslt_transform_loader, html_doc_transform

xslt_transform_function = xslt_transform_loader(__file__)

pre_normalize_html = xslt_transform_function('pre-normalize-html.xslt')
post_normalize_html = xslt_transform_function('post-normalize-html.xslt')

@html_doc_transform
def normalize_html(doc):
    doc = pre_normalize_html(doc)
    doc = split_elements(doc, separators = ['p-splitter'])
    # TODO: squash nested paragraph attributes
    doc = post_normalize_html(doc)
    return doc

@html_doc_transform
def split_elements(doc, separators = []):
    body = doc.xpath('//body')[0]
    children = body[:]
    body[:] = []
    
    body.extend(f 
        for e in children
        for f in iter_splitted_elements(e, separators)
    )
    
    return doc
    
    
def iter_splitted_elements(element, separators):
    children = element.getchildren()
    if len(children) == 0:
        yield element
        return
    
    tag = element.tag
    attrib = dict(element.attrib)
    accum = []
    for d in children:
        for e in iter_splitted_elements(d, separators):
            if e.tag in separators:
                if len(accum) > 0:
                    x = etree.Element(tag, attrib)
                    x.extend(accum)
                    yield x
                    accum = []
                yield e
            else:
                accum.append(e)
    x = etree.Element(tag, attrib)
    x.extend(accum)
    yield x
