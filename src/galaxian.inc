
* galaxian.inc

***    
*** BUILD OPTIONS
***

    * hardware options
    OPT_DISABLE_BG_LAYER=0
    OPT_DISABLE_SPRITES=0
   
	* cheats to test game
    * score is BCD format, only 6 digits
    OPT_START_SCORE=0x000000
	OPT_ALIENS_DONT_SHOOT=0	
	OPT_SMALL_SWARM=0
***
*** end of BUILD OPTIONS
***




* sound ordinals

    .equ  CREDIT_SND,         0x00
    .equ  SHOOT_SND,         0x01
    .equ  INTRO_SND,      0x02
    .equ  ALIEN_SHOT_SND,      0x03
    .equ  FLAGSHIP_SHOT_SND,      0x04
    .equ  PLAYER_SHOT_SND,      0x05
    .equ  ATTACK_END_SND,      0x06
    .equ  SWARM_1_SND,      0x07
    .equ  EXTRA_LIFE_SND,      0x08
    .equ  ATTACK_START_SND,      0x09
    .equ  EMPTY_SND,      0x0A


    
