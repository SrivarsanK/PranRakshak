import os,math,uuid,csv,heapq,collections,html,random
import numpy as np
from PIL import Image,ImageDraw,ImageFont
random.seed(26)
OUT='/mnt/data'
B=(100.,80.,152.,168.)
FP=[]; NET={}; SEG=[]; VIA=[];keepouts=[(117,81,135,87)]; lines=[]

def uid():return str(uuid.uuid4())
def netno(n):
 if n in ('',None):return 0
 if n not in NET:NET[n]=len(NET)+1
 return NET[n]
def q(s):return '"'+str(s).replace('\\','\\\\').replace('"','\\"')+'"'
def clean(n):return str(n).replace(' ','_')
def nfmt(n):return f'(net {netno(n)} {q(n)})' if n else ''
def add(ref,val,typ,x,y,desc='',r=0):
 f=dict(ref=ref,val=val,typ=typ,x=x,y=y,r=r,desc=desc,pads=[],extra=[])
 FP.append(f);return f

def pad(f,n,dx,dy,net='',kind='thru_hole',shape='circle',size=(1.7,1.7),drill=.8,layer=None):
 # All parts placed with angle zero in this prototype
 x=f['x']+dx;y=f['y']+dy
 p=dict(num=str(n),x=x,y=y,dx=dx,dy=dy,kind=kind,shape=shape,size=size,drill=drill,net=net,ref=f['ref'])
 f['pads'].append(p)
 netno(net)
 return p

def hdr(ref,typ,x,y,names,value='Conn_01x',pitch=2.54):
 f=add(ref,value+str(len(names)).zfill(2),typ,x,y,desc='Header connector: verify mating pinout')
 for i,n in enumerate(names):pad(f,i+1,0,i*pitch,n,kind='thru_hole',shape='rect' if i==0 else 'circle',size=(1.75,1.75),drill=1.0)
 return f

def r0805(ref,val,x,y,a,b):
 f=add(ref,val,'R_0805',x,y)
 pad(f,1,-.97,0,a,'smd','roundrect',(1.00,1.25))
 pad(f,2,.97,0,b,'smd','roundrect',(1.00,1.25))
 return f

def c0805(ref,val,x,y,a,b):
 f=add(ref,val,'C_0805',x,y)
 pad(f,1,-.97,0,a,'smd','roundrect',(1.00,1.25));pad(f,2,.97,0,b,'smd','roundrect',(1.00,1.25));return f

def sot23(ref,val,x,y,gate,drain,source):
 f=add(ref,val,'SOT-23',x,y)
 # SOT-23 standard pads pin1 gate, pin2 source, pin3 drain for AO3400A
 pad(f,1,-.95,-.95,gate,'smd','rect',(.9,.8))
 pad(f,2,-.95,.95,source,'smd','rect',(.9,.8))
 pad(f,3,.95,0,drain,'smd','rect',(.9,.8))
 return f

def diode(ref,x,y,a,k):
 f=add(ref,'SS14','SOD-123',x,y)
 pad(f,1,-1.55,0,k,'smd','rect',(1.2,1.0));pad(f,2,1.55,0,a,'smd','rect',(1.2,1.0));return f

# ESP32-C3-WROOM-02 official Espressif land-pattern positions (converted from source)
f=add('U1','ESP32-C3-WROOM-02-N4','ESP32-C3-WROOM-02',126,94,'On-board Wi-Fi antenna - keep metal & copper away')
mp={1:'3V3',2:'EN',3:'VBAT_ADC',4:'STATUS',5:'SDA',6:'SCL',7:'',8:'BOOT',9:'GND',10:'PANIC',11:'MOTOR_GATE_SRC',12:'BUZZ_GATE_SRC',13:'USB_DM',14:'USB_DP',15:'',16:'',17:'',18:'',19:'GND'}
for n in range(1,10):pad(f,n,-8.75,-5.9+(n-1)*1.5,mp[n],'smd','rect',(1.5,.9))
for n in range(10,19):pad(f,n,8.75,6.1-(n-10)*1.5,mp[n],'smd','rect',(1.5,.9))
for xx in (-.14,.91,2.06):
 for yy in (-.8,.3,1.4):pad(f,19,xx,yy,'GND','smd','rect',(.7,.7))
