#!/usr/bin/env python3
"""Pre-render secure, search-friendly localized pages; no indexing until explicit HTTPS config."""
import argparse,html,json,os,shutil
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
OUT=SITE/'dist'
CONTENT=json.loads((SITE/'content.json').read_text(encoding='utf-8'))
PRODUCT=ROOT.name
LOCALES=['pt-BR','en','es']
SEO_NAMES={'pt-BR':'Português','en':'English','es':'Español'}
UI={
 'pt-BR':dict(home='Início',about='Sobre',demo='Demonstração',start='Explorar demonstração',open='Conheça a proposta',features='Funcionalidades',how='Como funciona',open_source='Código aberto',contrib='Participe do desenvolvimento',disclaimer='Demonstração técnica. Não é um serviço em produção nem uma certificação.',about_title='Tecnologia prática, verificável e colaborativa',about_body='Projetado para resolver problemas mensuráveis e documentar limitações. Criado por Chris Cruz (@h4ckd4d) com abordagem de engenharia Red Team ética e autorização explícita.',demo_title='Experimente um cenário ilustrativo',demo_sub='Os cálculos desta página ocorrem no navegador, com dados fictícios. Nenhuma informação é enviada à API.',run='Calcular / Analisar',result='Resultado',footer='Concebido e desenvolvido por Chris Cruz — @h4ckd4d. Todos os direitos de terceiros preservados.',learn='Leia o projeto no GitHub'),
 'en':dict(home='Home',about='About',demo='Demo',start='Explore the demo',open='Explore the product',features='Capabilities',how='How it works',open_source='Open source',contrib='Contribute to development',disclaimer='Technical demonstration. Not a production service or certification.',about_title='Practical, verifiable and collaborative technology',about_body='Built to solve measurable problems while documenting limitations. Created by Chris Cruz (@h4ckd4d) using an ethical, explicitly authorized Red Team engineering approach.',demo_title='Try a sample scenario',demo_sub='Calculations run in your browser with fictitious data. No information is sent to the API.',run='Calculate / Analyze',result='Result',footer='Conceived and developed by Chris Cruz — @h4ckd4d. Third-party rights reserved.',learn='Read the project on GitHub'),
 'es':dict(home='Inicio',about='Acerca de',demo='Demostración',start='Explorar demostración',open='Explorar la propuesta',features='Funcionalidades',how='Cómo funciona',open_source='Código abierto',contrib='Colabore en el desarrollo',disclaimer='Demostración técnica. No es un servicio de producción ni una certificación.',about_title='Tecnología práctica, verificable y colaborativa',about_body='Creado para resolver problemas medibles y documentar limitaciones. Desarrollado por Chris Cruz (@h4ckd4d) con un enfoque ético de ingeniería Red Team y autorización explícita.',demo_title='Pruebe un escenario ilustrativo',demo_sub='Los cálculos ocurren en el navegador con datos ficticios. No se envían datos a la API.',run='Calcular / Analizar',result='Resultado',footer='Concebido y desarrollado por Chris Cruz — @h4ckd4d. Se respetan los derechos de terceros.',learn='Lea el proyecto en GitHub')
}
FORMS={
 'fieldquote':{
  'pt-BR':[('qty','Quantidade','2'),('price','Preço unitário','150.00'),('discount','Desconto (%)','5'),('tax','Taxa ilustrativa (%)','0')],
  'en':[('qty','Quantity','2'),('price','Unit price','150.00'),('discount','Discount (%)','5'),('tax','Illustrative tax (%)','0')],
  'es':[('qty','Cantidad','2'),('price','Precio unitario','150.00'),('discount','Descuento (%)','5'),('tax','Impuesto ilustrativo (%)','0')]},
 'energypilot':{
  'pt-BR':[('base','Consumo atual (kWh/mês)','1200'),('target','Consumo simulado (kWh/mês)','900'),('rate','Tarifa por kWh','0.85')],
  'en':[('base','Current use (kWh/month)','1200'),('target','Simulated use (kWh/month)','900'),('rate','Cost per kWh','0.85')],
  'es':[('base','Consumo actual (kWh/mes)','1200'),('target','Consumo simulado (kWh/mes)','900'),('rate','Tarifa por kWh','0.85')]},
 'accesspilot':{
  'pt-BR':[('html','HTML ilustrativo','<html><head></head><body><img src="sample.png"><input id="email"></body></html>')],
  'en':[('html','Example HTML','<html><head></head><body><img src="sample.png"><input id="email"></body></html>')],
  'es':[('html','HTML de ejemplo','<html><head></head><body><img src="sample.png"><input id="email"></body></html>')]}
}

def esc(value):return html.escape(str(value),quote=True)
def locales_for_url(site_url,route=''):
    return {lang:f'{site_url}/{lang}/{route}'.replace('//'+lang,'/'+lang) for lang in LOCALES}

