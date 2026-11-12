import unittest
from scripts.build_site import build
from scripts.check_seo import verify
from pathlib import Path
import os

class SEOTests(unittest.TestCase):
    def test_preview_prevents_indexing(self):
        build(preview=True)
        verify(Path(__file__).resolve().parents[1]/'site'/'dist',public=False)

    def test_production_requires_explicit_https(self):
        before=os.environ.get('SEO_PUBLIC'),os.environ.get('SITE_URL')
        try:
            os.environ['SEO_PUBLIC']='1';os.environ['SITE_URL']='http://localhost:8080'
            with self.assertRaises(SystemExit):build(preview=False)
        finally:
            for k,v in zip(('SEO_PUBLIC','SITE_URL'),before):
                if v is None:os.environ.pop(k,None)
                else:os.environ[k]=v

    def test_production_sitemap_and_hreflang(self):
        before=os.environ.get('SEO_PUBLIC'),os.environ.get('SITE_URL')
        try:
            os.environ['SEO_PUBLIC']='1';os.environ['SITE_URL']='https://publisher.example.org/my-project'
            build(preview=False)
            verify(Path(__file__).resolve().parents[1]/'site'/'dist',public=True)
        finally:
            for k,v in zip(('SEO_PUBLIC','SITE_URL'),before):
                if v is None:os.environ.pop(k,None)
                else:os.environ[k]=v
