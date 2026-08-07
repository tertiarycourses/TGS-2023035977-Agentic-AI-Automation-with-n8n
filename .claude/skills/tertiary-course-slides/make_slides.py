#!/usr/bin/env python3
"""Course deck: courseware/Agentic AI Automation with n8n-vNN.pptx

Style follows the reference deck (Business Process Automation with Power Automate
and Copilot Studio Agents): white theme, kicker + bold title, chevron flow strips,
outlined concept cards, comparison tables, takeaway bands, module dividers, and
ONE visual slide per lab (workflow chevron + n8n screenshot + LAB band) — the
click-by-click steps live in the Learner Guide, never on slides."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

import os as _os
import math
REPO = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))))

NAVY=RGBColor(0x0B,0x12,0x20); BLUE=RGBColor(0x1F,0x6F,0xEB); TEAL=RGBColor(0x10,0xB9,0x81)
AMBER=RGBColor(0xF5,0x9E,0x0B); INK=RGBColor(0x16,0x1B,0x26); GREY=RGBColor(0x5B,0x63,0x72)
LIGHT=RGBColor(0xF5,0xF8,0xFC); WHITE=RGBColor(0xFF,0xFF,0xFF); LINE=RGBColor(0xE2,0xE8,0xF0)
VIOLET=RGBColor(0x7C,0x3A,0xED); GREEN=RGBColor(0x12,0x7A,0x3E); RED=RGBColor(0xC6,0x2F,0x2F)
VERSION="v47"; VERSION_DATE="8 Aug 2026"
# ─── EDIT PER COURSE ─────────────────────────────────────────────
TITLE       = "Agentic AI Automation with n8n"   # <<Course Title>>
COURSE_CODE = "TGS-2023035977"                    # <<Course Code, e.g. TGS-XXXXXXXXXX>>
# ─────────────────────────────────────────────────────────────────

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
SW,SH=prs.slide_width,prs.slide_height; BLANK=prs.slide_layouts[6]; FONT="Arial"
def slide(): return prs.slides.add_slide(BLANK)
def rect(s,x,y,w,h,color,line=None):
    sh=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,x,y,w,h); sh.fill.solid(); sh.fill.fore_color.rgb=color
    sh.line.fill.background() if line is None else (setattr(sh.line.color,'rgb',line),setattr(sh.line,'width',Pt(1)))
    sh.shadow.inherit=False; return sh
def box(s,x,y,w,h,edge,fill=WHITE,lw=1.25,round_=True):
    sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE,x,y,w,h)
    try: sh.adjustments[0]=0.055
    except Exception: pass
    sh.fill.solid(); sh.fill.fore_color.rgb=fill
    sh.line.color.rgb=edge; sh.line.width=Pt(lw); sh.shadow.inherit=False; return sh
def oval(s,x,y,w,h,color):
    sh=s.shapes.add_shape(MSO_SHAPE.OVAL,x,y,w,h); sh.fill.solid(); sh.fill.fore_color.rgb=color
    sh.line.fill.background(); sh.shadow.inherit=False; return sh
def txt(s,x,y,w,h,runs,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,space=4):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=anchor
    tf.margin_left=tf.margin_right=Pt(0); tf.margin_top=tf.margin_bottom=Pt(0)
    if runs and not isinstance(runs[0],list): runs=[runs]
    first=True
    for para in runs:
        p=tf.paragraphs[0] if first else tf.add_paragraph(); first=False
        p.alignment=align; p.space_after=Pt(space); p.space_before=Pt(0)
        for (t,sz,col,bold) in para:
            r=p.add_run(); r.text=t; r.font.size=Pt(sz); r.font.bold=bold; r.font.color.rgb=col; r.font.name=FONT
    return tb
def bullets(s,x,y,w,h,items,size=18,color=INK,gap=10,mcolor=BLUE):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True; tf.margin_left=tf.margin_right=Pt(0)
    first=True
    for it in items:
        lvl=0; text=it
        if isinstance(it,tuple): text,lvl=it
        p=tf.paragraphs[0] if first else tf.add_paragraph(); first=False
        p.space_after=Pt(gap); p.space_before=Pt(0)
        rm=p.add_run(); rm.text=("   "*lvl)+("•  " if lvl==0 else "–  ")
        rm.font.size=Pt(size); rm.font.color.rgb=(mcolor if lvl==0 else GREY); rm.font.bold=True; rm.font.name=FONT
        r=p.add_run(); r.text=text; r.font.size=Pt(size-lvl); r.font.color.rgb=color; r.font.name=FONT
    return tb
PAGE={"n":0}
def footer(s,dark=False):
    PAGE["n"]+=1; c=WHITE if dark else GREY
    txt(s,Inches(0.55),Inches(7.08),Inches(6.2),Inches(0.3),[[(f"{TITLE}  ·  {COURSE_CODE}",8.5,c,False)]])
    txt(s,Inches(6.0),Inches(7.08),Inches(6),Inches(0.3),[[("© 2026 Tertiary Infotech Academy Pte Ltd",8.5,c,False)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(11.9),Inches(7.08),Inches(0.9),Inches(0.3),[[(str(PAGE["n"]),9,c,True)]],align=PP_ALIGN.RIGHT)
def head(s,title,kicker=None,kcolor=BLUE):
    rect(s,0,0,SW,SH,WHITE); rect(s,Inches(0.55),Inches(0.60),Inches(0.14),Inches(0.66),kcolor)
    y=Inches(0.55)
    if kicker:
        txt(s,Inches(0.8),Inches(0.5),Inches(11.8),Inches(0.34),[[(kicker,13,kcolor,True)]]); y=Inches(0.82)
    txt(s,Inches(0.8),y,Inches(12.0),Inches(0.85),[[(title,28,INK,True)]])

ASSETS=f"{REPO}/.claude/skills/tertiary-course-slides/assets"
_SKILL_ASSETS=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),"assets")
def _logo(name):
    for base in (ASSETS,_SKILL_ASSETS):
        p=_os.path.join(base,name)
        if _os.path.exists(p): return p
    return None
IMG=lambda p: f"{REPO}/{p}"

# ─── reference-style building blocks ─────────────────────────────
def intro_line(s,text,y=Inches(1.58)):
    txt(s,Inches(0.85),y,Inches(11.6),Inches(0.36),[[(text,12.5,GREY,False)]])
def chev_strip(s,items,y=Inches(2.0),h=Inches(1.05),color=BLUE,x0=Inches(0.85),tw=Inches(11.63),tsz=12.5,ssz=9):
    """Horizontal flow of outlined boxes joined by ▶ — items: (title, sub)."""
    n=len(items); gap=Inches(0.34)
    cw=int((tw-gap*(n-1))/n)
    for i,(t,sub) in enumerate(items):
        x=int(x0+(cw+gap)*i)
        box(s,x,y,cw,h,color)
        runs=[[(t,tsz,INK,True)]]
        if sub: runs.append([(sub,ssz,GREY,False)])
        txt(s,x+Inches(0.1),y,cw-Inches(0.2),h,runs,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=2)
        if i<n-1:
            txt(s,int(x+cw-Inches(0.03)),int(y+h/2-Inches(0.18)),int(gap+Inches(0.06)),Inches(0.36),
                [[("▶",12,color,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
def ncards(s,items,y=Inches(3.4),h=Inches(2.6),cols=2,numbered=True):
    """Grid of outlined cards — items: (color, title, body)."""
    n=len(items); rows=math.ceil(n/cols)
    X0=Inches(0.85); TOTW=Inches(11.63); gx=Inches(0.32); gy=Inches(0.24)
    cw=int((TOTW-gx*(cols-1))/cols); ch=int((h-gy*(rows-1))/rows)
    for i,(col,t,body) in enumerate(items):
        x=int(X0+(cw+gx)*(i%cols)); yy=int(y+(ch+gy)*(i//cols))
        box(s,x,yy,cw,ch,col)
        tx=x+Inches(0.22)
        if numbered:
            bd=Inches(0.34)
            oval(s,x+Inches(0.2),yy+Inches(0.16),bd,bd,col)
            txt(s,x+Inches(0.2),yy+Inches(0.16),bd,bd,[[(str(i+1),13,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
            txt(s,x+Inches(0.68),yy+Inches(0.17),cw-Inches(0.9),Inches(0.34),[[(t,13,col,True)]])
        else:
            txt(s,tx,yy+Inches(0.16),cw-Inches(0.44),Inches(0.34),[[(t,13,col,True)]])
        txt(s,tx,yy+Inches(0.6),cw-Inches(0.44),ch-Inches(0.76),[[(body,10.5,INK,False)]],space=3)
def takeaway(s,text,y=Inches(6.32),color=INK):
    box(s,Inches(0.85),y,Inches(11.63),Inches(0.46),LINE,fill=LIGHT,lw=1)
    txt(s,Inches(1.1),y,Inches(11.13),Inches(0.46),[[(text,12.5,color,True)]],anchor=MSO_ANCHOR.MIDDLE)
def data_table(s,widths,header,rows,y=Inches(2.0),rh=Inches(0.44),hcolor=BLUE,fsz=10.5):
    """Rect-based table: colored header row, striped body rows. widths in inches summing ≈11.63."""
    X0=Inches(0.85); xs=[X0]
    for w in widths: xs.append(int(xs[-1]+Inches(w)))
    for j,htxt in enumerate(header):
        rect(s,xs[j],y,int(Inches(widths[j])),rh,hcolor)
        txt(s,xs[j]+Inches(0.14),y,int(Inches(widths[j]))-Inches(0.28),rh,[[(htxt,11,WHITE,True)]],anchor=MSO_ANCHOR.MIDDLE)
    for i,row in enumerate(rows):
        yy=int(y+rh*(i+1)); fill=LIGHT if i%2 else WHITE
        for j,cell in enumerate(row):
            rect(s,xs[j],yy,int(Inches(widths[j])),rh,fill,line=LINE)
            txt(s,xs[j]+Inches(0.14),yy,int(Inches(widths[j]))-Inches(0.28),rh,
                [[(cell,fsz,INK,j==0)]],anchor=MSO_ANCHOR.MIDDLE)
    return int(y+rh*(len(rows)+1))
def pic_fit(s,img,x,y,maxw,maxh,border=True):
    if not _os.path.exists(img): return None
    pic=s.shapes.add_picture(img,x,y,width=maxw)
    if pic.height>maxh:
        s.shapes._spTree.remove(pic._element)
        pic=s.shapes.add_picture(img,x,y,height=maxh)
    pic.left=int(x+(maxw-pic.width)/2)
    if border:
        ln=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,pic.left-Pt(1),pic.top-Pt(1),pic.width+Pt(2),pic.height+Pt(2))
        ln.fill.background(); ln.line.color.rgb=LINE; ln.line.width=Pt(1); ln.shadow.inherit=False
    return pic
def lab_band(s,tag,name,meta,color=TEAL,y=Inches(6.22)):
    box(s,Inches(0.85),y,Inches(11.63),Inches(0.62),color,lw=1.25)
    rect(s,Inches(1.05),int(y+Inches(0.13)),Inches(1.05),Inches(0.36),color)
    txt(s,Inches(1.05),int(y+Inches(0.13)),Inches(1.05),Inches(0.36),[[(tag,12,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    txt(s,Inches(2.3),y+Inches(0.06),Inches(10.0),Inches(0.28),[[(name,12.5,INK,True)]])
    txt(s,Inches(2.3),y+Inches(0.335),Inches(10.0),Inches(0.26),[[(meta,9.5,GREY,False)]])
def lab_slide(kicker,tag,title,intro,flows,img,meta,cap="",color=TEAL):
    """ONE slide per lab: intro line, workflow chevron strip(s), n8n screenshot, LAB band.
    flows: list of chevron item-lists (1 or 2 strips). Steps belong in the Learner Guide."""
    s=slide(); head(s,title,kicker,kcolor=color)
    intro_line(s,intro)
    y=Inches(1.98)
    for f in flows:
        chev_strip(s,f,y=y,h=Inches(0.82),color=color,tsz=11.5,ssz=8.5)
        y=int(y+Inches(0.98))
    top=y+Inches(0.06); maxh=int((Inches(5.82) if cap else Inches(6.1))-top)
    if img: pic_fit(s,img,Inches(1.6),top,Inches(10.1),maxh)
    if cap: txt(s,Inches(0.85),Inches(5.9),Inches(11.6),Inches(0.24),[[(cap,9.5,GREY,False)]],align=PP_ALIGN.CENTER)
    lab_band(s,tag,title.split("—",1)[-1].strip() if "—" in title else title,meta,color=color)
    footer(s); return s
def website_lab(kicker,title,img,items,band=None,color=BLUE):
    s=slide(); head(s,title,kicker,color)
    bullets(s,Inches(0.85),Inches(2.0),Inches(5.4),Inches(3.9),items,size=15,gap=9)
    pic_fit(s,img,Inches(6.5),Inches(2.0),Inches(6.0),Inches(3.95))
    if band: lab_band(s,band[0],band[1],band[2])
    footer(s); return s
def concept(kicker,title,intro=None):
    s=slide(); head(s,title,kicker)
    if intro: intro_line(s,intro)
    return s
def section(kicker,title,n,sub="",applied="",color=BLUE):
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    bx=box(s,Inches(1.5),Inches(2.15),Inches(10.3),Inches(3.2),color,lw=1.5)
    rect(s,Inches(1.5),Inches(2.15),Inches(0.22),Inches(3.2),color)
    txt(s,Inches(2.1),Inches(2.5),Inches(9.3),Inches(0.4),[[(kicker,15,color,True)]])
    txt(s,Inches(2.1),Inches(2.95),Inches(9.4),Inches(1.2),[[(title,34,INK,True)]])
    if sub: txt(s,Inches(2.12),Inches(4.15),Inches(9.3),Inches(0.6),[[(sub,14,GREY,False)]])
    if applied: txt(s,Inches(2.12),Inches(4.75),Inches(9.3),Inches(0.4),[[(applied,12,color,True)]])
    txt(s,Inches(10.2),Inches(0.6),Inches(2.5),Inches(1.6),[[(n,72,LINE,True)]],align=PP_ALIGN.RIGHT)
    footer(s)
def content(title,items,kicker=None,size=20):
    s=slide(); head(s,title,kicker); bullets(s,Inches(0.85),Inches(1.9),Inches(11.6),Inches(4.9),items,size=size); footer(s); return s
def two_panel(title,ltitle,litems,rtitle,ritems,kicker=None,lcolor=BLUE,rcolor=VIOLET,take=None):
    """Reference-style two-column comparison: colored header bars + outlined bullet panels."""
    s=slide(); head(s,title,kicker)
    for (x,w,t,items,col) in ((Inches(0.85),Inches(5.68),ltitle,litems,lcolor),(Inches(6.8),Inches(5.68),rtitle,ritems,rcolor)):
        rect(s,x,Inches(1.95),w,Inches(0.5),col)
        txt(s,x,Inches(1.95),w,Inches(0.5),[[(t,14,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        box(s,x,Inches(2.45),w,Inches(3.7),col,lw=1.25,round_=False)
        bullets(s,x+Inches(0.3),Inches(2.7),w-Inches(0.6),Inches(3.3),items,size=13.5,mcolor=col,gap=9)
    if take: takeaway(s,take)
    footer(s); return s
def img_slide(title,img,caption,kicker="WORKFLOW",kcolor=TEAL):
    s=slide(); head(s,title,kicker,kcolor)
    pic_fit(s,img,Inches(1.0),Inches(1.9),Inches(11.3),Inches(4.55))
    txt(s,Inches(0.8),Inches(6.55),Inches(11.7),Inches(0.4),[[(caption,12,GREY,False)]],align=PP_ALIGN.CENTER)
    footer(s); return s
def website_slide(title,img,items,kicker,note=""):
    s=slide(); head(s,title,kicker,BLUE)
    bullets(s,Inches(0.85),Inches(1.95),Inches(5.4),Inches(4.6),items,size=16,gap=10)
    pic_fit(s,img,Inches(6.5),Inches(1.95),Inches(6.0),Inches(3.95))
    footer(s); return s
def gallery_slide(title,imgs,captions,kicker):
    s=slide(); head(s,title,kicker,TEAL)
    imgs2=[(i,c) for i,c in zip(imgs,captions) if _os.path.exists(i)]; n=len(imgs2)
    if not n: footer(s); return s
    slot=11.6/n; cell=Inches(slot)
    for k,(im,cap) in enumerate(imgs2):
        x0=Inches(0.85)+Inches(slot*k)
        pic_fit(s,im,x0+Inches(0.1),Inches(2.0),cell-Inches(0.3),Inches(3.7))
        txt(s,x0,Inches(5.95),cell,Inches(0.5),[[(cap,13,GREY,False)]],align=PP_ALIGN.CENTER)
    footer(s); return s
def brk(kind,dur,color):
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),color); rect(s,0,Inches(7.28),SW,Inches(0.22),color)
    rect(s,Inches(5.4),Inches(2.35),Inches(2.53),Inches(0.1),color)
    txt(s,0,Inches(2.75),SW,Inches(1.2),[[(kind,48,INK,True)]],align=PP_ALIGN.CENTER)
    txt(s,0,Inches(4.05),SW,Inches(0.8),[[(dur,22,color,True)]],align=PP_ALIGN.CENTER); footer(s)
def cover():
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),BLUE)
    rect(s,0,Inches(7.28),SW,Inches(0.22),TEAL)
    _org=_logo("tertiary-infotech-logo.png")
    if _org: s.shapes.add_picture(_org,Inches(0.85),Inches(0.7),height=Inches(1.05))
    _crs=_logo("n8n-course-logo.png")
    if _crs: s.shapes.add_picture(_crs,Inches(11.4),Inches(0.72),height=Inches(1.0))
    txt(s,Inches(0.9),Inches(2.3),Inches(12),Inches(0.6),[[("LEARNER GUIDE  ·  COURSE SLIDES",16,BLUE,True)]])
    txt(s,Inches(0.9),Inches(2.9),Inches(12.0),Inches(1.6),[[(TITLE,46,INK,True)]])
    rect(s,Inches(0.92),Inches(4.3),Inches(2.4),Inches(0.06),TEAL)
    txt(s,Inches(0.9),Inches(4.65),Inches(12),Inches(1.4),
        [[(f"WSQ Course Code: {COURSE_CODE}",16,GREY,False)],
         [("Conducted by Tertiary Infotech Academy Pte Ltd  ·  UEN 201200696W",14,GREY,False)],
         [(f"Version {VERSION}  ·  {VERSION_DATE}",14,BLUE,True)]],space=6)
    txt(s,Inches(0.9),Inches(6.55),Inches(12),Inches(0.34),[[("© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.  ·  www.tertiarycourses.com.sg",10,GREY,False)]])

# ─── admin components (wsq-slides house components — do not hand-roll) ──────
PALETTE=[BLUE,TEAL,VIOLET,AMBER]
def trainer_slide(kicker,name,role,rows,initials,accent=BLUE):
    s=slide(); head(s,"About the Trainer",kicker=kicker,kcolor=accent)
    lx=Inches(0.85); lw=Inches(3.65)
    rect(s,lx,Inches(1.95),lw,Inches(4.7),LIGHT); rect(s,lx,Inches(1.95),lw,Inches(0.12),accent)
    bd=Inches(1.7); ax=int(lx+(lw-bd)/2)
    oval(s,ax,Inches(2.5),bd,bd,accent)
    txt(s,ax,Inches(2.5),bd,bd,[[(initials,44,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    txt(s,lx+Inches(0.15),Inches(4.55),lw-Inches(0.3),Inches(0.6),[[(name,21,INK,True)]],align=PP_ALIGN.CENTER)
    txt(s,lx+Inches(0.15),Inches(5.2),lw-Inches(0.3),Inches(1.2),[[(role,13,GREY,False)]],align=PP_ALIGN.CENTER)
    rx=Inches(4.9); rw=Inches(7.6); ry=Inches(1.95); rh=Inches(4.7)
    n=len(rows); gy=Inches(0.2); th=int((rh-gy*(n-1))/n)
    for i,(label,val) in enumerate(rows):
        y=int(ry+(th+gy)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,rx,y,rw,th,LIGHT); rect(s,rx,y,Inches(0.1),th,col)
        vruns=[(val,14,INK,False)] if val else [("____________________________________________",13,LINE,False)]
        txt(s,rx+Inches(0.32),y,rw-Inches(0.6),th,
            [[(label.upper(),11,col,True)],vruns],anchor=MSO_ANCHOR.MIDDLE,space=3)
    footer(s); return s
def tile_grid(title,items,kicker=None,cols=2,size=15,icons=None,accent=BLUE):
    s=slide(); head(s,title,kicker=kicker,kcolor=accent)
    n=len(items); rows=math.ceil(n/cols)
    X0=Inches(0.85); Y0=Inches(1.95); TOTW=Inches(11.63); AREAH=Inches(4.78)
    gx=Inches(0.3); gy=Inches(0.26)
    cw=int((TOTW-gx*(cols-1))/cols); ch=int((AREAH-gy*(rows-1))/rows)
    bd=Inches(0.6)
    for i,it in enumerate(items):
        r=i//cols; c=i%cols
        x=int(X0+(cw+gx)*c); y=int(Y0+(ch+gy)*r); col=PALETTE[i%len(PALETTE)]
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,Inches(0.1),ch,col)
        oval(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,col)
        ic=icons[i] if icons else str(i+1)
        txt(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,[[(ic,19,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        tx=x+Inches(1.08); tw=cw-Inches(1.32)
        txt(s,tx,int(y+Inches(0.1)),tw,int(ch-Inches(0.16)),[[(it,size,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def flow_h(title,steps,kicker=None,color=BLUE):
    s=slide(); head(s,title,kicker=kicker,kcolor=color)
    n=len(steps); X0=Inches(0.85); TOTW=Inches(11.63); gap=Inches(0.34)
    cw=int((TOTW-gap*(n-1))/n); y=Inches(2.55); ch=Inches(3.15); bd=Inches(0.82)
    for i,st in enumerate(steps):
        x=int(X0+(cw+gap)*i)
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,cw,Inches(0.1),color)
        oval(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,color)
        txt(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,[[(str(i+1),30,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.16),int(y+Inches(1.55)),cw-Inches(0.32),int(ch-Inches(1.7)),[[(st,14,INK,False)]],align=PP_ALIGN.CENTER)
        if i<n-1:
            txt(s,int(x+cw-Inches(0.04)),int(y+ch/2-Inches(0.3)),int(gap+Inches(0.08)),Inches(0.6),
                [[("▶",15,color,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s

# ============================================================ BUILD
cover()

# ---------- ADMIN ----------
content("Digital Attendance (Mandatory)",[
 "It is mandatory to take the AM, PM and Assessment digital attendance for WSQ-funded courses.",
 "The trainer/administrator will display the digital attendance QR code generated from the SSG portal.",
 "Scan the QR code with your mobile phone camera and submit your attendance.",
 "A minimum of 75% attendance is required to be eligible for assessment and funding."],kicker="TRAQOM · SSG DIGITAL ATTENDANCE")
trainer_slide("YOUR TRAINER · GENERAL","Your Trainer","General Trainer template —\nto be completed by the trainer",
 [("Name",""),("Title / Designation",""),("Qualifications",""),
  ("Areas of expertise",""),("Training & industry experience",""),("Contact","")],
 initials="?",accent=GREY)
trainer_slide("YOUR TRAINER","Dr. Alfred Ang","Principal Trainer\nTertiary Infotech Academy Pte. Ltd.",
 [("Role","Principal Trainer, Tertiary Infotech Academy Pte. Ltd."),
  ("Qualifications","PhD — specialises in AI, automation and software engineering."),
  ("Delivers","WSQ courses on AI agents, automation (n8n) and app development."),
  ("Founder","Founder and lead instructor at Tertiary Infotech / Tertiary Courses.")],
 initials="AA",accent=BLUE)
content("Let's Know Each Other",[
 "Your name and organisation / role.",
 "Your experience with automation or AI tools (if any).",
 "What you want to automate after this course."],kicker="ICE-BREAKER")
tile_grid("Ground Rules",[
 "Set your mobile phone to silent mode.","Participate actively — no question is too small.",
 "Mutual respect: agree to disagree.","One conversation at a time.",
 "Be punctual; return from breaks on time.","75% attendance is required."],
 kicker="HOUSEKEEPING",cols=2,size=15)
website_slide("Download Course Material",
 IMG(".claude/skills/tertiary-course-slides/assets/lms-tms-portal.png"),
 ["Go to lms-tms.tertiaryinfotech.com.",
  "Enter your registered email and click Send OTP.",
  "Key in the one-time password from your inbox to log in.",
  "Open this course to download the slides and Learner Guide.",
  "Keep them open — the assessment is open book.",
  "Attendance and assessment submission also happen here."],
 kicker="COURSE PORTAL")
tile_grid("Download the Course Flows (GitHub)",[
 "Open the course repo: github.com/tertiarycourses/TGS-2023035977-Agentic-AI-Automation-with-n8n",
 "Code ▾ → Download ZIP (or git clone) — all workflows are in the labs/ folder.",
 "In n8n: Workflows → Add workflow → ... → Import from File → pick the activity .json.",
 "After importing, re-select YOUR OWN credentials on each node, then Save & Publish."],
 kicker="GET THE WORKFLOWS",cols=1,size=15)
# Lesson plan — three day cards
s=slide(); head(s,"Lesson Plan — 3 Days, 9:30am–6:30pm",kicker="SCHEDULE")
_days=[(BLUE,"Day 1 — Automate, then add AI",
        ["Topic 1: n8n basics — triggers, actions, data","Activities 1, 2, 3a, 3b — forms, storage, logic",
         "Topic 2: AI Agents — model · memory · tools · instructions","Activities 4a, 4b — Telegram agent + Data Table tool"]),
       (TEAL,"Day 2 — Connect it to the world",
        ["Topic 3: Webhooks — Activity 5 (website chatbot)","Topic 4: APIs & HTTP — Activity 6 (day-trading agent)",
         "Topic 5: RAG — Activities 7a, 7b (grounded agents)"]),
       (VIOLET,"Day 3 — Govern, then prove it",
        ["Topic 6: Security — human-in-the-loop + guardrails","Activities 8a, 8b, 8c — the HR Service Portal",
         "Topic 7: Mini capstone + presentations","Written Assessment (SAQ) 1 hr · Practical (PP) 1 hr"])]
for i,(col,t,items) in enumerate(_days):
    x=int(Inches(0.85)+Inches(3.99)*i)
    rect(s,x,Inches(1.95),Inches(3.75),Inches(0.5),col)
    txt(s,x,Inches(1.95),Inches(3.75),Inches(0.5),[[(t,12.5,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    box(s,x,Inches(2.45),Inches(3.75),Inches(3.5),col,round_=False)
    bullets(s,x+Inches(0.22),Inches(2.68),Inches(3.33),Inches(3.2),items,size=11.5,mcolor=col,gap=8)
takeaway(s,"Each day runs 9:30am–6:30pm — 8 instructional hours with a 1-hour lunch; tea breaks counted within.")
footer(s)
tile_grid("Learning Outcomes",[
 "LO1: Build automated workflows in n8n using triggers, actions, nodes and flows.",
 "LO2: Design AI agents with LLMs, memory and tools, triggered from chat / Telegram.",
 "LO3: Apply Retrieval-Augmented Generation (RAG) to ground agents in your documents.",
 "LO4: Integrate external systems via webhooks, APIs and HTTP requests.",
 "LO5: Apply human-in-the-loop and guardrails to secure agentic automations."],
 kicker="WHAT YOU'LL ACHIEVE",cols=1,size=15)
# The lab journey
tile_grid("Twelve Connected Labs",[
 "Act 1 — Form → Email: your first automation, on a real flyer.",
 "Act 2 — Data Table: store every submission, not just forward it.",
 "Act 3a/3b — IF logic: route Yes/No to storage or a thank-you.",
 "Act 4a — Telegram AI agent: model + memory + instruction.",
 "Act 4b — Agent + tool: answers HR questions from a Data Table.",
 "Act 5 — Webhook: your agent behind a public website chatbot.",
 "Act 6 — APIs: live candles + news → Buy / Sell / Hold calls.",
 "Act 7a — RAG: upload a PDF, ask the bot in Telegram.",
 "Act 7b — RAG at scale: 20 brochures in a real vector DB.",
 "Act 8a–8c — HR portal: approval gate, dashboard, guardrails.",
 "Capstone — design and demo your own end-to-end automation."],
 kicker="COURSE JOURNEY",cols=2,size=11.5)
content("Briefing for Assessment",[
 "Place phones and other materials under the table or on the floor.",
 "No photos or recording of assessment scripts.","No discussion during the assessment.",
 "Use a black/blue pen for hard-copy assessments.","No liquid paper / correction tape.",
 "Scripts are collected when time is up."],kicker="BEFORE THE ASSESSMENT")
content("Assessment",[
 "Written Assessment (SAQ) — 1 hour.","Practical Performance (PP) — 1 hour.",
 "Format: Open Book — slides, Learner Guide and approved materials only.",
 "A mini capstone project is presented on Day 3.","An appeal process is available if required."],kicker="FINAL ASSESSMENT")
flow_h("Assessment Flow",[
 "TRAQOM survey — scan the QR code on the LMS",
 "Assessment digital attendance — scan the SSG QR",
 "Sit WA (SAQ) then PP — open book",
 "Submit your answers on the LMS",
 "Sign the Assessment Summary Record"],kicker="ON ASSESSMENT DAY")

# ---------- TOPIC 1: WORKFLOW AUTOMATION ----------
K1="TOPIC 1 · WORKFLOW AUTOMATION"
K1L="TOPIC 1 · LAB WORKFLOW"
section("TOPIC 1","Workflow Automation with n8n","01",
 "What n8n is · triggers · data-processing nodes · JSON and expressions · executions",
 "Applied in Activities 1, 2, 3a and 3b")
s=concept(K1,"What Is n8n?","A workflow automation platform: connect apps, data and AI on one visual canvas — no-code to full-code.")
ncards(s,[(BLUE,"Build visually","Drag nodes onto a canvas and wire them together. 400+ app integrations, plus HTTP and Code nodes when no integration exists."),
 (TEAL,"Run anywhere","Free cloud trial at n8n.io, or self-host with Docker. Webhooks, schedules and chat triggers work the same in both."),
 (VIOLET,"AI-native","AI Agent and LangChain nodes are built in — attach any LLM (OpenAI, Gemini, Claude), memory, tools and vector stores.")],
 y=Inches(2.2),h=Inches(3.6),cols=3)
takeaway(s,"One canvas to connect apps, data and AI — automation and agents without gluing code by hand.")
footer(s)
website_slide("n8n.io",IMG(".claude/skills/tertiary-course-slides/assets/site-n8n.png"),
 ["n8n is an open, fair-code workflow automation platform.","Free cloud trial at n8n.io, or self-host with Docker.","Same visual editor in both.",
  "This course: start on the cloud trial, keep the Docker option for after."],
 kicker="THE PLATFORM")
s=concept(K1,"What Automation Removes","Automation is not 'the same work faster' — it removes the hand-offs where a person re-types what another system already knows.")
txt(s,Inches(0.85),Inches(2.1),Inches(1.4),Inches(0.8),[[("MANUAL",12,RED,True)]],anchor=MSO_ANCHOR.MIDDLE)
chev_strip(s,[("Form filled in",""),("Someone reads it",""),("Re-typed into Excel",""),("Someone remembers to reply","")],y=Inches(2.05),h=Inches(0.8),color=RED,x0=Inches(2.3),tw=Inches(10.18),tsz=11)
txt(s,Inches(0.85),Inches(3.25),Inches(1.4),Inches(0.8),[[("AUTOMATED",12,GREEN,True)]],anchor=MSO_ANCHOR.MIDDLE)
chev_strip(s,[("Form submitted",""),("Flow triggered",""),("Row written",""),("Reply sent","")],y=Inches(3.2),h=Inches(0.8),color=GREEN,x0=Inches(2.3),tw=Inches(10.18),tsz=11)
ncards(s,[(BLUE,"Consistency","The same input produces the same output, every time, at 3am."),
 (TEAL,"Traceability","Every run leaves an execution history someone can read a year later."),
 (VIOLET,"Capacity","People move up to judgement calls; the machine does the re-typing.")],
 y=Inches(4.35),h=Inches(1.75),cols=3,numbered=False)
takeaway(s,"Automate the hand-offs first — that is where time and errors live.")
footer(s)
s=concept(K1,"Every Workflow Is the Same Shape","Trigger first, then actions in order, with data flowing left to right. Only the nodes change.")
chev_strip(s,[("TRIGGER","what starts it"),("ACTION","do the work"),("ACTION","do more work"),("OUTPUT","reply, store or notify")],y=Inches(2.1),h=Inches(1.05),color=BLUE)
ncards(s,[(BLUE,"One trigger","A workflow has exactly one entry point. Change the trigger and you have a different flow — the actions may not change at all."),
 (TEAL,"Actions are ordered","Each action runs after the one before it and can read the outputs of every node before it."),
 (VIOLET,"Data flows as JSON","Every node passes a list of JSON items to the next — the same structure in every lab.")],
 y=Inches(3.5),h=Inches(2.55),cols=3)
takeaway(s,"Trigger, actions, output. Learn this once in Activity 1 and every later lab is a variation.")
footer(s)
# --- Triggers ---
s=concept(K1,"Trigger Nodes — What Is Allowed to Start a Workflow","The trigger you choose is a statement about who or what may start the process.")
ncards(s,[(BLUE,"Manual Trigger","Click Execute Workflow — for building and testing, and for one-off jobs like the Activity 7b ingestion run."),
 (TEAL,"Schedule Trigger","A clock starts the flow — cron or interval. Reports, reminders, nightly syncs."),
 (VIOLET,"Form Trigger","n8n hosts a web form for you; each submission starts a run. Activities 1–3."),
 (AMBER,"Webhook","External systems call a URL you expose. Websites and apps — Activities 5, 7b, 8."),
 (GREEN,"Chat / Telegram Trigger","Each chat message starts a run — n8n's chat UI or your Telegram bot. Activities 4, 6, 7a."),
 (RED,"App & Email Triggers","On new Gmail, new Sheet row, new Drive file, new IMAP email — react to changes in apps you already use.")],
 y=Inches(1.95),h=Inches(4.2),cols=3)
takeaway(s,"Pick the trigger by asking: who or what should be allowed to start this process?")
footer(s)
s=concept(K1,"Triggers Used in This Course","Every lab's trigger, and why that trigger is the right front door.")
data_table(s,[3.0,3.2,5.43],["Trigger","Where","Why it fits"],[
 ["Form Trigger","Activities 1, 2, 3a, 3b","A visitor RSVP must start the flow"],
 ["Telegram Trigger","Activities 4a, 4b, 6, 7a","Each bot message is one conversation turn"],
 ["Webhook — POST","Activities 5, 7b, 8a, 8c","A website sends data and waits for a reply"],
 ["Webhook — GET","Activity 8b","The dashboard pulls JSON from a URL"],
 ["Manual Trigger","Activity 7b ingestion","A human runs the document load once"],
],y=Inches(2.0),rh=Inches(0.5))
takeaway(s,"Schedule and app triggers follow the same pattern — swap the front door, keep the flow.")
footer(s)
img_slide("Trigger Nodes on the n8n Canvas",IMG(".claude/skills/tertiary-course-slides/assets/n8n-triggers.png"),
 "n8n trigger nodes: Manual · Schedule · WhatsApp · Telegram · Gmail · Chat · Form · Webhook",
 kicker=K1,kcolor=BLUE)
# --- Data-processing actions ---
s=concept(K1,"Data-Processing Nodes — The Workhorses","Between the trigger and the output, these nodes shape, route and transform the data.")
ncards(s,[(BLUE,"Edit Fields (Set)","Add, rename or reshape fields — the node you reach for first when data is the wrong shape."),
 (TEAL,"IF / Switch","Branch the flow: IF gives true/false paths; Switch gives one path per case."),
 (VIOLET,"Filter","Let only matching items continue — drop the rest of the list."),
 (AMBER,"Merge","Combine two branches — append rows, match by key, or choose one side."),
 (GREEN,"Split Out / Aggregate","Turn one item holding a list into many items — and back again."),
 (RED,"Code","JavaScript or Python for the 5% a built-in node cannot do."),
 (BLUE,"Loop / Wait","Process items in batches; pause a flow for time or an event."),
 (TEAL,"HTTP Request","Call any API on the internet — the universal escape hatch.")],
 y=Inches(1.95),h=Inches(4.2),cols=4)
takeaway(s,"Most flows are: trigger → reshape (Set) → decide (IF) → act (app node). Reach for Code last.")
footer(s)
img_slide("Data-Processing Nodes on the Canvas",IMG(".claude/skills/tertiary-course-slides/assets/n8n-key-nodes.png"),
 "If · Switch · Filter · Edit Fields · Split Out · Aggregate · Merge · Loop · Date & Time · Execute Workflow · Wait · Code",
 kicker=K1,kcolor=BLUE)
s=concept(K1,"Where the Data Goes — Storage & App Actions","Action nodes that write the result somewhere useful.")
ncards(s,[(BLUE,"Data Table","n8n's built-in spreadsheet — instant, no credential. Trial Data Tables are NOT permanent; use for class demos."),
 (TEAL,"Google Sheets / Excel","A real spreadsheet you keep — OAuth2 credential, Append Row. The persistent upgrade in Activity 3b."),
 (VIOLET,"Gmail / Outlook","Send (and in Activity 8a, Send and Wait for Response) — email as an output and as an approval gate."),
 (AMBER,"Vector Store","Store embeddings for RAG — in-memory for demos, Pinecone / Supabase / Qdrant for production.")],
 y=Inches(2.0),h=Inches(4.1),cols=2)
takeaway(s,"Anything you must keep goes to external storage — trial Data Tables vanish with the trial.")
footer(s)
# --- JSON / expressions / executions ---
s=concept(K1,"JSON — How Data Travels Between Nodes","Every node passes a list of items; each item is a JSON object of key/value pairs.")
bullets(s,Inches(0.85),Inches(2.05),Inches(5.6),Inches(3.6),[
 "JSON (JavaScript Object Notation) is a simple text format for data.",
 "Values can be text, numbers, true/false, lists [ ] or nested objects { }.",
 "Most APIs send and receive JSON — so does every n8n node.",
 "Click any node to inspect its input and output JSON."],size=14,gap=10)
bx=box(s,Inches(6.8),Inches(2.05),Inches(5.68),Inches(3.4),BLUE)
txt(s,Inches(7.1),Inches(2.25),Inches(5.1),Inches(0.3),[[("ONE FORM SUBMISSION AS JSON",11,BLUE,True)]])
txt(s,Inches(7.1),Inches(2.65),Inches(5.1),Inches(2.6),[[('{',13,INK,False)],
 [('  "Name": "Alice Tan",',13,INK,False)],
 [('  "Email": "alice@corp.com",',13,INK,False)],
 [('  "Attending": "Yes",',13,INK,False)],
 [('  "Pax": 2',13,INK,False)],
 [('}',13,INK,False)]],space=3)
takeaway(s,'Read any value later with an expression:  {{ $json.Name }}  →  "Alice Tan"')
footer(s)
s=concept(K1,"Expressions — The Token, Not the Text","An expression references a value that will exist at run time — it is resolved fresh on every run.")
chev_strip(s,[("Trigger runs","a submission arrives"),("Outputs exist","Name, Email, Attending…"),("Later node references them","{{ $json.Name }}"),("Value arrives at run time","different every run")],y=Inches(2.1),h=Inches(1.05),color=BLUE)
ncards(s,[(GREEN,"✓ Mapped with the picker","Drag the field from the input panel — n8n writes the expression for you and shows a live preview of the resolved value."),
 (RED,"✗ Typed as plain text","Type 'Name' as literal text and every email says 'Name'. If the path is wrong the value resolves to empty — not to an error.")],
 y=Inches(3.5),h=Inches(2.55),cols=2,numbered=False)
takeaway(s,"Use expressions in any field — subject lines, URLs, conditions. Drag, don't type.")
footer(s)
s=concept(K1,"Test vs Production Executions","The same workflow runs in two modes — know which one you are looking at.")
two=[(BLUE,"TEST — in the editor",["Click Execute Workflow to run once.","Data is shown live on the canvas, node by node.","Pin a node's output to freeze it while you build downstream.","Perfect for building — nothing needs to be Active."]),
     (VIOLET,"PRODUCTION — Active toggle ON",["Runs automatically when the trigger fires.","Nothing appears on the canvas — runs are logged in Executions.","Every run records status, timing and full data per node.","This is what your users experience."])]
for i,(col,t,items) in enumerate(two):
    x=int(Inches(0.85)+Inches(5.95)*i)
    rect(s,x,Inches(2.0),Inches(5.68),Inches(0.5),col)
    txt(s,x,Inches(2.0),Inches(5.68),Inches(0.5),[[(t,13.5,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    box(s,x,Inches(2.5),Inches(5.68),Inches(3.4),col,round_=False)
    bullets(s,x+Inches(0.3),Inches(2.75),Inches(5.1),Inches(3.0),items,size=13,mcolor=col,gap=9)
takeaway(s,"The Executions list is the honest account of what happened — debug from there, not from memory.")
footer(s)
img_slide("Execution History",IMG(".claude/skills/tertiary-course-slides/assets/n8n-execution-history.png"),
 "Executions tab — each run shows status, duration, ID and the full data at every node",
 kicker=K1,kcolor=BLUE)
img_slide("The n8n Editor",IMG(".claude/skills/tertiary-course-slides/assets/n8n-editor.png"),
 "n8n canvas: left sidebar navigation · centre canvas · node toolbar · Editor / Executions / Evaluations tabs",
 kicker=K1,kcolor=BLUE)
# --- setup ---
website_slide("Sign Up for n8n Cloud",
 IMG(".claude/skills/tertiary-course-slides/assets/n8n-register.png"),
 ["Go to app.n8n.cloud/register in your browser.",
  "Enter your company email and click Submit.",
  "Open the verification email from n8n and click the link to confirm.",
  "Set your password and complete the short profile questions.",
  "n8n creates your workspace at <name>.app.n8n.cloud and opens the editor.",
  "The free trial runs 14 days — no credit card needed."],
 kicker="YOUR LOGIN · CLOUD INSTANCE")
s=concept(K1,"Credentials — Connect Your Accounts Once","Nodes reference credentials by name; set them up once under Credentials → Add credential.")
ncards(s,[(BLUE,"Email","Gmail or Outlook via OAuth2 — used from Activity 1 onward."),
 (TEAL,"LLM","OpenAI / Google Gemini API key — powers every AI agent from Activity 4."),
 (VIOLET,"Telegram","Bot token from @BotFather — the chat front door for Activities 4, 6, 7a."),
 (AMBER,"Google Sheets","OAuth2 to your Google account — persistent storage in Activity 3b.")],
 y=Inches(2.0),h=Inches(3.7),cols=2)
takeaway(s,"Imported workflows keep credential NAMES only — always re-select your own after importing.")
footer(s)
# --- Topic 1 labs ---
lab_slide(K1L,"ACT 1","Activity 1 — Flyer with QR Code (Form → Email)",
 "Collect a visitor's RSVP with a hosted n8n Form and email it to the admin — then put the form's QR code on a real event flyer.",
 [[("Form Trigger","visitor submits the RSVP"),("Gmail — Send","admin receives the details")]],
 IMG("labs/activity1-flyer-form/Activity1-Flyer-Form.png"),
 "Form Trigger → Gmail  ·  Gmail OAuth2 credential  ·  full steps in the Learner Guide")
gallery_slide("Sample Flyers from Past Students",
 [IMG("labs/activity1-flyer-form/flyer-sample1-preview.png"),
  IMG("labs/activity1-flyer-form/flyer-sample2-preview.png"),
  IMG("labs/activity1-flyer-form/flyer-sample3.jpeg")],
 ["Network event","Event poster","Bowling party"],kicker="ACT 1 · GROUP ACTIVITY")
lab_slide(K1L,"ACT 2","Activity 2 — Capture Submissions in a Data Table",
 "Extend Activity 1 so every submission is also saved — your first taste of storing data, not just forwarding it.",
 [[("Form Trigger","same RSVP form"),("Data Table — Insert Row","every submission saved"),("Gmail — Send","admin still notified")]],
 IMG("labs/activity2-data-table/Activity2-Data-Table.png"),
 "Form Trigger → Data Table + Gmail  ·  columns mapped with {{ $json.… }} expressions  ·  steps in the Learner Guide")
lab_slide(K1L,"ACT 3a","Activity 3a — Conditional Response (Data Table)",
 "Add decision-making: attending guests are saved; everyone else gets a polite thank-you email.",
 [[("Form Trigger","+ Attending? Yes/No field"),("IF","Attending = Yes ?"),("Data Table","YES → save the RSVP"),("Gmail","NO → thank-you email")]],
 IMG("labs/activity3-conditional/Activity3a-Conditional-Data-Table.png"),
 "Form → IF → Data Table / Gmail  ·  both branches must be built  ·  steps in the Learner Guide")
lab_slide(K1L,"ACT 3b","Activity 3b — Conditional Response (Google Sheets)",
 "Same logic, persistent storage: the YES branch appends to a real Google Sheet you keep after the trial.",
 [[("Form Trigger","same form"),("IF","Attending = Yes ?"),("Google Sheets — Append","YES → a spreadsheet you keep"),("Gmail","NO → thank-you email")]],
 IMG("labs/activity3-conditional/Activity3b-Conditional-Google-Sheets.png"),
 "Form → IF → Google Sheets / Gmail  ·  Google Sheets OAuth2  ·  steps in the Learner Guide")
brk("Lunch Break","1 hour  ·  see you at 2:00 pm",AMBER)

# ---------- TOPIC 2: AI AGENTS ----------
K2="TOPIC 2 · AI AGENTS"
K2L="TOPIC 2 · LAB WORKFLOW"
section("TOPIC 2","AI Agents","02",
 "Generative vs agentic AI · model, memory, tools, instructions · model parameters · MCP",
 "Applied in Activities 4a and 4b",color=VIOLET)
two_panel("Generative AI vs Agentic AI",
 "GENERATIVE AI — answers",["You ask; it writes one answer.","No memory of your systems, no actions.","Quality depends on what you paste into the prompt.","Example: ChatGPT summarising a document."],
 "AGENTIC AI — acts",["Works toward a goal, not just one reply.","Calls tools: looks up data, calls APIs, writes records.","Holds a conversation with memory.","Example: a bot that checks the Employees table and answers."],
 kicker=K2,lcolor=BLUE,rcolor=VIOLET,
 take="Generative AI produces content. Agentic AI decides and does — which is why it needs governance.")
# anatomy of an agent
s=concept(K2,"Components of an AI Agent","Four parts, one hub: the agent node wires them together — and only some are under your direct control.")
box(s,Inches(4.7),Inches(3.3),Inches(3.9),Inches(1.15),VIOLET,lw=2)
txt(s,Inches(4.7),Inches(3.3),Inches(3.9),Inches(1.15),[[("THE AI AGENT",15,VIOLET,True)],[("plans · decides · calls tools",10.5,GREY,False)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=2)
_parts=[(BLUE,"MODEL","The LLM 'brain' — interprets language, reasons, chooses the next step. gpt-4.1-mini in this course.",Inches(0.85),Inches(2.0)),
        (TEAL,"MEMORY","Keeps the conversation — follow-up questions still make sense. Window buffer per chat/session.",Inches(8.85),Inches(2.0)),
        (AMBER,"TOOLS","Abilities it may use: Data Table lookups, vector stores, HTTP calls, sub-workflows.",Inches(0.85),Inches(4.5)),
        (GREEN,"INSTRUCTIONS","The system message — identity, scope, rules and refusals. Always in force.",Inches(8.85),Inches(4.5))]
for col,t,body,x,y in _parts:
    box(s,x,y,Inches(3.6),Inches(1.6),col)
    txt(s,x+Inches(0.2),y+Inches(0.14),Inches(3.2),Inches(0.32),[[(t,13,col,True)]])
    txt(s,x+Inches(0.2),y+Inches(0.5),Inches(3.2),Inches(1.1),[[(body,10.5,INK,False)]])
for (x1,y1) in [(Inches(4.45),Inches(2.85)),(Inches(8.85),Inches(2.85)),(Inches(4.45),Inches(4.9)),(Inches(8.85),Inches(4.9))]:
    pass  # visual adjacency carries the linkage
takeaway(s,"Model + Memory + Tools + Instructions — every agent in this course is exactly these four parts.")
footer(s)
s=concept(K2,"The Model — Popular LLM Providers","Any chat model plugs into the same AI Agent node — swap the brain, keep the agent.")
data_table(s,[3.0,4.4,4.23],["Provider","Models","Notes"],[
 ["OpenAI","gpt-4.1, gpt-4.1-mini, gpt-4o","Course default: gpt-4.1-mini"],
 ["Google","Gemini 2.x Flash / Pro","Used for embeddings in Activity 7"],
 ["Anthropic","Claude (Opus, Sonnet, Haiku)","Strong reasoning and safety"],
 ["Meta","Llama 3.x","Open weights — self-hostable"],
 ["Mistral","Mistral / Mixtral","Open weights — EU option"],
],y=Inches(2.0),rh=Inches(0.5))
takeaway(s,"Pick by task: small fast models for classification and guardrails, larger models for reasoning.")
footer(s)
s=concept(K2,"Model Parameters — Temperature and Friends","Settings on the chat-model node shape how the model answers — the most important is temperature.")
ncards(s,[(BLUE,"Temperature 0 – 0.3","Deterministic and repeatable. Use for classification, guardrails, data extraction — automation that must give the same decision twice."),
 (TEAL,"Temperature ≈ 0.7","Balanced — natural-sounding chat with some variety. The default for customer-facing assistants."),
 (AMBER,"Temperature 1.0 +","Creative and surprising. Marketing copy and brainstorming — never for decisions.")],
 y=Inches(1.95),h=Inches(2.2),cols=3)
ncards(s,[(VIOLET,"Top-p","Alternative sampling control — limits choices to the most probable tokens. Tune temperature OR top-p, not both."),
 (GREEN,"Max tokens","Caps the length of the reply — protects cost and keeps chat answers short."),
 (RED,"Frequency / presence penalty","Discourage repetition and nudge new topics — useful for long generations.")],
 y=Inches(4.3),h=Inches(1.85),cols=3)
takeaway(s,"For business automation keep temperature LOW — the same input should produce the same decision.")
footer(s)
s=concept(K2,"Memory — Why the Agent Remembers","Without memory every message is a stranger; with it, 'what about tomorrow?' makes sense.")
chev_strip(s,[("Msg 1: 'Any leave left?'","agent answers: 12 days"),("Stored in memory","keyed by chat / session ID"),("Msg 2: 'What about Bob?'","agent knows the topic is leave"),("Window slides","only the last N turns kept")],y=Inches(2.1),h=Inches(1.05),color=TEAL)
ncards(s,[(BLUE,"Simple (buffer window) memory","Keeps the last N exchanges of THIS conversation — n8n's default, used in all course agents."),
 (TEAL,"Session key","Memory is per chat ID — two Telegram users never see each other's context.")],
 y=Inches(3.5),h=Inches(2.4),cols=2,numbered=False)
takeaway(s,"Memory is conversation context — it is NOT long-term knowledge. Facts live in tools and documents (RAG).")
footer(s)
s=concept(K2,"Tools — What the Agent May Do","Attach tools to the agent's Tool input; the model decides when to call one, based on your description.")
ncards(s,[(BLUE,"Data Table / Sheets tool","Look up structured records — the Employees table in Activity 4b."),
 (TEAL,"Vector Store tool","Retrieve document chunks for grounded answers — the knowledge_base in Activity 7."),
 (VIOLET,"HTTP Request tool","Call any external API mid-conversation — prices, weather, CRM."),
 (AMBER,"Sub-workflow tool","Wrap an entire n8n workflow as one callable tool — your own logic, on demand.")],
 y=Inches(1.95),h=Inches(3.7),cols=2)
takeaway(s,"The tool DESCRIPTION is how the agent knows when to call it — write it for the model, not for a developer.")
footer(s)
s=concept(K2,"Instructions — The Four Parts That Constrain","The system message is always in force. Every good agent instruction in this course states four things.")
ncards(s,[(BLUE,"Identity","Who the agent is and what it must never do. 'You are HR Buddy, the HR assistant for staff of Acme Pte Ltd.'"),
 (GREEN,"Source rules","Where answers come from. 'Answer ONLY from the Employees tool / the uploaded documents.'"),
 (RED,"Refusals","What is out of bounds, stated positively. 'Do not reveal salaries or another person's records.'"),
 (AMBER,"Escalation","What to do at the boundary. 'If unsure, say so and direct the user to hr@acme.com.'")],
 y=Inches(1.95),h=Inches(4.2),cols=2)
takeaway(s,"Vague instructions produce confident wrong answers — every rule you skip, the model improvises.")
footer(s)
s=concept(K2,"Good vs Bad Instructions","The same bot, two system messages — one is testable, one is a hope.")
bx=box(s,Inches(0.85),Inches(2.0),Inches(5.68),Inches(3.9),RED)
txt(s,Inches(1.15),Inches(2.2),Inches(5.1),Inches(0.3),[[("✗  TOO VAGUE",12.5,RED,True)]])
txt(s,Inches(1.15),Inches(2.6),Inches(5.1),Inches(1.0),[[('"You are a helpful assistant. Answer the user\'s questions politely."',13,INK,False)]])
txt(s,Inches(1.15),Inches(3.7),Inches(5.1),Inches(2.0),[[("No identity · no sources · no refusals · no escalation.",11,GREY,False)],
 [("It will happily invent leave balances and reveal other people's data — politely.",11,GREY,False)]],space=6)
bx=box(s,Inches(6.8),Inches(2.0),Inches(5.68),Inches(3.9),GREEN)
txt(s,Inches(7.1),Inches(2.2),Inches(5.1),Inches(0.3),[[("✓  CONSTRAINED",12.5,GREEN,True)]])
txt(s,Inches(7.1),Inches(2.6),Inches(5.15),Inches(3.2),
 [[('"You are HR Buddy, the HR assistant for Acme staff.',12,INK,False)],
  [('Answer only questions on leave policy, payroll dates and claims.',12,INK,False)],
  [('Use the Employees tool for any staff lookup — never answer from general knowledge.',12,INK,False)],
  [('Never reveal salaries or another employee\'s personal data.',12,INK,False)],
  [('If you are not sure, say so and direct the user to hr@acme.com."',12,INK,False)]],space=5)
takeaway(s,"Identity · source rules · refusals · escalation — you can test each line by trying to break it.")
footer(s)
# MCP
s=concept(K2,"MCP — Model Context Protocol","An open standard that gives agents a common plug for tools and data — instead of one custom integration per pair.")
chev_strip(s,[("AI Agent","any MCP-capable client"),("MCP Client","speaks the protocol"),("MCP Server","exposes tools + data"),("Your Systems","databases, APIs, files")],y=Inches(2.1),h=Inches(1.05),color=VIOLET)
ncards(s,[(RED,"Without MCP","Every agent × every tool needs its own custom integration — N agents and M tools means N × M connectors to build and maintain."),
 (GREEN,"With MCP","Build ONE MCP server per system; any MCP-capable agent can use it. N + M pieces, and tools become reusable across agents.")],
 y=Inches(3.5),h=Inches(2.55),cols=2,numbered=False)
takeaway(s,"MCP is like USB-C for AI tools — one connector, many devices.")
footer(s)
two_panel("MCP in n8n",
 "MCP SERVER TRIGGER — n8n serves tools",["Expose your n8n workflows AS tools over MCP.","Claude, IDEs or other agents call your flows directly.","n8n becomes the tool layer for any MCP client.","Auth via bearer token on the server URL."],
 "MCP CLIENT TOOL — n8n consumes tools",["Attach external MCP servers to your n8n AI Agent.","The agent gains their tools without custom nodes.","Mix MCP tools with native n8n tools freely.","Same agent loop — more reach."],
 kicker=K2,lcolor=VIOLET,rcolor=BLUE,
 take="Two directions, one protocol: n8n can serve tools to other agents, and borrow tools for its own.")
# labs 4a/4b
lab_slide(K2L,"ACT 4a","Activity 4a — Telegram AI Agent (Customer Service)",
 "Your first agent: a customer-service bot on Telegram — model + memory + a system instruction.",
 [[("Telegram Trigger","each message to your bot"),("AI Agent","gpt-4.1-mini + window memory + instruction"),("Telegram — Send","reply lands in the chat")]],
 IMG("labs/activity4-telegram-agent/Activity4a-Telegram-Agent.png"),
 "Telegram bot via @BotFather  ·  OpenAI + Telegram credentials  ·  steps in the Learner Guide",color=VIOLET)
lab_slide(K2L,"ACT 4b","Activity 4b — Agent + Data Table Tool (HR Admin)",
 "Give the same agent a tool: an Employees Data Table (100 records) it can query — answers now come from real data.",
 [[("Telegram Trigger","same bot"),("AI Agent","+ Employees Data Table tool"),("Telegram — Send","answers grounded in the table")]],
 IMG("labs/activity4-telegram-agent/Activity4b-Telegram-Data-Table.png"),
 "Tool description tells the agent WHEN to use it  ·  instruction updated to route staff questions  ·  steps in the Learner Guide",color=VIOLET)
content("End of Day 1 — Recap",[
 "You built form automations, conditional logic and storage (Data Table → Google Sheets).",
 "You met the agent's four parts — model, memory, tools, instructions — and MCP.",
 "You shipped a Telegram AI agent, then grounded it in an Employees table.",
 "Tomorrow: webhooks, external APIs, and RAG."],kicker="WRAP-UP")

# ---------- TOPIC 3: WEBHOOKS ----------
K3="TOPIC 3 · WEBHOOKS"
K3L="TOPIC 3 · LAB WORKFLOW"
section("TOPIC 3","Webhooks","03",
 "The inbound URL · GET vs POST · Test vs Production URL · responding to the caller",
 "Applied in Activity 5",color=TEAL)
s=concept(K3,"What Is a Webhook?","A URL your workflow listens on. When the outside world calls it, your workflow runs — the reverse of you calling an API.")
chev_strip(s,[("Event happens","visitor sends a chat message"),("HTTP request to your URL","the website POSTs JSON"),("Workflow runs","n8n receives the data as input"),("Respond to Webhook","your reply returns to the caller")],y=Inches(2.1),h=Inches(1.05),color=TEAL)
ncards(s,[(BLUE,"Push, not pull","No polling, no schedule — the caller notifies you the moment something happens."),
 (TEAL,"Any caller","Websites, payment providers, forms, apps — anything that can send an HTTP request."),
 (VIOLET,"Paired node","Webhook starts the flow; Respond to Webhook sends the answer back on the same connection.")],
 y=Inches(3.5),h=Inches(2.55),cols=3)
takeaway(s,"A webhook is the reverse of an API call — the outside world calls YOU when an event happens.")
footer(s)
img_slide("Webhook Nodes in n8n",IMG(".claude/skills/tertiary-course-slides/assets/n8n-webhook.png"),
 "Webhook node starts the workflow when called · Respond to Webhook node returns data to the caller",
 kicker=K3,kcolor=TEAL)
two_panel("Webhook vs HTTP Request — Direction of the Call",
 "WEBHOOK — inbound",["An external service calls YOUR workflow.","You react the moment an event happens.","The trigger of the flow.","Activity 5: the website calls your agent."],
 "HTTP REQUEST — outbound",["YOUR workflow calls an external service.","You pull data when you choose.","An action inside the flow.","Activity 6: your flow calls Twelve Data."],
 kicker=K3,lcolor=TEAL,rcolor=BLUE,
 take="Same HTTP underneath — the only difference is who dials.")
s=concept(K3,"HTTP Methods on a Webhook — GET vs POST","The method is part of the contract with the caller: where the data rides, and what the call means.")
two=[(BLUE,"GET — read",["Data rides in the URL query string:","   ?email=alice@corp.com","A browser can call it by just visiting the URL.","Read in n8n as {{ $json.query.email }}.","Activity 8b: the dashboard GETs its leave data."]),
     (VIOLET,"POST — send",["Data rides in the request body as JSON:",'   { "message": "How much is the course?" }',"Used by website chat, forms and app callbacks.","Read in n8n as {{ $json.body.message }}.","Activities 5, 7b, 8a, 8c: the site POSTs to the flow."])]
for i,(col,t,items) in enumerate(two):
    x=int(Inches(0.85)+Inches(5.95)*i)
    rect(s,x,Inches(2.0),Inches(5.68),Inches(0.5),col)
    txt(s,x,Inches(2.0),Inches(5.68),Inches(0.5),[[(t,13.5,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    box(s,x,Inches(2.5),Inches(5.68),Inches(3.55),col,round_=False)
    bullets(s,x+Inches(0.3),Inches(2.72),Inches(5.1),Inches(3.2),[(it,1) if it.startswith("   ") else (it,0) for it in items],size=12.5,mcolor=col,gap=8)
takeaway(s,"GET reads, POST sends. Set the method on the Webhook node — the caller must match it.")
footer(s)
s=concept(K3,"Test URL vs Production URL","Every Webhook node gives you TWO URLs — they behave differently, and mixing them up is the #1 webhook bug.")
two=[(AMBER,"TEST URL — /webhook-test/…",["Works only while you click 'Listen for test event'.","Handles ONE call, then stops listening.","The run appears live on the canvas — great for debugging.","Dies the moment you leave the editor."]),
     (GREEN,"PRODUCTION URL — /webhook/…",["Requires the workflow toggled Active.","Always on — every call starts a run.","Runs are logged in the Executions list, not on the canvas.","This is the URL you give to websites and apps."])]
for i,(col,t,items) in enumerate(two):
    x=int(Inches(0.85)+Inches(5.95)*i)
    rect(s,x,Inches(2.0),Inches(5.68),Inches(0.5),col)
    txt(s,x,Inches(2.0),Inches(5.68),Inches(0.5),[[(t,13.5,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    box(s,x,Inches(2.5),Inches(5.68),Inches(3.4),col,round_=False)
    bullets(s,x+Inches(0.3),Inches(2.75),Inches(5.1),Inches(3.0),items,size=13,mcolor=col,gap=9)
takeaway(s,"Websites must call the PRODUCTION URL of an ACTIVE workflow — the Test URL stops when you leave the editor.")
footer(s)
s=concept(K3,"Configuring the Webhook Node","Four settings decide whether the browser's call succeeds.")
ncards(s,[(BLUE,"Method + Path","GET or POST, and the path that ends your URL — e.g. POST /webhook/hr-chat."),
 (TEAL,"Allowed Origins (CORS)","Browsers block cross-site calls unless allowed — set * in class so a local HTML page can call n8n."),
 (VIOLET,"Response mode","Immediately (ack), when the flow finishes, or via a Respond to Webhook node — the course flows use Respond to Webhook."),
 (AMBER,"Authentication","None for demos; Basic / Header / JWT for anything real — a public URL is a public door.")],
 y=Inches(1.95),h=Inches(3.7),cols=2)
takeaway(s,"'Failed to fetch' in the browser is usually CORS or a dead Test URL — check both first.")
footer(s)
lab_slide(K3L,"ACT 5","Activity 5 — Website Chatbot via Webhook (Investment Advisor)",
 "Put your agent behind a public web page: the enquiry form and the floating chatbot both POST to one n8n webhook.",
 [[("Webhook — POST","chat + enquiry form call it"),("AI Agent","compliance instruction — no advice"),("Respond to Webhook","reply returns to the page"),("Gmail","enquiry → advisor inbox")]],
 IMG("labs/activity5-investment-advisor/Activity5-Investment-Advisor.png"),
 "Production URL pasted into script.js  ·  CORS = *  ·  workflow Active  ·  steps in the Learner Guide")
website_lab("ACT 5 · THE WEBSITE","Activity 5 — The Investment Advisor Website",
 IMG("labs/activity5-investment-advisor/Activity5-website.png"),
 ["A public landing page with an enquiry form and a floating 'Ask Advisor' chatbot.",
  "Both the form and the chat POST to one n8n Webhook.",
  "The AI Agent replies in the chat; the advisor is emailed the enquiry.",
  "Set the webhook Production URL in script.js, then open index.html."])
brk("Tea Break","15 minutes",TEAL)

# ---------- TOPIC 4: API AND HTTP REQUEST ----------
K4="TOPIC 4 · API & HTTP"
K4L="TOPIC 4 · LAB WORKFLOW"
section("TOPIC 4","APIs and the HTTP Request Node","04",
 "Calling external services · request anatomy · status codes · API keys",
 "Applied in Activity 6",color=BLUE)
s=concept(K4,"What Is an API?","A service's front desk: you send a structured request over HTTP, it returns structured data — usually JSON.")
chev_strip(s,[("Your workflow","the client"),("HTTP request","method + URL + key + params"),("API server","processes the request"),("JSON response","fields your next node can read")],y=Inches(2.1),h=Inches(1.05),color=BLUE)
ncards(s,[(BLUE,"Live data on demand","Prices, weather, news, CRM records — data your workflow pulls the moment it needs it."),
 (TEAL,"You dial out","The opposite of a webhook: YOUR flow calls THEIR server, on your schedule."),
 (VIOLET,"One node fits all","The HTTP Request node calls any API on the internet — even ones n8n has no integration for.")],
 y=Inches(3.5),h=Inches(2.55),cols=3)
takeaway(s,"If a service has an API, n8n can use it — the HTTP Request node is the universal connector.")
footer(s)
s=concept(K4,"Anatomy of an HTTP Request","Four parts you configure on the HTTP Request node.")
data_table(s,[2.6,4.6,4.43],["Part","What it is","Activity 6 example"],[
 ["Method","GET (read) · POST (send) · PUT · DELETE","GET — read market candles"],
 ["URL / endpoint","The address of the resource","api.twelvedata.com/time_series"],
 ["Headers","Metadata, incl. authentication","(Twelve Data uses a query key instead)"],
 ["Query params / body","The inputs you send","symbol=AAPL & interval=1min & apikey=…"],
],y=Inches(2.0),rh=Inches(0.52))
takeaway(s,"Store API keys in Credentials — never hard-code them into the URL you share.")
footer(s)
s=concept(K4,"Reading the Response — Status Codes","The status code tells you whose problem it is before you read a single byte of the body.")
ncards(s,[(GREEN,"2xx — success","200 OK, 201 Created. The JSON body holds your data — map it to the next node."),
 (AMBER,"401 / 403 — auth","Bad or missing API key. Check the credential, not the flow."),
 (RED,"429 — rate limited","Too many calls for your plan — slow down or upgrade. Free tiers hit this fast."),
 (VIOLET,"4xx vs 5xx","4xx: your request is wrong. 5xx: their server is broken. Retry helps only with 5xx.")],
 y=Inches(1.95),h=Inches(3.7),cols=2)
takeaway(s,"4xx = fix your request · 5xx = wait and retry — never guess from the body alone.")
footer(s)
img_slide("The HTTP Request Node",IMG(".claude/skills/tertiary-course-slides/assets/n8n-http-request.png"),
 "HTTP Request node — configure method, URL, auth, query parameters; the JSON response flows to the next node",
 kicker=K4,kcolor=BLUE)
website_slide("Twelve Data — Market Data API",IMG(".claude/skills/tertiary-course-slides/assets/site-twelvedata.png"),
 ["Live stock / forex / crypto data over a simple REST API.","Sign up (free Basic plan), then Account → API Keys.","Paste the apikey into the three 'candles' HTTP nodes.","Free tier: 8 calls/min — enough for the lab."],kicker="ACT 6 · MARKET DATA API")
website_slide("NewsAPI — Headlines API",IMG(".claude/skills/tertiary-course-slides/assets/site-newsapi.png"),
 ["Recent news articles for any search query.","Register (free Developer plan) and copy your API key.","Store it as a Query Auth credential (name = apiKey) on the news node.","The agent reads sentiment from the headlines."],kicker="ACT 6 · NEWS API")
lab_slide(K4L,"ACT 6","Activity 6 — Finance APIs → Telegram (AI Day-Trading Agent)",
 "Ask the bot about a stock: it pulls candles on three timeframes plus news, and the agent argues a Buy / Sell / Hold call.",
 [[("Telegram Trigger","'Should I buy AAPL?'"),("Code — Extract Ticker","AAPL"),("HTTP ×4","candles 1m / 15m / 1h + news"),("AI Agent","technicals + sentiment → call"),("Telegram — Send","recommendation + reasoning")]],
 IMG("labs/activity6-finance-advisor/Activity6-Finance-Advisor.png"),
 "Twelve Data + NewsAPI keys  ·  imported flow, re-select credentials  ·  steps in the Learner Guide",color=BLUE)
website_lab("ACT 6 · THE WEBSITE","Activity 6 — The Stock Analysis Dashboard",
 IMG("labs/activity6-finance-advisor/Activity6-website.png"),
 ["A real-time dashboard with a live TradingView candlestick chart.",
  "Quote stats (price, change, OHLC, volume, 52-week range) from Twelve Data.",
  "A floating Telegram chat widget opens the AI day-trading agent.",
  "Save your Twelve Data key + bot username in the Settings panel."])
content("End of Day 2 — Recap",[
 "You exposed an AI agent to a public website via a webhook (Production URL + CORS).",
 "You pulled live market and news data through APIs into a Telegram agent.",
 "Tomorrow: RAG at production scale, human-in-the-loop, guardrails, and the capstone."],kicker="WRAP-UP")
brk("Lunch Break","1 hour",AMBER)

# ---------- TOPIC 5: RAG ----------
K5="TOPIC 5 · RAG"
K5L="TOPIC 5 · LAB WORKFLOW"
section("TOPIC 5","Retrieval-Augmented Generation","05",
 "Why retrieval · embeddings and vector stores · chunking and top_k · production vector DBs",
 "Applied in Activities 7a and 7b",color=AMBER)
s=concept(K5,"Why Retrieval, Rather Than a Bigger Prompt","You could paste all your documents into the instruction — until you can't.")
ncards(s,[(RED,"Everything in the prompt","Beyond a point the model ignores the middle. Every question pays tokens for ALL documents. Add document #41 and quality quietly drops."),
 (GREEN,"Retrieve, then generate","Find the two or three chunks that resemble the question and give the model ONLY those. Cost stays flat as the library grows.")],
 y=Inches(2.0),h=Inches(2.5),cols=2,numbered=False)
chev_strip(s,[("Question","embed it"),("Search the store","nearest chunks"),("Paste into the prompt","only what matched"),("Grounded answer","cites what it saw")],y=Inches(4.75),h=Inches(0.95),color=AMBER,tsz=11.5)
takeaway(s,"RAG = retrieval + generation. The retrieval decides whether the generation can possibly be right.")
footer(s)
s=concept(K5,"The RAG Pipeline — Ingest Once, Retrieve Every Question","Two phases: ingestion happens once per document; retrieval happens on every question.")
txt(s,Inches(0.85),Inches(2.0),Inches(2.0),Inches(0.4),[[("INGESTION — once",11,VIOLET,True)]])
chev_strip(s,[("Documents",""),("Chunk",""),("Embed",""),("Store as vectors","")],y=Inches(2.4),h=Inches(0.75),color=VIOLET,tsz=11)
txt(s,Inches(0.85),Inches(3.35),Inches(3.0),Inches(0.4),[[("RETRIEVAL — every question",11,AMBER,True)]])
chev_strip(s,[("Question",""),("Embed",""),("Nearest top_k",""),("Into the prompt",""),("Answer","")],y=Inches(3.75),h=Inches(0.75),color=AMBER,tsz=11)
ncards(s,[(BLUE,"Chunk","How a document is split — here one brochure = one chunk."),
 (TEAL,"Embedding","Text as a list of numbers; similar meaning → nearby vectors."),
 (VIOLET,"Similarity","Nearness of two vectors — how 'related' two texts are."),
 (GREEN,"top_k","How many chunks come back per question — 3 here.")],
 y=Inches(4.75),h=Inches(1.35),cols=4,numbered=False)
takeaway(s,"Four words — chunk, embedding, similarity, top_k — explain every RAG behaviour you will see.")
footer(s)
img_slide("How RAG Works",IMG(".claude/skills/tertiary-course-slides/assets/rag-flow.png"),
 "User → Prompt → Data Retrieval (search/retrieve over your data sources) → Generator → Response",
 kicker=K5,kcolor=AMBER)
s=concept(K5,"Vector Databases — Where the Embeddings Live","In-memory for demos; a hosted store for anything that must survive a restart.")
data_table(s,[2.6,3.0,3.0,3.03],["","Supabase (pgvector)","Pinecone","Qdrant"],[
 ["What it is","Postgres + extension","Managed SaaS index","Open-source vector DB"],
 ["Setup","SQL table + function","Create an index — no schema","Docker or Qdrant Cloud"],
 ["Best for","Teams already on Postgres","Zero-ops, scales fast","Full control, self-hosted"],
 ["Course embedding","OpenAI 1536-dim","Gemini 3072-dim","OpenAI 1536-dim"],
],y=Inches(2.0),rh=Inches(0.52))
box(s,Inches(0.85),Inches(4.75),Inches(11.63),Inches(1.3),RED)
txt(s,Inches(1.15),Inches(4.93),Inches(11.0),Inches(0.32),[[("THE DIMENSION RULE",12,RED,True)]])
txt(s,Inches(1.15),Inches(5.28),Inches(11.0),Inches(0.65),[[("The store's dimension MUST equal the embedding model's output — OpenAI text-embedding-3-small = 1536, Gemini gemini-embedding-001 = 3072. Mismatched dimensions are the #1 cause of failed inserts.",11.5,INK,False)]])
takeaway(s,"Swap the store, keep the RAG flow — but ingestion and retrieval must use the SAME embedding model.")
footer(s)
website_slide("Pinecone — Example Managed Store",IMG(".claude/skills/tertiary-course-slides/assets/site-pinecone.png"),
 ["Pinecone is a managed (cloud) vector database for RAG.","Free 'Starter' tier is enough for this lab.","Create an index: Dimensions = 3072 (Gemini), Metric = cosine.","Upload and retrieval must use the same namespace."],
 kicker="ACT 7b · VECTOR DATABASE")
lab_slide(K5L,"ACT 7a","Activity 7a — RAG Chatbot: Upload a PDF, Ask in Telegram",
 "The full RAG loop, no code: a web page ingests your IT-Support FAQ; a Telegram bot answers only from that document.",
 [[("Web Uploader","PDF text extracted in browser"),("Upload Webhook","POST to n8n"),("Gemini Embeddings","chunk + embed"),("Vector Store","in-memory; replaced per upload")],
  [("Telegram Trigger","'How do I reset my password?'"),("AI Agent","knowledge_base retriever tool"),("Telegram — Send","answers only from the document")]],
 IMG("labs/activity7-rag/Activity7a-RAG-Telegram.png"),
 "Gemini credential on 3 nodes  ·  off-topic questions are refused  ·  steps in the Learner Guide",color=AMBER)
website_lab("ACT 7a · INGESTION","Activity 7a — The Upload Page",
 IMG("labs/activity7-rag/Activity7a-website.png"),
 ["A single-page uploader extracts PDF text in the browser with PDF.js.",
  "Paste your n8n rag-upload webhook URL and click Test.",
  "Drop the IT-Support FAQ PDF and Send to Vector Store to ingest it.",
  "No build step — just open the HTML file."])
lab_slide(K5L,"ACT 7b","Activity 7b — Ingestion: 20 Brochures into a Vector DB",
 "Cook & Bake Academy: load 20 course brochures from Google Drive into your chosen vector database — run once.",
 [[("Manual Trigger","run once"),("Google Drive","list + download 20 brochures"),("Split + Embed","1 brochure = 1 chunk · Gemini 3072-d"),("Vector Store — Insert","index: course-brochures")]],
 IMG("labs/activity7-rag/Activity7b-Pinecone-Upload.png"),
 "Choose Supabase / Pinecone / Qdrant  ·  20 vectors after the run  ·  steps in the Learner Guide",color=AMBER,
 cap="Shown: Pinecone ingestion. Supabase & Qdrant flows are identical except the store node + OpenAI 1536-d embeddings.")
lab_slide(K5L,"ACT 7b","Activity 7b — CX Agent: Grounded Support Chatbot",
 "The answering half: the website chat widget POSTs each question; the agent retrieves matching brochures and answers grounded.",
 [[("Webhook — POST","website chat widget"),("AI Agent","Pinecone retriever tool + Gemini"),("Respond to Webhook","grounded answer to the widget")]],
 IMG("labs/activity7-rag/Activity7b-CX-Agent.png"),
 "Same index, same embeddings, same namespace as ingestion  ·  steps in the Learner Guide",color=AMBER)
website_lab("ACT 7b · THE WEBSITE","Cook & Bake Academy — Support Chatbot",
 IMG("labs/activity7-rag/Activity7b-website.png"),
 ["A one-page training-center site with a floating chat widget.",
  "Visitors ask about any course — duration, fee, location, schedule.",
  "Answers are grounded in the 20 ingested brochures.",
  "Set WEBHOOK_URL in script.js to your n8n CX Agent Production URL."])
brk("Tea Break","15 minutes",TEAL)

# ---------- TOPIC 6: SECURITY ----------
K6="TOPIC 6 · SECURITY & GOVERNANCE"
K6L="TOPIC 6 · LAB WORKFLOW"
section("TOPIC 6","Security, Human-in-the-Loop & Guardrails","06",
 "Where the human belongs · approval gates · input and output guardrails",
 "Applied in Activities 8a, 8b and 8c",color=RED)
s=concept(K6,"Human In, On, and Out of the Loop","Three arrangements people use interchangeably — and they are not the same thing.")
data_table(s,[3.4,3.1,2.6,2.53],["Pattern","Who decides","Who acts","Can AI proceed alone?"],[
 ["Human IN the loop","AI proposes, human decides","Human approves, system acts","NO — it blocks"],
 ["Human ON the loop","AI decides and acts","Human monitors, can intervene","Yes — reviewed after"],
 ["Human OUT of the loop","AI decides and acts","AI acts","Yes — nobody checks"],
],y=Inches(2.0),rh=Inches(0.56))
box(s,Inches(0.85),Inches(4.6),Inches(11.63),Inches(1.4),BLUE)
txt(s,Inches(1.15),Inches(4.78),Inches(11.0),Inches(0.32),[[("WHERE THIS COURSE PUTS THE HUMAN",12,BLUE,True)]])
txt(s,Inches(1.15),Inches(5.14),Inches(11.0),Inches(0.8),[[("Activity 8a — the manager approves leave before any email goes to the employee (IN the loop). The dashboard (8b) and chatbot (8c) run alone, but the chatbot is fenced by guardrails on both sides.",11.5,INK,False)]])
takeaway(s,"Ask who pays for the mistake — that answer sizes the agent's authority and places the human.")
footer(s)
s=concept(K6,"How an Approval Suspends a Running Flow","n8n's Send and Wait for Response physically pauses the workflow until a person clicks.")
chev_strip(s,[("Request submitted","employee applies for leave"),("Send & Wait","manager gets Approve / Decline email"),("The run SUSPENDS","minutes or days — it waits"),("A person responds","one click in the email"),("IF reads the outcome","approved → notify · declined → notify")],y=Inches(2.1),h=Inches(1.1),color=RED,tsz=11)
ncards(s,[(GREEN,"Outcome = Approve","Send the approval email, update the record, continue the business process."),
 (RED,"Outcome = Decline","Send the rejection with the manager's comments — never silence."),
 (AMBER,"Ack first","The portal gets an instant 'received' response BEFORE the wait — the browser never hangs on a manager.")],
 y=Inches(3.6),h=Inches(2.45),cols=3,numbered=False)
takeaway(s,"A pause that is still paused tomorrow is a real gate — that is the deliverable of Activity 8a.")
footer(s)
s=concept(K6,"Guardrails — Two Gates Around the Agent","An LLM checks every message in, and every reply out — the agent only sees and says what passes.")
chev_strip(s,[("User message","from the HR portal"),("INPUT guardrail","LLM: ALLOW / BLOCK"),("HR AI Agent","answers in-scope questions"),("OUTPUT guardrail","LLM: SAFE / LEAK"),("Reply or blocked","user sees the safe path")],y=Inches(2.1),h=Inches(1.1),color=RED,tsz=11)
ncards(s,[(BLUE,"Input (pre) guardrail blocks","Prompt injection ('ignore previous instructions'), jailbreaks, requests for another person's salary or private data."),
 (VIOLET,"Output (post) guardrail blocks","Salary figures, NRIC, credentials, system-instruction leaks — even when the agent was tricked into producing them.")],
 y=Inches(3.6),h=Inches(2.45),cols=2)
takeaway(s,"Instructions say what the agent SHOULD do; guardrails enforce what it MUST NOT — you need both.")
footer(s)
lab_slide(K6L,"ACT 8a","Activity 8a — Leave Application & Manager Approval (HITL)",
 "The employee applies on the portal; the flow acks, then suspends until the manager clicks Approve or Decline in email.",
 [[("Webhook — POST","hr-leave-apply"),("Respond — Ack","portal gets instant OK"),("Gmail — Send & Wait","manager: Approve / Decline"),("IF","approved = true ?"),("Gmail","notify the employee")]],
 IMG("labs/activity8-guardrails/Activity8 - Leave Application & Manager Approval (Human-in-the-Loop).png"),
 "Human-in-the-loop gate  ·  run suspends until the click  ·  steps in the Learner Guide",color=RED)
lab_slide(K6L,"ACT 8b","Activity 8b — HR Dashboard Data (GET Webhook)",
 "A GET webhook powers the portal's Dashboard tab — leave balance and history returned as JSON to the browser.",
 [[("Webhook — GET","hr-dashboard?email=…"),("Code","build the leave-data JSON"),("Respond to Webhook","JSON back to the portal")]],
 IMG("labs/activity8-guardrails/Activity8 - Dashboard Data (Leave Balance & History).png"),
 "GET query read from $json.query.email  ·  CORS = *  ·  steps in the Learner Guide",color=RED)
lab_slide(K6L,"ACT 8c","Activity 8c — AI Chatbot with Input & Output Guardrails",
 "HR Buddy answers general HR questions — every message passes the input gate, every reply passes the output gate.",
 [[("Webhook — POST","hr-chat"),("Input Guardrail","LLM: ALLOW / BLOCK"),("HR AI Agent","leave · payroll · claims"),("Output Guardrail","LLM: SAFE / LEAK"),("Respond","reply or blocked message")]],
 IMG("labs/activity8-guardrails/Activity8 - AI Chatbot with Input & Output Guardrails.png"),
 "Test it by trying to break it — the injection probe must be blocked  ·  steps in the Learner Guide",color=RED)
website_lab("ACT 8 · THE WEBSITE","Activity 8 — The HR Service Portal",
 IMG("labs/activity8-guardrails/Activity8-website.png"),
 ["One portal with four tabs: Dashboard, Apply Leave, HR Assistant, Settings.",
  "Dashboard pulls live leave balance & history from the GET webhook (8b).",
  "Apply Leave triggers the human-in-the-loop approval chain (8a).",
  "HR Assistant is the guarded AI chatbot — input & output guardrails (8c)."])
brk("Lunch Break","1 hour",AMBER)

# ---------- TOPIC 7: CAPSTONE ----------
K7="TOPIC 7 · MINI CAPSTONE"
section("TOPIC 7","Mini Capstone Project","07","Design · Build · Present","Everything from Activities 1–8, your problem",color=GREEN)
s=concept(K7,"Your Build — What It Must Include","In small groups, design and build an end-to-end automation for a problem you choose.")
ncards(s,[(BLUE,"A trigger","Form, webhook, Telegram or schedule — who or what starts your process?"),
 (VIOLET,"An AI agent","With at least one tool or a RAG source — the judgement in the middle."),
 (TEAL,"External data or storage","An API you call, or storage you write — Sheets, a vector DB, a Data Table."),
 (RED,"A control","A guardrail or a human-in-the-loop step — decide where the human belongs and defend it.")],
 y=Inches(1.95),h=Inches(3.7),cols=2)
takeaway(s,"Deliverables: a working workflow, a short demo, and a 3–5 minute presentation.")
footer(s)
website_lab("CAPSTONE · WORKED EXAMPLE","Capstone Example — Issue Reporting",
 IMG("labs/mini-capstone/issue-tracking/Capstone-website.png"),
 ["Paste your n8n Form production URL to generate a QR code.",
  "People scan the QR with a phone to open the submission form.",
  "Submissions (with photos) flow into Postgres and a public gallery.",
  "A complete worked capstone you can adapt for your own project."])
content("Presentation & Assessment",[
 "Present the problem, your design, and what you'd improve.",
 "Written Assessment (SAQ) — 1 hour · Practical Performance (PP) — 1 hour.",
 "Open book: slides, Learner Guide and approved materials.",
 "Remember to take the Assessment digital attendance (TRAQOM)."],kicker="WRAP-UP")

# ---------- ASSESSMENT ADMIN (repeated at END before Thank You — wsq-slides hard rule) ----------
content("Assessment",[
 "Written Assessment (SAQ) — 1 hour.  Practical Performance (PP) — 1 hour.",
 "Open book: slides, Learner Guide and approved materials only.",
 "Remember to take the Assessment digital attendance (TRAQOM).",
 "Submit your completed answers on the LMS at https://lms-tms.tertiaryinfotech.com/."],kicker="FINAL ASSESSMENT")
flow_h("Assessment Flow",[
 "TRAQOM survey — scan the QR code on the LMS",
 "Assessment digital attendance — scan the SSG QR",
 "Sit WA (SAQ) then PP — open book",
 "Submit your answers on the LMS",
 "Sign the Assessment Summary Record"],kicker="ON ASSESSMENT DAY")
content("Digital Attendance (Mandatory)",[
 "It is mandatory to take the AM, PM and Assessment digital attendance for WSQ-funded courses.",
 "The trainer/administrator displays the digital attendance QR code from the SSG portal.",
 "Scan the QR code with your mobile phone camera and submit your attendance.",
 "A minimum of 75% attendance is required to be eligible for assessment and funding."],kicker="TRAQOM · SSG DIGITAL ATTENDANCE")

# ---------- CLOSING ----------
s=slide(); rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),SH,BLUE)
rect(s,Inches(0.85),Inches(2.7),Inches(0.14),Inches(1.5),TEAL)
txt(s,Inches(1.25),Inches(2.7),Inches(11),Inches(1.2),[[("Thank You!",48,INK,True)]])
txt(s,Inches(1.27),Inches(4.1),Inches(11.5),Inches(1.4),
 [[("Keep your local n8n running and keep building your own agents.",18,GREY,False)],
  [("Download all flows: github.com/tertiarycourses/TGS-2023035977-Agentic-AI-Automation-with-n8n",13,BLUE,True)],
  [("Powered by Tertiary Infotech Academy Pte Ltd  ·  www.tertiarycourses.com.sg",12,GREY,False)]],space=8)
footer(s)

OUT=f"courseware/{TITLE}-{VERSION}.pptx"
prs.save(f"{REPO}/{OUT}")
print("Saved:",OUT,"| slides:",len(prs.slides._sldIdLst))
