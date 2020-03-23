from os import system
from copy import deepcopy
from classes_derivadas_camada1 import *
from constantes import *

#variáveis globais que ajudam na movimentação de soldados do jogador pelo mouse
houve_selecao = False
soldado_selecionado = None
bases_possiveis_movimento = []

#variáveis globais que definem a máquina de estados da IA
ESTADO_ACUMULO =    1
ESTADO_AVANCO =     2
ESTADO_ATAQUE =     3
ESTADO_RANDOMICO =  4

base_fronteira_menor_custo = None
soldado_escolhido = None
ultimo_estado = None

def resetar_variaveis_controle(cursor_mouse):
    global houve_selecao
    global soldado_selecionado
    global bases_possiveis_movimento
    #reseto variáveis de controle
    cursor_mouse.atualizar_xy(POSX_PADRAO_CURSOR,POSY_PADRAO_CURSOR)
    houve_selecao = False
    soldado_selecionado = None
    bases_possiveis_movimento = []
def retornar_path_imagem_bases_jogador_ou_computador(dono):
    if dono == JOGADOR:
        return PATH_IMAGEM_BASE_JOGADOR
    elif dono == COMPUTADOR:
        return PATH_IMAGEM_BASE_COMPUTADOR

#Classe genérica que engloba atributos e métodos comuns aos Exércitos: Jogador  e Computador
class Exercito:
    #métodos de carregamento e inicialização
    def __init__(self,dono,qtde_soldados,qtde_moedas,path_imagem_soldados):
        self.dono = dono
        self.qtde_soldados  = qtde_soldados
        self.qtde_moedas = qtde_moedas
        self.path_imagem_soldados = path_imagem_soldados
        self.soldados = self.criar_exercito()
    def criar_exercito(self):
        soldados = []
        posx = 0
        posy  = 528

        for i in range(self.qtde_soldados):

            if self.dono == JOGADOR:
                linha = 8
                posy = 512
            elif self.dono == COMPUTADOR:
                linha = 0
                posy = 0

            s = Soldado(dono=self.dono,x=posx,y=posy,l=linha,c=i,r=RAIO_SOLDADOS,path_imagem=self.path_imagem_soldados)
            soldados.append(s)
            posx = ((i+1) * (RAIO_BANCO_BASE * 2))


        return soldados

    #métodos de atualização lógica
    def retorna_bases_possiveis_movimento(self,bases_territorio,soldado_selecionado,turno_atual_jogo):
        bases_possiveis_movimento = []
        for base in bases_territorio:
            #busco base acima do soldado selecionado
            if base.funcao == FUNCAO_BANCO:
                if base.liberado_para_movimento(turno_atual_jogo):
                    if base.l == soldado_selecionado.l - 1 and base.c == soldado_selecionado.c and base.status_ocupacao == False:
                        bases_possiveis_movimento.append(base)
                    #busco base à direita do soldado selecionado
                    if base.l == soldado_selecionado.l and base.c == soldado_selecionado.c + 1 and base.status_ocupacao == False:
                        bases_possiveis_movimento.append(base)
                    #busco base abaixo do soldado selecionado
                    if base.l == soldado_selecionado.l + 1 and base.c == soldado_selecionado.c and base.status_ocupacao == False:
                        bases_possiveis_movimento.append(base)
                    #busco base à esquerda do soldado selecionado
                    if base.l == soldado_selecionado.l and base.c == soldado_selecionado.c - 1 and base.status_ocupacao == False:
                        bases_possiveis_movimento.append(base)
            else:
                if base.l == soldado_selecionado.l - 1 and base.c == soldado_selecionado.c and base.status_ocupacao == False:
                    bases_possiveis_movimento.append(base)
                #busco base à direita do soldado selecionado
                if base.l == soldado_selecionado.l and base.c == soldado_selecionado.c + 1 and base.status_ocupacao == False:
                    bases_possiveis_movimento.append(base)
                #busco base abaixo do soldado selecionado
                if base.l == soldado_selecionado.l + 1 and base.c == soldado_selecionado.c and base.status_ocupacao == False:
                    bases_possiveis_movimento.append(base)
                #busco base à esquerda do soldado selecionado
                if base.l == soldado_selecionado.l and base.c == soldado_selecionado.c - 1 and base.status_ocupacao == False:
                    bases_possiveis_movimento.append(base)

        return bases_possiveis_movimento
    def distancia_pontos(self,x1,y1,x2,y2):
        return float(((x2-x1)**2 + (y2-y1)**2)) ** 0.5
    def retornar_base_onde_soldado_esta(self,soldado,bases_territorio):
        for base in bases_territorio:
            if base.l == soldado.l and base.c == soldado.c:
                return base
        return None
    def faturar_movimento(self,exercito_inimigo,soldado,base,direcao_movimento=""):
        #se o movimento do soldado do jogador for em territorio próprio
        if soldado.dono == JOGADOR and base.dono == JOGADOR:
            if base.funcao != FUNCAO_BANCO:
                if direcao_movimento == "acima" or direcao_movimento == "esquerda":
                    self.decrementar_qtde_moedas(base.valor)
                elif direcao_movimento == "abaixo" or direcao_movimento == "direita":
                    self.incrementar_qtde_moedas(base.valor)
            else:
                self.incrementar_qtde_moedas(base.valor)
        #se o movimento do soldado do computador for em territorio próprio
        elif soldado.dono == COMPUTADOR and base.dono == COMPUTADOR:
            if base.funcao != FUNCAO_BANCO:
                if direcao_movimento == "abaixo" or direcao_movimento == "direita":
                    self.decrementar_qtde_moedas(base.valor)
                elif direcao_movimento == "acima" or direcao_movimento == "esquerda":
                    self.incrementar_qtde_moedas(base.valor)
            else:
                self.incrementar_qtde_moedas(base.valor)
        #se o soldado está se movendo para uma base na fronteira ou em territorio inimigo
        elif (soldado.dono == JOGADOR and base.dono == COMPUTADOR or base.dono == NEUTRO) or (soldado.dono == COMPUTADOR and base.dono == JOGADOR or base.dono == NEUTRO) :
            if base.funcao != FUNCAO_BANCO:
                #qualquer movimento em territorio inimigo que não seja para um banco decrementa moedas do exercito que está se movendo
                self.decrementar_qtde_moedas(base.valor)
                #caso o movimento se dê apenas em territorio inimigo (não em fronteira) decremento tbm as moedas do exercito inimigo
                if base.funcao != FUNCAO_FRONTEIRA:
                    exercito_inimigo.decrementar_qtde_moedas(base.valor)
            #independente de territorio, movimento para bancos sempre incrementam as moedas de quem está se movendo
            else:
                self.incrementar_qtde_moedas(base.valor)
    def atualizar_dados_base_soldado(self,soldado_a_mover,base_alvo):
        soldado_a_mover.atualizar_xy(base_alvo.get_xy()[0],base_alvo.get_xy()[1])
        soldado_a_mover.atualizar_lc(base_alvo.get_lc()[0],base_alvo.get_lc()[1])
        base_alvo.atualizar_status_ocupacao(True)
        base_alvo.atualizar_ocupante(soldado_a_mover.dono)
    def posicionar_soldado_na_base(self,exercito_inimigo,soldado,base,turno_atual_jogo):
        l_anterior_soldado,c_anterior_soldado = soldado.get_lc()
        self.atualizar_dados_base_soldado(soldado,base)
        if base.funcao == FUNCAO_BANCO:
            #defino banco como ocupado no turno atual
            base.definir_novo_turno_ocupacao(turno_atual_jogo)
            #print("TURNO OCUPACAO BANCO:",base.turno_ocupacao)
            #aplico o incremento de investimento dos bancos
            self.faturar_movimento(exercito_inimigo=exercito_inimigo,soldado=soldado,base=base)
        else:
            #busco a direcao de movimento
            if soldado.l - l_anterior_soldado < 0:
                direcao = "acima"
            elif soldado.l - l_anterior_soldado > 0:
                direcao = "abaixo"
            elif soldado.c - c_anterior_soldado < 0:
                direcao = "esquerda"
            elif soldado.c - c_anterior_soldado > 0:
                direcao = "direita"
            else:
                direcao = ""

            if direcao != "":
                #faturo o movimento feito pelo soldado
                self.faturar_movimento(exercito_inimigo=exercito_inimigo,soldado=soldado,base=base,direcao_movimento=direcao)
    def soldado_pode_se_mover(self,soldado,bases_territorio,turno_atual_jogo):
        base_soldado = self.retornar_base_onde_soldado_esta(soldado,bases_territorio)
        if base_soldado != None:
            #está em um banco e não está mais paralisado por ele
            if base_soldado.funcao == FUNCAO_BANCO and base_soldado.liberado_para_movimento(turno_atual_jogo):
                return True
            #está em uma base comum
            elif base_soldado.funcao != FUNCAO_BANCO:
                return True
            #está em um banco, porém ainda se encontra preso nele
            else:
                return False
        else:
            print("Erro ao tentar encontrar soldado no tabuleiro!")
            pygame.quit()
            exit(1)
    def incrementar_qtde_moedas(self,incremento_moedas):
        self.qtde_moedas += incremento_moedas
    def decrementar_qtde_moedas(self,decremento_moedas):
        if self.qtde_moedas - decremento_moedas >= 0:
            self.qtde_moedas -= decremento_moedas
        else:
            self.qtde_moedas = 0
    def get_qtde_moedas(self):
        return self.qtde_moedas
    def ficou_insolvente(self):
        return self.get_qtde_moedas() <= 0

    #métodos de desenho e debug
    def desenhar(self,tela):
        for soldado in self.soldados:
            soldado.desenhar(tela,True,False)
    def debug(self):
        print("----------------------EXÉRCITO----------------------")
        for soldado in self.soldados:
            soldado.debug()
        print("----------------------EXÉRCITO----------------------")