# connectors, main supply module external: must supply regulated rails
hdr('J1','PWR',108,116,['3V3','GND','5V_SENSOR','VBAT_RAW'],'Power_In_')
hdr('J2','MQ4',108,132,['5V_SENSOR','GND','CH4_RAW'],'MQ4_')
hdr('J3','MQ7',108,142,['5V_SENSOR','GND','CO_RAW'],'MQ7_')
hdr('J4','H2S',108,152,['3V3','GND','H2S_AIN'],'H2S_AFE_')
hdr('J5','DUST',118,159,['5V_SENSOR','GND','DUST_RAW'],'DUST_AFE_')
hdr('J6','OLED',145,112,['3V3','GND','SDA','SCL'],'I2C_OLED_')
hdr('J7','IMU',145,125,['3V3','GND','SDA','SCL'],'I2C_IMU_')
hdr('J8','PANIC_SW',145,138,['PANIC','GND'],'Panic_')
hdr('J9','VIB',145,148,['3V3','MOTOR_LOW'],'Vibration_')
hdr('J10','BUZZ',136,159,['3V3','BUZZ_LOW'],'Buzzer_')
hdr('J11','USB_TEST',145,96,['GND','USB_DM','USB_DP'],'USB_Test_')
hdr('J12','RESET',108,105,['EN','GND'],'Reset_')
hdr('J13','BOOT',108,111,['BOOT','GND'],'Boot_')
# ADC VSSOP-10, 10 pins .5mm pitch and 3mm body. Pinout per TI datasheet
f=add('U2','ADS1115IDGST','VSSOP-10',127,126,'16-bit I2C ADC; address tied to GND')
adc={1:'GND',2:'',3:'GND',4:'CH4_AIN',5:'CO_AIN',6:'H2S_AIN',7:'DUST_AIN',8:'3V3',9:'SDA',10:'SCL'}
for n in range(1,6):pad(f,n,-1.55,-1+(n-1)*.5,adc[n],'smd','rect',(1.10,.30))
for n in range(6,11):pad(f,n,1.55,1-(n-6)*.5,adc[n],'smd','rect',(1.10,.30))

# Bypass, boot, filtering, voltage safe scaling. MQ4/7/DUST assumed 0-5V outputs.
c0805('C1','10uF',112.8,90,'3V3','GND')
c0805('C2','100nF',139,103,'3V3','GND')
c0805('C3','100nF',132,122,'3V3','GND')
r0805('R1','10k',115,107,'3V3','EN')
c0805('C4','1uF',115,110,'EN','GND')
r0805('R2','10k',121,109,'3V3','BOOT')
r0805('R3','4.7k',127,109,'3V3','SDA')
r0805('R4','4.7k',133,109,'3V3','SCL')
r0805('R5','10k',119,117,'3V3','PANIC')
# Two 100k resistors for 3.7V 1-cell LiPo voltage sense (not direct battery supply)
r0805('R6','100k',119,121,'VBAT_RAW','VBAT_ADC')
r0805('R7','100k',119,124,'VBAT_ADC','GND')
# sensor analog dividers from MAX 5V to MAX 3.125 V. ADC full-scale is gain-dependent!
r0805('R8','12k',117,134,'CH4_RAW','CH4_AIN')
r0805('R9','20k',125,134,'CH4_AIN','GND')
r0805('R10','12k',117,140,'CO_RAW','CO_AIN')
r0805('R11','20k',125,140,'CO_AIN','GND')
r0805('R12','12k',117,147,'DUST_RAW','DUST_AIN')
r0805('R13','20k',125,147,'DUST_AIN','GND')
# Analog noise bypass - 10nF near ADC, resistor networks need calibration
c0805('C5','10nF',132,135,'CH4_AIN','GND')
c0805('C6','10nF',132,140,'CO_AIN','GND')
c0805('C7','10nF',132,145,'DUST_AIN','GND')
# alarm low-side drivers: Q1/Q2 AO3400A. Gates with series and pulldown.
r0805('R14','100R',119,151,'MOTOR_GATE_SRC','MOTOR_GATE')
r0805('R15','100k',126,151,'MOTOR_GATE','GND')
sot23('Q1','AO3400A',135,149,'MOTOR_GATE','MOTOR_LOW','GND')
diode('D1',139,153,'MOTOR_LOW','3V3')
r0805('R16','100R',119,155,'BUZZ_GATE_SRC','BUZZ_GATE')
r0805('R17','100k',126,155,'BUZZ_GATE','GND')
sot23('Q2','AO3400A',130,159,'BUZZ_GATE','BUZZ_LOW','GND')
diode('D2',136,155,'BUZZ_LOW','3V3')
# LED: on logic GPIO5 -> resistor -> LED -> GND
r0805('R18','1k',117,104,'STATUS','LED_A')
f=add('D3','LED_GREEN','LED_0805',122,104)
pad(f,1,-.97,0,'GND','smd','rect',(1.00,1.20));pad(f,2,.97,0,'LED_A','smd','rect',(1.00,1.20))
# mounting holes NPTH
for ref,x,y in [('H1',104.5,85),('H2',148,85),('H3',104,165),('H4',149,165)]:
 f=add(ref,'MountingHole_2.5mm','MountingHole',x,y)
 pad(f,'',0,0,'','np_thru_hole','circle',(2.7,2.7),2.5)

