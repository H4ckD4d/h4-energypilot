#!/usr/bin/env python3
"""SEO smoke validation for pre-rendered locale content."""
import argparse,json,sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
LANGS=('pt-BR','en','es')
class Meta(HTMLParser):
    def __init__(self):
        super().__init__();self.lang='';self.title='';self.in_title=False;self.meta={};self.links=[];self.jsonld=[];self.in_jsonld=False;self.buf=''
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='html':self.lang=d.get('lang')
        if tag=='title':self.in_title=True
        if tag=='link':self.links.append(d)
        if tag=='meta':self.meta[d.get('name') or d.get('property')]=d.get('content')
        if tag=='script' and d.get('type')=='application/ld+json':self.in_jsonld=True;self.buf=''
    def handle_data(self,data):
        if self.in_title:self.title+=data
        if self.in_jsonld:self.buf+=data
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
        if tag=='script' and self.in_jsonld:self.in_jsonld=False;self.jsonld.append(json.loads(self.buf))

def verify(directory,public=False):
    out=Path(directory);pages=[]
    for lang in LANGS:
        for route in ('','about','demo'):
            path=out/lang/(route if route else '')/'index.html'
            assert path.exists(),path
            p=Meta();p.feed(path.read_text(encoding='utf-8'))
            assert p.lang==lang,(path,p.lang)
            assert p.title and p.meta.get('description'),path
            assert p.meta.get('og:title') and p.meta.get('og:image') and p.meta.get('twitter:card'),path
            assert len(p.jsonld)==1 and p.jsonld[0].get('creator',p.jsonld[0].get('author')),path
            canon=[x['href'] for x in p.links if x.get('rel')=='canonical'];assert len(canon)==1,path
            alt={x['hreflang']:x['href'] for x in p.links if x.get('rel')=='alternate' and x.get('hreflang')}
            assert set(alt)=={'pt-BR','en','es','x-default'},path
            assert canon[0]==alt[lang],path
            assert alt['x-default']==alt['en'],path
            assert ('noindex' not in p.meta.get('robots',''))==(public and route!='demo'),path
            pages.append((lang,route,canon[0]))
    all_urls=[url for _,route,url in pages if route!='demo']
    robots=(out/'robots.txt').read_text()
    if public:
        assert 'Sitemap:' in robots and 'Allow:' in robots
        tree=ET.parse(out/'sitemap.xml')
        ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
        entries=tree.findall('s:url',ns)
        assert len(entries)==6
        for e in entries:
            url=e.find('s:loc',ns).text
            assert url in all_urls and urlsplit(url).scheme=='https'
            links=e.findall('x:link',ns)
            assert {x.attrib['hreflang'] for x in links}=={'pt-BR','en','es','x-default'}
        assert 'Disallow: /' not in robots
    else:
        assert 'Disallow: /' in robots
        assert not (out/'sitemap.xml').exists()
    print(f'SEO verified: {len(pages)} localized pages; mode={"public" if public else "preview"}')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory');p.add_argument('--public',action='store_true');a=p.parse_args()
    verify(a.directory,public=a.public)