#Classe que define atributos e métodos do exército do jogador
class ExercitoJogador(Exercito):
    #métodos de carregamento e inicialização
    def __init__(self):
        super().__init__(JOGADOR,QTDE_SOLDADOS_EXERCITOS,QTDE_MOEDAS_JOGADOR,PATH_IMAGEM_SOLDADOS_JOGADOR)

    #métodos de atualização lógica
    def retorna_soldado_selecionado_pelo_mouse(self):
        pos_mouse = pygame.mouse.get_pos()
        for soldado in self.soldados:
            if pygame.mouse.get_pressed()[0] and (soldado.x < pos_mouse[0] < (soldado.x + soldado.w)) and (soldado.y < pos_mouse[1] < (soldado.y + soldado.h)):
                return soldado
        return None
    def move_soldado(self,exercito_inimigo,soldado_selecionado,cursor_mouse,bases_possiveis,turno_atual_jogo):
        if len(bases_possiveis) > 0:
            distancias = []
            for base in bases_possiveis:
                pos_cursor_mousex,pos_cursor_mousey = cursor_mouse.get_xy()
                pos_basex,pos_basey = base.get_xy()
                dist = self.distancia_pontos(pos_basex,pos_basey,pos_cursor_mousex,pos_cursor_mousey)
                distancias.append((base,dist))

            #procuro a possibilidade com menor distancia do cursor do mouse
            base_menor_distancia = distancias[0]
            #system("clear")
            #print("*"*25,"CASAS POSSÍVEIS","*"*25)
            for base_dist in distancias:
            #    print("Distancia até o cursor:",base_dist[1])
            #    base_dist[0].debug()
                if base_dist[1] < base_menor_distancia[1]:
                    base_menor_distancia = base_dist


            #posiciono o soldado selecionado na base encontrada
            self.posicionar_soldado_na_base(exercito_inimigo,soldado_selecionado,base_menor_distancia[0],turno_atual_jogo)
            return True
        else:
            return False
    def jogar(self,exercito_inimigo,bases_territorio,cursor_mouse,turno_atual_jogo):
        global houve_selecao
        global soldado_selecionado
        global bases_possiveis_movimento
        moveu = False
        #print("??",houve_selecao)
        if not houve_selecao:

            soldado_selecionado = self.retorna_soldado_selecionado_pelo_mouse()
            if soldado_selecionado != None:
                houve_selecao = True
                bases_possiveis_movimento = self.retorna_bases_possiveis_movimento(bases_territorio,soldado_selecionado,turno_atual_jogo)
        else:
            #print("houve selecao")
            pos_mouse = pygame.mouse.get_pos()
            cursor_mouse.atualizar_xy(pos_mouse[0],pos_mouse[1])
            #se em algum momento o mouse é solto e havia um soldado selecionado
            if not pygame.mouse.get_pressed()[0]:
                if self.soldado_pode_se_mover(soldado_selecionado,bases_territorio,turno_atual_jogo):
                    moveu = self.move_soldado(exercito_inimigo,soldado_selecionado,cursor_mouse,bases_possiveis_movimento,turno_atual_jogo)

                resetar_variaveis_controle(cursor_mouse)

        return moveu

    #métodos de desenho e debug