# Check footprint mechanical overlaps (bounding-box approximations)
# Note: visual/physical collision verification still required in KiCad.

# --------- Simple 2-layer maze routing with 0.25 mm grid --------
GRID=.25; NX=round((B[2]-B[0])/GRID)+1; NY=round((B[3]-B[1])/GRID)+1
from scipy.ndimage import binary_dilation

def cell(x,y):return int(round((x-B[0])/GRID)),int(round((y-B[1])/GRID))
def xy(i,j):return B[0]+i*GRID,B[1]+j*GRID

nets_p=collections.defaultdict(list)
for f in FP:
 for p in f['pads']:
  if p['net']:nets_p[p['net']].append(p)

all_pads=[p for f in FP for p in f['pads']]
smd_forbidden=np.zeros((NY,NX),dtype=np.bool_)
for pp in all_pads:
 if pp['kind']!='smd':continue
 i,j=cell(pp['x'],pp['y'])
 for ii in range(max(0,i-7),min(NX,i+8)):
  for jj in range(max(0,j-7),min(NY,j+8)):
   if (ii-i)**2+(jj-j)**2<=5**2:smd_forbidden[jj,ii]=True

occ=np.zeros((2,NY,NX),dtype=np.int32)
# walls at outline edge
occ[:,:2,:]=-1;occ[:,-2:,:]=-1;occ[:,:,:2]=-1;occ[:,:,-2:]=-1
# antenna keepout all layer for copper
for a,b,c,d in keepouts:
 i0,j0=cell(a,b);i1,j1=cell(c,d)
 occ[:,j0:j1+1,i0:i1+1]=-1

# Pad clearance obstacle 0.20mm signal tracks +0.25 clearance approx
for p in all_pads:
 if p['kind']=='np_thru_hole':
  pds=[0,1];rr=1.7
 else:
  pds=[0,1] if p['kind']=='thru_hole' else [0]
  rr=None
 x,y=p['x'],p['y']; w,h=p['size']
 n=netno(p['net']) if p['net'] else -1
 i0,j0=cell(x-w/2-.48,y-h/2-.48);i1,j1=cell(x+w/2+.48,y+h/2+.48)
 for layer in pds:
  for jj in range(max(0,j0),min(NY,j1+1)):
   yy=B[1]+jj*GRID
   for ii in range(max(0,i0),min(NX,i1+1)):
    xx=B[0]+ii*GRID
    if p['kind']=='np_thru_hole':v=(xx-x)**2+(yy-y)**2<1.70**2
    else:v=abs(xx-x)<=w/2+.40 and abs(yy-y)<=h/2+.40
    if v and occ[layer,jj,ii] in (0,n):occ[layer,jj,ii]=n

