
* galaxian.inc

***    
*** BUILD OPTIONS
***

    * hardware options
    OPT_DISABLE_BG_LAYER=0
    OPT_DISABLE_SPRITES=0
    OPT_DISABLE_DISPLAY_MASKS=0
   
    * score is BCD format
    OPT_START_SCORE=0x0000000


***
*** end of BUILD OPTIONS
***

* offsets into object table
    .equ  _STATE,     0
    .equ  _ATTR,      1
    .equ  _EXTRA,     4
    .equ  _X,         8
    .equ  _dX,        10
    .equ  _ddX,       12
    .equ  _Y,         14
    .equ  _dY,        16
    .equ  _ddY,       18
    .equ  _CODE,      20
    .equ  _COLOUR,    21
    .equ  _PTS,       22
    .equ  _TIMER,     24
    .equ  _TIMER1,    25
      .equ  _NVEC,    25
    .equ  _TIMER2,    26
      .equ  _VECLEN,  26
    .equ  _FFREQ,     28
    .equ  _TYPE,      30

    .equ  _OBJSIZE,   32



* sound ordinals

    .equ  MAIN_THEME_SND,         0x01
    .equ  HIGHEST_SCORE_SND,      0x02
    .equ  HIGH_SCORE_SND,         0x03
    .equ  EXTRA_SOLVALOU_SND,     0x04
    .equ  FLYING_ENEMY_HIT_SND,   0x05
    .equ  GARU_ZAKATO_SND,        0x06
    .equ  ANDOR_GENESIS_SND,      0x07
    .equ  SHEONITE_SND,           0x08
    .equ  TELEPORT_SND,           0x09
    .equ  BACURA_HIT_SND,         0x0a
    .equ  SHOT_SND,               0x0b
    .equ  BOMB_SND,               0x0c
    .equ  BONUS_FLAG_SND,         0x0d
    .equ  SOLVALOU_SND,           0x0e
    * 60XX (noise chip?)
    .equ  COIN_SND,               0x10
    .equ  GROUND_EXPLOSION_SND,   0x11
    .equ  SOLVALOU_EXPLOSION_SND, 0x12
    
