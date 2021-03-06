from statistics import mean, median
import time

import pygame
import sys
import copy
import math


NEGRU = (0, 0, 0)
ROSU = (255, 0, 0)
VERDE = (0, 255, 0)
ALB = (255, 255, 255)

LINE_WIDTH = 1

# dimensiunea ferestrei in pixeli
L = 75
CELL_SIZE = (L, L)
DISPLAY_SIZE = (L*5, L*10)


class Buton:
	def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115), culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255), valoare=""):
		self.display = display
		self.culoareFundal = culoareFundal
		self.culoareFundalSel = culoareFundalSel
		self.text = text
		self.font = font
		self.w = w
		self.h = h
		self.selectat = False
		self.fontDimensiune = fontDimensiune
		self.culoareText = culoareText
		# creez obiectul font
		fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
		self.textRandat = fontObj.render(self.text, True, self.culoareText)
		self.dreptunghi = pygame.Rect(left, top, w, h)
		# aici centram textul
		self.dreptunghiText = self.textRandat.get_rect(
			center=self.dreptunghi.center)
		self.valoare = valoare

	def selecteaza(self, sel):
		self.selectat = sel
		self.deseneaza()

	def selecteazaDupacoord(self, coord):
		if self.dreptunghi.collidepoint(coord):
			self.selecteaza(True)
			return True
		return False

	def updateDreptunghi(self):
		self.dreptunghi.left = self.left
		self.dreptunghi.top = self.top
		self.dreptunghiText = self.textRandat.get_rect(
			center=self.dreptunghi.center)

	def deseneaza(self):
		culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
		pygame.draw.rect(self.display, culoareF, self.dreptunghi)
		self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
	def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
		self.listaButoane = listaButoane
		self.indiceSelectat = indiceSelectat
		self.listaButoane[self.indiceSelectat].selectat = True
		self.top = top
		self.left = left
		leftCurent = self.left
		for b in self.listaButoane:
			b.top = self.top
			b.left = leftCurent
			b.updateDreptunghi()
			leftCurent += (spatiuButoane+b.w)

	def selecteazaDupacoord(self, coord):
		for ib, b in enumerate(self.listaButoane):
			if b.selecteazaDupacoord(coord):
				self.listaButoane[self.indiceSelectat].selecteaza(False)
				self.indiceSelectat = ib
				return True
		return False

	def deseneaza(self):
		# atentie, nu face wrap
		for b in self.listaButoane:
			b.deseneaza()

	def getValoare(self):
		return self.listaButoane[self.indiceSelectat].valoare

# ECRAN INITIAL


