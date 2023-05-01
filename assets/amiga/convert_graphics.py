import os,re,bitplanelib,ast,json
from PIL import Image,ImageOps


import collections

this_dir = os.path.dirname(__file__)
src_dir = os.path.join(this_dir,"../../src/amiga")
ripped_tiles_dir = os.path.join(this_dir,"../tiles")
dump_dir = os.path.join(this_dir,"dumps")

def dump_asm_bytes(*args,**kwargs):
    bitplanelib.dump_asm_bytes(*args,**kwargs,mit_format=True)

black = (0,0,0)
# brown only used for flagship, in sprite palette
brown = (0xC3,0x3E,0)
# white used for shots
white = (0xC3,0xC3,0xD9)
# cyan for aliens & ship
cyan = (0,195,217)
# for ship & flags
gray = (195,195,217)
# pink for score & explosions
pink = (195,0,217)
yellow = (224,224,0)
red = (224,0,0)
violet = (133,0,217)
blue = (0,91,217)

deep_blue = (0,0,0xD9)
# 7 base colors
base_palette = [black,
red,
cyan,
deep_blue,
blue,    # blue
yellow,
violet
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

bg_cluts = [(black,)+x for x in (
(black,black,white),
(brown,deep_blue,yellow),
(blue,red,yellow),
(deep_blue,violet,red),
(blue,(0,133, 148),red),
(black,black,red),
(white,red,cyan),
(yellow,red,violet))]

palette = tile_palette + bob_palette + sprite_palette

with open(os.path.join(src_dir,"palette.68k"),"w") as f:
    bitplanelib.palette_dump(palette,f,pformat=bitplanelib.PALETTE_FORMAT_ASMGNU)

# open tiles
mame_tiles = Image.open(os.path.join(ripped_tiles_dir,"gfxset0 tiles 24x8 colors 8 set 3_0000.png"))
# for some reason, ripped tile height is x3, reduce size vertically

# convert fonts
fonts = Image.open(os.path.join(this_dir,"text.png"))

# missing: colon (0xD3), dash (0x91)
fonts_matrix = [list(range(0x11,0x11+15)),
list(range(0x11+15,0x11+26))+[0xFF,0xFF,0xD1-0x30,0xD2-0x30,0xD3-0x30],  # pts
list(range(0,10))+[0xFF,0x2B,0xFF],
[x-0x30 for x in [0xCA,0xCB,0xCC,0xCD,0xCE,0xCF,0x9E,0x9F]]  # namco codes
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

# duplicate digits in 0x90 area
for i in range(0,10):
    character_codes[0x90+i] = character_codes[i]

with open(os.path.join(src_dir,"graphics.68k"),"w") as f:
    f.write("\t.global\tcharacters\n")
    f.write("\t.global\tbg_cluts\n")
    f.write("bg_cluts:")
    amiga_cols = [bitplanelib.to_rgb4_color(x) for clut in bg_cluts for x in clut]
    bitplanelib.dump_asm_bytes(amiga_cols,f,mit_format=True,size=2)

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