#Classe que define a Inteligência Artificial do computador
class IA:
    def __init__(self):
        #IA comeca em estado acúmulo de moedas
        self.estado_ia = ESTADO_ACUMULO
    def subtrair_vetores(self,v1,v2):
        return [v1[0]-v2[0] , v1[1]-v2[1]]
    def somar_vetores(self,v1,v2):
        return (v1[0]+v2[0] , v1[1]+v2[1])
    def mudar_estado_ia(self,novo_estado_ia):
        self.estado_ia = novo_estado_ia
    def jogada_com_bonus(self,soldado,base):
        #se soldado do computador esta voltando ou indo pra sua direita e em seu próprio territorio ou se estiver se movendo para um banco qualquer é bônus
        return ( ( (soldado.l > base.l) or (soldado.c > base.c) ) and (base.dono == COMPUTADOR) ) or (base.funcao == FUNCAO_BANCO)
    def retornar_base_a_partir_de_lc(self,bases_territorio,l,c):
        for base in bases_territorio:
            if base.l == l and base.c == c:
                return base
        return None
    def retornar_base_a_partir_de_lc(self,bases_territorio,l,c):
        for base in bases_territorio:
            if base.l == l and base.c == c:
                return base
        return None
    def retornar_vetor_incremento(self,vetor_distancia):
        print("VDIST",vetor_distancia)
        vetor_incremento = [0,0]
        #se eu estiver a 1 linha do alvo e nao estiver ainda na coluna do alvo
        if vetor_distancia[0] == 1 and vetor_distancia[1] > 0:
            vetor_incremento[0] = 0
            vetor_incremento[1] = 1

        elif vetor_distancia[0] == 1 and vetor_distancia[1] < 0:
            vetor_incremento[0] = 0
            vetor_incremento[1] = -1

        elif vetor_distancia[0] == 1 and vetor_distancia[1] == 0:
            vetor_incremento[0] = 1
            vetor_incremento[1] = 0

        elif vetor_distancia[0] > 0:
            vetor_incremento[0] = 1

        elif vetor_distancia[0] < 0:
            vetor_incremento[0] = -1

        elif vetor_distancia[1] > 0:
            vetor_incremento[1] = 1

        elif vetor_distancia[1] < 0:
            vetor_incremento[1] = -1


        return vetor_incremento
    def retornar_custo_total_vetor(self,partida,vetor_distancia,alvo,bases_territorio):
        #-v[0] -> bonus -> computador recua
        #+v[0] -> onus -> computador avança
        #-v[1] -> bonus -> computador move-se para sua direita
        #+v[1] -> onus -> computador move-se para sua esquerda

        cursor = list(partida)
        custo_total_vetor = 0.00
        vetor_incremento = self.retornar_vetor_incremento(vetor_distancia)

        for qtde_linhas_percorridas in range(abs(vetor_distancia[0])):
            cursor  = self.somar_vetores(cursor,vetor_incremento)
            print(cursor)
            base_onde_esta_o_cursor = self.retornar_base_a_partir_de_lc(bases_territorio,cursor[0],cursor[1])
            if base_onde_esta_o_cursor != None:
                if base_onde_esta_o_cursor.funcao != FUNCAO_BANCO:
                    #onus
                    if vetor_incremento[0] == 1:
                        custo_total_vetor += base_onde_esta_o_cursor.get_valor()
                    #bonus
                    elif vetor_incremento[0] == -1:
                         custo_total_vetor -= base_onde_esta_o_cursor.get_valor()
                else:
                    #puno essa possibilidade de jogada com um custo surreal caso ela seja inviavel
                    #caminhos que passem por bancos são inviaveis para estrategia de avanco da IA
                    custo_total_vetor += 1000000000
            else:
                #puno essa possibilidade de jogada com um custo surreal caso ela seja inviavel
                custo_total_vetor += 1000000000


        for qtde_colunas_percorridas in range(abs(vetor_distancia[1])):
            cursor  = self.somar_vetores(cursor,vetor_incremento)
            base_onde_esta_o_cursor = self.retornar_base_a_partir_de_lc(bases_territorio,cursor[0],cursor[1])
            if base_onde_esta_o_cursor != None:
                if base_onde_esta_o_cursor.funcao != FUNCAO_BANCO:
                    #onus
                    if vetor_incremento[1] == 1:
                        custo_total_vetor += base_onde_esta_o_cursor.get_valor()
                    #bonus
                    elif vetor_incremento[1] == -1:
                         custo_total_vetor -= base_onde_esta_o_cursor.get_valor()
                else:
                    #puno essa possibilidade de jogada com um custo surreal caso ela seja inviavel
                    #caminhos que passem por bancos são inviaveis para estrategia de avanco da IA
                    custo_total_vetor += 1000000000
            else:
                #puno essa possibilidade de jogada com um custo surreal caso ela seja inviavel
                custo_total_vetor += 1000000000


        return custo_total_vetor
    def retornar_todas_jogadas_possiveis_computador(self,exercito_computador,bases_territorio,turno_atual_jogo):
        pares_soldado_bases_possiveis = []
        for soldado in exercito_computador.soldados:
            #verifica se o soldado pode ser movido (talvez esteja em um banco esperando tempo de investimento)
            if exercito_computador.soldado_pode_se_mover(soldado,bases_territorio,turno_atual_jogo):
                #pego as possibilidades de jogada
                bases_possiveis = exercito_computador.retorna_bases_possiveis_movimento(bases_territorio,soldado,turno_atual_jogo)

                #se tem como jogar com o soldado
                if len(bases_possiveis) > 0:
                    for base in bases_possiveis:
                        #adiciono essa jogada às minhas possibilidades de jogada
                        pares_soldado_bases_possiveis.append({"soldado":soldado,"base":base})


        return pares_soldado_bases_possiveis
    def retornar_jogadas_na_fronteira(self,jogadas_possiveis,exercito_computador,bases_territorio):
        jogadas_na_fronteira = []
        for jogada in jogadas_possiveis:
            soldado = jogada["soldado"]
            base_soldado = exercito_computador.retornar_base_onde_soldado_esta(soldado,bases_territorio)
            base_alvo_na_jogada = jogada["base"]
            if base_soldado.funcao == FUNCAO_FRONTEIRA and base_alvo_na_jogada.funcao != FUNCAO_FRONTEIRA and base_alvo_na_jogada.esta_ocupada() == False and base_alvo_na_jogada.get_dono() == JOGADOR:
                jogadas_na_fronteira.append(jogada)

        return jogadas_na_fronteira
    def retornar_jogadas_em_territorio_inimigo_para_ataque(self,jogadas_possiveis,exercito_computador,bases_territorio):
        jogadas_territorio_inimigo = []
        for jogada in jogadas_possiveis:
            soldado = jogada["soldado"]
            base_soldado = exercito_computador.retornar_base_onde_soldado_esta(soldado,bases_territorio)
            base_alvo_na_jogada = jogada["base"]
            if base_alvo_na_jogada.dono == JOGADOR and base_alvo_na_jogada.funcao != FUNCAO_BANCO and base_alvo_na_jogada.esta_ocupada() == False:
                jogadas_territorio_inimigo.append(jogada)

        return jogadas_territorio_inimigo + self.retornar_jogadas_na_fronteira(jogadas_possiveis,exercito_computador,bases_territorio)
    def resetar_variaveis_controle_maquina_estado(self):
        global base_fronteira_menor_custo
        global soldado_escolhido


        base_fronteira_menor_custo = None
        soldado_escolhido = None
    def estado_acumulo(self,exercito_computador,exercito_inimigo,bases_territorio,turno_atual_jogo):
        global ultimo_estado

        #marco ultimo estado
        ultimo_estado = ESTADO_ACUMULO

        #pego todas as possibilidades de jogadas do computador
        jogadas_possiveis = self.retornar_todas_jogadas_possiveis_computador(exercito_computador,bases_territorio,turno_atual_jogo)
        #divido todas as jogadas possíveis em duas listas: jogadas_com_bonus,jogadas_com_onus
        jogadas_com_bonus = []
        jogadas_com_onus = []

        for par_s_bp in jogadas_possiveis:
            if self.jogada_com_bonus(par_s_bp['soldado'],par_s_bp['base']):
                jogadas_com_bonus.append(par_s_bp)
            else:
                jogadas_com_onus.append(par_s_bp)

        #se existe alguma jogada com bonus
        if len(jogadas_com_bonus) > 0:
            #procuro a jogada de maior bonus
            jogada_maior_bonus = {"soldado":None,"base":None,"bonus":-1}
            for jogada in jogadas_com_bonus:
                if jogada["base"].valor > jogada_maior_bonus["bonus"]:
                    jogada_maior_bonus = {"soldado":jogada["soldado"],"base":jogada["base"],"bonus":jogada["base"].get_valor()}

            #executo a jogada
            exercito_computador.posicionar_soldado_na_base(exercito_inimigo,jogada_maior_bonus["soldado"],jogada_maior_bonus["base"],turno_atual_jogo)
            #informo ao jogo que computador jogou
            return True

        #se nao existe jogadas com bonus, mas existe jogadas com onus
        elif len(jogadas_com_onus) > 0:
            #busco jogadas onde soldado esteja em posicao de ataque (na fronteira ou em territorio inimigo)
            jogadas_ataque = self.retornar_jogadas_em_territorio_inimigo_para_ataque(jogadas_possiveis,exercito_computador,bases_territorio)

            #se existe possibilidade de ataque ao inimigo
            if len(jogadas_ataque) > 0:
                #mudo o estado da IA para o ESTADO_ATAQUE
                self.mudar_estado_ia(ESTADO_ATAQUE)
                #informo ao jogo que computador ainda não jogou (proximo frame ele jogara já no novo estado ESTADO_ATAQUE)
                return False

            #se nas jogadas com ônus não existe ao menos um soldado apto a atacar o inimigo
            else:
                #mudo o estado da IA para ESTADO_AVANCO
                self.mudar_estado_ia(ESTADO_AVANCO)
                #informo ao jogo que computador ainda não jogou (proximo frame ele jogara já no novo estado ESTADO_AVANCO)
                return False

        #se nao há jogadas possiveis
        else:
            #mudo o estado da IA para ESTADO_AVANCO
            self.mudar_estado_ia(ESTADO_AVANCO)

            #computador pula turno (apos pular o turno ele tenta avancar)
            return True
    def estado_avanco(self,exercito_computador,exercito_inimigo,bases_territorio,turno_atual_jogo):
        global ultimo_estado
        global soldado_escolhido
        global base_fronteira_menor_custo

        #busco possibilidades de jogada atacando
        jogadas_possiveis = self.retornar_todas_jogadas_possiveis_computador(exercito_computador,bases_territorio,turno_atual_jogo)
        jogadas_ataque = self.retornar_jogadas_em_territorio_inimigo_para_ataque(jogadas_possiveis,exercito_computador,bases_territorio)

        #se existe ao menos uma possibilidade de jogar atacando
        if len(jogadas_ataque) > 0:
            #reseto variaveis globais de controle do estado ESTADO_AVANCO
            self.resetar_variaveis_controle_maquina_estado()
            #mudo o estado da IA para ESTADO_ATAQUE
            self.mudar_estado_ia(ESTADO_ATAQUE)
            #informo ao jogo que computado ainda não jogou (jogará no próximo frame já no ESTADO_ATAQUE)
            return False

        #não existe possibilidade de ataque e o computador possui poucas moedas e ele não veio do ESTADO_ACUMULO
        elif exercito_computador.get_qtde_moedas() < QTDE_MOEDAS_VOLTAR_ACUMULAR and ultimo_estado != ESTADO_ACUMULO:
            #reseto variaveis globais de controle do estado ESTADO_AVANCO
            self.resetar_variaveis_controle_maquina_estado()
            #Mudo estado para ESTADO_ACUMULO
            self.mudar_estado_ia(ESTADO_ACUMULO)
            #informo ao jogo que computador ainda não jogou (próximo frame ele entra no estado acúmulo)
            return False

        #computador está em condicoes de iniciar rotinas do estado ESTADO_AVANCO
        else:
            #se eu ainda não fiz os cálculos das minhas variaveis globais de controle
            if base_fronteira_menor_custo == None  or soldado_escolhido == None:
                #busco a base da fronteira com menor custo de penetração
                menor_custo = (VALOR_MAXIMO_BASES * MULTIPLICADOR_FRONTEIRA) ** 2
                for base in bases_territorio:
                    if base.funcao == FUNCAO_FRONTEIRA and base.valor < menor_custo:
                        base_aux = base
                        menor_custo = base.valor

                #salvo essa base de menor custo na fronteira encontrada anteriormente
                base_fronteira_menor_custo = base_aux

                #crio vetores de distancia em l e em c para cada soldado ate essa base encontrada
                pares_soldado_vetor_distancia = []
                for soldado in exercito_computador.soldados:
                    lc_base = tuple(base_fronteira_menor_custo.get_lc())
                    lc_soldado = tuple(soldado.get_lc())
                    vet_dist = self.subtrair_vetores(lc_base,lc_soldado)

                    pares_soldado_vetor_distancia.append({"vetor":vet_dist,"soldado":soldado})

                #pego o melhor vetor distancia possivel com base em seu custo total (escolho o soldado que esta no caminho menos oneroso até a base fronteira de menor custo de penetração)
                par_vetor_menor_custo = {"vetor":None,"soldado":None,"custo_total":100000000000}
                for par_vet_dist in pares_soldado_vetor_distancia:
                    soldado = par_vet_dist["soldado"]
                    partida = tuple(soldado.get_lc())
                    vetor_distancia = par_vet_dist["vetor"]
                    custo_total_vetor = self.retornar_custo_total_vetor(partida=partida,vetor_distancia=vetor_distancia,alvo=base_fronteira_menor_custo,bases_territorio=bases_territorio)
                    if custo_total_vetor < par_vetor_menor_custo["custo_total"]:
                        par_vetor_menor_custo = {"vetor":vetor_distancia,"soldado":soldado,"custo_total":custo_total_vetor}

                #marco o soldado escolhido e seu respectivo vetor distancia até a base na fronteira de menor custo
                soldado_escolhido = par_vetor_menor_custo["soldado"]

                #informo ao jogo que computador ainda não jogou (apenas fez os calculos necessarios para jogar no proximo frame)
                return False

            #uma vez feito os cálculos das variáveis globais de controle
            else:
                #marco ultimo estado
                ultimo_estado = ESTADO_AVANCO


                #pego a base onde o soldado escolhido para movimento se encontra
                base_soldado = exercito_computador.retornar_base_onde_soldado_esta(soldado_escolhido,bases_territorio)

                #pego o vetor da posicao da base_soldado
                vetor_base_soldado = tuple(base_soldado.get_lc())

                #pego o vetor da posicao da fronteira de menor custo de invasão
                vetor_pos_base_fronteira = tuple(base_fronteira_menor_custo.get_lc())

                #pego o vetor distancia entre o soldado e a base_fronteira_menor_custo
                vetor_distancia_soldado_base_fronteira = self.subtrair_vetores(vetor_pos_base_fronteira,vetor_base_soldado)

                #pego o vetor incremento
                vetor_incremento = self.retornar_vetor_incremento(vetor_distancia_soldado_base_fronteira)



                print("VINC",vetor_incremento)

                #calculo a nova base do soldado após movimento definido por vetor_incremento
                vetor_base_a_ocupar = self.somar_vetores(vetor_base_soldado,vetor_incremento)

                #pego a base correspondente à posição encontrada em vetor_base_a_ocupar
                base_alvo = self.retornar_base_a_partir_de_lc(bases_territorio,vetor_base_a_ocupar[0],vetor_base_a_ocupar[1])

                #caso a IA esteja tentando avancar com um soldado cuja passagem esteja bloqueada
                if base_alvo.l == soldado_escolhido.l and base_alvo.c == soldado_escolhido.c:
                    #mudo para ESTADO_RANDOMICO
                    self.mudar_estado_ia(ESTADO_RANDOMICO)
                    #informo ao jogo que computador ainda não jogou (jogara de forma randomica no proximo frame)
                    return False

                #posiciono o soldado escolhido na base alvo encontrada (movimento de fato)
                exercito_computador.posicionar_soldado_na_base(exercito_inimigo,soldado_escolhido,base_alvo,turno_atual_jogo)
                print("POSICIONOU SOLDADO:",base_alvo.get_lc())

                #informo ao jogo que computador jogou
                return True
    def estado_ataque(self,exercito_computador,exercito_inimigo,bases_territorio,turno_atual_jogo):
        global ultimo_estado

        #se não vim do estado ESTADO_ACUMULO e tenho poucas moedas
        if ultimo_estado != ESTADO_ACUMULO and exercito_computador.get_qtde_moedas() < QTDE_MOEDAS_VOLTAR_ACUMULAR:
            self.mudar_estado_ia(ESTADO_ACUMULO)
            return False
        #busco atacar
        else:
            jogadas_possiveis = self.retornar_todas_jogadas_possiveis_computador(exercito_computador,bases_territorio,turno_atual_jogo)
            jogadas_ataque = self.retornar_jogadas_em_territorio_inimigo_para_ataque(jogadas_possiveis,exercito_computador,bases_territorio)

            #existe a possibilidade de atacar o territorio inimigo
            if len(jogadas_ataque) > 0:
                print("QTDE JOGADAS POSSIVEIS TOTAL:",len(jogadas_possiveis))
                print("QTDE JOGADAS ATAQUE:",len(jogadas_ataque))

                #marco ultimo estado
                ultimo_estado = ESTADO_ATAQUE

                #busco a jogada de maior onus
                jogada_maior_onus = None
                maior_onus = -10000000
                for jogada in jogadas_ataque:
                    onus_jogada = jogada["base"].get_valor()
                    if onus_jogada > maior_onus and jogada["base"].funcao != FUNCAO_FRONTEIRA and jogada["base"].dono == JOGADOR :
                        jogada_maior_onus = jogada
                        maior_onus = onus_jogada

                #jogo de fato
                if jogada_maior_onus != None:
                    soldado = jogada_maior_onus["soldado"]
                    base_alvo = jogada_maior_onus["base"]
                    exercito_computador.posicionar_soldado_na_base(exercito_inimigo,soldado,base_alvo,turno_atual_jogo)

                    #informo ao jogo que o computador jogou
                    return True

                #não é possível atacar o inimigo
                else:
                    #mudo estado para ESTADO_RANDOMICO
                    self.mudar_estado_ia(ESTADO_RANDOMICO)
                    #informo ao jogo que computador ainda nao jogou (jogara no estado ESTADO_RANDOMICO no proximo frame)
                    return False

            #não é possível atacar o inimigo
            else:
                #mudo estado para ESTADO_RANDOMICO
                self.mudar_estado_ia(ESTADO_RANDOMICO)
                #informo ao jogo que computador ainda nao jogou (jogara no estado ESTADO_RANDOMICO no proximo frame)
                return False
    def estado_randomico(self,exercito_computador,exercito_inimigo,bases_territorio,turno_atual_jogo):
        global ultimo_estado

        #seleciono aleatoriamente um soldado
        randmin,randmax = 0,len(exercito_computador.soldados)
        soldado_sorteado = exercito_computador.soldados[randrange(randmin,randmax)]
        #verifica se o soldado sorteado pode ser movido (talvez esteja em um banco esperando tempo de investimento)
        if exercito_computador.soldado_pode_se_mover(soldado_sorteado,bases_territorio,turno_atual_jogo):
            #pego as possibilidades de jogada
            bases_possiveis = exercito_computador.retorna_bases_possiveis_movimento(bases_territorio,soldado_sorteado,turno_atual_jogo)
            #se tem como jogar com o soldado sorteado
            if len(bases_possiveis) > 0:
                #sorteio uma jogada aleatória
                base_escolhida = bases_possiveis[randrange(0,len(bases_possiveis))]
                #posiciono o soldado na base
                exercito_computador.posicionar_soldado_na_base(exercito_inimigo,soldado_sorteado,base_escolhida,turno_atual_jogo)

                #mudo estado para ESTADO_AVANCO
                self.mudar_estado_ia(ESTADO_AVANCO)

                #informo ao jogo que o computador jogou
                return True

        #computador continua em modo randomico enquanto nao achar uma jogada que de certo
        return False

    def jogar(self,exercito_computador,exercito_inimigo,bases_territorio,turno_atual_jogo):
        self.debug()

        #a IA possui uma máquina de estados com 4 estados: acúmulo, avanço, ataque e randomico
        if self.estado_ia == ESTADO_ACUMULO:
            #Estratégia: Buscar sempre movimentos com bônus
            jogou = self.estado_acumulo(exercito_computador,exercito_inimigo,bases_territorio,turno_atual_jogo)
            return jogou

        elif self.estado_ia == ESTADO_AVANCO:
            #Estratégia: Buscar o caminho que teoricamente possui um dos menores custos possíveis até a fronteira com menor custo de penetração
            jogou = self.estado_avanco(exercito_computador,exercito_inimigo,bases_territorio,turno_atual_jogo)
            return jogou

        elif self.estado_ia == ESTADO_ATAQUE:
            #Estratégia: Mover-se no territorio inimigo buscando pelas bases mais onerosas possiveis (buscando zerar o inimigo)
            jogou = self.estado_ataque(exercito_computador,exercito_inimigo,bases_territorio,turno_atual_jogo)
            return jogou

        elif self.estado_ia == ESTADO_RANDOMICO:
            jogou = self.estado_randomico(exercito_computador,exercito_inimigo,bases_territorio,turno_atual_jogo)
            return jogou

    def debug(self):
        print("*"*23,"IA","*"*23)
        if self.estado_ia == ESTADO_ACUMULO:
            print("Estado IA: ESTADO_ACUMULO")
        elif self.estado_ia == ESTADO_AVANCO:
            print("Estado IA: ESTADO_AVANCO")
        elif self.estado_ia == ESTADO_ATAQUE:
            print("Estado IA: ESTADO_ATAQUE")
        elif self.estado_ia == ESTADO_RANDOMICO:
            print("Estado IA: ESTADO_RANDOMICO")
        print("*"*50)

