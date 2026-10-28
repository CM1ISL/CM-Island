"""Construit le site CM Island en plusieurs pages.
Sorties :
  /home/claude/site/cm-island-site.html  -> page d'accueil (artefact, sans squelette)
  /home/claude/site/dist/*.html, style.css -> pages complètes (publication + GitHub Pages plus tard)
  /home/claude/site/preview/ -> version de contrôle locale (accueil avec squelette)
"""
import base64, pathlib, re

SRC = pathlib.Path('/home/claude/site/src')
OUT = pathlib.Path('/home/claude/site')
DIST = OUT / 'dist'; DIST.mkdir(exist_ok=True)
PREV = OUT / 'preview'; PREV.mkdir(exist_ok=True)
FONT = pathlib.Path('/tmp/claude-0/-home-claude/3717aa67-5044-5e52-9d35-060dc2c9bb97/scratchpad/fonts/Anaktoria.woff2')

MONT = FONT.parent / 'Montserrat-latin-wght.woff2'
css = (SRC / 'style.css').read_text().replace('__ANAK__', base64.b64encode(FONT.read_bytes()).decode()).replace('__MONT__', base64.b64encode(MONT.read_bytes()).decode())

JSONLD = (SRC / 'jsonld.json').read_text()
BASE = 'https://www.cmisland.com/'

def faq_jsonld():
    import html as H
    q = (SRC / 'questions.body.html').read_text()
    items = re.findall(r'<summary>(.*?)</summary><p>(.*?)</p>', q)
    import json
    return json.dumps({'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':H.unescape(a),'acceptedAnswer':{'@type':'Answer','text':H.unescape(re.sub('<.*?>','',r))}} for a,r in items]}, ensure_ascii=False)

def head(titre, description, accueil=False, fichier='index.html'):
    url = BASE + ('' if fichier == 'index.html' else fichier)
    h = f'''<title>{titre}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CM Island">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{titre}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<link rel="stylesheet" href="style.css">'''
    if accueil:
        h = '<meta name="claude:viewport-fit-sides" content="cover">\n' + h + '\n<script type="application/ld+json">' + JSONLD + '</script>'
    if fichier == 'merci.html':
        h += '\n<meta name="robots" content="noindex, nofollow">'
    if fichier == 'questions.html':
        h += '\n<script type="application/ld+json">' + faq_jsonld() + '</script>'
    return h

def nav(actif='', accueil=False):
    def lien(href, txt, cle):
        cur = ' aria-current="page"' if cle == actif else ''
        return f'<a href="{href}"{cur}>{txt}</a>'
    return f'''<header class="nav bande" id="haut">
  <div class="cadre">
    <a class="marque" href="index.html" aria-label="CM Island, accueil"><b>CM Island</b><span>Créateur d'univers</span></a>
    <nav class="liens" aria-label="Navigation principale">
      {lien('offres.html', 'Accompagnements', 'offres')}
      {lien('#methode' if accueil else 'index.html#methode', 'Méthode', 'methode')}
      {lien('apropos.html', 'À propos', 'apropos')}
      {lien('questions.html', 'Questions', 'questions')}
      <a class="btn btn-bleu" href="reservation.html"{' aria-current="page"' if actif=='rdv' else ''}>Réserver un appel</a>
    </nav>
    <button class="menu-mobile" id="menu" aria-expanded="false" aria-controls="menu">Menu</button>
  </div>
</header>'''

APPEL = '''  <section class="appel bande" id="rendez-vous" aria-labelledby="t-appel">
    <div class="cadre">
      <p class="surtitre">Appel découverte · 30 minutes</p>
      <h2 id="t-appel">Discutons de votre stratégie</h2>
      <p>Trente minutes pour comprendre votre entreprise, vos objectifs et voir si CM Island peut vous accompagner.</p>
      <a class="btn btn-bordeaux" href="reservation.html">Réserver un appel découverte</a>
      <small>Ou par e-mail : emma.tranchant@cmisland.com</small>
    </div>
  </section>'''