def deseneaza_alegeri(display, tabla_curenta):
	btn_alg = GrupButoane(
		top=30,
		left=30,
		listaButoane=[
			Buton(display=display, w=80, h=30, text="minimax", valoare="1"),
			Buton(display=display, w=80, h=30, text="alphabeta", valoare="2")
		],
		indiceSelectat=1)
	btn_juc = GrupButoane(
		top=100,
		left=30,
		listaButoane=[
			Buton(display=display, w=50, h=30, text="White", valoare="W"),
			Buton(display=display, w=50, h=30, text="Black", valoare="B")
		],
		indiceSelectat=0)
	btn_dificultate = GrupButoane(
		top=170,
		left=30,
		listaButoane=[
			Buton(display=display, w=60, h=30, text="Easy", valoare=1),
			Buton(display=display, w=60, h=30, text="Medium", valoare=3),
			Buton(display=display, w=60, h=30, text="Hard", valoare=5)
		],
		indiceSelectat=0)
	ok = Buton(display=display, top=240, left=30, w=40,
			   h=30, text="ok", culoareFundal=(155, 0, 55))
	btn_alg.deseneaza()
	btn_juc.deseneaza()
	btn_dificultate.deseneaza()
	ok.deseneaza()
	while True:
		for ev in pygame.event.get():
			if ev.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif ev.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				if not btn_alg.selecteazaDupacoord(pos):
					if not btn_juc.selecteazaDupacoord(pos):
						if not btn_dificultate.selecteazaDupacoord(pos):
							if ok.selecteazaDupacoord(pos):
								display.fill((0, 0, 0))  # stergere ecran
								tabla_curenta.deseneaza_grid()
								return btn_juc.getValoare(), btn_alg.getValoare(), btn_dificultate.getValoare()
		pygame.display.update()


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

		if x == 2:
			return [stanga, dreapta, jos]

		if x == 7:
			return [stanga, dreapta, sus]

		return directii_normale

	def final(self, jucator):
		nr_piese_JMAX = 0
		nr_piese_JMIN = 0
		castiga_alb = True
		castiga_negru = True

		# verific daca un triunghi a fost cucerit de adversar
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

		# calculez cate piese are jucatorul si calculatorul
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

		# verific daca jucatorul curent nu mai are mutari, daca da a castigat adversarul
		mutari = self.mutari(jucator)
		if len(mutari) == 0:
			print(jucator + " nu mai are mutari")
			return self.jucator_opus(jucator)

		return False

	def pozitii_in_care_poate_muta(self, x, y):
		# pozitiile in care poate muta jucatorul pentru a le colora cu verde si afisa in interfata
		# se refera strict la locuri pe tabla nu la starile rezultate
		jucator = self.matr[x][y]
		inamic = self.jucator_opus(jucator)
		pozitii = []

		are_capturi = self.are_capturi(jucator)

		if are_capturi:
			if self.are_capturi_din_punct(inamic, x, y):
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

	def are_capturi_din_punct(self, inamic, x, y, matrice=None):
		# returneaza daca din punctul (x, y) se poate realiza o captura
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
		# genereaza starile din (x, y) care rezulta cu ajutorul unei capturi
		# captura poate fi multipla
		l_mutari = []
		if self.are_capturi_din_punct(inamic, x, y, matrice):
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
					# Continua recursia la (x_dupa, y_dupa)
					l_mutari.extend(self.stari_dupa_capturi(
						jucator, inamic, x_dupa, y_dupa, copie_matr))
			return l_mutari
		else:
			# opreste recursia si returneaza jocul obtinut
			return [Joc(matrice)]

	def mutari_cu_capturi(self, jucator):
		# returneaza daca exista capturi in jocul curent si o lista cu starile de dupa capturi
		l_mutari = []
		are_capturi = False
		inamic = Joc.jucator_opus(jucator)
		for i in range(self.NR_LINII):
			for j in range(self.NR_COLOANE):
				if self.matr[i][j] == jucator:
					if self.are_capturi_din_punct(inamic, i, j):
						are_capturi = True
						l_mutari.extend(self.stari_dupa_capturi(
							jucator, inamic, i, j, self.matr))
		return are_capturi, l_mutari

	def are_capturi(self, jucator):
		# returneaza daca exista capturi in jocul curent
		are_capturi = False
		inamic = Joc.jucator_opus(jucator)
		for i in range(self.NR_LINII):
			for j in range(self.NR_COLOANE):
				if self.matr[i][j] == jucator:
					if self.are_capturi_din_punct(inamic, i, j):
						are_capturi = True
		return are_capturi

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
		are_capturi_din_punct, l_mutari = self.mutari_cu_capturi(jucator)
		if are_capturi_din_punct:
			return l_mutari
		else:
			return self.mutari_fara_capturi(jucator)

	def estimeaza_scor(self, adancime, jucator, estimare=2):
		t_final = self.final(jucator)
		# if (adancime==0):
		if t_final == self.__class__.JMAX:
			return (990+adancime)
		elif t_final == self.__class__.JMIN:
			return (-999-adancime)
		elif t_final == 'remiza':
			return 0
		else:
			if estimare == 1:
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
			else:
				# returnez (nr de piese ale computerului - nr de piese ale jucatorului) * 5 +
    			# + (avansul pieselor calculatorului - avansul pieselor jucatorului)
				nr_piese_JMAX = 0
				nr_piese_JMIN = 0
				for i in range(self.NR_LINII):
					for j in range(self.NR_COLOANE):
						if self.matr[i][j] == self.JMAX:
							nr_piese_JMAX += 1
						if self.matr[i][j] == self.JMIN:
							nr_piese_JMIN += 1

				avans_JMAX = 0
				avans_JMIN = 0
				for i in range(self.NR_LINII):
					for j in range(self.NR_COLOANE):
						if self.matr[i][j] == self.JMAX:
							avans_JMAX += i
						if self.matr[i][j] == self.JMIN:
							avans_JMIN += self.NR_LINII-1-i
				return (nr_piese_JMAX - nr_piese_JMIN) * 5 + avans_JMAX - avans_JMIN



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
		self.parinte = parinte

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


def afis_daca_final(stare_curenta: Stare, timpi_gandire_calculator):
	final = stare_curenta.tabla_joc.final(stare_curenta.j_curent)
	if(final):
		if (final == "remiza"):
			print("Remiza!")
		else:
			print("A castigat "+final)

			# afisam date despre timpii de gandire ai calculatorului
			print(f"Timp minim de gantire {min(timpi_gandire_calculator)}")
			print(f"Timp maxim de gantire {max(timpi_gandire_calculator)}")
			print(f"Mediana timpilor de gantire {median(timpi_gandire_calculator)}")
			print(f"Media timpilor de gantire {mean(timpi_gandire_calculator)}")
		return True

	return False


