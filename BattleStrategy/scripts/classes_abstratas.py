import pygame
from constantes import COR_TEXTO_VALORES, PATH_FONTE_VALORES,TAM_FONTE_VALORES

#Classe genérica que engloba atributos e métodos comuns às classes Banco , Base e Soldado
class ComumBancoBaseSoldado:
    #métodos de carregamento e inicialização
    def __init__(self,dono,x,y,l,c,r,path_imagem):
        self.path_imagem = path_imagem
        self.imagem = self.carregar_imagem(path_imagem)
        self.dono = dono
        self.x = x
        self.y = y
        self.w = self.imagem.get_width()
        self.h = self.imagem.get_height()
        self.l = l
        self.c = c
        self.r = r


    def carregar_imagem(self,path):
        try:
            return pygame.image.load(path)
        except:
            print("Erro ao tentar carregar imagem",path)
            exit(1)

    #métodos de atualização lógica
    def atualizar_xy(self,x,y):
        self.x = x
        self.y = y
    def get_xy(self):
        return self.x,self.y
    def atualizar_lc(self,l,c):
        self.l = l
        self.c = c
    def get_lc(self):
        return self.l,self.c
    def atualizar_dono(self,novo_dono):
        self.dono = novo_dono
    def get_dono(self):
        return self.dono
    def atualizar_imagem(self,path_imagem):
        self.imagem = self.carregar_imagem(path_imagem)

    def atualizar_dono(self,novo_dono):
        self.dono = novo_dono

    #métodos de desenho e debug
    def desenhar(self,tela,centralizar_na_casa,centralizar_em_xy):
        if not centralizar_em_xy and not centralizar_na_casa:
            tela.blit(self.imagem,(self.x,self.y))
        if centralizar_em_xy == True:
            tela.blit(self.imagem,(self.x-self.r,self.y-self.r))
        if centralizar_na_casa == True:
            tela.blit(self.imagem,(self.x+self.r,self.y+self.r))

    def debug(self):
        print("Dono:",self.dono)
        print("[x,y]:",[self.x,self.y])
        print("[l,c]:",[self.l,self.c])
        print("Raio:",self.r)
        print("[w,h]:",[self.w,self.h])

#Classe genérica que engloba atributos e métodos comuns às classes Banco e Base
class ComumBancoBase(ComumBancoBaseSoldado):
    #métodos de carregamento e inicialização
    def __init__(self,dono,status_ocupacao,valor,x,y,l,c,r,ocupante,path_imagem):
        super().__init__(dono,x,y,l,c,r,path_imagem)
        try:
            self.fonte = pygame.font.Font(PATH_FONTE_VALORES,TAM_FONTE_VALORES)
        except:
            print("Erro ao carregar fonte para Bases e Bancos!")
            pygame.quit()
            exit(1)
        self.status_ocupacao = status_ocupacao
        self.valor = valor
        self.ocupante = ocupante

    #métodos de atualização lógica
    def esta_ocupada(self):
        return self.status_ocupacao

    def atualizar_status_ocupacao(self,novo_status_ocupacao):
        self.status_ocupacao = novo_status_ocupacao

    def atualizar_valor(self,novo_valor):
        self.valor = novo_valor
    def get_valor(self):
        return self.valor
    def atualizar_ocupante(self,novo_ocupante):
        self.ocupante = novo_ocupante

    #métodos de desenho e debug
    def desenhar(self,tela):
        super().desenhar(tela,False,False)
        texto_superficie = self.fonte.render(str(self.valor),True,COR_TEXTO_VALORES)
        tela.blit(texto_superficie,(self.x,self.y))

    def debug(self):
        super().debug()
        print("ocupada?",self.status_ocupacao)
        print("ocupante:",self.ocupante)
        print("valor:",self.valor)
