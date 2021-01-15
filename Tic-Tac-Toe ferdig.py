import pygame as pg
import numpy as np

pg.init()

# Konstanter
skjermbredde = 600
skjermhøyde = 600
linjebredde = 11
brettrader = 3
brettkolonner = 3
sirkelradius = 60
sirkelbredde = 15
kryssbredde = 25
plass = 50 # ledig plass mellom linjer og kryss

BG_farge = (213, 100, 124) # Bakgrunnsfarge RGB kode
linjefarge = (156, 34, 93) # Linjefarge RGB kode
sirkelfarge = (239, 231, 200) # Sirkelfarge RGB kode
kryssfarge = (66, 66, 66) # Kryssfarge RGB kode

# Lager en skjerm
screen = pg.display.set_mode ((skjermbredde, skjermhøyde))

# Lager en tittel til skjermen
pg.display.set_caption ("Tic Tac Toe")

# Brett

board = np.zeros ((brettrader, brettkolonner))
# print (board)

def tegn_brettlinjer ():
    # 1. Horisontale linje
    pg.draw.line (screen, linjefarge, (0, 200), (600, 200), linjebredde)
    # 2. Horisontale linje
    pg.draw.line (screen, linjefarge, (0, 400), (600, 400), linjebredde)
    # 1. Vertikale linje
    pg.draw.line (screen, linjefarge, (200, 0), (200, 600), linjebredde)
    # 2. Vertikale linje
    pg.draw.line (screen, linjefarge, (400, 0), (400, 600), linjebredde)
    
def tegn_figur():
    for rad in range (brettrader):
        for kolonne in range (brettkolonner):
            if board [rad][kolonne] == 1:
                pg.draw.circle (screen, sirkelfarge, (int (kolonne * 200 + 100), int (rad * 200 + 100)), sirkelradius, sirkelbredde)
            elif board [rad][kolonne] == 2:
                pg.draw.line( screen, kryssfarge, (kolonne * 200 + plass, rad * 200 + 200 - plass), (kolonne * 200 + 200 - plass, rad * 200 + plass), kryssbredde )	
                pg.draw.line( screen, kryssfarge, (kolonne * 200 + plass, rad * 200 + plass), (kolonne * 200 + 200 - plass, rad * 200 + 200 - plass), kryssbredde )
                
    
def marker_rute (rad, kolonne, spiller):
    board [rad][kolonne] = spiller

def ledig_rute (rad, kolonne):
    if board[rad][kolonne] == 0:
        return True
    else:
        return False

def fullt_brett ():
    for rad in range (brettrader):
        for kolonne in range (brettkolonner):
            if board[rad][kolonne] == 0:
                return False
    return True

def vertikal_vinner_linje (kolonne, spiller):
    posX = kolonne * 200 + 100
    
    if spiller == 1:
        farge = sirkelfarge
    elif spiller == 2:
        farge = kryssfarge
        
    pg.draw.line (screen, farge, (posX, 15), (posX, skjermhøyde - 15), 20)

def horisontal_vinner_linje (rad, spiller):
    posY = rad * 200 + 100
    
    if spiller == 1:
        farge = sirkelfarge
    elif spiller == 2:
        farge = kryssfarge
        
    pg.draw.line (screen, farge, (15, posY), (skjermbredde - 15, posY), 20)
    
def diagonal1_vinner_linje (spiller):
    if spiller == 1:
        farge = sirkelfarge
    elif spiller == 2:
        farge = kryssfarge
    
    pg.draw.line (screen, farge, (15, skjermhøyde - 15), (skjermbredde - 15, 15), 20)
    
def diagonal2_vinner_linje (spiller):
    if spiller == 1:
        farge = sirkelfarge
    elif spiller == 2:
        farge = kryssfarge
    
    pg.draw.line (screen, farge, (15, 15), (skjermbredde - 15, skjermhøyde - 15), 20)

def sjekk_vinn (spiller):
    # Sjekk for vertikal vinn
    for kolonne in range (brettkolonner):
        if board [0][kolonne] == spiller and board [1][kolonne] == spiller and board [2][kolonne] == spiller:
            vertikal_vinner_linje(kolonne, spiller)
            return True
    # Sjekk for horisontal vinn
    for rad in range (brettrader):
        if board [rad][0] == spiller and board [rad][1] == spiller and board [rad][2] == spiller:
            horisontal_vinner_linje(rad, spiller)
            return True

    # Sjekk for 1. diagonal vinn
    if board [2][0] == spiller and board [1][1] == spiller and board [0][2] == spiller:
        diagonal1_vinner_linje(spiller)
        return True
    
    # Sjekk for 2. diagonal vinn
    if board [0][0] == spiller and board [1][1] == spiller and board [2][2] == spiller:
        diagonal2_vinner_linje(spiller)
        return True

    # Uavgjort
    return False

def restart ():
    # Lager startskjerm igjen
     screen.fill (BG_farge)
     tegn_brettlinjer()
     # Gjør at spiller 1 starter
     spiller = 1
     # Gjør alle rutene om til 0 (tomme)
     for rad in range (brettrader):
         for kolonne in range (brettkolonner):
             board [rad][kolonne] = 0


# Fyller skjermen med en farge
screen.fill (BG_farge)
# Tegner linjene på brettet
tegn_brettlinjer()
# Setter "O" som første spiller
spiller = 1

run = True
game_over = False

while run:
    for event in pg.event.get():
        
        if event.type == pg.QUIT:
            run = False
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                restart()
                game_over = False
            
        if event.type == pg.MOUSEBUTTONDOWN and not game_over:
            
            musX = event.pos [0] # Henter x-posisjon til mus ved klikk
            musY = event.pos [1] # Henter y-posisjon til mus ved klikk
            klikket_kolonne = int(musX // 200)
            klikket_rad = int (musY // 200)
            
            if ledig_rute (klikket_rad, klikket_kolonne):
                if spiller == 1:
                    marker_rute(klikket_rad, klikket_kolonne, spiller)
                    if sjekk_vinn(spiller):
                        game_over = True
                    spiller = 2
                    
                elif spiller == 2:
                    marker_rute(klikket_rad, klikket_kolonne, spiller)
                    if sjekk_vinn(spiller):
                        game_over = True
                    spiller = 1
                tegn_figur()

    pg.display.update()
    
pg.quit()