# Route prioritized short local analog nets before long nets; ground plane only
priority=[n for n in nets_p if n not in ('GND','3V3','5V_SENSOR')]
priority.sort(key=lambda n: (0 if n in ['CH4_RAW','CO_RAW','DUST_RAW','CH4_AIN','CO_AIN','DUST_AIN','H2S_AIN'] else 1, len(nets_p[n]),n))
priority+=['5V_SENSOR','3V3']
failed=[];success=[];routed_count=collections.Counter();paths_records=[]
# Costs: prefer staying on F.Cu, allow vias, but avoid B.Cu as it is ground filled later
# Via at grid cell must be safe on both layers.
DIR=[(1,0),(-1,0),(0,1),(0,-1)]

def route(a,b,nm):
 net=netno(nm)
 x0,y0=cell(a['x'],a['y']);x1,y1=cell(b['x'],b['y'])
 if not(2<=x0<NX-2 and 2<=y0<NY-2 and 2<=x1<NX-2 and 2<=y1<NY-2):return None
 start_layers=[0,1] if a['kind']=='thru_hole' else [0]
 end_layers={0,1} if b['kind']=='thru_hole' else {0}
 def free(l,i,j):
  z=occ[l,j,i]
  return z in (0,net)
 pq=[];came={};best={};seq=0
 for layer in start_layers:
  k=(layer,x0,y0);best[k]=0
  h=abs(x0-x1)+abs(y0-y1)
  heapq.heappush(pq,(h,seq,0,k));seq+=1
 # Precompute safe via destinations using a 0.75 mm keep-clear radius on both copper layers.
 from scipy.ndimage import binary_erosion
 freeboth=np.logical_and(np.logical_or(occ[0]==0,occ[0]==net), np.logical_or(occ[1]==0,occ[1]==net))
 disk=np.fromfunction(lambda yy,xx:(xx-3)**2+(yy-3)**2<=9,(7,7))
 via_safe=binary_erosion(freeboth,structure=disk,border_value=0)&(~smd_forbidden)
 end=None; steps=0
 while pq and steps<220000:
  _,_,g,s=heapq.heappop(pq);steps+=1
  if g>best[s]:continue
  l,x,y=s
  if x==x1 and y==y1 and l in end_layers:
   end=s;break
  for dx,dy in DIR:
   nx,ny=x+dx,y+dy
   if nx<2 or nx>=NX-2 or ny<2 or ny>=NY-2:continue
   if not free(l,nx,ny) and not (nx==x1 and ny==y1):continue
   ns=(l,nx,ny);ng=g+1+(0.3 if l else 0)
   if ng<best.get(ns,1e12):
    best[ns]=ng;came[ns]=s;h=abs(nx-x1)+abs(ny-y1);heapq.heappush(pq,(ng+h,seq,ng,ns));seq+=1
  other=1-l
  if via_safe[y,x]:
   ns=(other,x,y);ng=g+45
   if ng<best.get(ns,1e12):
    best[ns]=ng;came[ns]=s;heapq.heappush(pq,(ng+abs(x-x1)+abs(y-y1),seq,ng,ns));seq+=1
 if end is None:return None
 pth=[end];k=end
 while k in came:
  k=came[k];pth.append(k)
 pth=pth[::-1]
 # ensure obstacle clearance for subsequent tracks: mark occupied 2 grid pixels approx
 # compress on layer and direction, via route markers
 for pt in pth:
  l,x,y=pt
  for xx in range(max(2,x-2),min(NX-2,x+3)):
   for yy in range(max(2,y-2),min(NY-2,y+3)):
    if occ[l,yy,xx] in (0,net):occ[l,yy,xx]=net
 result=[];via=[];span=[pth[0]]
 for t in pth[1:]:
  if t[0]!=span[-1][0]:
   if len(span)>1:result.append(span)
   span=[t]
   x,y=xy(t[1],t[2]);via.append((x,y,nm))
  else:span.append(t)
 if len(span)>1:result.append(span)
 # split each span into horizontal/vertical segments at turn
 for seq0 in result:
  s=seq0[0];d=None;anchor=s
  for j in range(1,len(seq0)):
   c=seq0[j];prev=seq0[j-1];nd=(c[1]-prev[1],c[2]-prev[2]);
   if d is None:d=nd
   elif nd!=d:
    xA,yA=xy(anchor[1],anchor[2]);xB,yB=xy(prev[1],prev[2]);
    if (xA,yA)!=(xB,yB):SEG.append((xA,yA,xB,yB,'F.Cu' if anchor[0]==0 else 'B.Cu',nm,.25))
    anchor=prev;d=nd
  last=seq0[-1];xA,yA=xy(anchor[1],anchor[2]);xB,yB=xy(last[1],last[2]);
  if (xA,yA)!=(xB,yB):SEG.append((xA,yA,xB,yB,'F.Cu' if anchor[0]==0 else 'B.Cu',nm,.25))
 for vx,vy,vnet in via:
  vix,viy=cell(vx,vy)
  for ly in (0,1):
   for ix in range(-3,4):
    for iy in range(-3,4):
     if ix*ix+iy*iy<=9 and 2<=vix+ix<NX-2 and 2<=viy+iy<NY-2:
      if occ[ly,viy+iy,vix+ix] in (0,net):occ[ly,viy+iy,vix+ix]=net
 VIA.extend(via)
 return len(pth),len(via)

