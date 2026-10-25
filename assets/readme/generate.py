"""Generate original, dependency-free SVG artwork for the repository README."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
NAVY, PANEL, CYAN, WHITE, MUTED, GOLD = '#0b1728', '#12263d', '#55dacb', '#f2f7fc', '#b7c9db', '#f4c66a'

def svg(name, w, h, body, title, desc):
    text = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<style>text{{font-family:Arial,Helvetica,sans-serif}}.title{{font-weight:700}}</style>
{body}</svg>'''
    (ROOT / name).write_text(text, encoding='utf-8')

def text(x,y,s,size=18,color=WHITE,weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(s)}</text>'

def rect(x,y,w,h,fill=PANEL,r=12,stroke='none'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'

icons = {
 'hazard': '<path d="M12 3 22 21H2Z"/><path d="M12 9v5m0 3v.2"/>',
 'sensor': '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4m6-4v4M9 18v4m6-4v4M2 9h4m-4 6h4m12-6h4m-4 6h4"/><circle cx="12" cy="12" r="2"/>',
 'zone': '<circle cx="12" cy="10" r="3"/><path d="M19 10c0 5-7 12-7 12S5 15 5 10a7 7 0 0 1 14 0Z"/>',
 'water': '<path d="M12 2S5 10 5 15a7 7 0 0 0 14 0c0-5-7-13-7-13Z"/><path d="M8 15c0 2 1 3 3 3"/>',
 'network': '<rect x="8" y="2" width="8" height="6" rx="1"/><rect x="1" y="16" width="8" height="6" rx="1"/><rect x="15" y="16" width="8" height="6" rx="1"/><path d="M12 8v4H5v4m7-4h7v4"/>',
 'evidence': '<path d="M6 2h9l4 4v16H6Z"/><path d="M14 2v5h5M9 12h7m-7 4h7"/>',
 'cad': '<path d="m12 2 10 5v10l-10 5-10-5V7Zm0 10v10M2 7l10 5 10-5M7 4.5l10 5v5"/>',
 'chart': '<path d="M3 3v18h19M6 15l5-5 5 2 5-6"/><circle cx="11" cy="10" r="1"/>',
 'roadmap': '<path d="M5 22V5a3 3 0 0 1 6 0v14a3 3 0 0 0 6 0V2"/><path d="m14 5 3-3 3 3"/>',
 'team': '<circle cx="9" cy="7" r="3"/><path d="M2 21v-3a7 7 0 0 1 14 0v3M17 4a3 3 0 0 1 0 6m2 4c3 1 3 4 3 7"/>',
}
for name, shape in icons.items():
    svg(f'{name}.svg',24,24,f'<g fill="none" stroke="#249b90" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{shape}</g>',name+' icon','Original line icon for PRAN RAKSHAK.')

body=rect(0,0,1200,420,NAVY,20)
body+='<defs><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#1c3249" stroke-width=".6"/></pattern></defs><rect x="730" y="0" width="470" height="420" fill="url(#grid)"/>'
body+=rect(48,40,318,30,'#19374b',15)+text(64,61,'VISHWAKARMA AWARDS 2026–27',13,CYAN,700)
body+=text(48,145,'PRAN',70,WHITE,700)+text(48,222,'RAKSHAK',70,WHITE,700)
body+=text(50,270,'Earlier warnings. A clearer path to rescue.',23,WHITE)
body+=text(50,306,'Gas & dust sensing  /  Worker zones  /  Offline supervision',17,MUTED)
body+='<path d="M50 340h64" stroke="#55dacb" stroke-width="4"/>'
body+=text(50,376,'TEAM CODEMIUM',14,CYAN,700)+text(235,376,'STAGE 2  ·  VK26-IITH-SM-0275',14,MUTED)
body+='<g transform="translate(800 80)"><path d="M0 150a130 130 0 0 1 260 0" fill="#e6af43"/><path d="M100 35V9h60v26M130 14v128" fill="none" stroke="#f9db89" stroke-width="16" stroke-linecap="round"/><rect x="-14" y="142" width="288" height="30" rx="15" fill="#f4c66a"/><rect x="181" y="104" width="62" height="52" rx="9" fill="#173b51" stroke="#55dacb" stroke-width="2"/><circle cx="212" cy="130" r="12" fill="#55dacb"/><path d="M252 91q32-24 0-48m14 58q49-36 0-72" fill="none" stroke="#55dacb" stroke-width="3"/><path d="M20 205h65l42 32h99" stroke="#55dacb" stroke-width="2" fill="none"/><g fill="#55dacb"><circle cx="20" cy="205" r="5"/><circle cx="127" cy="237" r="5"/><circle cx="226" cy="237" r="5"/></g></g>'
body+=text(814,376,'SMART HELMET / CONCEPT',13,MUTED,700)
svg('hero.svg',1200,420,body,'PRAN RAKSHAK — Vishwakarma Awards 2026–27','Concept illustration of a connected safety helmet. Team Codemium, Stage 2. Proposed gas and dust sensing, worker zones and offline supervision.')

body=''
for x,w,label,color in [(0,238,'STAGE 2 · DESIGN & ANALYSIS',CYAN),(250,238,'ESP32-C3 + RASPBERRY PI',WHITE),(500,238,'NATIVE ENGINEERING FILES',GOLD)]:
    body+=rect(x,0,w,34,NAVY,6)+text(x+13,22,label,12,color,700)
svg('badges.svg',738,34,body,'Project status and technology','Stage 2 design and analysis; ESP32-C3 and Raspberry Pi; native engineering files available.')

body=rect(0,0,1200,460,NAVY,16)+text(36,43,'FROM THE WORKER TO THE LOCAL CONTROL ROOM',19,WHITE,700)+text(36,72,'Proposed architecture · firmware and network validation pending',15,MUTED)
for x,w,title,lines in [(36,325,'01 / SENSE & WARN',['ESP32-C3 wearable node','CH4 · CO · conditioned H2S','Motion + manual panic input','Local vibration / display / alarm']), (440,320,'02 / CONNECT LOCALLY',['Fixed monitoring nodes','Wi-Fi + MQTT baseline','Node identity + timestamps','Proposed mesh extension']), (838,326,'03 / SUPERVISE OFFLINE',['Raspberry Pi 4 gateway','MQTT broker + rules + logging','Last-seen worker zones','Supervisor warnings'])]:
    body+=rect(x,108,w,220,PANEL,12,'#284660')+text(x+22,145,title,19,CYAN,700)
    for i,line in enumerate(lines):body+=text(x+22,184+i*33,line,17,WHITE if i==0 else MUTED)
body+='<g stroke="#55dacb" stroke-width="3" fill="none"><path d="M371 218h55m-10-8 10 8-10 8M770 218h55m-10-8 10 8-10 8"/><path d="M998 341v35H198v-35" stroke-dasharray="7 6"/><path d="m190 350 8-9 8 9"/></g>'
body+=text(375,402,'Warnings returned over the local network',17,CYAN)+text(36,438,'Dust interface proposed; runoff sensing and airflow-based leak estimation remain wider design scope.',15,MUTED)
svg('architecture.svg',1200,460,body,'Proposed PRAN RAKSHAK system architecture','Wearable ESP32-C3 sensing and local warnings connect over Wi-Fi/MQTT to fixed nodes and a Raspberry Pi offline gateway. Gateway records telemetry and last-seen zones. Mesh, firmware and network tests remain pending.')

body=rect(0,0,1200,178,NAVY,14)
for x,num,title,sub in [(32,'4','EDITABLE SCHEMATIC SHEETS','ERC: 0 errors · 68 warnings'),(432,'4','SOLVED LID MESHES','Assumed material, supports and load'),(832,'7,411','FINAL-MESH TETRAHEDRA','Selected metrics meet refinement criterion')]:
    body+=text(x,63,num,44,CYAN,700)+text(x,101,title,15,WHITE,700)+text(x,132,sub,14,MUTED)
svg('evidence-strip.svg',1200,178,body,'Published design evidence','Four schematic sheets, with zero ERC electrical errors and 68 warnings. Four actual lid meshes; final mesh has 7411 tetrahedra. FEA is assumption-based and selected-metric convergence is numerical evidence only.')
print('Generated',len(list(ROOT.glob('*.svg'))),'SVG assets')
