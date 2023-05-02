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
pink = (195,0,217)
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

block_dict = {}

# hackish convert of c gfx table to dict of lists
# (Thanks to Mark Mc Dougall for providing the ripped gfx as C tables)
with open(os.path.join(this_dir,"..","galaxian_gfx.c")) as f:
    block = []
    block_name = ""
    start_block = False

    for line in f:
        if "uint8" in line:
            # start group
            start_block = True
            if block:
                txt = "".join(block).strip().strip(";")
                block_dict[block_name] = {"size":size,"data":ast.literal_eval(txt)}
                block = []
            block_name = line.split()[1].split("[")[0]
            size = int(line.split("[")[2].split("]")[0])
        elif start_block:
            line = re.sub("//.*","",line)
            line = line.replace("{","[").replace("}","]")
            block.append(line)

    if block:
        txt = "".join(block).strip().strip(";")
        block_dict[block_name] = {"size":size,"data":ast.literal_eval(txt)}

bg_cluts = []
cuclut = []
for clut in block_dict["clut"]["data"]:
    cuclut.append(clut)
    if len(cuclut)==4:
        bg_cluts.append(cuclut)
        cuclut = []


palette = tile_palette + bob_palette + sprite_palette

with open(os.path.join(src_dir,"palette.68k"),"w") as f:
    bitplanelib.palette_dump(palette,f,pformat=bitplanelib.PALETTE_FORMAT_ASMGNU)


character_codes = list()

extraction_palette = bg_cluts[2]  # use a 4-color palette with 4 different colors!

for k,chardat in enumerate(block_dict["tile"]["data"]):
    img = Image.new('RGB',(8,8))
    d = iter(chardat)
    for i in range(8):
        for j in range(8):
            v = next(d)
            img.putpixel((j,i),extraction_palette[v])
    character_codes.append(bitplanelib.palette_image2raw(img,None,extraction_palette))
    #scaled = ImageOps.scale(img,5,0)
    #scaled.save(os.path.join(dump_dir,f"char_{k:02x}.png"))

for k,sprdat in enumerate(block_dict["sprite"]["data"]):
    for m,spritepal in enumerate(bg_cluts):
        d = iter(sprdat)
        img = Image.new('RGB',(16,16))
        for i in range(16):
            for j in range(16):
                v = next(d)
                img.putpixel((j,i),spritepal[v])

        scaled = ImageOps.scale(img,5,0)
        scaled.save(os.path.join(dump_dir,f"sprite_{k:02x}_{m}.png"))

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