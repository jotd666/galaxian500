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
brown = (222,71,0)
# white used for shots
white = (222,222,247)
# cyan for aliens & ship
cyan = (0,222, 247)
# for ship & flags
gray = (195,195,217)
# pink for score & explosions
pink = (195,0,217)
yellow = (255,255,0)
red = (255,0,0)
violet = (151,0,247)
pink = (222,0,247)
blue = (0,104,247)
light_blue =  (0, 151, 168)
deep_blue = (0,0,247)
# 7 base colors
base_palette = [black,
red,
light_blue,
deep_blue,
blue,    # blue
yellow,
violet
]

# 4 first colors are dynamic
# 4 last colors: same so all are bullet color
tile_palette = [black]*4+[white]*4
bob_palette = base_palette + [brown]  # all aliens are represented

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

with open(os.path.join(this_dir,"sprite_config.json")) as f:
    sprite_config = {int(k):v for k,v in json.load(f).items()}


sprites = collections.defaultdict(dict)

for k,data in sprite_config.items():
    sprdat = block_dict["sprite"]["data"][k]
    for m,clut_index in enumerate(data["cluts"]):
        spritepal = bg_cluts[clut_index]
        hw_sprite = data.get("hw_sprite")
        d = iter(sprdat)
        img = Image.new('RGB',(16,16))
        y_start = 8 if data["clip_right"] else 0
        for i in range(16):
            for j in range(16):
                v = next(d)
                if j >= y_start:
                    img.putpixel((j,i),spritepal[v])

        entry = dict()
        sprites[k][clut_index] = entry
        sprites[k]["name"] = data['name']

        outname = f"{k:02x}_{clut_index}_{data['name']}.png"
        if hw_sprite is None:
            left = bitplanelib.palette_image2raw(img,None,bob_palette)
            if data["mirror"]:
                right = bitplanelib.palette_image2raw(ImageOps.mirror(img),None,bob_palette)
        else:
            entry["palette"]=spritepal
            entry["hw_sprite"]=hw_sprite

            left = bitplanelib.palette_image2sprite(img,None,spritepal)
            if data["mirror"]:
                right = bitplanelib.palette_image2sprite(ImageOps.mirror(img),None,spritepal)

        entry.update({"left":left,"right":right})


##        scaled = ImageOps.scale(img,5,0)
##        scaled.save(os.path.join(dump_dir,outname))

with open(os.path.join(src_dir,"graphics.68k"),"w") as f:
    f.write("\t.global\tcharacters\n")
    f.write("\t.global\tsprites\n")
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
    f.write("sprites:\n")

    sprite_names = [None]*256
    for i in range(256):
        sprite = sprites.get(i)
        f.write("\t.long\t")
        if sprite:
            name = f"{sprite['name']}_{i:02x}"
            sprite_names[i] = name
            f.write(name)
        else:
            f.write("0")
        f.write("\n")

    for i in range(256):
        sprite = sprites.get(i)
        if sprite:
            name = sprite_names[i]
            f.write(f"{name}:\n")
            for j in range(8):
                slot = sprite.get(j)
                f.write("\t.long\t")
                if slot:
                    # clut is valid for this sprite
                    f.write(f"{name}_{j}")
                else:
                    f.write("0")
                f.write("\n")

    for i in range(256):
        sprite = sprites.get(i)
        if sprite:
            name = sprite_names[i]
            for j in range(8):
                slot = sprite.get(j)
                if slot:
                    # clut is valid for this sprite
                    f.write(f"{name}_{j}:\n\t.word\t")

                    hw_sprite = slot.get("hw_sprite")

                    if hw_sprite is None:
                        f.write("0   | BOB\n")
                        # just bob pointers
                        left_ptr = f"\t.long\t{name}_{j}_left\n"
                        f.write(left_ptr)
                        if "right" in slot:
                            f.write(f"\t.long\t{name}_{j}_right\n")
                        else:
                            f.write(left_ptr)
                    else:
                        f.write("1   | HW SPRITE\n")

    f.write("\t.datachip\n")

    for i in range(256):
        sprite = sprites.get(i)
        if sprite:
            name = sprite_names[i]
            for j in range(8):
                slot = sprite.get(j)
                if slot:
                    # clut is valid for this sprite
                    hw_sprite = slot.get("hw_sprite")

                    if hw_sprite is None:
                        # just bob data
                        f.write(f"{name}_{j}_left:")
                        bitplanelib.dump_asm_bytes(slot["left"],f,mit_format=True)
                        if "right" in slot:
                            f.write(f"{name}_{j}_right:")
                            bitplanelib.dump_asm_bytes(slot["right"],f,mit_format=True)


