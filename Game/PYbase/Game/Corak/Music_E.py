import pygame as pg
from Game.Corak.dicio import *

class sound_E():
    def __init__(s, type, vol):
        type[1] = "../Sound/" + type[1] + ".wav"

        if type[0] == 0:
            music_l.append(s)
            s.m = pg.mixer.Sound(type[1])
        elif type[0] == 1:
            effect_l.append(s)
            s.m = pg.mixer.Sound(type[1])

        s.vol = vol
        s.main = 7
        s.vol_update()

    def set_vol(s, vol):
        s.vol = vol
        s.vol_update()

    """returns"""
    def chg_vol(s, vol):
        temp=s.vol+vol
        if temp>1:
            s.vol=1
            return -1
        elif temp<0:
            s.vol=0
            return -1
        else:
            s.vol = temp
            s.vol_update()
            return 0

    def vol_update(s):
        s.m.set_volume((s.vol / 10) * s.main)

"""effects"""
def chg_main_e(chg):
    if -1 < effect_l[0].main+chg < 11:
        for sound in effect_l:
            sound.main+=chg
            sound.vol_update()

"""music"""
def chg_main_m(chg):
    if -1 < music_l[0].main+chg < 11:
        for sound in music_l:
            sound.main+=chg
            sound.vol_update()

def chg_main_a(main):
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

global mixer
mixer = []
music_l=[]
effect_l=[]

pg.mixer.pre_init(44200, 16, 2)
pg.mixer.init()

vol = []
trigger = []
Mvol = 10
Evol = 10

#

loop = sound_E([0, "kpLoop"], 0)
Piano = sound_E([0, "pianoloop"], 0)
mLoop = sound_E([0, "mLoop"], 0)

#menu
select_e = sound_E([1, "select"], 0.9)
click_e =sound_E([1, "click"], 0.8)
click2_e = sound_E([1, "click2"], 0.7)