FOOTER = '''<footer class="bande">
  <div class="cadre">
    <div>
      <a class="marque" href="index.html"><b>CM Island</b><span>Créateur d'univers</span></a>
      <p>Content strategist &amp; community manager. Fondée en Guadeloupe, au service des entreprises des Antilles et de l'Hexagone.</p>
    </div>
    <div>
      <h3>Explorer</h3>
      <ul><li><a href="offres.html">Accompagnements</a></li><li><a href="index.html#methode">Méthode</a></li><li><a href="apropos.html">À propos</a></li><li><a href="questions.html">Questions fréquentes</a></li></ul>
    </div>
    <div>
      <h3>Contact</h3>
      <ul><li>emma.tranchant@cmisland.com</li><li><a href="https://www.instagram.com/cm_island/" rel="noopener">Instagram</a></li><li><a href="reservation.html">Réserver un appel</a></li></ul>
    </div>
    <div class="bas"><span>© 2026 CM Island · Emma Tranchant EI · TVA non applicable, art. 293 B du CGI</span><span><a href="mentions-legales.html">Mentions légales</a> · <a href="confidentialite.html">Politique de confidentialité</a> · <a href="cgv.html">CGV</a></span></div>
  </div>
</footer>'''

SCRIPT = '''<script>
(function(){
  if('scrollRestoration' in history){history.scrollRestoration='manual';}
  function enHaut(){if(location.hash){return;}window.scrollTo(0,0);var h=document.getElementById('haut');if(h&&h.scrollIntoView){try{h.scrollIntoView({block:'start'});}catch(e){h.scrollIntoView(true);}}}
  enHaut();
  window.addEventListener('load',enHaut);
  window.addEventListener('pageshow',enHaut);
  var nav=document.querySelector('.nav'), b=document.getElementById('menu');
  b.addEventListener('click',function(){var o=nav.classList.toggle('ouvert');b.setAttribute('aria-expanded',String(o));b.textContent=o?'Fermer':'Menu';});
  nav.querySelectorAll('.liens a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('ouvert');b.setAttribute('aria-expanded','false');b.textContent='Menu';});});
  var voir=document.getElementById('voir-dispo'), offre=new URLSearchParams(location.search).get('offre');
  var noms={strategie:'Stratégie',gestion:'Gestion',immersion:'Immersion',profils:'Mise en place des profils',services:'Services complémentaires'};
  if(voir){voir.addEventListener('click',function(){
    var src='https://cal.com/cm-island/appel-decouverte?embed=true&theme=light&layout=month_view';
    if(offre && noms[offre]){src+='&notes='+encodeURIComponent("Offre qui m’intéresse : "+noms[offre]);}
    var f=document.createElement('iframe');f.src=src;f.title='Réserver un appel découverte avec CM Island';f.setAttribute('allow','fullscreen');
    var z=document.getElementById('agenda');z.innerHTML='';z.appendChild(f);f.focus();
  });}
  var etapes=document.querySelectorAll('.etape'), panneau=document.getElementById('detail-etape');
  if(panneau){
    etapes.forEach(function(e){e.addEventListener('click',function(){
      etapes.forEach(function(x){x.setAttribute('aria-expanded','false');});
      e.setAttribute('aria-expanded','true');
      var t=document.getElementById(e.dataset.detail);
      panneau.innerHTML='<span class="num">'+e.querySelector('.num').textContent+'</span>'+t.innerHTML;
    });});
  }
})();
</script>'''

def page(nom, titre, description, actif, corps, accueil=False):
    body = nav(actif, accueil) + '\n\n<main>\n' + corps + '\n' + ('' if actif=='rdv' or nom in ('strategie.html','gestion.html','immersion.html','profils.html','merci.html') else APPEL) + '\n</main>\n\n' + FOOTER + '\n\n' + SCRIPT + '\n'
    h = head(titre, description, accueil, nom)
    complet = f'<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{h}\n</head>\n<body>\n{body}</body>\n</html>\n'
    (DIST / nom).write_text(complet)
    (PREV / nom).write_text(complet)
    if accueil:
        (OUT / 'cm-island-site.html').write_text(h + '\n\n' + body)


(DIST / 'style.css').write_text(css)
(PREV / 'style.css').write_text(css)

