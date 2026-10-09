"""Replace only raster inset regions, leaving the reference layout unchanged."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import numpy as np

root = Path(__file__).parent / 'images'
target = root / 'mechanisms/hsm_recovery_reference_style_draft.png'
backup = target.with_name('hsm_recovery_reference_style_before_panda.png')
if not backup.exists():
    backup.write_bytes(target.read_bytes())
base = Image.open(backup).convert('RGB')
out = base.copy()
photos = Image.open(root / 'liquid_operation.png.png').convert('RGB')
w,h = photos.size

def frame(i):
    r,c = divmod(i,3)
    return photos.crop((c*w//3,r*h//2,(c+1)*w//3,(r+1)*h//2))

changed = Image.new('L',base.size,0)
mark = ImageDraw.Draw(changed)

def insert(rect, photo, focus=(.5,.5)):
    x0,y0,x1,y1=rect
    inset=ImageOps.fit(photo,(x1-x0,y1-y0),method=Image.Resampling.LANCZOS,centering=focus)
    out.paste(inset,(x0,y0))
    mark.rectangle((x0,y0,x1-1,y1-1),fill=255)

# Top stages: original Panda photo crops, no pose synthesis.
for rect,i in [((38,70,361,236),0),((466,70,695,237),3),
               ((806,70,1032,237),3),((1136,70,1396,237),4),
               ((1502,69,1740,236),5)]:
    insert(rect,frame(i))

# Skill library illustrations and image input thumbnails.
insert((49,412,222,509),frame(0))
insert((246,443,310,494),frame(3))
insert((48,561,223,646),frame(4))
insert((398,561,511,646),frame(4))
insert((50,696,218,781),frame(1))

# The actual installed gripper, not a generic generated end effector.
gripper=frame(0).crop((78,122,201,274))
insert((409,414,494,502),gripper)
insert((686,568,762,640),gripper)

# Recovery and safe-stop retain their module titles, frame, and operator icon.
insert((1122,418,1318,659),frame(5),focus=(.33,.5))
insert((1441,689,1633,860),frame(5),focus=(.33,.5))

# Restore original motion arrows on top of the replacement photographs.
for rect in [(1220,139,1287,165),(1208,486,1250,567)]:
    tile=base.crop(rect)
    p=np.asarray(tile)
    # Preserve dark navy/black arrow ink, not peach background.
    mask=((p[:,:,0]<90)&(p[:,:,1]<100)&(p[:,:,2]<130)).astype('uint8')*255
    out.paste(tile,rect[:2],Image.fromarray(mask))

# Prove no pixel outside explicitly replaced inset rectangles was modified.
a,b=np.asarray(base),np.asarray(out)
outside=np.asarray(changed)==0
assert np.array_equal(a[outside],b[outside]), 'Unexpected layout modification'
out.save(target)
out.save(target.with_name('hsm_recovery_reference_style_panda_photos.png'))
print('Updated the requested original diagram; unchanged layout pixels verified.')
print('Backup:',backup)
