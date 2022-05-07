import time

import pygame
import sys
import copy
import math


ADANCIME_MAX = 3

NEGRU = (0, 0, 0)
ROSU = (255, 0, 0)
VERDE = (0, 255, 0)
ALB = (255, 255, 255)

LINE_WIDTH = 1

# dimensiunea ferestrei in pixeli
L = 75
CELL_SIZE = (L, L)
DISPLAY_SIZE = (L*5, L*10)

# def elem_identice(lista):
#     if(all(elem == lista[0] for elem in lista[1:])):
#         return lista[0] if lista[0] != Joc.GOL else False
#     return False


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_LINII = 10
    NR_COLOANE = 5
    JMIN = None
    JMAX = None
    GOL = '#'
    INACCESIBIL = "X"
    WHITE = "W"
    BLACK = "B"

    @classmethod
    def initializeaza(cls, display, NR_LINII=NR_LINII, NR_COLOANE=NR_COLOANE, dim_celula=L):
        cls.display = display
        cls.dim_celula = dim_celula
        cls.white_circle_iamge = pygame.image.load('white_circle.png')
        cls.white_circle_iamge = pygame.transform.scale(cls.white_circle_iamge, (dim_celula, math.floor(
            dim_celula*cls.white_circle_iamge.get_height()/cls.white_circle_iamge.get_width())))
        cls.black_circle_image = pygame.image.load('black_circle.png')
        cls.black_circle_image = pygame.transform.scale(cls.black_circle_image, (dim_celula, math.floor(
            dim_celula*cls.black_circle_image.get_height()/cls.black_circle_image.get_width())))
        cls.celuleGrid = []  # este lista cu patratelele din grid
        for linie in range(NR_LINII):
            cls.celuleGrid.append([])
            for coloana in range(NR_COLOANE):
                patrat = pygame.Rect(coloana*(dim_celula),
                                     linie*(dim_celula), dim_celula, dim_celula)
                cls.celuleGrid[linie].append(patrat)

    def deseneaza_linii_grid(self):
        # desenez liniile tablei
        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[0][0].center,
                         self.__class__.celuleGrid[2][2].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[0][0].center,
                         self.__class__.celuleGrid[0][4].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[1][1].center,
                         self.__class__.celuleGrid[1][3].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[0][1].center,
                         self.__class__.celuleGrid[1][1].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[0][2].center,
                         self.__class__.celuleGrid[9][2].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[0][3].center,
                         self.__class__.celuleGrid[1][3].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[0][4].center,
                         self.__class__.celuleGrid[2][2].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[2][0].center,
                         self.__class__.celuleGrid[2][4].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[3][0].center,
                         self.__class__.celuleGrid[3][4].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[4][0].center,
                         self.__class__.celuleGrid[4][4].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[5][0].center,
                         self.__class__.celuleGrid[5][4].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[6][0].center,
                         self.__class__.celuleGrid[6][4].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[7][0].center,
                         self.__class__.celuleGrid[7][4].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[2][0].center,
                         self.__class__.celuleGrid[7][0].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[2][1].center,
                         self.__class__.celuleGrid[7][1].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[2][3].center,
                         self.__class__.celuleGrid[7][3].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[2][4].center,
                         self.__class__.celuleGrid[7][4].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[7][2].center,
                         self.__class__.celuleGrid[9][0].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[7][2].center,
                         self.__class__.celuleGrid[9][4].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[8][1].center,
                         self.__class__.celuleGrid[8][3].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[9][0].center,
                         self.__class__.celuleGrid[9][4].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[8][1].center,
                         self.__class__.celuleGrid[9][1].center,
                         width=LINE_WIDTH)

        pygame.draw.line(self.__class__.display, NEGRU,
                         self.__class__.celuleGrid[8][3].center,
                         self.__class__.celuleGrid[9][3].center,
                         width=LINE_WIDTH)

        pygame.display.update()

    # tabla de exemplu este ["#","x","#","0",......]
    def deseneaza_grid(self, marcaj=None, posibile_pozitii=[]):

        for linie in range(Joc.NR_LINII):
            for coloana in range(Joc.NR_COLOANE):
                if marcaj == (linie, coloana):
                    # daca am o patratica selectata, o desenez cu rosu
                    culoare = ROSU
                elif (linie, coloana) in posibile_pozitii:
                    culoare = VERDE
                else:
                    # altfel o desenez cu alb
                    culoare = ALB
                # alb = (255,255,255)
                pygame.draw.rect(self.__class__.display, culoare,
                                 self.__class__.celuleGrid[linie][coloana])

        self.deseneaza_linii_grid()

        for linie in range(Joc.NR_LINII):
            for coloana in range(Joc.NR_COLOANE):
                if self.matr[linie][coloana] == self.__class__.WHITE:
                    self.__class__.display.blit(self.__class__.white_circle_iamge, (coloana*(self.__class__.dim_celula), linie*(
                        self.__class__.dim_celula) + (self.__class__.dim_celula-self.__class__.white_circle_iamge.get_height())//2))
                elif self.matr[linie][coloana] == self.__class__.BLACK:
                    self.__class__.display.blit(self.__class__.black_circle_image, (coloana*(self.__class__.dim_celula), linie*(
                        self.__class__.dim_celula)+(self.__class__.dim_celula-self.__class__.black_circle_image.get_height())//2))
        # pygame.display.flip() # !!! obligatoriu pentru a actualiza interfata (desenul)

        pygame.display.update()

    @classmethod
    def matrice_initiala(cls):
        matr = []
        for i in range(4):
            matr.append([cls.BLACK] *
                                cls.NR_COLOANE)
        for i in range(cls.NR_LINII-8):
            matr.append([cls.GOL] *
                                cls.NR_COLOANE)
        for i in range(4):
            matr.append([cls.WHITE] *
                                cls.NR_COLOANE)

        matr[1][0] = cls.INACCESIBIL
        matr[1][4] = cls.INACCESIBIL

        matr[8][0] = cls.INACCESIBIL
        matr[8][4] = cls.INACCESIBIL

        matr[3][0] = cls.GOL
        matr[3][4] = cls.GOL

        matr[6][0] = cls.GOL
        matr[6][4] = cls.GOL

        return matr
    
    def __init__(self, tabla=None):
        if tabla:
            self.matr = tabla
        else:
            self.matr = self.__class__.matrice_initiala()

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    @classmethod
    def directii(cls, x, y):
        # directiile in care se poate deplasa de la coordonatele (x, y)
        sus = (-1, 0)
        dreapta = (0, 1)
        jos = (1, 0)
        stanga = (0, -1)
        directii_normale = [sus, jos, stanga, dreapta]

        if (x, y) in [(0, 0), (1, 1)]:
            return [(1, 1), (-1, -1), sus, dreapta]

        if (x, y) == (2, 2):
            return [(-1, -1), (-1, 1)] + directii_normale

        if (x, y) in [(0, 4), (1, 3)]:
            return [(-1, 1), (1, -1), sus, stanga]

        if (x, y) == (7, 2):
            return [(1, 1), (1, -1)] + directii_normale

        if (x, y) in [(8, 1), (9, 0)]:
            return [(1, -1), (-1, 1), dreapta, jos]

        if (x, y) in [(8, 3), (9, 4)]:
            return [(1, 1), (-1, -1), stanga, jos]

        return directii_normale

    def final(self, jucator):
        nr_piese_JMAX = 0
        nr_piese_JMIN = 0
        castiga_alb = True
        castiga_negru = True

        for i in range(2):
            for j in range(self.NR_COLOANE):
                if self.matr[i][j] != self.WHITE and self.matr[i][j] != self.INACCESIBIL:
                    castiga_alb = False
                    break
        if self.matr[2][2] != self.WHITE and self.matr[2][2] != self.INACCESIBIL:
            castiga_alb = False
        if castiga_alb:
            print("Alb a cucerit triunghiul negru")
            return self.WHITE

        for i in range(self.NR_LINII-2, self.NR_LINII):
            for j in range(self.NR_COLOANE):
                if self.matr[i][j] != self.BLACK and self.matr[i][j] != self.INACCESIBIL:
                    castiga_negru = False
                    break
        if self.matr[7][2] != self.BLACK and self.matr[7][2] != self.INACCESIBIL:
            castiga_negru = False
        if castiga_negru:
            print("Negru a cucerit triunghiul alb")
            return self.BLACK

        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE):
                if self.matr[i][j] == self.JMAX:
                    nr_piese_JMAX += 1
                if self.matr[i][j] == self.JMIN:
                    nr_piese_JMIN += 1
        if nr_piese_JMAX == 0:
            print("Calculatorul nu mai are piese")
            return self.JMIN
        if nr_piese_JMIN == 0:
            print("Jucatorul nu mai are piese")
            return self.JMAX

        mutari = self.mutari(jucator)
        if len(mutari) == 0:
            print(jucator + " nu mai are mutari")
            return self.jucator_opus(jucator)

        return False

    def pozitii_in_care_poate_muta(self, x, y):
        jucator = self.matr[x][y]
        inamic = self.jucator_opus(jucator)
        pozitii = []

        are_capturi, mutari_cu_capturi = self.mutari_cu_capturi(jucator)

        if are_capturi:
            if self.are_capturi(inamic, x, y):
                directii = Joc.directii(x, y)
                for (i, j) in directii:
                    x_nou = x + i
                    y_nou = y + j
                    x_dupa = x + 2*i
                    y_dupa = y + 2*j
                    if x_nou < 0 or y_nou < 0 or x_nou >= Joc.NR_LINII or y_nou >= Joc.NR_COLOANE:
                        continue
                    if x_dupa < 0 or y_dupa < 0 or x_dupa >= Joc.NR_LINII or y_dupa >= Joc.NR_COLOANE:
                        continue

                    if self.matr[x_nou][y_nou] == inamic and self.matr[x_dupa][y_dupa] == Joc.GOL:
                        pozitii.append((x_dupa, y_dupa))
                return pozitii
        else:
            directii = Joc.directii(x, y)
            for (i, j) in directii:
                x_nou = x + i
                y_nou = y + j
                if x_nou < 0 or y_nou < 0 or x_nou >= Joc.NR_LINII or y_nou >= Joc.NR_COLOANE:
                    continue

                if self.matr[x_nou][y_nou] == Joc.GOL:
                    # se poate muta
                    copie_matr = copy.deepcopy(self.matr)
                    copie_matr[x][y] = Joc.GOL
                    copie_matr[x_nou][y_nou] = jucator
                    pozitii.append((x_nou, y_nou))

        return pozitii

    def are_capturi(self, inamic, x, y, matrice=None):
        if matrice == None:
            matrice = self.matr
        
        # verific daca piesa aceasta poate captura
        directii = Joc.directii(x, y)
        for (i, j) in directii:
            x_nou = x + i
            y_nou = y + j
            x_dupa = x + 2*i
            y_dupa = y + 2*j
            if x_nou < 0 or y_nou < 0 or x_nou >= Joc.NR_LINII or y_nou >= Joc.NR_COLOANE:
                continue
            if x_dupa < 0 or y_dupa < 0 or x_dupa >= Joc.NR_LINII or y_dupa >= Joc.NR_COLOANE:
                continue

            if matrice[x_nou][y_nou] == inamic and matrice[x_dupa][y_dupa] == Joc.GOL:
                return True

        return False

    def stari_dupa_capturi(self, jucator, inamic, x, y, matrice):
        l_mutari = []
        if self.are_capturi(inamic, x, y, matrice):
            directii = Joc.directii(x, y)
            for (i, j) in directii:
                x_nou = x + i
                y_nou = y + j
                x_dupa = x + 2*i
                y_dupa = y + 2*j
                if x_nou < 0 or y_nou < 0 or x_nou >= Joc.NR_LINII or y_nou >= Joc.NR_COLOANE:
                    continue
                if x_dupa < 0 or y_dupa < 0 or x_dupa >= Joc.NR_LINII or y_dupa >= Joc.NR_COLOANE:
                    continue

                if matrice[x_nou][y_nou] == inamic and matrice[x_dupa][y_dupa] == Joc.GOL:
                    # poate captura
                    copie_matr = copy.deepcopy(matrice)
                    copie_matr[x][y] = Joc.GOL
                    copie_matr[x_nou][y_nou] = Joc.GOL
                    copie_matr[x_dupa][y_dupa] = jucator
                    # print(f"Continua recursia la ({x_dupa}, {y_dupa})")
                    l_mutari.extend(self.stari_dupa_capturi(
                        jucator, inamic, x_dupa, y_dupa, copie_matr))
            return l_mutari
        else:
            # print(f"opreste recursia la ({x}, {y})")
            return [Joc(matrice)]

    def mutari_cu_capturi(self, jucator):
        l_mutari = []
        are_capturi = False
        inamic = Joc.jucator_opus(jucator)
        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE):
                if self.matr[i][j] == jucator:
                    if self.are_capturi(inamic, i, j):
                        are_capturi = True
                        l_mutari.extend(self.stari_dupa_capturi(
                            jucator, inamic, i, j, self.matr))
        return are_capturi, l_mutari

    def mutari_fara_capturi(self, jucator):
        l_mutari = []
        for x in range(self.NR_LINII):
            for y in range(self.NR_COLOANE):
                if self.matr[x][y] == jucator:
                    directii = Joc.directii(x, y)
                    for (i, j) in directii:
                        x_nou = x + i
                        y_nou = y + j
                        if x_nou < 0 or y_nou < 0 or x_nou >= Joc.NR_LINII or y_nou >= Joc.NR_COLOANE:
                            continue

                        if self.matr[x_nou][y_nou] == Joc.GOL:
                            # se poate muta
                            copie_matr = copy.deepcopy(self.matr)
                            copie_matr[x][y] = Joc.GOL
                            copie_matr[x_nou][y_nou] = jucator
                            l_mutari.append(Joc(copie_matr))

        return l_mutari

    def mutari(self, jucator):  # jucator = simbolul jucatorului care muta
        are_capturi, l_mutari = self.mutari_cu_capturi(jucator)
        if are_capturi:
            return l_mutari
        else:
            return self.mutari_fara_capturi(jucator)

    def estimeaza_scor(self, adancime, jucator):
        t_final = self.final(jucator)
        # if (adancime==0):
        if t_final == self.__class__.JMAX:
            return (99+adancime)
        elif t_final == self.__class__.JMIN:
            return (-99-adancime)
        elif t_final == 'remiza':
            return 0
        else:
            # returnez nr de piese ale computerului - nr de piese ale jucatorului
            nr_piese_JMAX = 0
            nr_piese_JMIN = 0
            for i in range(self.NR_LINII):
                for j in range(self.NR_COLOANE):
                    if self.matr[i][j] == self.JMAX:
                        nr_piese_JMAX += 1
                    if self.matr[i][j] == self.JMIN:
                        nr_piese_JMIN += 1
            return nr_piese_JMAX - nr_piese_JMIN

    def sirAfisare(self):
        sir = "  |"
        sir += " ".join([str(i) for i in range(self.NR_COLOANE)])+"\n"
        sir += "-"*(self.NR_COLOANE+1)*2+"\n"
        for i in range(self.NR_LINII):  # itereaza prin linii
            sir += str(i)+" |"+" ".join([str(x) for x in self.matr[i]])+"\n"
        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc: Joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [
            Stare(mutare, juc_opus, self.adancime-1, parinte=self) for mutare in l_mutari]

        # print(f"Din starea {self} se poate ajunge in starile {l_stari_mutari}")
        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:"+self.j_curent+")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare: Stare):

    if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
        stare.estimare = stare.tabla_joc.estimeaza_scor(
            stare.adancime, stare.j_curent)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare: Stare):
    if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
        stare.estimare = stare.tabla_joc.estimeaza_scor(
            stare.adancime, stare.j_curent)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if(alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if(beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta: Stare):
    final = stare_curenta.tabla_joc.final(stare_curenta.j_curent)
    if(final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat "+final)

        return True

    return False


def main():
    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input(
            "Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input(
            "Doriti sa jucati cu alb ('W') sau cu negru ('B')?").upper()
        if (Joc.JMIN in ['W', 'B']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie W sau B.")
    Joc.JMAX = 'W' if Joc.JMIN == 'B' else 'B'

    # initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, "W", ADANCIME_MAX)

    # setari interf grafica
    pygame.init()
    pygame.display.set_caption('ASTAR Bina Mircea')

    ecran = pygame.display.set_mode(size=DISPLAY_SIZE)
    Joc.initializeaza(ecran)

    de_mutat = False
    posibile_mutari = []
    tabla_curenta.deseneaza_grid()
    while True:

        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul
            # [MOUSEBUTTONDOWN, MOUSEMOTION,....]
            # l=pygame.event.get()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # inchide fereastra
                    sys.exit()
                elif event.type == pygame.KEYUP and event.key == pygame.K_r:
                    print("RESTART JOC")
                    tabla_curenta = Joc()
                    stare_curenta = Stare(tabla_curenta, "W", ADANCIME_MAX)
                    stare_curenta.tabla_joc.deseneaza_grid()

                    
                elif event.type == pygame.MOUSEBUTTONDOWN:  # click

                    pos = pygame.mouse.get_pos()  # coordonatele clickului

                    for linie in range(Joc.NR_LINII):
                        for coloana in range(Joc.NR_COLOANE):

                            # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                            if Joc.celuleGrid[linie][coloana].collidepoint(pos):
                                ###############################
                                if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.JMIN:
                                    if (de_mutat and linie == de_mutat[0] and coloana == de_mutat[1]):
                                        # daca am facut click chiar pe patratica selectata, o deselectez
                                        de_mutat = False
                                        posibile_mutari = []
                                        stare_curenta.tabla_joc.deseneaza_grid()
                                    else:
                                        de_mutat = (linie, coloana)
                                        posibile_mutari = stare_curenta.tabla_joc.pozitii_in_care_poate_muta(
                                            linie, coloana)
                                        # desenez gridul cu patratelul marcat
                                        stare_curenta.tabla_joc.deseneaza_grid(
                                            de_mutat, posibile_mutari)

                                elif stare_curenta.tabla_joc.matr[linie][coloana] == Joc.GOL:
                                    if de_mutat and (linie, coloana) in posibile_mutari:

                                        stare_curenta.tabla_joc.matr[de_mutat[0]
                                                                     ][de_mutat[1]] = Joc.GOL

                                        x, y = de_mutat
                                        de_mutat = False

                                        # verific daca captureaza o piesa
                                        if abs(x - linie) == 2 or abs(y - coloana) == 2:
                                            x_sters = int((x + linie) / 2)
                                            y_sters = int((y + coloana) / 2)
                                            stare_curenta.tabla_joc.matr[x_sters][y_sters] = Joc.GOL

                                        # plasez simbolul pe "tabla de joc"
                                        stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
                                        stare_curenta.tabla_joc.deseneaza_grid()
                                        # afisarea starii jocului in urma mutarii utilizatorului
                                        print("\nTabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))

                                        # testez daca jocul a ajuns intr-o stare finala
                                        # si afisez un mesaj corespunzator in caz ca da
                                        if (afis_daca_final(stare_curenta)):
                                            break

                                        # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                        stare_curenta.j_curent = Joc.jucator_opus(
                                            stare_curenta.j_curent)

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            stare_curenta.tabla_joc.deseneaza_grid()
            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " +
                  str(t_dupa-t_inainte)+" milisecunde.")

            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
