import os
from django.conf import settings
from django.template import Origin, TemplateDoesNotExist
import zipfile
from django.template.loaders.base import Loader as BaseLoader

import warnings
from django.utils.deprecation import RemovedInDjango20Warning

class ZipOrigin(Origin):
    def __init__(self, zfile, *args,**kwargs):
        self.zfile = zfile
        super(ZipOrigin, self).__init__(*args,**kwargs)

class Loader(BaseLoader):
    def __init__(self, engine):
        self.engine = engine

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Return an Origin object pointing to an absolute path in each directory
        in template_dirs. For security reasons, if a path doesn't lie inside
        one of the template_dirs it is excluded from the result set.
        """

        template_zipfiles = getattr(settings, "TEMPLATE_ZIP_FILES", ['library.zip'])

        # Try each ZIP file in TEMPLATE_ZIP_FILES.
        for fname in template_zipfiles:
            try:
                z = zipfile.ZipFile(fname)
                source = z.read('templates/%s' % (template_name))
            except (IOError, KeyError):
                continue
            z.close()
            # We found a template, so return the source.
            template_path = "%s:%s" % (fname, template_name)    
            yield ZipOrigin(
                zfile=fname,
                name=template_path,
                template_name=template_name,
                loader=self,
                )

    def get_contents(self, origin):
        try:
            z = zipfile.ZipFile(origin.zfile)
            source = z.read('templates/%s' % (origin.template_name))
        except Exception:
            raise TemplateDoesNotExist(origin)

        return source



    def load_template_source(template_name, template_dirs=None):
        warnings.warn(
            'The load_template_sources() method is deprecated. Use '
            'get_template() or get_contents() instead.',
            RemovedInDjango20Warning,
        )
        for origin in self.get_template_sources(template_name):
            try:
                return self.get_contents(origin), origin.name
            except TemplateDoesNotExist:
                pass
        raise TemplateDoesNotExist(template_name)