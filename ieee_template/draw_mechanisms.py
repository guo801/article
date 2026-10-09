"""Publication diagrams derived from the manuscript; SVG and 300-dpi PNG."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import textwrap
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon

OUT = Path(__file__).parent / 'images' / 'mechanisms'
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none'})
INK = '#243647'
BLUE = '#e8f0fa'
GREEN = '#e8f4ef'
GOLD = '#fff3dc'
RED = '#fbe9e7'

def canvas(title, subtitle):
    fig, ax = plt.subplots(figsize=(13.5, 8.4))
    fig.patch.set_facecolor('white')
    ax.set(xlim=(0, 13.5), ylim=(-2.4, 6))
    ax.axis('off')
    ax.text(.35, 5.65, title, fontsize=19, weight='bold', color=INK)
    ax.text(.35, 5.25, subtitle, fontsize=10.5, color='#596b7b')
    return fig, ax

def box(ax, x, y, w, h, title, text='', color=BLUE):
    ax.add_patch(FancyBboxPatch((x,y), w,h, boxstyle='round,pad=0.025,rounding_size=0.13',
                             facecolor=color, edgecolor='#8196ab', linewidth=1.15))
    ax.text(x+w/2, y+h*.72 if text else y+h/2, title, ha='center', va='center',
            fontsize=11.5, weight='bold', color=INK)
    if text:
        text = '\n'.join(textwrap.fill(line, width=max(22, int(w*10))) for line in text.split('\n'))
        ax.text(x+w/2, y+h*.34, text, ha='center', va='center', fontsize=9.7,
                color=INK, linespacing=1.5)

def arrow(ax, a, b, label='', dashed=False, bend=0):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>', mutation_scale=14,
        linewidth=1.35, color='#526c84', linestyle='--' if dashed else '-',
        connectionstyle=f'arc3,rad={bend}'))
    if label:
        ax.text((a[0]+b[0])/2, (a[1]+b[1])/2+.12, label, fontsize=9,
                ha='center', color=INK, bbox=dict(facecolor='white',edgecolor='none',pad=2))

def save(fig, name):
    technical_details(ax, name)
    illustrated_band(ax, name)
    fig.savefig(OUT / f'{name}.svg', bbox_inches='tight', pad_inches=.15)
    fig.savefig(OUT / f'{name}.png', dpi=300, bbox_inches='tight', pad_inches=.15)
    plt.close(fig)

def technical_details(ax, name):
    """Expose internal computation, without inventing experimental results."""
    if name == 'sim_to_real_mechanism':
        cards = [
            ('SIMULATION DATASET', r'$\mathcal{D}_{sim}=\{(s_t,a_t)\}_{1}^{N}$', BLUE),
            ('SUPERVISED OBJECTIVE', r'$\mathcal{L}_{BC}=\mathbb{E}\|\pi_\theta(s)-a\|^2$', BLUE),
            ('PARAMETER ANCHOR', r'$\theta_{sim}\ \rightarrow\ \lambda\|\theta-\theta_{sim}\|^2$', GREEN),
            ('REAL DEMONSTRATIONS', r'$\mathcal{D}_{real},\quad M\ll N$', GOLD)]
        yy=2.24
    elif name == 'state_synchronization_mechanism':
        cards = [
            ('TIMESTAMPED RECORD', r'$\{q,\dot q, T_{obj},c,t,source\}$', BLUE),
            ('COORDINATE TRANSFORM', r'$T^{base}_{obj}=T^{base}_{cam}T^{cam}_{obj}$', BLUE),
            ('INTERPOLATED JOINTS', r'$q(t^*)=(1-\alpha)q_k+\alpha q_{k+1}$', BLUE),
            ('VALIDITY GATE', r'$t^*-t_{obs}\leq\tau,\quad c\geq c_{min}$', GOLD)]
        yy=2.24
    else:
        cards = [
            ('SKILL DISPATCH', r'$\pi_{grasp}\ |\ planner_{transit}\ |\ \pi_{pour}$', GREEN),
            ('OBSERVABLE GUARDS', 'grasp / target / dock / freshness', BLUE),
            ('DETERMINISTIC UPDATE', r'$s_{t+1}=\delta(s_t,g(o_t))$', GOLD),
            ('RECOVERY BUDGET', 'retry count + elapsed time', RED)]
        yy=-.02
    for i,(title,body,c) in enumerate(cards):
        xx=.4+i*3.2
        ax.add_patch(FancyBboxPatch((xx,yy),3.0,.59,boxstyle='round,pad=.02,rounding_size=.06',facecolor=c,edgecolor='#9cb0c1',lw=.8))
        ax.text(xx+.15,yy+.43,title,fontsize=7.8,weight='bold',color='#526c84',va='center')
        ax.text(xx+1.5,yy+.17,body,fontsize=8.6,ha='center',va='center',color=INK)
    if name != 'hsm_recovery_mechanism':
        for i in range(4):
            xx=1.9+i*3.2
            arrow(ax,(xx,3.14),(xx,2.86),dashed=True)
    if name == 'state_synchronization_mechanism':
        ax.text(2.2,.24,r'Occluded grasped object: $T^{base}_{obj}=T^{base}_{ee}T^{ee}_{obj}$',ha='center',fontsize=8.1,color='#957027')
    if name == 'hsm_recovery_mechanism':
        # Failure branches are routed around the guard-verification branch.
        elbow(ax,[(9.1,3.45),(9.1,2.63),(7.65,2.63),(7.65,2.15)])
        ax.text(8.35,2.8,'grasp lost / stale data',ha='center',fontsize=8,color='#a46539',bbox=dict(facecolor='white',edgecolor='none',pad=1))
        arrow(ax,(1.95,2.15),(1.95,3.45),dashed=True)
        ax.text(1.95,2.45,'Each state invokes a skill\nand monitors its return status',ha='center',fontsize=8.2,color='#526c84',bbox=dict(facecolor='white',edgecolor='none',pad=2))

def robot(ax, x, y, pose=0, virtual=False):
    """Articulated robot schematic, deliberately not a hardware CAD model."""
    col = '#2699bc' if virtual else '#54697b'
    pts = [(x,y),(x,y+.35),(x+.25,y+1.05),(x+.85,y+1.32),
           (x+1.25,y+.85 if pose != 1 else y+1.25),(x+1.42,y+.72 if pose != 1 else y+1.1)]
    ax.add_patch(Rectangle((x-.22,y-.08),.44,.12,facecolor=col,zorder=4))
    for a,b in zip(pts,pts[1:]):
        ax.plot([a[0],b[0]],[a[1],b[1]],color=col,lw=12,solid_capstyle='round',zorder=4,alpha=.8 if virtual else 1)
        ax.plot([a[0],b[0]],[a[1],b[1]],color='#e1eef3',lw=7,solid_capstyle='round',zorder=5)
    for a,b in pts[1:-1]:
        ax.add_patch(Circle((a,b),.105,facecolor=col,edgecolor='white',lw=1,zorder=6))
    gx,gy=pts[-1]
    ax.plot([gx-.13,gx-.13,gx+.13,gx+.13],[gy-.2,gy,gy,gy-.2],color=col,lw=2.6,zorder=6)
    return gx,gy

def vessel(ax,x,y,tilt=False):
    ax.add_patch(Polygon([(x-.13,y+.42),(x-.13,y),(x+.13,y),(x+.13,y+.42)],
        closed=False,fill=False,edgecolor='#445c70',lw=1.6,zorder=7))
    ax.add_patch(Rectangle((x-.11,y+.025),.22,.16,facecolor='#54bed0',alpha=.7,zorder=6))

def illustrated_band(ax,name):
    ax.plot([.4,13],[-.3,-.3],color='#d3dfe9',lw=1)
    labels = {
      'sim_to_real_mechanism':['Randomized virtual workcell','Real-arm adaptation','Precision liquid handling'],
      'state_synchronization_mechanism':['RGB-D and joint observations','Timestamped state packets','Updated virtual workcell'],
      'hsm_recovery_mechanism':['Approach and grasp','Verify grip and transfer','Recover or safely halt']
    }[name]
    for i,x in enumerate([.55,4.95,9.35]):
        ax.add_patch(FancyBboxPatch((x,-2.22),3.7,1.85,boxstyle='round,pad=0.02,rounding_size=.1',facecolor='#f8fafc',edgecolor='#d2dfe9'))
        ax.text(x+1.85,-2.04,labels[i],ha='center',fontsize=9.3,weight='bold',color=INK)
        ax.plot([x+.25,x+3.4],[-1.77,-1.77],color='#8196ab',lw=2)
        if name=='state_synchronization_mechanism' and i==1:
            # Three asynchronous streams converge at a shared sampling instant.
            for k,t in enumerate(['Joints','RGB-D','Gripper']):
                yy=-.66-k*.34
                ax.text(x+.12,yy,t,fontsize=8,color=INK,va='center')
                ax.plot([x+.9,x+3.45],[yy,yy],color='#a6bacb',lw=1)
                for xx in ([1.0,1.4,1.8,2.2,2.6,3.0] if k==0 else [1.12,1.9,2.72] if k==1 else [1.3,2.1,2.9]):
                    ax.add_patch(Circle((x+xx,yy),.045,facecolor=['#459db9','#d9a143','#529983'][k]))
            ax.plot([x+2.4,x+2.4],[-1.5,-.49],ls='--',color='#b55f6f',lw=1.5)
            ax.text(x+2.4,-1.65,'common time t*',ha='center',fontsize=8.5,color='#b55f6f')
            ax.text(x+2.4,-.43,'ALIGN',ha='center',fontsize=8,weight='bold',color='#b55f6f')
            continue
        virtual = (name=='sim_to_real_mechanism' and i==0) or (name=='state_synchronization_mechanism' and i==2)
        gx,gy=robot(ax,x+.65,-1.7,pose=1 if i==1 else 0,virtual=virtual)
        vessel(ax,x+2.55,-1.73)
        vessel(ax,gx,gy-.46)
        if name=='state_synchronization_mechanism' and i==0:
            ax.add_patch(Rectangle((x+2.7,-.78),.42,.23,facecolor='#526c84'))
            ax.add_patch(Circle((x+2.8,-.66),.045,facecolor='#79d6df'))
            ax.plot([x+2.7,gx],[ -.78,gy],ls='--',color='#37a9b9',lw=1)
        if virtual:
            for k in range(4): ax.plot([x+.2,x+3.45],[-1.78+k*.16,-1.78+k*.16],color='#b8d9e7',lw=.6,zorder=0)
        if name=='sim_to_real_mechanism':
            if i==0:
                # A parameter wheel makes randomization visible rather than decorative.
                for j,(txt,c) in enumerate([('light','#f1c966'),('mass','#729cbd'),('friction','#72b8a3')]):
                    yy=-.64-j*.32
                    ax.add_patch(FancyBboxPatch((x+2.35,yy-.12),1.13,.24,boxstyle='round,pad=.02',facecolor=c,edgecolor='none',alpha=.5))
                    ax.text(x+2.91,yy,txt,ha='center',va='center',fontsize=7.7,color=INK)
                ax.add_patch(FancyArrowPatch((x+2.5,-1.55),(x+2.5,-.45),connectionstyle='arc3,rad=.7',arrowstyle='-|>',color='#2699bc',mutation_scale=10,lw=1))
            elif i==1:
                ax.text(x+2.8,-.62,'SIM → REAL',ha='center',fontsize=8,weight='bold',color='#92712e')
                for j in range(3):
                    ax.add_patch(Rectangle((x+2.25+j*.24,-1.05+j*.09),.18,.22,facecolor=GOLD,edgecolor='#c2a35e',lw=.8))
                ax.text(x+2.75,-1.32,'few demos',ha='center',fontsize=7.5,color=INK)
            else:
                ax.add_patch(FancyArrowPatch((gx+.15,gy+.1),(x+2.52,-1.25),connectionstyle='arc3,rad=-.25',arrowstyle='-|>',color='#48aab9',mutation_scale=10,lw=1.2,linestyle='--'))
                ax.text(x+2.9,-.62,'TEST',ha='center',fontsize=8,weight='bold',color='#258d73')
                ax.text(x+2.9,-.91,'success\nprecision',ha='center',fontsize=7.5,color=INK)
        if name=='state_synchronization_mechanism' and i==2:
            # Dashed object outlines distinguish estimates from measured poses.
            ax.add_patch(Rectangle((gx-.2,gy-.55),.27,.42,fill=False,edgecolor='#d29c3b',ls='--',lw=1.2))
            ax.text(x+2.85,-.6,'SOURCE TAGS',ha='center',fontsize=7.8,weight='bold',color=INK)
            ax.text(x+2.85,-.9,'● measured',ha='center',fontsize=7.8,color='#2699bc')
            ax.text(x+2.85,-1.15,'- - estimated',ha='center',fontsize=7.8,color='#b3832d')
        if name=='hsm_recovery_mechanism':
            badge=['1','✓','!'][i]
            ax.text(x+3.1,-.88,badge,ha='center',fontsize=18,weight='bold',color=['#526c84','#258d73','#c56c38'][i])
            if i==0:
                ax.add_patch(FancyArrowPatch((gx-.35,gy+.18),(gx+.1,gy-.2),connectionstyle='arc3,rad=-.4',arrowstyle='-|>',color='#526c84',mutation_scale=10,lw=1.2))
            elif i==1:
                for d in [-1,1]: arrow(ax,(gx+d*.38,gy-.3),(gx+d*.15,gy-.3))
            else:
                ax.add_patch(FancyArrowPatch((gx+.3,gy-.15),(gx-.3,gy+.25),connectionstyle='arc3,rad=.6',arrowstyle='-|>',color='#c56c38',mutation_scale=12,lw=1.4,linestyle='--'))
                ax.text(x+2.9,-1.3,'bounded\nretry',ha='center',fontsize=7.8,color='#a46437')
    for x in [4.3,8.7]:
        if name=='sim_to_real_mechanism':
            # A small bridge visually marks the reality gap.
            ax.plot([x,x+.12,x+.43,x+.55],[-1.3,-1.12,-1.12,-1.3],color='#b29764',lw=2)
            ax.text(x+.28,-.96,'adapt' if x<5 else 'deploy',ha='center',fontsize=7,color='#92712e')
        else: arrow(ax,(x,-1.24),(x+.55,-1.24))

def elbow(ax, points):
    ax.plot([p[0] for p in points[:-1]], [p[1] for p in points[:-1]], color='#526c84', linewidth=1.35)
    arrow(ax,points[-2],points[-1])

fig, ax = canvas('Sim-to-real adaptation for precision manipulation',
                 'Simulation demonstrations and domain randomization precede regularized adaptation on real demonstrations.')
box(ax,.4,3.2,2.6,1.4,'Simulation data','SpaceMouse demonstrations\nLighting, textures, mass, friction')
box(ax,3.7,3.2,2.6,1.4,'Behavioral cloning','Fit observation-to-action policy\nMinimize demonstration error')
box(ax,7.0,3.2,2.6,1.4,'Simulation policy','Pretrained parameters\nReference for regularization',GREEN)
box(ax,10.3,3.2,2.6,1.4,'Few-shot adaptation','Real demonstrations\nTask loss + parameter penalty',GOLD)
for x in [3.0,6.3,9.6]: arrow(ax,(x,3.9),(x+.7,3.9))
box(ax,.4,.7,2.6,1.4,'Physical deployment','Execute learned liquid-handling\noperations',GREEN)
box(ax,3.7,.7,2.6,1.4,'Task evaluation','Success / trials\nVolume and concentration error')
box(ax,7.0,.7,5.9,1.4,'Controlled comparison','Vanilla BC  |  Domain randomization  |  DR + few-shot\nUse independent physical test episodes')
elbow(ax,[(11.6,3.2),(13.23,3.2),(13.23,2.18),(1.7,2.18),(1.7,2.1)])
arrow(ax,(3.0,1.4),(3.7,1.4))
arrow(ax,(6.3,1.4),(7.0,1.4))
save(fig,'sim_to_real_mechanism')

fig, ax = canvas('Time-aligned physical-to-simulation state synchronization',
                 'Measured states retain timestamps and sources; occluded object poses are propagated from a verified grasp.')
box(ax,.4,3.15,2.7,1.5,'Physical observations','Joint encoders and gripper\nRGB-D object poses')
box(ax,3.7,3.15,2.7,1.5,'Coordinate alignment','Calibrated camera extrinsics\nCommon robot-base frame')
box(ax,7.0,3.15,2.7,1.5,'Time alignment','Acquisition timestamps\nJoint-state interpolation')
box(ax,10.3,3.15,2.7,1.5,'Observation validation','Freshness and confidence\nReject stale object samples',GOLD)
for x in [3.1,6.4,9.7]: arrow(ax,(x,3.9),(x+.6,3.9))
box(ax,.4,.65,3.6,1.5,'Occlusion propagation','Force-confirmed grasp\nEnd-effector pose + grasp transform',GOLD)
box(ax,5.0,.65,3.6,1.5,'Synchronized scene','Measured joints and visible objects\nEstimated poses carry source labels',GREEN)
box(ax,9.5,.65,3.5,1.5,'Use of synchronized states','Visualization and replay\nSimulated / physical comparison')
elbow(ax,[(11.65,3.15),(13.23,3.15),(13.23,2.19),(6.8,2.19),(6.8,2.15)])
arrow(ax,(4.0,1.4),(5.0,1.4),'during occlusion')
arrow(ax,(8.6,1.4),(9.5,1.4))
save(fig,'state_synchronization_mechanism')

fig, ax = canvas('Failure-aware hierarchical state machine',
                 'Deterministic transition guards coordinate learned skills and classical planning routines.')
nodes=[(.4,'Approach'),(2.95,'Grasp'),(5.5,'Verify'),(8.05,'Transit'),(10.6,'Handover')]
for x,title in nodes: box(ax,x,3.45,2.15,1.1,title)
for i in range(4): arrow(ax,(nodes[i][0]+2.15,4.0),(nodes[i+1][0],4.0))
ax.text(6.55,4.85,'Advance only when the corresponding completion guard passes',
        ha='center',fontsize=10,color=INK)
box(ax,.4,.65,3.1,1.5,'Skill interface','Precondition / completion guard\nTimeout / failure code',GREEN)
box(ax,4.35,.65,3.6,1.5,'Recover and reposition','Stop motion; attempt safe recovery\nIncrement retry counter',GOLD)
box(ax,9.3,.65,3.5,1.5,'Safe stop','Retry or timeout limit reached\nOperator review',RED)
arrow(ax,(6.57,3.45),(6.15,2.15),'verification fails')
arrow(ax,(7.95,1.4),(9.3,1.4),'limit reached')
arrow(ax,(4.6,2.15),(4.0,3.45),'retry',bend=.2)
save(fig,'hsm_recovery_mechanism')
print(f'Generated 3 SVGs and 3 PNGs in {OUT}')
