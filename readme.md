# Galaxian (68K)

This is a transcode from the original arcade game Z80 to 68K assembly.


### PROGRESS:

#### Transcode

-

#### Amiga

-

#### Neo Geo

- tested & playable on MVS, NGCD
- TBD: stars

### FEATURES:

### CREDITS:

- Jean-Francois Fabre (aka jotd): Amiga code and assets
- Mark McDougall (aka tcdev): Neo Geo code and assets
- DanyPPC: Amiga icon
- phx: ptplayer sound/music replay Amiga code
- Namco: original game :)

### CONTROLS (Amiga: 2-button joystick required):

- red/fire: fire/start game (from menu)
- blue/2nd button: insert coin (from menu)
- green/5 key: insert coin
- yellow/1 key: start game
- play/P key: pause

## REBUILDING FROM SOURCES:

### AMIGA:

#### Prerequesites:

- Bebbo's amiga gcc compiler
- Windows
- python
- sox
- "bitplanelib.py" (asset conversion tool needs it) at https://github.com/jotd666/amiga68ktools.git

#### Build process:

- install above tools & adjust python paths
- make -f makefile.am

#### When changing asset-related data (since dependencies aren't good):

- To update the "graphics.68k" & "palette*.68k" files from "assets/amiga" subdir, 
  just run the "convert_graphics.py" python script, 
- To update sounds, use "convert_sounds.py"
  python script (audio) to create sound*.68k files.

### NEO GEO:

#### Prerequesites:

- Windows
- NeoDev kit (Fabrice Martinez, Jeff Kurtz, et al)  
  https://wiki.neogeodev.org/index.php?title=Development_tools

#### Build process:

- install NeoDev and set path accordingly
- clone repository
- make -f makefile.ng OUTPUT={cart|cd}
  - (OUTPUT defaults to cart)
  
#### Install process (MAME):

- make -f makefile.ng OUTPUT={cart|cd} MAMEDIR={mamedir} install
  - (mamedir defaults to '.')
- paste xevious.xml into MAME's hash/neogeo.xml file

#### To run in MAME:

- cart : 'mame neogeo xevious'
- cd : 'mame neocdz -cdrom roms/neocdz/xevious.iso'
  
