from pathlib import Path
import re,html,os
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,KeepTogether,PageBreak,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parents[2]
FONTDIR=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'
# Prefer Arial on Windows; ReportLab's bundled Vera fonts provide portable fallback.
import reportlab
fallback=Path(reportlab.__file__).parent/'fonts'
regular=FONTDIR/'arial.ttf';bold=FONTDIR/'arialbd.ttf'
if not regular.exists():regular=fallback/'Vera.ttf';bold=fallback/'VeraBd.ttf'
pdfmetrics.registerFont(TTFont('ReportBody',str(regular)));pdfmetrics.registerFont(TTFont('ReportBold',str(bold)))
pdfmetrics.registerFontFamily('ReportBody',normal='ReportBody',bold='ReportBold',italic='ReportBody',boldItalic='ReportBold')
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='Body',fontName='ReportBody',fontSize=10,leading=14.4,spaceAfter=8,textColor=colors.HexColor('#253443')))
styles.add(ParagraphStyle(name='ReportTitle',fontName='ReportBold',fontSize=22,leading=27,spaceAfter=16,textColor=colors.HexColor('#173c57')))
styles.add(ParagraphStyle(name='Section',fontName='ReportBold',fontSize=13.2,leading=17,spaceBefore=13,spaceAfter=8,keepWithNext=True,textColor=colors.HexColor('#173c57')))
styles.add(ParagraphStyle(name='Cell',parent=styles['Body'],fontSize=8.2,leading=11,spaceAfter=0))
styles.add(ParagraphStyle(name='Caption',parent=styles['Body'],fontSize=8.5,leading=12,textColor=colors.HexColor('#526574')))
W,H=A4;content=W-94

def inline(t):
 t=t.replace('—','-').replace('–','-').replace('−','-').replace('\u2011','-')
 t=html.escape(t);return re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',t)
def para(t,style='Body'):return Paragraph(inline(t),styles[style])
def table(rows):
 n=len(rows[0]);widths=([content*.29]+[content*.71/(n-1)]*(n-1)) if n>2 else [content*.25,content*.75]
 data=[[para(x,'Cell') for x in row] for row in rows]
 t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8f0f5')),('TEXTCOLOR',(0,0),(-1,0),colors.HexColor('#173c57')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#9fb3c1')),('LINEBELOW',(0,1),(-1,-1),.35,colors.HexColor('#d7e0e6'))]))
 return t

def main():
 source=ROOT/'reports/consolidacao-fase3/relatorio_atualizado.md';target=ROOT/'reports/relatorio_final.pdf'
 text=source.read_text(encoding='utf8');story=[];rows=[]
 for line in text.splitlines()+['']:
  if line.startswith('|'):
   if not re.fullmatch(r'[|\-: ]+',line):rows.append([x.strip() for x in line.strip('|').split('|')])
   continue
  if rows:story.extend([table(rows),Spacer(1,10)]);rows=[]
  if not line.strip():continue
  if line.startswith('# '):story.append(para(line[2:],'ReportTitle'))
  elif line.startswith('## '):story.append(para(line[3:],'Section'))
  else:story.append(para(line))
 story.append(PageBreak());story.append(para('Evidências visuais da avaliação histórica v1','ReportTitle'))
 story.append(para('As figuras desta seção pertencem à versão v1 congelada. Não são uma avaliação final do candidato com rendimento escolar. A curva precisão-recall resume o teste histórico; SHAP descreve associações do modelo e não efeitos causais.'))
 for filename,caption in [('pr-teste.png','Curva precisão-recall da avaliação histórica, sem novo cálculo de teste.'),('shap-logistica.png','Importância SHAP da logística contextual v1. A UF concentra parte importante da informação territorial.')]:
  p=ROOT/'images'/filename
  if p.exists():
   img=Image(str(p));scale=min(content/img.imageWidth,245/img.imageHeight);img.drawWidth=img.imageWidth*scale;img.drawHeight=img.imageHeight*scale
   story.append(KeepTogether([img,Spacer(1,6),para(caption,'Caption'),Spacer(1,14)]))
 story.append(PageBreak());story.append(para('Fontes e documentos de apoio','ReportTitle'))
 sources=[('Enunciados das Fases 2 e 3','Documentos fornecidos no curso; Fase 3, p. 2-5, define classificação individual, integração com Gold, enriquecimento e prevenção de vazamento.'),('Dados de origem','Backup auditado da Fase 2; manifestos e dicionários estão em data/source e data/gold_fase2.'),('IBGE','População e densidade de 2022; PIB e composição econômica de 2021. Referências e hashes nos manifestos de fontes.'),('INEP','Taxas municipais de distorção e rendimento de 2022 e INSE de 2021. Rede municipal, localização total, código IBGE para o vínculo.'),('FUNDEB e PNAD','VAAT de 2023, publicação de 28/08/2023, e renda domiciliar por UF de 2022. Experimentos não indicaram ganho relevante na configuração testada.'),('Reprodução','README.md, requirements.txt, src/modeling/enrichment.py e src/evaluation/baselines.py. Resultados completos e protocolos estão nas subpastas de reports.')]
 for title,desc in sources:story.append(para(title,'Section'));story.append(para(desc))
 story.append(para('Endereços oficiais','Section'))
 urls=['https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais','https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/2023','https://www.ibge.gov.br/biblioteca/visualizacao/periodicos/3100/rdpc_2022.pdf']
 for u in urls:story.append(Paragraph('<link href="'+u+'" color="#176596">'+html.escape(u)+'</link>',styles['Caption']));story.append(Spacer(1,8))
 def footer(c,doc):
  c.saveState();c.setStrokeColor(colors.HexColor('#cbd7df'));c.line(47,40,W-47,40);c.setFont('ReportBody',8);c.setFillColor(colors.HexColor('#526574'));c.drawString(47,27,'Tech Challenge - Fase 3 | Relatório consolidado | 28/10/2026');c.drawRightString(W-47,27,str(doc.page));c.restoreState()
 doc=SimpleDocTemplate(str(target),pagesize=A4,rightMargin=47,leftMargin=47,topMargin=43,bottomMargin=56,title='Alfabetização no Brasil - Relatório consolidado da Fase 3',author='menilsonmatos')
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
 print(target)
if __name__=='__main__':main()
