"""
This file is the main file of My-PyChess application.
Run this file to launch the program.

In this file, we handle the main menu which gets displayed at runtime.
"""
import sys  
import pygame

import chess
import menus
from tools.loader import MAIN
from tools import sound

sys.stdout.flush()

pygame.init()
clock = pygame.time.Clock()

if pygame.version.vernum[0] >= 2:
    win = pygame.display.set_mode((500, 500), pygame.SCALED)
else:
    win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("My-PyChess")
pygame.display.set_icon(MAIN.ICON)

sngl = (260, 140, 220, 40)
mult = (260, 200, 200, 40)
onln = (260, 260, 120, 40)
load = (260, 320, 200, 40)
pref = (0, 450, 210, 40)
abt = (390, 450, 110, 40)
hwto = (410, 410, 90, 30)
stok = (0, 410, 240, 30)

def showMain(prefs):
    global cnt, img

    win.blit(MAIN.BG[img], (0, 0))

    if prefs["slideshow"]:
        cnt += 1
        if cnt >= 150:
            s = pygame.Surface((500, 500))
            s.set_alpha((cnt - 150) * 4)
            s.fill((0, 0, 0))
            win.blit(s, (0, 0))

        if cnt == 210:
            cnt = 0
            img = 0 if img == 3 else img + 1
    else:
        cnt = -150
        img = 0

    win.blit(MAIN.HEADING, (80, 20))
    pygame.draw.line(win, (255, 255, 255), (80, 100), (130, 100), 4)
    pygame.draw.line(win, (255, 255, 255), (165, 100), (340, 100), 4)
    win.blit(MAIN.VERSION, (345, 95))

    win.blit(MAIN.SINGLE, sngl[:2])
    win.blit(MAIN.MULTI, mult[:2])
    win.blit(MAIN.ONLINE, onln[:2])

# Initialize a few more variables
cnt = 0
img = 0
run = True

prefs = menus.pref.load()

music = sound.Music()
music.play(prefs)
while run:
    clock.tick(30)
    showMain(prefs)

    x, y = pygame.mouse.get_pos()

    if sngl[0] < x < sum(sngl[::2]) and sngl[1] < y < sum(sngl[1::2]):
        win.blit(MAIN.SINGLE_H, sngl[:2])

    if mult[0] < x < sum(mult[::2]) and mult[1] < y < sum(mult[1::2]):
        win.blit(MAIN.MULTI_H, mult[:2])

    if onln[0] < x < sum(onln[::2]) and onln[1] < y < sum(onln[1::2]):
        win.blit(MAIN.ONLINE_H, onln[:2])


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User has clicked somewhere, determine which button and
            # call a function to handle the game into a different window.
            x, y = event.pos

            if sngl[0] < x < sum(sngl[::2]) and sngl[1] < y < sum(sngl[1::2]):
                sound.play_click(prefs)
                ret = menus.splayermenu(win)
                if ret == 0:
                    run = False
                elif ret != 1:
                    if ret[0]:
                        run = chess.mysingleplayer(win, ret[1], prefs)
                    else:
                        run = chess.singleplayer(win, ret[1], ret[2], prefs)

            elif mult[0] < x < sum(mult[::2]) and mult[1] < y < sum(mult[1::2]):
                sound.play_click(prefs)
                ret = menus.timermenu(win, prefs)
                if ret == 0:
                    run = False
                elif ret != 1:
                    run = chess.multiplayer(win, ret[0], ret[1], prefs)

            elif onln[0] < x < sum(onln[::2]) and onln[1] < y < sum(onln[1::2]):
                sound.play_click(prefs)
                ret = menus.onlinemenu(win)
                if ret == 0:
                    run = False
                elif ret != 1:
                    run = chess.online(win, ret[0], ret[1], prefs, ret[1])

            elif load[0] < x < sum(load[::2]) and load[1] < y < sum(load[1::2]):
                sound.play_click(prefs)
                ret = menus.loadgamemenu(win)
                if ret == 0:
                    run = False

                elif ret != 1:
                    if ret[0] == "multi":
                        run = chess.multiplayer(win, *ret[1:3], prefs, ret[3])
                    elif ret[0] == "single":
                        run = chess.singleplayer(win, *ret[1:3], prefs, ret[3])
                    elif ret[0] == "mysingle":
                        run = chess.mysingleplayer(win, ret[1], prefs, ret[2])

            elif pref[0] < x < sum(pref[::2]) and pref[1] < y < sum(pref[1::2]):
                sound.play_click(prefs)
                run = menus.prefmenu(win)
                
                prefs = menus.pref.load()
                if music.is_playing():
                    if not prefs["sounds"]:
                        music.stop()
                else:
                    music.play(prefs)
                    
            elif hwto[0] < x < sum(hwto[::2]) and hwto[1] < y < sum(hwto[1::2]):
                sound.play_click(prefs)
                run = menus.howtomenu(win)

            elif abt[0] < x < sum(abt[::2]) and abt[1] < y < sum(abt[1::2]):
                sound.play_click(prefs)
                run = menus.aboutmenu(win)

            elif stok[0] < x < sum(stok[::2]) and stok[1] < y < sum(stok[1::2]):
                sound.play_click(prefs)
                run = menus.sfmenu(win)

    pygame.display.flip()

music.stop()
pygame.quit()
