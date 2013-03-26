from .base import BaseDownloadFormat

class FB2Download(BaseDownloadFormat):
    extension = 'fb2.zip'
    name = 'FB2'
    debug_content_type = 'text/xml'
    
    def render(self, story, filename, extension, debug = False, **kw):
        import zipfile
        from cStringIO import StringIO
        import lxml.etree as etree
        from ..filters import fb2
        
        chapters = story.chapter_set.order_by('order')
        chapters = [fb2.html_to_fb2(c.text_as_html, title = c.title) for c in chapters]
        chapters = [self._get_annotation_doc(story)] + chapters
        
        doc = fb2.join_fb2_docs(
            chapters,
            title = story.title,
            author_name = story.authors.all()[0].username, # TODO: multiple authors
        )
        data = etree.tostring(doc, encoding = 'utf8', xml_declaration = True)
        
        if not debug:
            buf = StringIO()
            
            zf = zipfile.ZipFile(buf, mode = 'w', compression = zipfile.ZIP_DEFLATED)
            zf.writestr(filename + '.fb2', data)
            zf.close()
        
            data = buf.getvalue()
        
        return data
        
    def _get_annotation_doc(self, story):
        from ..filters import fb2
        
        doc = fb2.html_to_fb2('<html><head><annotation>%s</annotation></head><body></body></html>' % story.summary_as_html)
        for body in doc.xpath('//fb2:body', namespaces = { 'fb2': 'http://www.gribuser.ru/xml/fictionbook/2.0' }):
            body.getparent().remove(body)
            
        return doc