#Classe que define atributos e métodos do exército controlado pelo computador (IA)
class ExercitoComputador(Exercito):
    #métodos de carregamento e inicialização
    def __init__(self,qtde_moedas):
        super().__init__(COMPUTADOR,QTDE_SOLDADOS_EXERCITOS,qtde_moedas,PATH_IMAGEM_SOLDADOS_COMPUTADOR)
        self.ia = IA()

    #métodos de atualização lógica
    #LEMBRAR DE IMPLEMENTAR TBM UMA FORMA DO COMPUTADOR PULAR TURNO CASO DEMORE PARA ENCONTRAR UMA JOGADA
    def jogar(self,exercito_inimigo,bases_territorio,turno_atual_jogo,usar_ia=False):
        if not usar_ia:
            #seleciono aleatoriamente um soldado
            randmin,randmax = 0,len(self.soldados)
            soldado_sorteado = self.soldados[randrange(randmin,randmax)]
            #verifica se o soldado sorteado pode ser movido (talvez esteja em um banco esperando tempo de investimento)
            if self.soldado_pode_se_mover(soldado_sorteado,bases_territorio,turno_atual_jogo):
                #pego as possibilidades de jogada
                bases_possiveis = self.retorna_bases_possiveis_movimento(bases_territorio,soldado_sorteado,turno_atual_jogo)
                #se tem como jogar com o soldado sorteado
                if len(bases_possiveis) > 0:
                    #sorteio uma jogada aleatória
                    base_escolhida = bases_possiveis[randrange(0,len(bases_possiveis))]
                    #posiciono o soldado na base
                    self.posicionar_soldado_na_base(exercito_inimigo,soldado_sorteado,base_escolhida,turno_atual_jogo)
                    return True

        else:
            jogou = self.ia.jogar(exercito_computador=self,exercito_inimigo=exercito_inimigo,bases_territorio=bases_territorio,turno_atual_jogo=turno_atual_jogo)
            return jogou

        return False

    #métodos de desenho e debug

