# -*- coding: utf-8 -*-
"""Design system for the supplement register: tokens, CSS and client behaviour.

Direction: analytical certificate. Data is monospaced, colour is a specification
signal only, and the signature element is a five-cell spec strip per item.
Convention: no raw double-quote inside any Python string literal.
"""

CSS = r'''
/* ============================================================ tokens */
:root{
  /* paper and ink: lab notebook stock, blue-black ink */
  --paper:#F5F7F6; --panel:#FFFFFF; --panel-2:#FAFBFA;
  --ink:#13181A; --ink-2:#3A4442; --muted:#5B6562; --faint:#8A9490;
  --rule:#D6DCD8; --rule-2:#E7ECE9;
  /* specification signals, never decorative */
  --pass:#0F6B4F; --caution:#9C640C; --fail:#A02B22; --ref:#1C5A87;
  --pass-bg:#E8F2ED; --caution-bg:#F8F0DF; --fail-bg:#F8ECEA; --ref-bg:#E9F1F7;
  /* type */
  --display:Constantia,"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --body:Corbel,Optima,Candara,"Segoe UI",system-ui,-apple-system,sans-serif;
  --data:"Cascadia Mono",Consolas,"SF Mono",Menlo,"DejaVu Sans Mono",ui-monospace,monospace;
  /* metrics */
  --gutter:clamp(16px,4vw,34px); --maxw:1240px;
  --r:3px;
  --strip-ink:#FFF;
}
@media (prefers-color-scheme:dark){
  :root{
    --paper:#0D1113; --panel:#141A1C; --panel-2:#111719;
    --ink:#E4EAE7; --ink-2:#C2CCC8; --muted:#8A9693; --faint:#6A7673;
    --rule:#232C2F; --rule-2:#1B2325;
    --pass:#4FBE92; --caution:#DFA43C; --fail:#E5766B; --ref:#6DA6D4;
    --pass-bg:#13251E; --caution-bg:#251E10; --fail-bg:#261715; --ref-bg:#13212B;
    --strip-ink:#0B0F11;
  }
}
:root[data-theme="light"]{
  --paper:#F5F7F6; --panel:#FFFFFF; --panel-2:#FAFBFA;
  --ink:#13181A; --ink-2:#3A4442; --muted:#5B6562; --faint:#8A9490;
  --rule:#D6DCD8; --rule-2:#E7ECE9;
  --pass:#0F6B4F; --caution:#9C640C; --fail:#A02B22; --ref:#1C5A87;
  --pass-bg:#E8F2ED; --caution-bg:#F8F0DF; --fail-bg:#F8ECEA; --ref-bg:#E9F1F7;
  --strip-ink:#FFF;
}
:root[data-theme="dark"]{
  --paper:#0D1113; --panel:#141A1C; --panel-2:#111719;
  --ink:#E4EAE7; --ink-2:#C2CCC8; --muted:#8A9693; --faint:#6A7673;
  --rule:#232C2F; --rule-2:#1B2325;
  --pass:#4FBE92; --caution:#DFA43C; --fail:#E5766B; --ref:#6DA6D4;
  --pass-bg:#13251E; --caution-bg:#251E10; --fail-bg:#261715; --ref-bg:#13212B;
  --strip-ink:#0B0F11;
}

*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);
  font-size:16.5px;line-height:1.62;font-feature-settings:"kern" 1,"liga" 1}
html[data-lang="en"] .zh{display:none!important}
html[data-lang="zh"] .en{display:none!important}
html[data-lang="zh"] body{line-height:1.82;font-family:var(--body)}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 var(--gutter)}
.narrow{max-width:78ch}
::selection{background:var(--ref);color:var(--panel)}
:focus-visible{outline:2px solid var(--ref);outline-offset:2px;border-radius:2px}

/* numerals and identifiers are instrument output */
.d,.num,code,kbd,.spec b,th.sortable span.ind,.count,.mono{font-family:var(--data);
  font-variant-numeric:tabular-nums;font-feature-settings:"tnum" 1}

/* ============================================================ masthead */
.mast{border-bottom:1px solid var(--rule);background:var(--panel);
  position:sticky;top:0;z-index:60;backdrop-filter:saturate(1.2) blur(6px)}
.mast-in{max-width:var(--maxw);margin:0 auto;padding:10px var(--gutter);
  display:flex;gap:18px;align-items:center;flex-wrap:wrap}
.mast .id{display:flex;flex-direction:column;line-height:1.2}
.mast .id b{font-family:var(--display);font-size:16px;font-weight:600;letter-spacing:-.005em}
.mast .id span{font-family:var(--data);font-size:10.5px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--faint)}
.mast nav{display:flex;gap:2px;flex-wrap:wrap;margin-left:auto}
.mast nav a{font-size:12.5px;color:var(--muted);text-decoration:none;padding:5px 8px;border-radius:var(--r)}
.mast nav a:hover{color:var(--ink);background:var(--panel-2)}
.ctl{display:flex;gap:8px;align-items:center}
.seg{display:inline-flex;border:1px solid var(--rule);border-radius:var(--r);overflow:hidden;background:var(--panel-2)}
.seg button{appearance:none;border:0;background:transparent;color:var(--muted);cursor:pointer;
  font:inherit;font-size:12px;font-weight:600;padding:5px 11px;letter-spacing:.02em}
.seg button:hover{color:var(--ink)}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.iconbtn{appearance:none;border:1px solid var(--rule);background:var(--panel-2);color:var(--muted);
  cursor:pointer;border-radius:var(--r);width:30px;height:28px;font-size:13px;line-height:1}
.iconbtn:hover{color:var(--ink)}

/* ============================================================ hero / report header */
.hero{padding:clamp(30px,6vw,62px) 0 22px;border-bottom:1px solid var(--rule)}
.eyebrow{font-family:var(--data);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--faint);display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.eyebrow s{text-decoration:none;color:var(--rule)}
h1{font-family:var(--display);font-weight:600;font-size:clamp(30px,5.4vw,54px);line-height:1.06;
  letter-spacing:-.018em;margin:14px 0 0;max-width:22ch}
h1 em{font-style:italic;color:var(--ink-2)}
.dek{margin:16px 0 0;max-width:66ch;color:var(--ink-2);font-size:17px}
.meta-grid{display:grid;gap:0;grid-template-columns:repeat(auto-fit,minmax(132px,1fr));
  margin:28px 0 0;border:1px solid var(--rule);border-radius:var(--r);overflow:hidden;background:var(--panel)}
.meta-grid div{padding:11px 13px;border-right:1px solid var(--rule-2)}
.meta-grid div:last-child{border-right:0}
.meta-grid b{display:block;font-family:var(--data);font-size:21px;letter-spacing:-.02em;line-height:1.2}
.meta-grid span{font-size:11.5px;color:var(--muted);display:block;margin-top:2px}
.meta-grid div.warn b{color:var(--fail)}
.meta-grid div.good b{color:var(--pass)}

/* ============================================================ spec strip: the signature */
.spec{display:inline-flex;gap:2px;vertical-align:middle}
.spec b{width:20px;height:20px;border-radius:2px;display:grid;place-items:center;
  font-size:10.5px;font-weight:700;letter-spacing:0;color:var(--strip-ink);cursor:help}
.spec b.p{background:var(--pass)} .spec b.c{background:var(--caution)}
.spec b.f{background:var(--fail)}  .spec b.n{background:var(--faint)}
.spec b.o{background:transparent;border:1px solid var(--rule);color:var(--faint)}
.spec.lg b{width:26px;height:26px;font-size:12px}
.legend{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));margin:18px 0 0}
.legend section{border:1px solid var(--rule);border-radius:var(--r);background:var(--panel);padding:12px 14px}
.legend h4{margin:0 0 8px;font-family:var(--data);font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--faint);font-weight:700}
html[data-lang="zh"] .legend h4{letter-spacing:.04em;text-transform:none;font-size:12px}
.legend ul{margin:0;padding:0;list-style:none;font-size:13px}
.legend li{display:flex;gap:9px;align-items:flex-start;margin:5px 0}
.legend li .spec{flex:0 0 auto;margin-top:1px}

/* ============================================================ register */
.reg{margin:0 0 10px;padding:26px 0 0}
.reg-bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:0 0 14px}
.search{position:relative;flex:1 1 260px;min-width:200px}
.search input{width:100%;font:inherit;font-size:14px;padding:8px 30px 8px 30px;color:var(--ink);
  background:var(--panel);border:1px solid var(--rule);border-radius:var(--r)}
.search input::placeholder{color:var(--faint)}
.search svg{position:absolute;left:9px;top:50%;transform:translateY(-50%);width:14px;height:14px;
  stroke:var(--faint);fill:none;stroke-width:1.8}
.search kbd{position:absolute;right:8px;top:50%;transform:translateY(-50%);font-size:10px;
  color:var(--faint);border:1px solid var(--rule);border-radius:2px;padding:1px 4px;background:var(--panel-2)}
.chips{display:flex;gap:5px;flex-wrap:wrap}
.chip{appearance:none;cursor:pointer;font:inherit;font-size:12px;padding:5px 10px;border-radius:999px;
  border:1px solid var(--rule);background:var(--panel);color:var(--muted);white-space:nowrap;transition:.12s}
.chip:hover{color:var(--ink);border-color:var(--faint)}
.chip[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:var(--paper)}
.chip[aria-pressed="true"].p{background:var(--pass);border-color:var(--pass);color:#fff}
.chip[aria-pressed="true"].c{background:var(--caution);border-color:var(--caution);color:#fff}
.chip[aria-pressed="true"].f{background:var(--fail);border-color:var(--fail);color:#fff}
.chip .n{font-family:var(--data);font-size:10.5px;opacity:.72;margin-left:5px}
.reg-note{font-size:12.5px;color:var(--muted);display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}
.count{color:var(--ink);font-weight:600}
.linkbtn{appearance:none;background:none;border:0;padding:0;font:inherit;font-size:12.5px;
  color:var(--ref);cursor:pointer;text-decoration:underline;text-underline-offset:2px}

.tablewrap{border:1px solid var(--rule);border-radius:var(--r);background:var(--panel);overflow-x:auto}
table.reg-t{border-collapse:collapse;width:100%;font-size:14px;min-width:1180px;table-layout:fixed}
table.reg-t col.c-nm{width:21%}table.reg-t col.c-sp{width:150px}table.reg-t col.c-vd{width:8.5%}
table.reg-t col.c-fd{width:8%}table.reg-t col.c-ds{width:10%}table.reg-t col.c-sy{width:9.5%}
table.reg-t col.c-df{width:12%}table.reg-t col.c-wh{width:18%}
table.reg-t th,table.reg-t td{text-align:left;padding:8px 11px;border-bottom:1px solid var(--rule-2);
  vertical-align:middle;overflow-wrap:break-word}
table.reg-t thead th{position:sticky;top:49px;z-index:20;background:var(--panel-2);
  font-family:var(--data);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);font-weight:700;border-bottom:1px solid var(--rule);white-space:nowrap}
html[data-lang="zh"] table.reg-t thead th{letter-spacing:.03em;text-transform:none;font-size:12px}
th.sortable{cursor:pointer;user-select:none}
th.sortable:hover{color:var(--ink)}
th.sortable span.ind{opacity:.35;margin-left:4px;font-size:9px}
th.sortable[aria-sort="ascending"] span.ind,th.sortable[aria-sort="descending"] span.ind{opacity:1;color:var(--ref)}
table.reg-t tbody tr{cursor:pointer;transition:background .1s}
table.reg-t tbody tr:hover{background:var(--panel-2)}
table.reg-t tbody tr.open{background:var(--panel-2)}
table.reg-t tbody tr:last-child td{border-bottom:0}
td.nm{font-weight:600;line-height:1.32}
td.nm .sub{display:block;font-size:11.5px;color:var(--muted);font-weight:400;margin-top:1px}
td.who{color:var(--ink-2);font-size:12.5px;line-height:1.45;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
td.nm .sub{display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden}
td.nm .sub.fnc{-webkit-line-clamp:2;color:var(--muted);font-size:11.5px;line-height:1.38;margin-top:2px}
td.tier{font-family:var(--data);font-size:10.5px;letter-spacing:.06em;color:var(--muted);text-transform:uppercase}
tr.detail{display:none}
tr.detail.show{display:table-row}
tr.detail td{background:var(--panel-2);border-bottom:1px solid var(--rule);padding:0}
.detail-in{padding:14px 16px;display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(255px,1fr))}
.detail-in section h5{margin:0 0 5px;font-family:var(--data);font-size:10px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--faint)}
html[data-lang="zh"] .detail-in section h5{letter-spacing:.03em;text-transform:none;font-size:11.5px}
.detail-in p{margin:0;font-size:13.5px;color:var(--ink-2)}
.detail-in .go{margin-top:9px;grid-column:1/-1}
.detail-in .go a{font-size:13px;color:var(--ref);text-decoration:none;border-bottom:1px solid currentColor}
.empty{padding:34px 16px;text-align:center;color:var(--muted);font-size:14px;display:none}
.empty.show{display:block}

/* ============================================================ prose */
main section.blk{padding:52px 0 0;scroll-margin-top:60px}
h2{font-family:var(--display);font-weight:600;font-size:clamp(21px,2.6vw,28px);line-height:1.18;
  letter-spacing:-.012em;margin:0 0 4px;display:flex;gap:12px;align-items:baseline}
h2 .no{font-family:var(--data);font-size:12px;letter-spacing:.06em;color:var(--faint);font-weight:400;flex:0 0 auto}
h3{font-family:var(--display);font-size:18.5px;font-weight:600;margin:30px 0 6px;letter-spacing:-.008em}
h4{font-size:14px;margin:20px 0 5px}
p{margin:11px 0;max-width:80ch}
a{color:var(--ref);text-decoration-thickness:1px;text-underline-offset:2px}
.lede{color:var(--ink-2);font-size:16.5px;max-width:74ch}
ol.rules{counter-reset:r;list-style:none;padding:0;margin:16px 0;max-width:82ch}
ol.rules li{counter-increment:r;position:relative;padding:0 0 0 42px;margin:15px 0}
ol.rules li::before{content:counter(r,decimal-leading-zero);position:absolute;left:0;top:2px;
  font-family:var(--data);font-size:11px;color:var(--faint);letter-spacing:.04em}
ol.rules li b{display:block;margin-bottom:2px}
ol.plain{max-width:82ch;padding-left:22px}
ol.plain li{margin:11px 0}

.tw{overflow-x:auto;margin:15px 0;border:1px solid var(--rule);border-radius:var(--r);background:var(--panel)}
table.dt{border-collapse:collapse;width:100%;font-size:13.5px;min-width:600px}
table.dt th,table.dt td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--rule-2);vertical-align:top}
table.dt thead th{background:var(--panel-2);font-family:var(--data);font-size:10.5px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--muted);font-weight:700;border-bottom:1px solid var(--rule)}
html[data-lang="zh"] table.dt thead th{letter-spacing:.03em;text-transform:none;font-size:12px}
table.dt tbody tr:last-child td{border-bottom:0}
table.dt td.num{font-family:var(--data);white-space:nowrap}

.note{border-left:2px solid var(--ref);background:var(--panel);padding:13px 17px;margin:18px 0;
  border-radius:0 var(--r) var(--r) 0;font-size:14.5px}
.note.pass{border-left-color:var(--pass);background:var(--pass-bg)}
.note.caution{border-left-color:var(--caution);background:var(--caution-bg)}
.note.fail{border-left-color:var(--fail);background:var(--fail-bg)}
.note p{margin:0;max-width:76ch}.note p+p{margin-top:8px}
.note .lbl{font-family:var(--data);font-size:10px;letter-spacing:.11em;text-transform:uppercase;
  display:block;margin-bottom:5px;color:var(--muted)}
html[data-lang="zh"] .note .lbl{letter-spacing:.04em;text-transform:none;font-size:11.5px}

figure{margin:26px 0;border:1px solid var(--rule);border-radius:var(--r);background:var(--panel);padding:16px 10px 8px}
figcaption{font-size:13px;color:var(--muted);padding:8px 12px 0;max-width:92ch}
figcaption b{color:var(--ink)}
svg.fig{width:100%;height:auto;display:block}

/* ============================================================ item cards */
.item{border:1px solid var(--rule);border-radius:var(--r);background:var(--panel);margin:18px 0;overflow:hidden;
  scroll-margin-top:64px}
.item>header{padding:13px 17px;border-bottom:1px solid var(--rule);display:flex;gap:12px;
  align-items:center;flex-wrap:wrap;background:var(--panel-2)}
.item>header .nm{font-family:var(--display);font-size:19px;font-weight:600;letter-spacing:-.01em;flex:1 1 auto}
.kv{padding:12px 17px;border-bottom:1px solid var(--rule-2);font-size:13.5px}
.kv div{margin:3px 0;display:flex;gap:10px}
.kv b{font-family:var(--data);font-size:10px;letter-spacing:.09em;text-transform:uppercase;color:var(--faint);
  flex:0 0 118px;padding-top:3px}
html[data-lang="zh"] .kv b{letter-spacing:.02em;text-transform:none;font-size:11.5px;flex-basis:78px}
.pc{display:grid;grid-template-columns:1fr 1fr}
@media (max-width:900px){.pc{grid-template-columns:1fr}}
.pc>div{padding:13px 17px}
.pc>.p{background:var(--pass-bg)}
.pc>.c{background:var(--fail-bg);border-left:1px solid var(--rule-2)}
@media (max-width:900px){.pc>.c{border-left:0;border-top:1px solid var(--rule-2)}}
.pc h5{margin:0 0 8px;font-family:var(--data);font-size:10px;letter-spacing:.11em;text-transform:uppercase}
html[data-lang="zh"] .pc h5{letter-spacing:.04em;text-transform:none;font-size:12px}
.pc>.p h5{color:var(--pass)} .pc>.c h5{color:var(--fail)}
.pc ul{margin:0;padding-left:17px;font-size:13.5px}
.pc li{margin:6px 0}
.food{border-top:1px solid var(--rule);padding:13px 17px;background:var(--panel-2)}
.food>h5{margin:0 0 9px;font-family:var(--data);font-size:10px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--faint)}
html[data-lang="zh"] .food>h5{letter-spacing:.04em;text-transform:none;font-size:12px}
.fbadges{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}
.tag{display:inline-block;font-size:11px;font-weight:700;padding:2px 8px;border-radius:2px;white-space:nowrap;
  border:1px solid transparent}
.tag.p{background:var(--pass-bg);color:var(--pass);border-color:var(--pass)}
.tag.c{background:var(--caution-bg);color:var(--caution);border-color:var(--caution)}
.tag.f{background:var(--fail-bg);color:var(--fail);border-color:var(--fail)}
.tag.n{background:var(--panel);color:var(--muted);border-color:var(--rule)}
.food .ftw{overflow-x:auto;margin:10px 0;border:1px solid var(--rule);border-radius:var(--r);background:var(--panel)}
.food table{border-collapse:collapse;width:100%;font-size:12.5px;min-width:770px;table-layout:fixed}
.food col.cf{width:23%}.food col.ca{width:17%}.food col.cp{width:16%}
.food col.cv{width:13%}.food col.cs{width:11%}.food col.cr{width:20%}
.food th,.food td{padding:6px 10px;border-bottom:1px solid var(--rule-2);text-align:left;vertical-align:top;
  overflow-wrap:break-word}
.food th{background:var(--panel-2);font-family:var(--data);font-size:10px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--muted);font-weight:700}
html[data-lang="zh"] .food th{letter-spacing:.02em;text-transform:none;font-size:11.5px}
.food tr:last-child td{border-bottom:0}
.food td.num{font-family:var(--data);font-variant-numeric:tabular-nums}
.food td.fd{font-weight:600}
.food td.src{font-size:10.5px;line-height:1.45;color:var(--muted);font-family:var(--data)}
.unc{display:inline-block;font-family:var(--body);font-size:9.5px;font-weight:700;letter-spacing:.03em;
  padding:0 4px;border-radius:2px;border:1px solid var(--caution);color:var(--caution);white-space:nowrap;
  margin-left:4px;vertical-align:1px;cursor:help}
.fline{font-size:13.5px;margin:7px 0;max-width:none;color:var(--ink-2)}
.fline b{font-family:var(--data);font-size:10px;letter-spacing:.09em;text-transform:uppercase;color:var(--faint);
  margin-right:6px}
html[data-lang="zh"] .fline b{letter-spacing:.02em;text-transform:none;font-size:11.5px}
.fnone{font-size:13.5px;color:var(--muted);font-style:italic}
.refs{padding:9px 17px;font-family:var(--data);font-size:10.5px;color:var(--faint);
  border-top:1px solid var(--rule-2);word-break:break-word}

.food.fnb{background:var(--panel)}
.food.fnb .lead{font-family:var(--display);font-size:16.5px;line-height:1.42;color:var(--ink);
  margin:0 0 10px;max-width:64ch}
html[data-lang="zh"] .food.fnb .lead{font-family:var(--body);font-size:16px}
.food.fnb .nodef{color:var(--muted);font-style:italic;border-left:2px solid var(--rule);padding-left:11px}

/* ============================================================ footer */
footer{margin-top:64px;border-top:1px solid var(--rule);background:var(--panel)}
footer .in{max-width:var(--maxw);margin:0 auto;padding:26px var(--gutter) 46px;color:var(--muted);font-size:13px}
footer p{max-width:80ch}

.tocbtn{display:none}
@media (max-width:860px){
  .mast nav{display:none}
  h1{font-size:clamp(26px,8vw,34px)}
  table.reg-t thead th{top:0}
}
@media (prefers-reduced-motion:reduce){
  *{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important}
  html{scroll-behavior:auto}
}
@media not (prefers-reduced-motion:reduce){
  html{scroll-behavior:smooth}
  tbody.stagger tr.row{animation:rise .34s cubic-bezier(.22,.7,.3,1) both}
}
@keyframes rise{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
@media print{
  .mast,.reg-bar,.tocbtn{display:none}
  body{background:#fff;font-size:10.5pt}
  .item,figure,.tablewrap,.tw{break-inside:avoid;border-color:#bbb}
  tr.detail{display:table-row!important}
}
'''

