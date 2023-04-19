import os,re,bitplanelib,ast,json
from PIL import Image,ImageOps

import gen_color_dict
import sprite_specific

import collections

this_dir = os.path.dirname(__file__)
src_dir = os.path.join(this_dir,"../../src/amiga")

def dump_asm_bytes(*args,**kwargs):
    bitplanelib.dump_asm_bytes(*args,**kwargs,mit_format=True)

black = (0,0,0)
# brown only used for flagship, in sprite palette
brown = (195,62,0)
# white used for shots
white = (217,217,217)
# cyan for aliens & ship
cyan = (0,195,217)
# for ship & flags
gray = (195,195,217)
# pink for score & explosions
pink = (195,0,217)
yellow = (224,224,0)
red = (224,0,0)

deep_blue = (0,0,217)
# 7 base colors
base_palette = [black,
red,
cyan,
deep_blue,
(0,91,217),    # blue
yellow,
(133,0,217),   # violet
]

tile_palette = base_palette + [brown]      # last col for flagship as tile
bob_palette = base_palette + [white]   # last col for player shots

ship_sprite_palette = [black,red,cyan,gray]   # could also be used for level flags
flagship_sprite_palette = [black,brown,yellow,deep_blue]
sprite_palette = (ship_sprite_palette +  # 0: ship
flagship_sprite_palette +   # 2-3: 2 flagships
flagship_sprite_palette +   # 4-5: 2 flagships
[black,pink,pink,pink]    # 6: score, 7: starfield
)

palette = tile_palette + bob_palette + sprite_palette

with open(os.path.join(src_dir,"palette.68k"),"w") as f:
    #f.write("palette:\n")
    bitplanelib.palette_dump(palette,f,pformat=bitplanelib.PALETTE_FORMAT_ASMGNU)

