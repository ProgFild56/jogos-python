from random import randrange
from classes_abstratas import *
from constantes import *

#Classe que define as bases de movimento comum no jogo
class Base(ComumBancoBase):
    #métodos de carregamento e inicialização
    def __init__(self,dono,status_ocupacao,x,y,l,c,r,ocupante,path_imagem,eh_fronteira):
        if not eh_fronteira:
            valor = randrange(VALOR_MINIMO_BASES,VALOR_MAXIMO_BASES)
            funcao = FUNCAO_BASE
        else:
            valor = randrange(VALOR_MINIMO_BASES*MULTIPLICADOR_FRONTEIRA,VALOR_MAXIMO_BASES*MULTIPLICADOR_FRONTEIRA)
            funcao = FUNCAO_FRONTEIRA

        super().__init__(dono,status_ocupacao,valor,x,y,l,c,r,ocupante,path_imagem)
        self.funcao = funcao

    #métodos de atualização lógica

    #métodos de desenho e debug
    def debug(self):
        print("-------------------Base-------------------")
        print("Função:",self.funcao)
        super().debug()
        print("-------------------Base-------------------")

#Classe que define os bancos no jogo (pontos onde se paralisa um soldado por n turnos em troca de dinheiro)
class Banco(ComumBancoBase):
    #métodos de carregamento e inicialização
    def __init__(self,dono,status_ocupacao,x,y,l,c,r,ocupante,path_imagem,qtde_turnos_exigidos):
        valor = VALOR_PADRAO_BANCOS
        super().__init__(dono,status_ocupacao,valor,x,y,l,c,r,ocupante,path_imagem)
        self.funcao = FUNCAO_BANCO
        self.qtde_turnos_exigidos = qtde_turnos_exigidos
        self.turno_ocupacao = None

    #métodos de atualização lógica
    def atualizar_qtde_turnos_exigidos(self,nova_qtde_turnos):
        self.qtde_turnos_exigidos = nova_qtde_turnos
    def liberado_para_movimento(self,turno_atual_jogo):
        if self.turno_ocupacao == None:
            return True
        elif turno_atual_jogo - self.turno_ocupacao >= self.qtde_turnos_exigidos:
            return True
        else:
            return False
    def zerar_turno_ocupacao(self):
        self.turno_ocupacao = None

    def definir_novo_turno_ocupacao(self,turno_atual_jogo):
        self.turno_ocupacao = turno_atual_jogo

    #métodos de desenho e debug
    def debug(self):
        print("-------------------Banco-------------------")
        print("Função:",self.funcao)
        super().debug()
        print("Turno da ocupação:",self.turno_ocupacao)
        print("Qtde de turnos exigidos:",self.qtde_turnos_exigidos)
        print("-------------------Banco-------------------")

#Classe que define os soldados no jogo
class Soldado(ComumBancoBaseSoldado):
    #métodos de carregamento e inicialização
    def __init__(self,dono,x,y,l,c,r,path_imagem):
        super().__init__(dono,x,y,l,c,r,path_imagem)

    #métodos de atualização lógica

    #métodos de desenho e debug
    def debug(self):
        print("-------------------Soldado-------------------")
        super().debug()
        print("-------------------Soldado-------------------")