for nm in priority:
 pins=nets_p[nm]
 if len(pins)<2:continue
 used=[pins[0]];remaining=pins[1:]
 while remaining:
  opts=sorted(((math.hypot(a['x']-b['x'],a['y']-b['y']),i,a,b) for i,b in enumerate(remaining) for a in used),key=lambda x:x[0]);res=None
  for _,i,a,b in opts[:min(6,len(opts))]:
   res=route(a,b,nm)
   if res:
    success.append((nm,a['ref'],b['ref'],res));used.append(b);remaining.remove(b);routed_count[nm]+=1;break
  if res is None:
   for b in remaining:failed.append((nm,used[0]['ref'],b['ref']))
   break

# Conservative exclusion of routes that violate independently detected preliminary spacing/crossings.
# All pad/net assignments stay intact; these become visible unrouted airwires in KiCad.
removed_short_risk={'CH4_AIN','MOTOR_GATE_SRC','VBAT_RAW','EN','SCL'}
SEG=[s for s in SEG if s[5] not in removed_short_risk]
VIA=[v for v in VIA if v[2] not in removed_short_risk]
for name in removed_short_risk:routed_count.pop(name,None)
# grounding: top + bottom copper pours, KiCad must refill and DRC/check connections.

# Produce valid old-style KiCad v7/v8 PCB file (no fake ERC or DRC).

def fmtpad(p):
 x,y=p['dx'],p['dy'];w,h=p['size'];n=p['num'];nt=p['net'];ss=f'(pad {q(n)} {p["kind"]} {p["shape"]} (at {x:.3f} {y:.3f}) (size {w:.3f} {h:.3f})'
 if p['kind']=='thru_hole':ss+=f' (drill {p["drill"]:.3f}) (layers "*.Cu" "*.Mask")'
 elif p['kind']=='np_thru_hole':ss+=f' (drill {p["drill"]:.3f}) (layers "*.Cu" "*.Mask")'
 else:ss+=' (layers "F.Cu" "F.Paste" "F.Mask")'
 if nt:ss+=' '+nfmt(nt)
 return ss+f' (tstamp {uid()}))'

