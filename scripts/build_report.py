from pathlib import Path
import json,re,textwrap
from docx import Document
from docx.shared import Inches,Pt,RGBColor,Cm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
R=Path(__file__).resolve().parents[1]
model=json.loads((R/'docs/report_model.json').read_text())
for p in model['pages']:
 p['paragraphs']=[t.replace('{{PAGES_STATUS}}','Documentació i aplicació responen HTTP 200, verificat amb curl el 26 d’octubre de 2026 a les 12.36 (Europe/Madrid). GitHub confirma gh-pages i / (root).') for t in p['paragraphs']]
 if p['title']=='1 Introducció':p['images']=[{'path':'evidencias/pages/25-documentacio.png','caption':'Figura. Documentació del procés oberta en GitHub Pages.'}]
 if p['title']=='3 Creació del repositori':p['paragraphs'][1]='Entorn verificat: Git 2.52.0, GitHub CLI 2.102.0, Node.js 24.21.0 i npm 11.19.0 (registre 085). El primer commit és 5a3c16a. Abans d’eixe commit, HEAD encara no existia; el registre conserva eixa resposta real.'
 if p['title']=='6 Release v1.0':
  p['logs']=['033','039','042','058'];p['images']=[{'path':'evidencias/github/16-release-v1.png','caption':'Figura. GitHub Release v1.0 publicada, amb etiqueta i commit reals.'}]
 if p['title']=='7 Hotfix':p['logs']=['044','050','053']
 if 'Contingut HTML' in p['title'] and p['title'].startswith('5 '):p['paragraphs']=p['paragraphs'][:3]
 if p['title']=='8 Historial de Git':p['logs']=['054']
 if p['title']=='10 GitHub Pages':
  p['logs']=['071','078','083'];p['images']=[{'path':'evidencias/pages/24-configuracio.png','caption':'Figura. Pages confirma gh-pages com a branca i / (root) com a directori.'}]
  p['paragraphs'][1]='La documentació se servix des de l’arrel de gh-pages i l’aplicació des d’app/. La creació per API va retornar 409 perquè Pages ja estava activat; la consulta posterior va confirmar la font correcta. No es presenta l’intent com una creació nova completada.'
 if p['title']=='11 Resultat de l’aplicació':
  p['images']=[{'path':'evidencias/aplicacion/26-app-publicada.png','caption':'Figura. Aplicació oberta des de l’adreça pública de GitHub Pages.'}]
  p['links']=[{'label':'Aplicació interactiva publicada','url':'https://lucamzm.github.io/javascript-dom-gitflow/app/'}]
 if p['title']=='11 Resultat de l’aplicació — Verificació':
  p['paragraphs'].append('La verificació final amb curl obté HTTP 200 per al repositori, la documentació i l’aplicació. També s’han accionat els controls en el navegador sobre la URL pública, amb resultats visibles i sense errors de consola; qa-publicada.json conserva l’estat consultat.')
 if p['title']=='11 Resultat de l’aplicació — Verificació':
  p['paragraphs'].append('La segona execució automatitzada sobre GitHub Pages aprova 15 de 15 proves i tots els enllaços externs. L’auditoria Git aprova 30 de 30 comprovacions de branques, pares de fusió, etiquetes i igualtat del codi entre main i develop.')
 if p['title']=='12 Conclusions':p['images']=[{'path':'evidencias/aplicacion/26-mobil.png','caption':'Figura. Aplicació publicada a 390 píxels, sense desbordament horitzontal.'}]
 if p['title']=='12 Conclusions':p['paragraphs'][-1]='La publicació està verificada amb HTTP 200 i navegador. La preparació de la release es va identificar com usuari1 en lloc d’usuari3; es declara esta desviació de distribució de papers sense alterar l’historial. Els documents finals reunixen les evidències i els resultats.'

doc=Document();s=doc.sections[0];s.page_width=Cm(21);s.page_height=Cm(29.7);s.top_margin=Cm(1.8);s.bottom_margin=Cm(1.8);s.left_margin=Cm(1.8);s.right_margin=Cm(1.8)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3','Caption']:
 st=doc.styles[name];st.font.name='Calibri';st.font.color.rgb=RGBColor(0,0,0)
 st.paragraph_format.space_after=Pt(6)
