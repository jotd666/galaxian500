import os,re,bitplanelib,ast,json
from PIL import Image,ImageOps

import gen_color_dict
import sprite_specific

import collections

this_dir = os.path.dirname(__file__)
src_dir = os.path.join(this_dir,"../../src/amiga")
dump_dir = os.path.join(this_dir,"dumps")

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

# convert fonts
fonts = Image.open(os.path.join(this_dir,"text.png"))

fonts_matrix = [list(range(0x11,0x11+15)),
list(range(0x11+15,0x11+27))+[5,5,5,5],  # yet unknown codes
list(range(0,10))+[6,6,6],
[7,7,7,7,7,7]  # namco unknown codes
]

character_codes = [None] * 256
character_codes[0x10] = bytes(8)  # blank
for j,lst in enumerate(fonts_matrix):
    y = j * 8
    for i,e in enumerate(lst):
        x = i * 8
        img = Image.new('RGB',(8,8))
        img.paste(fonts,(-x,-y))
        #img.save(os.path.join(dump_dir,f"{x}_{y}.png"))
        p = bitplanelib.palette_extract(img)
        character_codes[e] = bitplanelib.palette_image2raw(img,None,p,forced_nb_planes=1)

with open(os.path.join(src_dir,"graphics.68k"),"w") as f:
    f.write("\t.global\tcharacters\n")
    f.write("characters:\n")
    for i,c in enumerate(character_codes):
        if c is not None:
            f.write(f"\t.long\tchar_{i}\n")
        else:
            f.write("\t.long\t0\n")
    for i,c in enumerate(character_codes):
        if c is not None:
            f.write(f"char_{i}:")
            bitplanelib.dump_asm_bytes(c,f,mit_format=True)