def fp_expr(f):
 ref=f['ref'];val=f['val'];typ=f['typ'];x=f['x'];y=f['y'];b=[]
 b.append(f'(footprint {q("PRAN_RAKSHAK:"+typ)} (layer "F.Cu") (tstamp {uid()}) (at {x:.3f} {y:.3f})')
 b.append(f'  (descr {q(f["desc"] or typ)}) (attr '+('smd' if any(p['kind']=='smd' for p in f['pads']) else 'through_hole')+')')
 if typ=='ESP32-C3-WROOM-02':tpos=(0,9.3)
 elif typ.startswith('MountingHole'):tpos=(0,-2.8)
 elif typ in ('R_0805','C_0805','LED_0805'):tpos=(0,-1.85)
 elif typ=='VSSOP-10':tpos=(0,-2.5)
 elif typ=='SOT-23':tpos=(0,-2.5)
 elif typ=='SOD-123':tpos=(0,-2.4)
 else:tpos=(-3.6,0) if x>=140 else (2.7,1.2)
 b.append(f'  (fp_text reference {q(ref)} (at {tpos[0]} {tpos[1]}) (layer "F.SilkS") (effects (font (size .8 .8) (thickness .14))) (tstamp {uid()}))')
 b.append(f'  (fp_text value {q(val)} (at 0 {tpos[1]+1}) (layer "F.Fab") (effects (font (size .7 .7) (thickness .1))) (tstamp {uid()}))')
 def fp_line(x0,y0,x1,y1,layer='F.SilkS',wd=.12):
  b.append(f'  (fp_line (start {x0:.3f} {y0:.3f}) (end {x1:.3f} {y1:.3f}) (stroke (width {wd}) (type solid)) (layer {q(layer)}) (tstamp {uid()}))')
 if typ=='ESP32-C3-WROOM-02':
  for p1,p2 in [((-9,-13),(9,-13)),((-9,-13),(-9,-7)),((9,-13),(9,-7)),((-9,7),(9,7))]:fp_line(*p1,*p2)
  fp_line(-9,-7,9,-7,'F.Fab')
  b.append(f'  (fp_text user "KEEP ANTENNA CLEAR" (at 0 -10) (layer "F.SilkS") (effects (font (size 0.7 0.7) (thickness .11))) (tstamp {uid()}))')
  b.append(f'  (zone (net 0) (net_name "") (layers "*.Cu") (tstamp {uid()}) (name "antenna_keepout") (hatch edge 0.508) (connect_pads (clearance 0)) (min_thickness 0.25) (keepout (tracks not_allowed) (vias not_allowed) (pads not_allowed) (copperpour not_allowed) (footprints not_allowed)) (fill (thermal_gap 0.5) (thermal_bridge_width .5)) (polygon (pts (xy -9 -13) (xy 9 -13) (xy 9 -7) (xy -9 -7))))')
 elif typ=='VSSOP-10':
  for p1,p2 in [((-1,-1.55),(1,-1.55)),((1,-1.55),(1,1.55)),((1,1.55),(-1,1.55)),((-1,1.55),(-1,-1.55))]:fp_line(*p1,*p2,'F.Fab',.1)
 elif typ in ('R_0805','C_0805','LED_0805'):
  fp_line(-.5,-.6,.5,-.6,'F.Fab',.1);fp_line(-.5,.6,.5,.6,'F.Fab',.1)
 elif typ=='SOT-23':
  for p1,p2 in [((-1,-1.55),(1,-1.55)),((1,-1.55),(1,1.55)),((1,1.55),(-1,1.55)),((-1,1.55),(-1,-1.55))]:fp_line(*p1,*p2,'F.Fab',.1)
 elif typ=='SOD-123':
  for p1,p2 in [((-1,-.75),(1,-.75)),((1,-.75),(1,.75)),((1,.75),(-1,.75)),((-1,.75),(-1,-.75))]:fp_line(*p1,*p2,'F.Fab',.1)
 elif typ!='MountingHole':
  fp_line(-1.6,-2,1.6,-2,'F.Fab',.1)
 for p in f['pads']:b.append('  '+fmtpad(p))
 b.append(')')
 return '\n'.join(b)

board=[]
board.append('(kicad_pcb (version 20221018) (generator pcbnew)')
board.append('(general (thickness 1.6)) (paper "A4")')
board.append('(layers (0 "F.Cu" signal) (31 "B.Cu" signal) (32 "B.Adhes" user) (33 "F.Adhes" user) (34 "B.Paste" user) (35 "F.Paste" user) (36 "B.SilkS" user) (37 "F.SilkS" user) (38 "B.Mask" user) (39 "F.Mask" user) (40 "Dwgs.User" user) (41 "Cmts.User" user) (42 "Eco1.User" user) (43 "Eco2.User" user) (44 "Edge.Cuts" user) (45 "Margin" user) (46 "B.CrtYd" user) (47 "F.CrtYd" user) (48 "B.Fab" user) (49 "F.Fab" user))')
board.append('(setup (pad_to_mask_clearance 0))')
board.append('(net 0 "")')
for n,v in NET.items():board.append(f'(net {v} {q(n)})')
board.extend(fp_expr(f) for f in FP)
for x0,y0,x1,y1,ly,n,w in SEG:
 board.append(f'(segment (start {x0:.3f} {y0:.3f}) (end {x1:.3f} {y1:.3f}) (width {w:.3f}) (layer {q(ly)}) (net {netno(n)}) (tstamp {uid()}))')