normal=doc.styles['Normal'];normal.font.size=Pt(10.5);normal.paragraph_format.line_spacing=1.08
for name,size in [('Title',30),('Heading 1',19),('Heading 2',14),('Caption',9)]:doc.styles[name].font.size=Pt(size)
doc.styles['Heading 1'].paragraph_format.space_after=Pt(9)
doc.core_properties.title='Pràctica 1 — Sistemes de control de versions';doc.core_properties.author='Luca Mazmishvili';doc.core_properties.subject='Memòria del laboratori DOM i Git Flow'
foot=s.footer.paragraphs[0];foot.alignment=WD_ALIGN_PARAGRAPH.RIGHT
foot.add_run('Luca Mazmishvili · Pràctica 1     ')
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');foot._p.append(fld)
for r in foot.runs:r.font.size=Pt(8)

def link(par,label,url):
 rel=par.part.relate_to(url,'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',is_external=True)
 a=OxmlElement('w:hyperlink');a.set(qn('r:id'),rel);r=OxmlElement('w:r');pr=OxmlElement('w:rPr');color=OxmlElement('w:color');color.set(qn('w:val'),'174D8C');pr.append(color);sz=OxmlElement('w:sz');sz.set(qn('w:val'),'18');pr.append(sz);r.append(pr);t=OxmlElement('w:t');t.text=label;r.append(t);a.append(r);par._p.append(a)
figure_counter=0
def picture(path,caption):
 global figure_counter
 figure_counter+=1
 caption=f'Figura {figure_counter}. '+re.sub(r'^Figura(?: \d+)?\.\s*','',caption)
 p=R/path
 if not p.exists():return
 im=Image.open(p);w=2.2 if '26-mobil' in str(p) else (6.45 if '18-hotfix' in str(p) else 6.75);h=w*im.height/im.width
 # Full-width captures; preserve proportions and never crop evidence.
 para=doc.add_paragraph();para.paragraph_format.keep_with_next=True
 para.add_run().add_picture(str(p),width=Inches(w))
 cap=doc.add_paragraph(caption,'Caption');cap.paragraph_format.space_after=Pt(7)

def log_excerpt(id):
 f=next((R/'evidencias/terminal').glob(id+'-*.txt'),None)
 if not f:return
 content=f.read_text();lines=content.splitlines()
 if id=='054':
  stop=lines.index('Codi de retorn: 0');text='\n'.join(lines[1:stop]).rstrip();size=7.5
 else:
  first=next(i for i,v in enumerate(lines) if v.startswith('$ '));end=next(i for i,v in enumerate(lines[first:],first) if v.startswith('Codi de retorn:'))
  output=[x for x in lines[first+1:end] if x.strip()]
  # Keep a short, explicitly labelled extract; source remains linked in full.
  useful=[]
  for line in output:
   if len(line)>240 and line.startswith('{'):
    useful.append(line[:220]+' […]');break
   if line.startswith(' create mode') or line.startswith('A  ') or line.startswith('?? '):continue
   useful.append(line)
   if len(useful)>=1:break
  text=lines[first]+'\n'+'\n'.join(useful)
  if len(output)>len(useful):text+='\n[…]'
  text+='\n'+lines[end]
  head=next((x for x in lines if x.startswith('HEAD: ')),'')
  # HEAD complet en el registre enllaçat; els hashes rellevants es descriuen en el text.
  size=7.8
 para=doc.add_paragraph();para.paragraph_format.space_after=Pt(5);para.paragraph_format.line_spacing=1.0
 run=para.add_run(text);run.font.name='Courier New';run.font.size=Pt(size)
 source=doc.add_paragraph();source.paragraph_format.space_after=Pt(5);source.paragraph_format.line_spacing=1
 run=source.add_run('Eixida registrada'+(' íntegra del gràfic. ' if id=='054' else ' · extracte. '));run.font.size=Pt(8)
 link(source,f.name,'https://lucamzm.github.io/javascript-dom-gitflow/evidencias/terminal/'+f.name)