JS = r'''
(function(){
  'use strict';
  var d=document, root=d.documentElement;

  /* ---------------- language ---------------- */
  function setLang(l){
    root.setAttribute('data-lang',l);
    root.setAttribute('lang', l==='zh' ? 'zh-CN' : 'en');
    var a=d.getElementById('lang-en'), b=d.getElementById('lang-zh');
    if(a) a.setAttribute('aria-pressed', String(l==='en'));
    if(b) b.setAttribute('aria-pressed', String(l==='zh'));
    try{ localStorage.setItem('sr-lang',l); }catch(e){}
  }
  window.setLang=setLang;

  /* ---------------- theme ---------------- */
  function setTheme(t){
    if(t==='auto'){ root.removeAttribute('data-theme'); }
    else { root.setAttribute('data-theme',t); }
    try{ localStorage.setItem('sr-theme',t); }catch(e){}
    var btn=d.getElementById('theme-btn');
    if(btn){
      btn.textContent = t==='auto' ? '◑' : (t==='dark' ? '●' : '○');
      btn.setAttribute('title','Theme: '+t+' (click to change)');
      btn.setAttribute('aria-label','Theme: '+t);
    }
  }
  window.cycleTheme=function(){
    var cur=null; try{ cur=localStorage.getItem('sr-theme'); }catch(e){}
    var order=['auto','light','dark'];
    var i=order.indexOf(cur||'auto');
    setTheme(order[(i+1)%order.length]);
  };

  (function init(){
    var l=null,t=null;
    try{ l=localStorage.getItem('sr-lang'); t=localStorage.getItem('sr-theme'); }catch(e){}
    if(!l) l=(navigator.language||'').toLowerCase().indexOf('zh')===0 ? 'zh' : 'en';
    setLang(l); setTheme(t||'auto');
  })();

  /* ---------------- register ---------------- */
  var tbody=d.getElementById('reg-body');
  if(!tbody) return;
  var rows=[].slice.call(tbody.querySelectorAll('tr.row'));
  var searchEl=d.getElementById('reg-search');
  var countEl=d.getElementById('reg-count');
  var emptyEl=d.getElementById('reg-empty');
  var clearEl=d.getElementById('reg-clear');
  var chips=[].slice.call(d.querySelectorAll('.chip[data-facet]'));
  var active={};           /* facet -> Set of values */
  var query='';
  var sortKey=null, sortDir=1;

  function detailFor(tr){ var n=tr.nextElementSibling; return (n && n.classList.contains('detail')) ? n : null; }

  function matches(tr){
    if(query){
      if((tr.getAttribute('data-search')||'').indexOf(query)<0) return false;
    }
    for(var f in active){
      if(!active[f] || !active[f].size) continue;
      var v=tr.getAttribute('data-'+f)||'';
      if(!active[f].has(v)) return false;
    }
    return true;
  }

  function apply(){
    var shown=0;
    rows.forEach(function(tr){
      var ok=matches(tr);
      tr.style.display = ok ? '' : 'none';
      var det=detailFor(tr);
      if(det && !ok){ det.classList.remove('show'); tr.classList.remove('open'); tr.setAttribute('aria-expanded','false'); }
      if(det) det.style.display = ok ? '' : 'none';
      if(ok) shown++;
    });
    if(countEl) countEl.textContent=String(shown);
    if(emptyEl) emptyEl.classList.toggle('show', shown===0);
    var any = query || Object.keys(active).some(function(f){ return active[f] && active[f].size; });
    if(clearEl) clearEl.style.display = any ? '' : 'none';
    writeHash(any);
    updateChipCounts();
  }

  /* live counts on each chip, computed against the other active facets */
  function updateChipCounts(){
    chips.forEach(function(c){
      var f=c.getAttribute('data-facet'), v=c.getAttribute('data-val');
      var n=0;
      rows.forEach(function(tr){
        if(query && (tr.getAttribute('data-search')||'').indexOf(query)<0) return;
        for(var g in active){
          if(g===f) continue;
          if(!active[g] || !active[g].size) continue;
          if(!active[g].has(tr.getAttribute('data-'+g)||'')) return;
        }
        if((tr.getAttribute('data-'+f)||'')===v) n++;
      });
      var el=c.querySelector('.n');
      if(el) el.textContent=String(n);
      c.disabled = (n===0 && c.getAttribute('aria-pressed')!=='true');
      c.style.opacity = c.disabled ? '.4' : '';
    });
  }

  chips.forEach(function(c){
    c.addEventListener('click',function(){
      var f=c.getAttribute('data-facet'), v=c.getAttribute('data-val');
      active[f]=active[f]||new Set();
      var on=c.getAttribute('aria-pressed')==='true';
      if(on){ active[f].delete(v); c.setAttribute('aria-pressed','false'); }
      else { active[f].add(v); c.setAttribute('aria-pressed','true'); }
      apply();
    });
  });

  if(searchEl){
    searchEl.addEventListener('input',function(){ query=searchEl.value.trim().toLowerCase(); apply(); });
    searchEl.addEventListener('keydown',function(e){
      if(e.key==='Escape'){ searchEl.value=''; query=''; apply(); searchEl.blur(); }
    });
  }
  if(clearEl){
    clearEl.addEventListener('click',function(){
      query=''; if(searchEl) searchEl.value='';
      active={}; chips.forEach(function(c){ c.setAttribute('aria-pressed','false'); });
      apply();
    });
  }

  /* row expansion */
  tbody.addEventListener('click',function(e){
    var a=e.target.closest ? e.target.closest('a') : null;
    if(a) return;
    var tr=e.target.closest ? e.target.closest('tr.row') : null;
    if(!tr) return;
    var det=detailFor(tr);
    if(!det) return;
    var open=det.classList.toggle('show');
    tr.classList.toggle('open',open);
    tr.setAttribute('aria-expanded',String(open));
  });
  tbody.addEventListener('keydown',function(e){
    if(e.key!=='Enter' && e.key!==' ') return;
    var tr=e.target.closest ? e.target.closest('tr.row') : null;
    if(!tr) return;
    e.preventDefault();
    tr.click();
  });

  /* sorting */
  var ths=[].slice.call(d.querySelectorAll('th.sortable'));
  var order={verdict:['TAKE','CONSIDER','SKIP','AVOID'],
             grade:['A','B','C','D'],
             food:['RICH','SPLIT','TRACE','SYNTHETIC','NOT_FOOD'],
             dose:['YES','PARTIAL','NO','NA'],
             syn:['NONE','PARTIAL','CONDITIONAL','FULL','NA']};
  function keyval(tr,k){
    var v=tr.getAttribute('data-'+k)||'';
    if(order[k]){ var i=order[k].indexOf(v); return i<0?99:i; }
    return (tr.getAttribute('data-name')||'').toLowerCase();
  }
  ths.forEach(function(th){
    th.setAttribute('tabindex','0');
    function run(){
      var k=th.getAttribute('data-key');
      if(sortKey===k){ sortDir=-sortDir; } else { sortKey=k; sortDir=1; }
      ths.forEach(function(o){ o.removeAttribute('aria-sort'); });
      th.setAttribute('aria-sort', sortDir===1?'ascending':'descending');
      var pairs=rows.map(function(tr){ return [tr, detailFor(tr)]; });
      pairs.sort(function(a,b){
        var x=keyval(a[0],k), y=keyval(b[0],k);
        if(x<y) return -1*sortDir;
        if(x>y) return 1*sortDir;
        var nx=(a[0].getAttribute('data-name')||''), ny=(b[0].getAttribute('data-name')||'');
        return nx.localeCompare(ny);
      });
      tbody.classList.remove('stagger');
      pairs.forEach(function(p){ tbody.appendChild(p[0]); if(p[1]) tbody.appendChild(p[1]); });
      rows=pairs.map(function(p){ return p[0]; });
    }
    th.addEventListener('click',run);
    th.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); run(); } });
  });

  /* shareable filtered view */
  function writeHash(any){
    if(!any){ if(location.hash.indexOf('#f=')===0) history.replaceState(null,'',location.pathname+location.search); return; }
    var parts=[];
    if(query) parts.push('q:'+encodeURIComponent(query));
    Object.keys(active).forEach(function(f){
      if(active[f] && active[f].size){ var vals=[]; active[f].forEach(function(v){vals.push(v);}); parts.push(f+':'+vals.join(',')); }
    });
    history.replaceState(null,'','#f='+parts.join(';'));
  }
  function readHash(){
    var h=location.hash||'';
    if(h.indexOf('#f=')!==0) return;
    h.slice(3).split(';').forEach(function(part){
      var i=part.indexOf(':'); if(i<0) return;
      var f=part.slice(0,i), v=part.slice(i+1);
      if(f==='q'){ query=decodeURIComponent(v).toLowerCase(); if(searchEl) searchEl.value=decodeURIComponent(v); return; }
      active[f]=new Set(v.split(','));
      chips.forEach(function(c){
        if(c.getAttribute('data-facet')===f && active[f].has(c.getAttribute('data-val'))) c.setAttribute('aria-pressed','true');
      });
    });
  }
  readHash();
  apply();

  /* keyboard: / focuses search, L toggles language */
  d.addEventListener('keydown',function(e){
    var t=e.target, typing=/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName||'');
    if(e.key==='/' && !typing){ e.preventDefault(); if(searchEl) searchEl.focus(); return; }
    if((e.key==='l'||e.key==='L') && !typing && !e.metaKey && !e.ctrlKey && !e.altKey){
      setLang(root.getAttribute('data-lang')==='en'?'zh':'en');
    }
  });
})();
'''