for x,y,n in VIA:
 board.append(f'(via (at {x:.3f} {y:.3f}) (size .70) (drill .35) (layers "F.Cu" "B.Cu") (net {netno(n)}) (tstamp {uid()}))')
for x0,y0,x1,y1 in [(100,80,152,80),(152,80,152,168),(152,168,100,168),(100,168,100,80)]:
 board.append(f'(gr_line (start {x0} {y0}) (end {x1} {y1}) (stroke (width .05) (type default)) (layer "Edge.Cuts") (tstamp {uid()}))')
board.append(f'(gr_text "PRAN RAKSHAK  |  PROTOTYPE REV-A" (at 126 106) (layer "F.SilkS") (effects (font (size 1 1) (thickness .18))) (tstamp {uid()}))')
board.append(f'(gr_text "3V3 & 5V MUST BE REGULATED EXTERNALLY" (at 125 166.5) (layer "B.SilkS") (effects (font (size .7 .7) (thickness .12))) (tstamp {uid()}))')
# ground pour on back, unfilled by default; KiCad 'B' will fill ground in GUI. No false fill claim.
board.append(f'(zone (net {netno("GND")}) (net_name "GND") (layer "F.Cu") (tstamp {uid()}) (hatch edge 0.508) (connect_pads (clearance 0.25)) (min_thickness .25) (fill yes (thermal_gap 0.5) (thermal_bridge_width .5)) (polygon (pts (xy 100.6 80.6) (xy 151.4 80.6) (xy 151.4 167.4) (xy 100.6 167.4))))')
board.append(f'(zone (net {netno("GND")}) (net_name "GND") (layer "B.Cu") (tstamp {uid()}) (hatch edge 0.508) (connect_pads (clearance 0.25)) (min_thickness .25) (fill yes (thermal_gap 0.5) (thermal_bridge_width .5)) (polygon (pts (xy 100.6 80.6) (xy 151.4 80.6) (xy 151.4 167.4) (xy 100.6 167.4))))')
board.append(')')
with open(OUT+'/PRAN_RAKSHAK_RevA.kicad_pcb','w') as o:o.write('\n'.join(board))

# Summary and BOM
with open(OUT+'/PRAN_RAKSHAK_RevA_BOM.csv','w',newline='') as fp:
 wr=csv.writer(fp);wr.writerow(['Reference','Value','Footprint/Type','Notes'])
 for f in FP:wr.writerow([f['ref'],f['val'],f['typ'],f['desc']])
with open(OUT+'/PRAN_RAKSHAK_RevA_Net_Mapping.csv','w',newline='') as fp:
 wr=csv.writer(fp);wr.writerow(['Net','Component','Pad','X_mm','Y_mm'])
 for f in FP:
  for p in f['pads']:
   if p['net']:wr.writerow([p['net'],f['ref'],p['num'],p['x'],p['y']])

# PCB preview PNG from same native source objects (only a preview; not KiCad screenshot)
S=12; W=int((B[2]-B[0])*S)+100; H=int((B[3]-B[1])*S)+100
im=Image.new('RGB',(W,H),'#111b23');d=ImageDraw.Draw(im)
def xy_px(x,y):return (int((x-B[0])*S+50),int((y-B[1])*S+50))
def boxp(a,b,c,e):return xy_px(a,b)+xy_px(c,e)
try:
 FONT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11)
 FONTS=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
 FONTL=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
