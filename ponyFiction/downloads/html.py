from .base import ZipFileDownloadFormat

class HTMLDownload(ZipFileDownloadFormat):
    extension = 'html.zip'
    name = 'HTML'
    chapter_template = 'chapter_pure_html.html'
    chapter_extension = 'html'
    