def construct_urls(base,route):
    return {lang:base+'/'+lang+'/'+(route+'/' if route else '') for lang in LOCALES}

def render(lang,route,base,preview):
    ui=UI[lang]; title=CONTENT['title'];label=CONTENT['tag']
    topic=CONTENT['hero'][lang]
    if route=='about':topic=ui['about_title']
    if route=='demo':topic=ui['demo_title']
    description={'pt-BR':CONTENT['desc'],'en':CONTENT['en_desc'],'es':CONTENT['es_desc']}[lang]
    if route=='about':
        description={'pt-BR':'Conheça a origem, os princípios de engenharia e os colaboradores do projeto ',
                     'en':'Learn about the mission, engineering principles and contributors behind ',
                     'es':'Conozca el origen, los principios de ingeniería y los colaboradores de '}[lang]+title+'.'
    elif route=='demo':
        description={'pt-BR':'Demonstração local e ilustrativa, sem envio de dados para servidores, do projeto ',
                     'en':'Try a synthetic browser-only demonstration of ',
                     'es':'Pruebe una demostración ilustrativa sin enviar datos del proyecto '}[lang]+title+'.'
    subtitle=CONTENT['subtitle'][lang] if not route else ui['about_body'] if route=='about' else ui['demo_sub']
    metatitle=esc(f'{title} | {topic}')
    canon=f'{base}/{lang}/'+(route+'/' if route else '')
    home=f'{base}/{lang}/'
    nav='<nav aria-label="Primary"><a href="'+esc(home)+'">'+ui['home']+'</a><a href="'+esc(home+'about/')+'">'+ui['about']+'</a><a href="'+esc(home+'demo/')+'">'+ui['demo']+'</a></nav>'
    all_lang=construct_urls(base,route)
    alternates='\n'.join('<link rel="alternate" hreflang="'+k+'" href="'+esc(u)+'">' for k,u in all_lang.items())+'\n<link rel="alternate" hreflang="x-default" href="'+esc(all_lang['en'])+'">'
    langlinks=' '.join('<a lang="'+k+'" hreflang="'+k+'" href="'+esc(u)+'">'+SEO_NAMES[k]+'</a>' for k,u in all_lang.items())
    indexable=not preview and route!='demo'
    org={'@type':'Person','name':'Chris Cruz','url':'https://github.com/H4ckD4d'}
    schema={'@context':'https://schema.org','@type':'SoftwareApplication','name':title,'applicationCategory':'BusinessApplication','operatingSystem':'Web','description':description,
            'url':canon,'creator':org,'author':org,'license':'https://opensource.org/license/mit','inLanguage':lang,'isAccessibleForFree':True,
            'softwareVersion':'0.1.0'}
    if route=='about':schema={'@context':'https://schema.org','@type':'AboutPage','name':topic,'url':canon,'inLanguage':lang,'author':org}
    if route=='demo':schema={'@context':'https://schema.org','@type':'WebPage','name':topic,'url':canon,'inLanguage':lang,'author':org}
    jsonld=json.dumps(schema,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    keywords=CONTENT['keywords'][lang]
    if route=='':
        cards=''.join('<article class="feature"><span class="feature-mark">0'+str(i+1)+'</span><h3>'+esc(n)+'</h3><p>'+esc(desc)+'</p></article>' for i,(n,desc) in enumerate(CONTENT['features'][lang]))
        main='<section class="hero"><div class="eyebrow">H4 OPEN TECHNOLOGY / '+esc(CONTENT['tag'])+'</div><h1>'+esc(topic)+'</h1><p class="lede">'+esc(subtitle)+'</p><div class="actions"><a class="button" href="'+esc(home+'demo/')+'">'+ui['start']+'</a><a class="button outline" href="'+esc(home+'about/')+'">'+ui['open']+'</a></div><div class="hero-notice">'+esc(ui['disclaimer'])+'</div></section><section id="features" class="features-section"><h2>'+ui['features']+'</h2><div class="features">'+cards+'</div></section>'
    elif route=='about':
        main='<section class="hero short"><div class="eyebrow">H4 / MISSION</div><h1>'+esc(topic)+'</h1><p class="lede">'+esc(subtitle)+'</p><p class="lede">'+esc(description)+'</p><a class="button" href="https://github.com/H4ckD4d/'+esc(PRODUCT)+'">'+esc(ui['learn'])+'</a></section>'
    else:
        inputs=[]
        for ident,lab,value in FORMS[CONTENT['type']][lang]:
            inp='<textarea id="f-'+ident+'" name="'+ident+'" rows="8" spellcheck="false">'+esc(value)+'</textarea>' if ident=='html' else '<input id="f-'+ident+'" name="'+ident+'" type="number" step="any" required min="0" value="'+esc(value)+'">'
            inputs.append('<label for="f-'+ident+'">'+esc(lab)+'</label>'+inp)
        main='<section class="hero short"><div class="eyebrow">LOCAL DEMO / NO CUSTOMER DATA</div><h1>'+esc(topic)+'</h1><p class="lede">'+esc(subtitle)+'</p><form id="demo-form" class="demo-card">'+''.join(inputs)+'<button type="submit" class="button">'+ui['run']+'</button></form><div class="output"><h2>'+ui['result']+'</h2><output id="demo-result" aria-live="polite"></output></div></section>'
    img=f'{base}/assets/preview.svg'; icon=f'{base}/assets/favicon.svg'
    css=f'{base}/assets/style.css'; js=f'{base}/assets/demo.js'
    return f"""<!DOCTYPE html>
<html lang="{esc(lang)}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{metatitle}</title>
<meta name="description" content="{esc(description)}"><meta name="keywords" content="{esc(keywords)}">
<meta name="robots" content="{'index,follow' if indexable else 'noindex,nofollow'}">
<meta name="author" content="Chris Cruz (@h4ckd4d)">
<link rel="canonical" href="{esc(canon)}">
{alternates}
<link rel="icon" type="image/svg+xml" href="{esc(icon)}">
<link rel="stylesheet" href="{esc(css)}">
<meta property="og:type" content="website"><meta property="og:title" content="{metatitle}">
<meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{esc(canon)}">
<meta property="og:image" content="{esc(img)}"><meta property="og:locale" content="{esc(lang.replace('-','_'))}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{metatitle}">
<meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{esc(img)}">
<script type="application/ld+json">{jsonld}</script>
</head>
<body data-product="{CONTENT['type']}" data-locale="{lang}">
<a class="skip-link" href="#main">Skip to content</a>
<div class="site"><header class="topbar"><a href="{esc(home)}" class="brand" aria-label="{esc(title)} home"><span class="brandmark">H4</span><span>{esc(title)}</span></a>{nav}<div class="languages">{langlinks}</div></header>
<main id="main">{main}</main>
<footer><div class="footlinks"><a href="https://github.com/H4ckD4d/{PRODUCT}">{ui['open_source']}</a> · <a href="https://github.com/H4ckD4d/{PRODUCT}/issues">{ui['contrib']}</a> · <a href="{esc(home+'about/')}">{ui['about']}</a></div><p>{ui['footer']}</p><p class="muted">{ui['disclaimer']}</p></footer></div>
{'<script defer src="'+esc(js)+'"></script>' if route=='demo' else ''}
</body>
</html>
"""

def build(preview=False):
    site_url=os.environ.get('SITE_URL','').strip().rstrip('/')
    public=os.environ.get('SEO_PUBLIC')=='1' and not preview
    if public:
        parsed=urlsplit(site_url)
        if (parsed.scheme!='https' or not parsed.hostname or parsed.hostname in ('localhost','127.0.0.1')
            or parsed.query or parsed.fragment or parsed.username or parsed.password):
            raise SystemExit('SEO_PUBLIC requires a valid, explicit HTTPS SITE_URL')
        base=site_url
    else:
        if not preview:
            raise SystemExit('Run with --preview, or set SITE_URL=https://... and SEO_PUBLIC=1')
        base='http://localhost:8080'
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir(parents=True,exist_ok=True)
    shutil.copytree(SITE/'assets',OUT/'assets',dirs_exist_ok=True)
    for lang in LOCALES:
        for route in ('','about','demo'):
            target=OUT/lang/(route if route else '')/'index.html'
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(render(lang,route,base,not public),encoding='utf-8')
    (OUT/'index.html').write_text('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=pt-BR/"></head><body><a href="pt-BR/">Português</a></body></html>',encoding='utf-8')
    if public:
        (OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n',encoding='utf-8')
        ns='http://www.sitemaps.org/schemas/sitemap/0.9'
        xhtml='http://www.w3.org/1999/xhtml'
        ET.register_namespace('',ns);ET.register_namespace('xhtml',xhtml)
        root=ET.Element('{'+ns+'}urlset')
        for route in ('','about'):
            urls=construct_urls(base,route)
            for lang in LOCALES:
                item=ET.SubElement(root,'{'+ns+'}url')
                ET.SubElement(item,'{'+ns+'}loc').text=urls[lang]
                for loc,href in [*urls.items(),('x-default',urls['en'])]:
                    ET.SubElement(item,'{'+xhtml+'}link',{'rel':'alternate','hreflang':loc,'href':href})
        ET.ElementTree(root).write(OUT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    else:
        (OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n',encoding='utf-8')
    print(json.dumps({'project':PRODUCT,'mode':'public' if public else 'preview','out':str(OUT),
                      'indexed_routes':6 if public else 0},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');args=p.parse_args()
    build(preview=args.preview)