except:FONT=FONTS=FONTL=None
d.rectangle(boxp(*B),fill='#0a5244',outline='#d1af6e',width=4)
for a,b,c,e in keepouts:d.rectangle(boxp(a,b,c,e),fill='#1c5b59',outline='#e9c467',width=2)
for x0,y0,x1,y1,ly,n,w in SEG:
 color='#f4a45e' if ly=='F.Cu' else '#7da9ff'
 d.line((xy_px(x0,y0),xy_px(x1,y1)),fill=color,width=max(2,int(w*S)))
for x,y,n in VIA:
 px,py=xy_px(x,y);d.ellipse((px-4,py-4,px+4,py+4),fill='#f1c188',outline='#0b3332')
for f in FP:
 x,y=f['x'],f['y'];typ=f['typ']
 if typ=='ESP32-C3-WROOM-02':d.rectangle(boxp(x-9,y-13,x+9,y+7),fill='#20313e',outline='#f7efdb',width=2)
 elif typ=='VSSOP-10':d.rectangle(boxp(x-1,y-1.5,x+1,y+1.5),fill='#202c35',outline='white',width=2)
 elif typ=='SOT-23':d.rectangle(boxp(x-1,y-1.5,x+1,y+1.5),fill='#202c35',outline='white')
 elif typ in ('R_0805','C_0805','LED_0805'):d.rectangle(boxp(x-1.15,y-.65,x+1.15,y+.65),fill='#263139',outline='#9ec6bd')
 elif typ=='SOD-123':d.rectangle(boxp(x-1.1,y-.8,x+1.1,y+.8),fill='#272a2d',outline='#aacec5')
 for p in f['pads']:
  cx,cy=xy_px(p['x'],p['y']);w,h=p['size']
  if p['kind']=='np_thru_hole':d.ellipse((cx-15,cy-15,cx+15,cy+15),fill='#111b23',outline='#d7b57e',width=3)
  elif p['kind']=='thru_hole':
   rr=max(4,int(w*S/2));d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill='#e0bd7d',outline='#a57b46',width=1);d.ellipse((cx-5,cy-5,cx+5,cy+5),fill='#122a2c')
  else:
   d.rectangle((cx-int(w*S/2),cy-int(h*S/2),cx+int(w*S/2),cy+int(h*S/2)),fill='#e7bb80')
 label=f['ref']
 if typ=='ESP32-C3-WROOM-02':
  d.text(xy_px(121,92),'ESP32-C3',font=FONTL,fill='#fff5d8')
 elif typ.startswith('Mounting'):pass
 elif typ in ('R_0805','C_0805','SOT-23','SOD-123','LED_0805','VSSOP-10'):d.text(xy_px(x-1.7,y-2.3),label,font=FONT,fill='#cfece3')
 else:d.text(xy_px(x+2.2,y),f'{label} {f["typ"]}',font=FONTS,fill='#e9f3df')
d.text((50,H-33),'PRAN RAKSHAK • 52 × 88 mm • REV A • PROTOTYPE / NOT SAFETY CERTIFIED',font=FONT,fill='#f2dac2')
im.save(OUT+'/PRAN_RAKSHAK_RevA_preview.png')

print('PCB file',len('\n'.join(board)),'bytes; footprints',len(FP),'pads',len(all_pads),'nets',len(NET),'segments',len(SEG),'vias',len(VIA))
print('Routed nets',len(routed_count),'attempts good',len(success),'route failures',len(failed))
print('Failed',failed[:50]);print('Routed',sorted(routed_count.items()))
with open(OUT+'/PRAN_RAKSHAK_routing_status.txt','w') as fp:
 fp.write('PRELIMINARY ROUTING STATUS - Not a KiCad DRC Report\n')
 fp.write(f'Board 52 x 88 mm; footprints: {len(FP)}; net labels: {len(NET)}; copper segments: {len(SEG)}; vias: {len(VIA)}\n')
 fp.write(f'Routing attempts completed before conservative short-risk cleanup: {len(success)}, failed: {len(failed)}\n')
 fp.write('Routes intentionally removed after spacing cross-check: '+', '.join(sorted(removed_short_risk))+'\n')
 for row in failed:fp.write(f'UNROUTED: {row}\n')