for n, (fichier, titre, desc, actif, acc) in {
    'index': ('index.html', 'CM Island · Content strategist &amp; community manager en Guadeloupe', "CM Island, créateur d'univers. Content strategist et community manager en Guadeloupe, pour les entreprises des Antilles et de l'Hexagone : stratégie social media, création de contenu, tournage et community management.", '', True),
    'offres': ('offres.html', 'Accompagnements social media : Stratégie, Gestion, Immersion · CM Island', "Les accompagnements de CM Island : Stratégie, Gestion et Immersion. Contenu détaillé, tarifs et conditions. Content strategist et community manager en Guadeloupe.", 'offres', False),
    'a-propos': ('apropos.html', 'À propos · Emma Tranchant, fondatrice de CM Island', "CM Island, agence de stratégie digitale fondée en Guadeloupe par Emma Tranchant, content strategist et community manager.", 'apropos', False),
    'rendez-vous': ('reservation.html', 'Réserver un appel découverte · CM Island', "Réservez un appel découverte de 30 minutes avec CM Island, content strategist et community manager en Guadeloupe.", 'rdv', False),
    'strategie': ('strategie.html', 'Stratégie social media en Guadeloupe : audit et stratégie · CM Island', "Offre Stratégie de CM Island : audit complet de votre communication et stratégie social media sur mesure. 950 €. Content strategist en Guadeloupe, pour les Antilles et l'Hexagone.", 'offres', False),
    'gestion': ('gestion.html', 'Gestion des réseaux sociaux et community management · CM Island', "Offre Gestion de CM Island : création des contenus, publication, community management et bilan mensuel. À partir de 1 100 € par mois. Community manager en Guadeloupe.", 'offres', False),
    'immersion': ('immersion.html', 'Immersion : gestion des réseaux et tournage vidéo en Guadeloupe · CM Island', "Offre Immersion de CM Island : gestion de vos réseaux sociaux et une journée de tournage par mois chez vous, en Guadeloupe. À partir de 1 650 € par mois.", 'offres', False),
    'profils': ('profils.html', 'Mise en place des profils réseaux sociaux · CM Island', "Création ou remise à niveau de vos profils Instagram, Facebook, TikTok et LinkedIn. 450 €, livraison sous 7 jours ouvrés. CM Island, Guadeloupe.", 'offres', False),
    'mentions-legales': ('mentions-legales.html', 'Mentions légales · CM Island', "Mentions légales du site cmisland.com : éditeur, directrice de la publication, hébergeur et propriété intellectuelle.", 'legal', False),
    'confidentialite': ('confidentialite.html', 'Politique de confidentialité · CM Island', "Comment CM Island collecte et protège vos données personnelles : finalités, durées de conservation, destinataires, cookies et droits.", 'legal', False),
    'cgv': ('cgv.html', 'Conditions générales de vente · CM Island', "Conditions générales de vente de CM Island : prestations, commande, prix, paiement, validations, propriété intellectuelle, durée et résiliation.", 'legal', False),
    'merci': ('merci.html', 'Merci · CM Island', "Confirmation de paiement et prochaines étapes de votre accompagnement CM Island.", 'merci', False),
    'questions': ('questions.html', 'Questions fréquentes sur le community management · CM Island', "Questions fréquentes sur CM Island : content strategy, community management, tarifs, engagement, tournage en Guadeloupe et accompagnement à distance.", 'questions', False),
}.items():
    corps = (SRC / f'{n}.body.html').read_text().replace('__MAJ__', '25 octobre 2026')
    page(fichier, titre, desc, actif, corps, acc)
# Fichiers pour la mise en ligne (GitHub Pages)
pages = ['', 'offres.html', 'strategie.html', 'gestion.html', 'immersion.html', 'profils.html', 'apropos.html', 'questions.html', 'reservation.html', 'mentions-legales.html', 'confidentialite.html', 'cgv.html']
(DIST / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{p}</loc></url>\n' for p in pages) + '</urlset>\n')
(DIST / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + BASE + 'sitemap.xml\n')
(DIST / 'llms.txt').write_text((SRC / 'llms.txt').read_text())
(DIST / 'CNAME').write_text('www.cmisland.com\n')
print('ok')
