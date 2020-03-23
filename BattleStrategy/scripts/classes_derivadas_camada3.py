from classes_derivadas_camada2 import *
from constantes import *

#Classe que define o cursor do mouse quando selecionar um soldado do jogador para movimento
class CursorSelecaoMouse(ComumBancoBaseSoldado):
    #métodos de carregamento e inicialização
    def __init__(self):
        super().__init__(None,POSX_PADRAO_CURSOR,POSY_PADRAO_CURSOR,-1,-1,RAIO_CURSOR,PATH_IMAGEM_CURSOR_MOUSE)


    #métodos de atualização lógica

    #métodos de desenho e debug
    def debug(self):
        print("-------------------Cursor-------------------")
        super().debug()
        print("-------------------Cursor-------------------")
class BotaoPularTurno:
    #métodos de carregamento e inicialização
    def __init__(self):
        self.imagem = self.carregar_imagem()
        self.x = POSX_BOTAO
        self.y = POSY_BOTAO
        self.w = self.imagem.get_width()
        self.h = self.imagem.get_height()
    def carregar_imagem(self):
        img = None
        try:
            img = pygame.image.load(PATH_IMAGEM_BOTAO_PULAR_TURNO)
        except:
            print("Erro ao carregar imagem do botão")
            pygame.quit()
            exit(1)
        return img

    #métodos de atualização lógica
    def clicado(self,evento_mouse):
        pos_mouse = evento_mouse.pos
        if evento_mouse.button == 1 and (self.x < pos_mouse[0] < (self.x + self.w)) and (self.y < pos_mouse[1] <  (self.y + self.h)):
            return True

        return False

    #métodos de desenho e debug
    def desenhar(self,tela):
        tela.blit(self.imagem,(self.x,self.y))
class Tabuleiro:
    #métodos de carregamento e inicialização
    def __init__(self,nivel_jogo):
        self.territorio = Territorio()
        self.exercito_jogador = ExercitoJogador()
        self.exercito_computador = ExercitoComputador(QTDE_MOEDAS_COMPUTADOR_POR_NIVEL * nivel_jogo)


    #métodos de atualização lógica
    def atualizar(self,cursor_mouse,turno_atual_jogo):
        self.territorio.atualizar_status_ocupacao_bases(self.exercito_jogador.soldados,self.exercito_computador.soldados)
        if turno_atual_jogo % 2 == 0:
            jogou = self.exercito_computador.jogar(self.exercito_jogador,self.territorio.bases_territorio,turno_atual_jogo,True)
            if jogou == True:
                print("PC JOGOU!")
                return turno_atual_jogo + 1
        else:
            jogou = self.exercito_jogador.jogar(self.exercito_computador,self.territorio.bases_territorio,cursor_mouse,turno_atual_jogo)
            if jogou == True:
                print("JOGADOR JOGOU!")
                return turno_atual_jogo + 1

        #verifico vitória de algum dos jogadores (humano ou computador)
        if self.exercito_jogador.ficou_insolvente():
            print("COMPUTADOR GANHOU!!!")
            pygame.quit()
            exit()
        elif self.exercito_computador.ficou_insolvente():
            print("JOGADOR GANHOU!!!")
            pygame.quit()
            exit()
        return turno_atual_jogo
    #métodos de desenho e debug
    def desenhar(self,tela):
        self.territorio.desenhar(tela)
        self.exercito_computador.desenhar(tela)
        self.exercito_jogador.desenhar(tela)

class Hud:
    def __init__(self,x,y,w,h):
        try:
            self.fonte = pygame.font.Font(PATH_FONTE_HUD,TAM_FONTE_HUD)
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.cor_fundo = COR_FUNDO_HUD
            self.cor_texto = COR_TEXTO_HUD
        except:
            print("Erro ao tentar carregar fonte",PATH_FONTE_HUD)
            pygame.quit()
            exit(1)
    def escrever(self,tela,texto,x,y):
        superficie_texto = self.fonte.render(texto,True,self.cor_texto)
        tela.blit(superficie_texto,(x,y))
    def desenhar(self,tela,turno_atual_jogo,nivel_atual_jogo,qtde_moedas_jogador,qtde_moedas_computador):
        pygame.draw.rect(tela,self.cor_fundo,(self.x,self.y,self.w,self.h))
        self.escrever(tela,"Moedas Jogador: %d"%(qtde_moedas_jogador),self.x+40,self.y+20)
        self.escrever(tela,"Moedas Computador: %d"%(qtde_moedas_computador),self.x+W_TELA-330,self.y+20)
        self.escrever(tela,"Turno: %d"%(turno_atual_jogo),self.x+40,self.y+50)
        self.escrever(tela,"Dificuldade: %d"%(nivel_atual_jogo),self.x+W_TELA-330,self.y+50)



class TelaPrincipal:
    def __init__(self,nivel_jogo):
        pygame.init()
        self.w = W_TELA
        self.h = H_TELA
        self.titulo = TITULO_TELA
        self.turno_jogo = 1
        self.nivel_jogo = nivel_jogo

        try:
            self.icone = pygame.image.load(PATH_ICONE)
        except:
            print("Não foi possível carregar ícone do jogo!")
            pygame.quit()
            exit(1)

        pygame.display.set_caption(self.titulo)
        pygame.display.set_icon(self.icone)
        self.tela = pygame.display.set_mode((self.w,self.h))

        self.clock = pygame.time.Clock()

        self.cursor_mouse = CursorSelecaoMouse()
        self.botao_pular_turno = BotaoPularTurno()
        self.tabuleiro = Tabuleiro(self.nivel_jogo)
        self.hud = Hud(x=0,y=H_TELA-100,w=self.w,h=100)
    def tratar_eventos(self):
        for e in pygame.event.get():
            if e.type ==   pygame.QUIT:
                pygame.quit()
                exit(0)
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.botao_pular_turno.clicado(e):
                    self.turno_jogo += 1
    def atualizar(self):
        self.turno_jogo = self.tabuleiro.atualizar(self.cursor_mouse,self.turno_jogo)
    def desenhar(self):
        self.tela.fill(COR_FUNDO_TELA)
        self.tabuleiro.desenhar(self.tela)
        self.hud.desenhar(tela=self.tela,turno_atual_jogo=self.turno_jogo,nivel_atual_jogo=self.nivel_jogo,qtde_moedas_jogador=self.tabuleiro.exercito_jogador.get_qtde_moedas(),qtde_moedas_computador=self.tabuleiro.exercito_computador.get_qtde_moedas())
        self.cursor_mouse.desenhar(self.tela,False,True)
        self.botao_pular_turno.desenhar(self.tela)
        pygame.display.update()

    def loop(self):
        while True:
            self.clock.tick(FPS)
            self.atualizar()
            self.desenhar()
            self.tratar_eventos()