def muta_piesa(de_mutat, linie, coloana, stare_curenta: Stare, cu_captura=False):

	stare_actualizata = Stare(copy.deepcopy(stare_curenta.tabla_joc),
							  stare_curenta.j_curent, stare_curenta.adancime, stare_curenta)

	stare_actualizata.tabla_joc.matr[de_mutat[0]][de_mutat[1]] = Joc.GOL
	x, y = de_mutat
	de_mutat = False

	# verific daca captureaza o piesa
	if cu_captura:
		x_sters = int((x + linie) / 2)
		y_sters = int((y + coloana) / 2)
		stare_actualizata.tabla_joc.matr[x_sters][y_sters] = Joc.GOL

	# plasez simbolul pe "tabla de joc"
	stare_actualizata.tabla_joc.matr[linie][coloana] = Joc.JMIN
	stare_actualizata.tabla_joc.deseneaza_grid()

	return stare_actualizata


def main():
	# initializare tabla
	tabla_curenta = Joc()
	print("Tabla initiala")
	print(str(tabla_curenta))

	# setari interf grafica
	pygame.init()
	pygame.display.set_caption('ASTAR Bina Mircea')

	ecran = pygame.display.set_mode(size=DISPLAY_SIZE)
	Joc.initializeaza(ecran)
	# initializare algoritm

	Joc.JMIN, tip_algoritm, ADANCIME_MAX = deseneaza_alegeri(
		ecran, tabla_curenta)

	Joc.JMAX = 'W' if Joc.JMIN == 'B' else 'B'

	# creare stare initiala
	stare_curenta = Stare(tabla_curenta, "W", ADANCIME_MAX)

	de_mutat = False
	posibile_mutari = []
	captura_in_progres = False
	tabla_curenta.deseneaza_grid()
	timpi_gandire_calculator = []
	t_inainte = int(round(time.time() * 1000))

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

				elif event.type == pygame.KEYUP and event.key == pygame.K_u:
					print("UNDO JOC")
					if stare_curenta.parinte == None:
						print("Nu se poate da undo pentru ca este in starea initiala")
						continue
					stare_curenta = stare_curenta.parinte
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

								elif stare_curenta.tabla_joc.matr[linie][coloana] == Joc.GOL and de_mutat and (linie, coloana) in posibile_mutari:
									x, y = de_mutat

									# jucatorul muta o piesa intr-o pozitie posibila
									if captura_in_progres:
										stare_curenta = muta_piesa(
											de_mutat, linie, coloana, stare_curenta, cu_captura=True)
										if not stare_curenta.tabla_joc.are_capturi_din_punct(Joc.JMAX, linie, coloana):
											captura_in_progres = False
										else:
											posibile_mutari = stare_curenta.tabla_joc.pozitii_in_care_poate_muta(
												linie, coloana)
											t_dupa = int(
												round(time.time() * 1000))
											print("Jucatorul a \"gandit\" timp de " +
												  str(t_dupa-t_inainte)+" milisecunde.")

									else:
										if stare_curenta.tabla_joc.are_capturi_din_punct(Joc.JMAX, x, y):
											captura_in_progres = True
											posibile_mutari = stare_curenta.tabla_joc.pozitii_in_care_poate_muta(
												linie, coloana)

										stare_curenta = muta_piesa(
											de_mutat, linie, coloana, stare_curenta, cu_captura=captura_in_progres)

										if not captura_in_progres:
											t_dupa = int(
												round(time.time() * 1000))
											print("Jucatorul a \"gandit\" timp de " +
												  str(t_dupa-t_inainte)+" milisecunde.")

									# afisarea starii jocului in urma mutarii utilizatorului
									print("\nTabla dupa mutarea jucatorului")
									print(str(stare_curenta))
         
									if not stare_curenta.tabla_joc.are_capturi_din_punct(Joc.JMAX, linie, coloana):
										captura_in_progres = False

									# testez daca jocul a ajuns intr-o stare finala
									# si afisez un mesaj corespunzator in caz ca da
									if (afis_daca_final(stare_curenta, timpi_gandire_calculator)):
										break

									# S-a realizat o mutare. Schimb jucatorul cu cel opus
									if not captura_in_progres:
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
			timpi_gandire_calculator.append(t_dupa-t_inainte)
			print("Calculatorul a \"gandit\" timp de " +
				  str(t_dupa-t_inainte)+" milisecunde.")

			if (afis_daca_final(stare_curenta, timpi_gandire_calculator)):
				break

			# S-a realizat o mutare. Schimb jucatorul cu cel opus
			stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

			# incep timerul pt jucator
			t_inainte = int(round(time.time() * 1000))


if __name__ == "__main__":
	main()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