#Classe que define o que compõe cada território incluindo bases (computador e jogador), bancos e fronteira (região neutra)
class Territorio:
    #métodos de carregamento e inicialização
    def __init__(self):
        self.bases_territorio = self.cria_bases_territorio()
    def cria_bases_territorio(self):
        bases_territorio = []
        base_auxiliar = None
        dono = None
        ocupacao = False
        raio = RAIO_BANCO_BASE
        ocupante = None
        path_img = None


        for l in range(QTDE_LINHAS_TERRITORIO):
            posy = l * (RAIO_BANCO_BASE * 2)
            for c in range(QTDE_COLUNAS_TERRITORIO):
                eh_fronteira = False
                posx = c * (RAIO_BANCO_BASE * 2)
                eh_banco = False

                #FRONTEIRA
                if l == LINHA_DIVISORIA_TERRITORIOS and c != QTDE_COLUNAS_TERRITORIO-1:
                    ocupacao = False
                    dono = NEUTRO
                    ocupante = NEUTRO
                    path_img = PATH_IMAGEM_BASE_FRONTEIRA
                    eh_fronteira = True
                #TERRITORIO DO COMPUTADOR
                elif l < LINHA_DIVISORIA_TERRITORIOS  and c != QTDE_COLUNAS_TERRITORIO-1:
                    dono = COMPUTADOR
                    path_img = PATH_IMAGEM_BASE_COMPUTADOR

                    if l == 0:
                        ocupacao = True
                        ocupante = COMPUTADOR
                    else:
                        ocupacao = False
                        ocupante = NEUTRO
                #TERRITORIO DO JOGADOR
                elif l > LINHA_DIVISORIA_TERRITORIOS and c != QTDE_COLUNAS_TERRITORIO-1:
                    dono = JOGADOR
                    path_img = PATH_IMAGEM_BASE_JOGADOR
                    if l == QTDE_LINHAS_TERRITORIO-1:
                        ocupacao = True
                        ocupante = JOGADOR
                    else:
                        ocupacao = False
                        ocupante = NEUTRO
                #BANCOS
                elif c == QTDE_COLUNAS_TERRITORIO-1 and l != LINHA_DIVISORIA_TERRITORIOS:
                    ocupacao = False
                    dono = NEUTRO
                    ocupante = NEUTRO
                    path_img = PATH_IMAGEM_BANCO
                    eh_banco = True
                else:
                    continue
                if not eh_banco:
                    base_auxiliar = Base(dono=dono,status_ocupacao=ocupacao,x=posx,y=posy,l=l,c=c,r=raio,ocupante=ocupante,path_imagem=path_img,eh_fronteira = eh_fronteira)
                else:
                    base_auxiliar = Banco(dono=dono,status_ocupacao=ocupacao,x=posx,y=posy,l=l,c=c,r=raio,ocupante=ocupante,path_imagem=path_img,qtde_turnos_exigidos=QTDE_TURNOS_EXIGIDOS_BANCOS)

                bases_territorio.append(base_auxiliar)

        return bases_territorio

    #métodos de atualização lógica
    def atualizar_status_ocupacao_bases(self,soldados_jogador,soldados_computador):
        exercitos = soldados_jogador + soldados_computador
        ocupada = False
        for base in self.bases_territorio:
            ocupada = False
            for soldado in exercitos:
                if soldado.l == base.l and soldado.c == base.c:
                    ocupada = True
                    break
            if ocupada == False:
                base.atualizar_status_ocupacao(False)
                base.atualizar_ocupante(NEUTRO)
                if base.funcao == FUNCAO_BANCO:
                    base.zerar_turno_ocupacao()

    #métodos de desenho e debug
    def desenhar(self,tela):
        for casa_aux in self.bases_territorio:
            casa_aux.desenhar(tela)
    def debug(self):
        print("----------------------TERRITÓRIO----------------------")
        for casa_aux in self.base_territorio:
            casa_aux.debug()
        print("----------------------TERRITÓRIO----------------------")