# Cover
p=doc.add_paragraph();p.paragraph_format.space_after=Pt(80)
doc.add_paragraph('Pràctica 1 — Sistemes de control de versions','Title')
doc.add_paragraph('Memòria del desenvolupament JavaScript DOM amb Git Flow','Subtitle')
doc.add_paragraph('Alumne: Luca Mazmishvili\nGitHub: LucaMZM\nProfessor: enminqui2\n26 d’octubre de 2026')
doc.add_paragraph('Lliurament acadèmic amb aplicació funcional, historial de branques, GitHub Project, documentació publicada i evidències reals.')
for l,u in [('Repositori','https://github.com/LucaMZM/javascript-dom-gitflow'),('Documentació','https://lucamzm.github.io/javascript-dom-gitflow/')]:link(doc.add_paragraph(),l+' · '+u,u)
doc.add_page_break();doc.add_heading('Índex',0)
idx=json.loads((R/'docs/page_numbers.json').read_text()) if (R/'docs/page_numbers.json').exists() else {}
for i,p in enumerate(model['pages'],3):
 par=doc.add_paragraph(p['title']+'    '+str(idx.get(p['title'],i)))
 par.paragraph_format.space_after=Pt(7)
 par.runs[0].font.size=Pt(10)
for title in ['Annex A Evidències de les fases','Annex B Evidències de publicació']:
 doc.add_paragraph(title+'    '+str(idx.get(title,'—')))

for page in model['pages']:
 heading=doc.add_heading(page['title'],1);heading.paragraph_format.page_break_before=True
 for txt in page['paragraphs']:doc.add_paragraph(txt)
 if page['logs']:doc.add_paragraph('Comandaments i resultats reals','Heading 2')
 for id in page['logs']:log_excerpt(id)
 for pic in page['images']:picture(pic['path'],pic['caption'])
 for a in page['links']:link(doc.add_paragraph(),a['label']+' · '+a['url'],a['url'])

mapping=[
('1 Repositori creat','github/01-repositori.png','003'),('2 Creació main i develop',None,'001,005,006'),('3 Estructura inicial','aplicacion/03-home.png','010'),('4 Creació feature contingut',None,'011'),('5 Funcionalitat contingut','aplicacion/05-contingut.png','015'),('6 Fusió contingut',None,'016,018'),('7 Creació feature atributs',None,'019'),('8 Funcionalitat atributs','aplicacion/08-atributs.png','022'),('9 Fusió atributs',None,'023,025'),('10 Creació feature estils',None,'026'),('11 Funcionalitat estils','aplicacion/11-estils.png','029'),('12 Fusió estils',None,'030,032'),('13 Historial gràfic','git/13-historial-registrat.png','054'),('14 Creació release',None,'033'),('15 Integració release',None,'039,042'),('16 Etiqueta i Release','github/16-release-v1.png','040,058'),('17 Creació hotfix',None,'044'),('18 Canvi del hotfix','aplicacion/18-hotfix.png','047,048'),('19 Integració hotfix',None,'050,053'),('20 Branques publicades','github/20-branques.png','081'),('21 GitHub Project','github/21-project-proces.png',None),('22 Accés enminqui2','github/22-acces-professor.png',None),('23 Branca gh-pages',None,'071,075,076'),('24 Configuració Pages','pages/24-configuracio.png','078'),('25 Documentació publicada','pages/25-documentacio.png','083'),('26 Aplicació publicada','aplicacion/26-app-publicada.png','083')]
for title,items in [('Annex A Evidències de les fases',mapping[:13]),('Annex B Evidències de publicació',mapping[13:])]:
 heading=doc.add_heading(title,1);heading.paragraph_format.page_break_before=True
 doc.add_paragraph('Les captures són reals de navegador. Quan no hi ha captura de terminal, s’adjunta l’eixida registrada amb data, codi de retorn, estat Git i hash. La imatge del gràfic és una captura de navegador que mostra el registre autèntic, identificada com a tal.')
 for label,img,ids in items:
  para=doc.add_paragraph();run=para.add_run(label+'\n');run.bold=True
  if img:link(para,'Captura de navegador','https://lucamzm.github.io/javascript-dom-gitflow/evidencias/'+img)
  if ids:
   para.add_run(' · Registres: ')
   for n,id in enumerate(ids.split(',')):
    f=next((R/'evidencias/terminal').glob(id+'-*.txt'));link(para,id,'https://lucamzm.github.io/javascript-dom-gitflow/evidencias/terminal/'+f.name)
    if n<len(ids.split(','))-1:para.add_run(', ')
  para.paragraph_format.space_after=Pt(6);para.paragraph_format.keep_together=True
for element in doc.styles.element.iter(qn('w:pBdr')):
 element.getparent().remove(element)
for element in doc.element.iter(qn('w:pBdr')):
 element.getparent().remove(element)
out=R/'entrega/Practica1_GitFlow_LucaMZM.docx';doc.save(out)
(R/'docs/report_final_model.json').write_text(json.dumps(model,ensure_ascii=False,indent=2))
print(out)
