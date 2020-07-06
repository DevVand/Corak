import pygame as pg
from Game.Corak.dicio import *

class sound_E():

    def __init__(s, type, vol):
        s.type = type[0]
        type[1] = "../Sound/" + type[1] + ".wav"

        if type[0] == 0:
            pg.mixer.Sound(type[1])

        s.vol = vol
        s.main = 10

    def set_vol(s, vol):
        s.vol = vol
        s.vol_update()

    def chg_vol(s, vol):
        s.vol += vol
        s.vol_update()

    def vol_update(s):
        s.set_volume((s.vol / 10) * s.main)


def chg_main_e(main):
    main += main
    for sound in sound_E:
        if sound.type == 2: sound.vol_update(sound.vol)

def chg_main_m(main):
    main += main
    for sound in sound_E:
        if sound.type <= 1: sound.vol_update(sound.vol)

def chg_main(main):
    main += main
    for sound in sound_E: sound.vol_update(sound.vol)




'audio setting   \' '
#mixer = pg.mixer.Sound("../Sound/s_4.wav")

mixerOn = [True, # 0 strt
           True, # 1 music
           True, # 2 menu
          [False, False],
          [False, True, 0],
          [False, False, False, False]
          ]
pg.mixer.pre_init(44200, 16, 2)
pg.mixer.init()

vol = []
trigger = []
Mvol = 10
Evol = 10

#
loop = sound_E([0, "kpLoop"], 0)
trigger.append([True, False])

Piano = sound_E([0, "pianoloop"], 0)
trigger.append([False, False])

mLoop = sound_E([0, "mLoop"], 0)
trigger.append([False, False])

#menu
menuTrigger = []
select = pg.mixer.Sound("../Sound/select.wav")
select.set_volume(0.9)
menuTrigger.append([False, False])

clicks = pg.mixer.Sound("../Sound/click.wav")
clicks.set_volume(0.8)
menuTrigger.append([False, False])

click2 = pg.mixer.Sound("../Sound/click2.wav")
click2.set_volume(0.7)
menuTrigger.append([False, False])

pg.mixer.music.set_volume(0)

Piano.play(-1)
mLoop.play(-1)
pg.mixer.music.play(-1)

menuCount = 0