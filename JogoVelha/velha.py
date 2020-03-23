"""
--------------------------------------------------JOGO DA VELHA SINGLEPLAYER-------------------------------------------------------
"""
#Importo o pygame...
import pygame

#Importo o método randrange para sortear quem começa a jogar...
from random import randrange

#Classe do jogo que representa o tabuleiro...
class TelaTabuleiro:
	def __init__(self,screen):
		
		#marcações de casas no jogo (ocupadas e livres)...
		#[donocasa1,donocasa2,etc...]
		#dono = jogador = 0
		#dono = computador = 1
		#dono = ninguem = -1
		self.CASA_JOGADOR = self.JOGADOR = 0
		self.CASA_COMPUTADOR = self.COMPUTADOR =  1
		self.CASA_LIVRE = self.NINGUEM = -1
		
		#preencho tabuleiro com -1...
		self.tabuleiro_logico = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
		
		
		#abstraio posicoes graficas das casas do tabuleiro...
		
		self.p1 = (0+5,3)
		self.p2 = (72+12,3)
		self.p3 = (144+17,3)

		self.p4 = (0+5,66+13)
		self.p5 = (72+12,66+13)
		self.p6 = (144+17,66+13)

		self.p7 = (0+5,132+21)
		self.p8 = (72+12,132+21)
		self.p9 = (144+17,132+21)

		self.casas_tabuleiro = [self.p1,self.p2,self.p3,self.p4,self.p5,self.p6,self.p7,self.p8,self.p9]
		
		#crio meus sprites...
		self.sprite_tabuleiro = pygame.image.load("./sprites/tabuleiro.png")
		self.sprite_xis = pygame.image.load("./sprites/xis.jpeg")
		self.sprite_bola = pygame.image.load("./sprites/bola.jpeg")
		
		#carrego meus sons...
		self.som_aplausos = pygame.mixer.Sound("./audios/aplausos.ogg")
		self.som_vaias = pygame.mixer.Sound("./audios/vaias.ogg")
		self.som_jogada = pygame.mixer.Sound("./audios/jogada.ogg")
		
		#chamo o gameloop dessa tela...
		encerrar = False
		while encerrar == False:
			self.tabuleiro_logico = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
			for evento in pygame.event.get():
				if evento.type == pygame.QUIT:
					encerrar = True
					continue
			
			self.gameloop(screen)
	def gameloop(self,screen):
		
		# variáveis de controle do gameloop...
		tela_ativa = True
		ganhador = self.NINGUEM
		quem_joga = randrange(2)
		
		#desenho o tabuleiro e atualizo a tela antes do loop pra evitar tela preta...
		self.desenha_base_tabuleiro(screen)
		pygame.display.update()
		
		#gameloop...
		while tela_ativa and ganhador == self.NINGUEM:
			#limpo a tela para a cor passada...
			screen.fill((100,0,100))
			
			#desenho a base do tabuleiro na tela...
			self.desenha_base_tabuleiro(screen)
			
			#busco pelo evento sair da aplicacao...
			for evento in pygame.event.get():
				if evento.type == pygame.QUIT:
					self.tela_ativa = False
					continue

			#ações dos jogadores...
			
			#se a jogada é do jogador...
			if quem_joga == self.JOGADOR:
				self.jogador_joga(screen)
				self.som_jogada.play()
				self.desenha_itens_no_tabuleiro(screen)
				pygame.time.delay(100)

			#se a jogada é do computador...			
			elif quem_joga == self.COMPUTADOR:
				self.computador_joga(screen)
				self.som_jogada.play()
				self.desenha_itens_no_tabuleiro(screen)
				pygame.time.delay(100)
			
			#inverto quem joga a próxima jogada...
			quem_joga = not quem_joga
			
			#procuro por um ganhador...
			ganhador = self.quem_ganhou()
			
			#procuro pelo empate...
			if self.houve_empate():
				ganhador = self.NINGUEM
				tela_ativa = False
			
			#atualizo a tela...
			pygame.display.update()
			
		delay = 2000
		if ganhador == self.JOGADOR:
			self.som_aplausos.play()
			delay = 5300
		elif ganhador == self.COMPUTADOR:
			self.som_vaias.play()
			delay = 2500
			
		pygame.time.delay(delay)
	def desenha_base_tabuleiro(self,screen):
		screen.blit(self.sprite_tabuleiro,(0,0))	
	def desenha_xis(self,screen,casa):
		screen.blit(self.sprite_xis,self.casas_tabuleiro[casa-1])
	def desenha_bola(self,screen,casa):
		screen.blit(self.sprite_bola,self.casas_tabuleiro[casa-1])
	def casa_escolhida_esta_livre(self,casa_escolhida):
		return self.tabuleiro_logico[casa_escolhida - 1] == self.CASA_LIVRE
	def converte_coordenada_para_casa(self,coordenada):
		#se o y da coordenada for na primeira fila de 3 casas...
		if coordenada[1] < self.p4[1]:
			#se o x da coordenada for na primeira coluna da fila...
			if coordenada[0] < self.p2[0]:
				return 1
			#se o x da coordenada for na segunda coluna da fila...
			elif coordenada[0] < self.p3[0]:
				return 2
			#se o x da coordenada for na terceira coluna da fila...
			else:
				return 3
		#se o y da coordenada for na segunda fila de 3 casas...
		elif coordenada[1] < self.p7[1]:
			#se o x da coordenada for na primeira coluna da fila...
			if coordenada[0] < self.p5[0]:
				return 4
			#se o x da coordenada for na segunda coluna da fila...
			elif coordenada[0] < self.p6[0]:
				return 5
			#se o x da coordenada for na terceira coluna da fila...
			else:
				return 6
		#se o y da coordenada for na terceira fila de 3 casas...
		else:
			#se o x da coordenada for na primeira coluna da fila...
			if coordenada[0] < self.p8[0]:
				return 7
			#se o x da coordenada for na segunda coluna da fila...
			elif coordenada[0] < self.p9[0]:
				return 8
			#se o x da coordenada for na terceira coluna da fila...
			else:
				return 9
	def marca_jogada_no_tabuleiro_logico(self,casa_escolhida,casa_de_quem_agora):
		self.tabuleiro_logico[casa_escolhida - 1] = casa_de_quem_agora
	def jogador_joga(self,screen):
		continuar_loop = True
		while continuar_loop:
			for evento in pygame.event.get():
				if evento.type == pygame.MOUSEBUTTONDOWN:
					#pego a posição do mouse...
					pos_mouse = pygame.mouse.get_pos()
					
					#converto essa posição para uma casa no jogo...
					casa_escolhida = self.converte_coordenada_para_casa(pos_mouse)
					
					#verifico se a casa escolhida está livre...
					if self.casa_escolhida_esta_livre(casa_escolhida):
						self.marca_jogada_no_tabuleiro_logico(casa_escolhida,self.CASA_JOGADOR)
						print("jogador jogou => ",self.tabuleiro_logico)
						continuar_loop = False
						break
				else:
					if evento.type == pygame.QUIT:
						pygame.quit()
						exit()
	def computador_joga(self,screen):
		#pego as casas do tabuleiro e crio abstração de suas linhas, colunas e diagonais...
		
		linha1 = self.tabuleiro_logico[0:3]
		linha2 = self.tabuleiro_logico[3:6]
		linha3 = self.tabuleiro_logico[6:9]
		
		coluna1 = [self.tabuleiro_logico[0],self.tabuleiro_logico[3],self.tabuleiro_logico[6]]
		coluna2 = [self.tabuleiro_logico[1],self.tabuleiro_logico[4],self.tabuleiro_logico[7]]
		coluna3 = [self.tabuleiro_logico[2],self.tabuleiro_logico[5],self.tabuleiro_logico[8]]
		
		diagonal1 = [self.tabuleiro_logico[0],self.tabuleiro_logico[4],self.tabuleiro_logico[8]]
		diagonal2 = [self.tabuleiro_logico[2],self.tabuleiro_logico[4],self.tabuleiro_logico[6]]
		
        #modo possibilidade de vitória (ataque final)...
		
		#condicoes onde o computador pode ganhar o jogo...
		if self.CASA_JOGADOR not in linha1 and sum(linha1) == 1:
			for i in range(3):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		elif self.CASA_JOGADOR not in linha2 and sum(linha2) == 1:
			for i in range(3,6):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		elif self.CASA_JOGADOR not in linha3 and sum(linha3) == 1:
			for i in range(6,9):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		elif self.CASA_JOGADOR not in coluna1 and sum(coluna1) == 1:
			for i in range(0,7,3):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		elif self.CASA_JOGADOR not in coluna2 and sum(coluna2) == 1:
			for i in range(1,8,3):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		elif self.CASA_JOGADOR not in coluna3 and sum(coluna3) == 1:
			for i in range(2,9,3):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		elif self.CASA_JOGADOR not in diagonal1 and sum(diagonal1) == 1:
			for i in range(0,9,4):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		elif self.CASA_JOGADOR not in diagonal2 and sum(diagonal2) == 1:
			for i in range(2,7,2):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		
		#modo possibilidade de derrota (bloqueio)...
		
		#condicoes onde o computador pode perder o jogo...
		elif self.CASA_COMPUTADOR not in linha1 and sum(linha1) == -1:
			for i in range(3):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		elif self.CASA_COMPUTADOR not in linha2 and sum(linha2) == -1:
			for i in range(3,6):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		elif self.CASA_COMPUTADOR not in linha3 and sum(linha3) == -1:
			for i in range(6,9):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		elif self.CASA_COMPUTADOR not in coluna1 and sum(coluna1) == -1:
			for i in range(0,7,3):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		elif self.CASA_COMPUTADOR not in coluna2 and sum(coluna2) == -1:
			for i in range(1,8,3):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		elif self.CASA_COMPUTADOR not in coluna3 and sum(coluna3) == -1:
			for i in range(2,9,3):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		elif self.CASA_COMPUTADOR not in diagonal1 and sum(diagonal1) == -1:
			for i in range(0,9,4):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		elif self.CASA_COMPUTADOR not in diagonal2 and sum(diagonal2) == -1:
			for i in range(2,7,2):
				if self.tabuleiro_logico[i] == self.CASA_LIVRE:
					self.tabuleiro_logico[i] = self.CASA_COMPUTADOR
					break
		else:
			#modo aleatório (início do jogo)...
			while True:
				casa_escolhida = 1 + randrange(9)
				if self.casa_escolhida_esta_livre(casa_escolhida):
					self.marca_jogada_no_tabuleiro_logico(casa_escolhida,self.CASA_COMPUTADOR)
					break

		print("computador jogou => ",self.tabuleiro_logico)
	def desenha_itens_no_tabuleiro(self,screen,lado_jogador="xis"):
		for casa in range(9):
			if self.tabuleiro_logico[casa] == self.CASA_JOGADOR:
				if lado_jogador == "xis":
					self.desenha_xis(screen,casa + 1)
				else:
					self.desenha_bola(screen,casa + 1)
			elif self.tabuleiro_logico[casa] == self.CASA_COMPUTADOR:
				if lado_jogador == "xis":
					self.desenha_bola(screen,casa + 1)
				else:
					self.desenha_xis(screen,casa + 1)
	def quem_ganhou(self):
		#pego as casas do tabuleiro e crio abstração de suas linhas, colunas e diagonais...
		
		linha1 = self.tabuleiro_logico[0:3]
		linha2 = self.tabuleiro_logico[3:6]
		linha3 = self.tabuleiro_logico[6:9]
		
		coluna1 = [self.tabuleiro_logico[0],self.tabuleiro_logico[3],self.tabuleiro_logico[6]]
		coluna2 = [self.tabuleiro_logico[1],self.tabuleiro_logico[4],self.tabuleiro_logico[7]]
		coluna3 = [self.tabuleiro_logico[2],self.tabuleiro_logico[5],self.tabuleiro_logico[8]]
		
		diagonal1 = [self.tabuleiro_logico[0],self.tabuleiro_logico[4],self.tabuleiro_logico[8]]
		diagonal2 = [self.tabuleiro_logico[2],self.tabuleiro_logico[4],self.tabuleiro_logico[6]]
		
		#condicoes onde o jogador ganha o jogo...
		condj1 = self.CASA_LIVRE not in linha1 and sum(linha1) == 0
		condj2 = self.CASA_LIVRE not in linha2 and sum(linha2) == 0
		condj3 = self.CASA_LIVRE not in linha3 and sum(linha3) == 0
		condj4 = self.CASA_LIVRE not in coluna1 and sum(coluna1) == 0
		condj5 = self.CASA_LIVRE not in coluna2 and sum(coluna2) == 0
		condj6 = self.CASA_LIVRE not in coluna3 and sum(coluna3) == 0
		condj7 = self.CASA_LIVRE not in diagonal1 and sum(diagonal1) == 0
		condj8 = self.CASA_LIVRE not in diagonal2 and sum(diagonal2) == 0

		#condicoes onde o computador ganha o jogo...
		condc1 = self.CASA_LIVRE not in linha1 and sum(linha1) == 3
		condc2 = self.CASA_LIVRE not in linha2 and sum(linha2) == 3
		condc3 = self.CASA_LIVRE not in linha3 and sum(linha3) == 3
		condc4 = self.CASA_LIVRE not in coluna1 and sum(coluna1) == 3
		condc5 = self.CASA_LIVRE not in coluna2 and sum(coluna2) == 3
		condc6 = self.CASA_LIVRE not in coluna3 and sum(coluna3) == 3
		condc7 = self.CASA_LIVRE not in diagonal1 and sum(diagonal1) == 3
		condc8 = self.CASA_LIVRE not in diagonal2 and sum(diagonal2) == 3
		
		if condj1 or condj2 or condj3 or condj4 or condj5 or condj6 or condj7 or condj8:
			return self.JOGADOR
		elif condc1 or condc2 or condc3 or condc4 or condc5 or condc6 or condc7 or condc8:
			return self.COMPUTADOR
		else:
			return self.NINGUEM
	def houve_empate(self):
		return self.CASA_LIVRE not in self.tabuleiro_logico and self.quem_ganhou() == self.NINGUEM

#Classe que representa o jogo...
class Velha:
	def __init__(self,nome_tela,dimensoes_tela):
	
		NOME_TELA = nome_tela
		DIMENSOES_TELA = (230,219)
		ICONE_TELA = "icone.jpeg"
		
		pygame.init()
		
		self.configura_tela(NOME_TELA,ICONE_TELA,DIMENSOES_TABULEIRO)
		
		TelaTabuleiro(self.screen)
		
		pygame.quit()
	
	def configura_tela(self,nome_tela,icone_tela,dimensoes_tela):
		self.screen = pygame.display.set_mode(dimensoes_tela)
		pygame.display.set_caption(nome_tela)
		pygame.display.set_icon(pygame.image.load(icone_tela))


if __name__ == "__main__":
	DIMENSOES_TABULEIRO = (230,219)
	Velha('Velha',DIMENSOES_TABULEIRO)
	
