import pygame
import sys
import time
import random
import os

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Phylactery: AlphaV1.0')

# Adiciona uma variável para rastrear o tempo desde a última alimentação
last_feed_time = time.time()

# Obtém o caminho do diretório atual do script
script_dir = os.path.dirname(__file__)

# Concatena o caminho do diretório com o nome da pasta e o nome dos arquivos de imagem
bixinho_left = os.path.join(script_dir, 'sprites', 'skull_L.png')
bixinho_right = os.path.join(script_dir, 'sprites', 'skull_R.png')
#nivel 1:
skullwizardR = os.path.join(script_dir, 'sprites', 'skullwizard_R.png')
skullwizardL = os.path.join(script_dir, 'sprites', 'skullwizard_L.png')
deathknightR = os.path.join(script_dir, 'sprites', 'Deathknight_R.png')
deathknightL = os.path.join(script_dir, 'sprites', 'Deathknight_L.png')
shadowlurkerR = os.path.join(script_dir, 'sprites', 'ShadowLurker_R.png')
shadowlurkerL = os.path.join(script_dir, 'sprites', 'ShadowLurker_L.png')
#nivel 2:
LichL = os.path.join(script_dir, 'sprites', '.png')
LichR = os.path.join(script_dir, 'sprites', '.png')
MummyL = os.path.join(script_dir, 'sprites', '.png')
MummyR = os.path.join(script_dir, 'sprites', '.png')
BoneclawL = os.path.join(script_dir, 'sprites', 'boneclaw_L.png')
BoneclawR = os.path.join(script_dir, 'sprites', 'boneclaw_R.png')
DeathTyrantL = os.path.join(script_dir, 'sprites', '.png')
DeathTyrantR = os.path.join(script_dir, 'sprites', '.png')
AncientVampireL = os.path.join(script_dir, 'sprites', '.png')
AncientVampireR = os.path.join(script_dir, 'sprites', '.png')
AparitionL = os.path.join(script_dir, 'sprites', '.png')
AparitionR = os.path.join(script_dir, 'sprites', '.png')

#Botões:
botaoAP =os.path.join(script_dir, 'buttons', 'botao_a.png')
botaoZP =os.path.join(script_dir, 'buttons', 'botao_z.png')
botaoXP =os.path.join(script_dir, 'buttons', 'botao_x.png')
botaoCP =os.path.join(script_dir, 'buttons', 'botao_c.png')
#Backgrounds:
StartBG = os.path.join(script_dir, 'backgrounds', 'BG0.png')
GameBG = os.path.join(script_dir, 'backgrounds', 'BG1.png')

# Carrega as imagens do bixinho inicial
bixinho_left = pygame.image.load(bixinho_left)
bixinho_right = pygame.image.load(bixinho_right)
bixinho_rect = bixinho_left.get_rect()
bixinho_rect.center = (width // 2, height // 2 + 50)

# Carrega a imagem dos botões dentro do tamagochi
botao_alimento = pygame.image.load(botaoAP)
botao_a = botao_alimento.get_rect()
botao_a.center = (width -700 , height-125)
#botão Z
botao_for = pygame.image.load(botaoZP)
botao_z = botao_for.get_rect()
botao_z.center = (width -700, height -60)
#botão X
botao_int = pygame.image.load(botaoXP)
botao_x = botao_int.get_rect()
botao_x.center = (width -625, height-60)
#botão C
botao_agi = pygame.image.load(botaoCP)
botao_c = botao_agi.get_rect()
botao_c.center = (width -550, height -60)

# Carrega a imagem do novo jogo
novo_jogo_background = pygame.image.load(GameBG)
novo_jogo_background = pygame.transform.scale(novo_jogo_background, (width, height))
intro_background = pygame.image.load(StartBG)
intro_background = pygame.transform.scale(intro_background, (width, height))

# Inicializa as variáveis para a animação do bixinho
last_animation_time = time.time()
animation_interval = 1  # Intervalo de 1 segundo para a animação
direction_change_interval = 5  # Intervalo de 5 segundos para trocar a direção
direction_change_count = 0  # Contador de trocas de direção

# Inicializa as variáveis para os status do bixinho
fome = 5
energia = 5
forca = 0
inteligencia = 0
agilidade = 0
vida = 10
nivel = 1
evolucao = 0
base = 0
cheat = 9 # de 0 a 9, muda o valor dos treinos

#inicia a imagem inicial
bixinho_image = bixinho_left 

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Função para decrementar a fome aleatoriamente

def decrease_hunger():
    global fome, last_feed_time
    fome -= 1
    evolution_trigger_lvl1()
    if fome < 0:
        fome = 0
    last_feed_time = time.time()  # Atualiza o tempo da última alimentação
    save_game()

# Função para alimentar o bixinho
def feed_bixinho():
    global fome
    fome += 5
    if fome > 10:
        fome = 10
    save_game()

# Função para regenerar energia
def energy_boost():
    global energia,nivel
    energia += 1
    aux = 5*nivel
    if energia > aux:
        energia = aux
    save_game()

#função para perder energia
def energy_loss():
    global energia
    energia -=1
    if energia <0:
        energia =0
    save_game()

def train_int(): #cada treino perde 1 de energia e 2 de fome, e ganha 1 do escolhido.
    global inteligencia, energia, fome, nivel, cheat
    aux2 = nivel
    aux = aux2*10 #variavel nivel para evoluir o numero maximo do status dependendo do nível do bixinho
    if energia <1:
        inteligencia = inteligencia
    elif energia >0:
        if fome <2:
            inteligencia = inteligencia
        elif fome >1:
            decrease_hunger()
            decrease_hunger()
            energy_loss()
            inteligencia += 1 + cheat
            if inteligencia >aux:
                inteligencia = aux
            save_game()

def train_for(): #cada treino perde 1 de energia e 2 de fome, e ganha 1 do escolhido.
    global forca, energia, fome, nivel, cheat
    aux = nivel*10 #variavel nivel para evoluir o numero maximo do status dependendo do nível do bixinho
    if energia <1:
        forca = forca
    elif energia >0:
        if fome <2:
            forca = forca
        elif fome >1:
            decrease_hunger()
            decrease_hunger()
            energy_loss()
            forca += 1 + cheat
            if forca >aux:
                forca = aux
            save_game()    

def train_agi(): #cada treino perde 1 de energia e 2 de fome, e ganha 1 do escolhido.
    global agilidade, energia, fome, nivel, cheat
    aux = nivel*10 #variavel nivel para evoluir o numero maximo do status dependendo do nível do bixinho
    if energia <1:
        agilidade = agilidade
    elif energia >0:
        if fome <2:
            agilidade = agilidade
        elif fome >1:
            decrease_hunger()
            decrease_hunger()
            energy_loss()
            agilidade += 1 + cheat
            if agilidade >aux:
                agilidade = aux
            save_game()

# Adiciona uma função para verificar o estado do bixinho
def check_bixinho_state():
    global fome, last_feed_time
    # Verifica se o bixinho ficou com 0 de fome por 1 hora
    if fome == 0 and (time.time() - last_feed_time) > 3600:  # 3600 segundos = 1 hora
        game_over_screen()

def game_over_screen():
    global screen

    screen.fill((0, 0, 0))  # Preenche a tela com preto
    draw_text('Game Over: Seu bixinho morreu', pygame.font.Font(None, 36), (255, 255, 255), screen, 200, 200)
    pygame.display.flip()
    
    # Aguarda alguns segundos antes de fechar o jogo
    pygame.time.delay(5000)  # 5000 milissegundos = 5 segundos
    pygame.quit()
    sys.exit()

def main_menu(): #tela inicial do game
    while True:
        screen.fill((0, 0, 0))
        # Carrega o background
        screen.blit(intro_background, (0, 0))

        # Opção Novo Jogo
        draw_text('Novo Jogo: Pressione Enter', pygame.font.Font(None, 36), (255, 255, 255), screen, 300, 200)
        # Opção Carregar
        draw_text('Carregar jogo: Pressione L', pygame.font.Font(None, 36), (255, 255, 255), screen, 300, 300)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    if menu_cursor == 0:  # Novo Jogo
                        new_game()
                elif event.key == pygame.K_l:
                    load_game()
                    new_game()

def new_game():
    global botao_alimento, botao_c, botao_agi, botao_z, botao_for, botao_a, botao_x, botao_int, bixinho_image, bixinho_rect, direction_change_count, fome, forca, inteligencia, agilidade, vida, nivel

    # Carrega o novo background
    screen.blit(novo_jogo_background, (0, 0))

    # Adiciona um temporizador para a decaída de fome e de energia
    pygame.time.set_timer(pygame.USEREVENT + 1, random.randint(20000, 60000))  # fome
    pygame.time.set_timer(pygame.USEREVENT + 2, random.randint(200000, 600000))  # energia

    # Adiciona um temporizador para verificar o estado do bixinho
    pygame.time.set_timer(pygame.USEREVENT + 3, 1000)  # Verifica a cada segundo

    # Loop do novo jogo
    while True:
        handle_events()  # inputs do player

        # Atualiza a imagem do bixinho
        update_bixinho_animation()

        # Desenhos na tela
        screen.blit(novo_jogo_background, (0, 0))  # Apaga a imagem antiga, e desenha o Background
        screen.blit(bixinho_image, bixinho_rect)  # desenha o bixinho na tela
        screen.blit(botao_int, botao_x)  # desenha a imagem do botão: inteligência
        screen.blit(botao_alimento, botao_a)  # botão Alimento
        screen.blit(botao_for, botao_z)  # botão força
        screen.blit(botao_agi, botao_c)  # botão agilidade

        # Desenha as barras de status
        draw_status_bars()

        pygame.display.flip()
        pygame.time.Clock().tick(30)  # Limita a taxa de atualização

        if evolucao != 0:
            evoluir()
            pygame.display.flip()  # Atualiza a tela após evoluir


def handle_events(): # eventos que o player controla
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_a:  # Tecla A, para alimentar o bixinho
                feed_bixinho()
            elif event.key == pygame.K_x: # tecla X, para treinar inteligencia
                train_int()
            elif event.key == pygame.K_z: # tecla Z, treino de força
                train_for()
            elif event.key == pygame.K_c: # tecla C, treino de agilidade
                train_agi()
        elif event.type == pygame.USEREVENT + 1:  # Timer para decair a fome
            decrease_hunger()
        elif event.type == pygame.USEREVENT +2: # Timer para ganhar energia
            energy_boost()
        elif event.type == pygame.USEREVENT + 3:  # Timer para verificar o estado do bixinho
            check_bixinho_state()

def update_bixinho_animation():
    global bixinho_image, bixinho_rect, last_animation_time, direction_change_count

    current_time = time.time()

    # Atualiza a imagem do bixinho a cada segundo
    if current_time - last_animation_time >= animation_interval:
        update_direction(current_time)
        last_animation_time = current_time

def update_direction(current_time):
    global bixinho_image, bixinho_rect, direction_change_count

    # Troca a direção do bixinho a cada direction_change_interval segundos
    if int(current_time) % direction_change_interval == 0 and direction_change_count == 0:
        bixinho_image = pygame.transform.flip(bixinho_image, True, False)
        direction_change_count += 1
    elif int(current_time) % direction_change_interval != 0:
        direction_change_count = 0  # Reseta o contador se não estiver no intervalo de troca de direção

def draw_status_bars():
    bar_width = 100
    bar_height = 10
    bar_spacing = 20

    # Desenha a barra de fome
    pygame.draw.rect(screen, (0, 255, 0), (50, 50, bar_width * (fome / 10), bar_height))
    draw_text(f'fome: {fome}', pygame.font.Font(None, 24), (255, 255, 255), screen, 50, 30)

    pygame.draw.rect(screen, (0,255,0), (50, 50, bar_width * (energia / 10), bar_height))
    draw_text(f'Energia: {energia}', pygame.font.Font(None, 24), (255,255,255), screen, 50, 50)

    # Desenha a barra de Força
    pygame.draw.rect(screen, (255, 0, 0), (50, 50 + bar_height + bar_spacing, bar_width * (forca / 10), bar_height))
    draw_text(f'Força: {forca}', pygame.font.Font(None, 24), (255, 255, 255), screen, 50, 80)

    # Desenha a barra de Inteligência
    pygame.draw.rect(screen, (0, 0, 255), (50, 50 + 2 * (bar_height + bar_spacing), bar_width * (inteligencia / 10), bar_height))
    draw_text(f'Inteligência: {inteligencia}', pygame.font.Font(None, 24), (255, 255, 255), screen, 50, 130)

    # Desenha a barra de Agilidade
    pygame.draw.rect(screen, (255, 255, 0), (50, 50 + 3 * (bar_height + bar_spacing), bar_width * (agilidade / 10), bar_height))
    draw_text(f'Agilidade: {agilidade}', pygame.font.Font(None, 24), (255, 255, 255), screen, 50, 180)

    # Desenha a barra de Vida
    pygame.draw.rect(screen, (255, 0, 255), (50, 50 + 4 * (bar_height + bar_spacing), bar_width * (vida / (10 + nivel * 10)), bar_height))
    draw_text(f'Vida: {vida}', pygame.font.Font(None, 24), (255, 255, 255), screen, 50, 230)

    # Desenha o Nível
    draw_text(f'Nível: {nivel}', pygame.font.Font(None, 24), (255, 255, 255), screen, 50, 280)

def evolution_trigger_lvl1():
    global inteligencia,forca,agilidade,nivel,evolucao, base
    if inteligencia > 9:
        if nivel < 2:
            evolucao = 1 # codigo da evolução para int
            nivel += 1
    elif forca > 9:
        if nivel < 2:
            evolucao = 2 #codigo para força
            nivel += 1
    elif agilidade > 9:
        if nivel < 2:
            evolucao = 3 #codigo para agilidade
            nivel += 1
    elif inteligencia > 19: #int to int
        if nivel < 3: 
            if base == 1:
                evolucao = 4
                nivel += 1
    elif forca > 19: #int -> For
        if nivel == 2 and base == 1:
            evolucao = 5
            nivel += 1
    elif agilidade > 19: #int -> Agi
        if nivel == 2 and base == 1:
            evolucao = 6
            nivel += 1
    elif inteligencia > 19: #For -> int
        if nivel == 2 and base == 2:
            evolucao = 5
            nivel += 1
    elif forca > 19: #For -> For
        if nivel == 2 and base == 2:
            evolucao = 7
            nivel += 1
    elif agilidade > 19: #For -> Agi
        if nivel == 2 and base == 2:
            evolucao = 8
            nivel += 1
    elif inteligencia > 19: #Agi -> int
        if nivel == 2 and base == 3:
            evolucao = 6
            nivel += 1
    elif forca > 19: #Agi -> For
        if nivel == 2 and base == 3:
            evolucao = 8
            nivel += 1
    elif agilidade > 19: #Agi -> Agi
        if nivel == 2 and base == 3:
            evolucao = 9
            nivel += 1
    save_game()

def evoluir():
    global evolucao, bixinho_left, bixinho_rect, bixinho_right,bixinho_image, base

    if evolucao == 1:  # evoluir para Inteligencia
        bixinho_left = pygame.image.load(skullwizardL)
        bixinho_right = pygame.image.load(skullwizardR)
        evolucao = 0
        base = 1
    elif evolucao == 2:  # evoluir para força
        bixinho_left = pygame.image.load(deathknightL)
        bixinho_right = pygame.image.load(deathknightR)
        evolucao = 0
        base = 2
    elif evolucao == 3:  # evoluir para Agilidade
        bixinho_left = pygame.image.load(shadowlurkerL)
        bixinho_right = pygame.image.load(shadowlurkerR)
        evolucao = 0
        base = 3
    elif evolucao == 4: #Linha Int -> Int
        bixinho_left = pygame.image.load(LichL)
        bixinho_right = pygame.image.load(LichR)
        evolucao = 0
    elif evolucao == 5: #Linha Int -> For
        bixinho_left = pygame.image.load(MummyL)
        bixinho_right = pygame.image.load(MummyR)
        evolucao = 0
    elif evolucao == 6: #Linha Int -> Agi
        bixinho_left = pygame.image.load(BoneclawL)
        bixinho_right = pygame.image.load(BoneclawR)
        evolucao = 0
    elif evolucao == 7: #Linha Int -> Int
        bixinho_left = pygame.image.load(DeathTyrantL)
        bixinho_right = pygame.image.load(DeathTyrantR)
        evolucao = 0
    elif evolucao == 8: #Linha Int -> Int
        bixinho_left = pygame.image.load(AncientVampireL)
        bixinho_right = pygame.image.load(AncientVampireR)
        evolucao = 0
    elif evolucao == 9: #Linha Int -> Int
        bixinho_left = pygame.image.load(AparitionL)
        bixinho_right = pygame.image.load(AparitionR)
        evolucao = 0

    bixinho_image = bixinho_left
    bixinho_rect = bixinho_left.get_rect()
    bixinho_rect.center = (width // 2, height // 2 + 50)
    save_game()
    pygame.display.flip()  # Atualiza a tela após evoluir

    screen.blit(bixinho_image, bixinho_rect)
    pygame.display.flip()

def save_game():
    global inteligencia, nivel, agilidade, forca, vida, evolucao, energia, fome,base
    if os.path.exists("save.txt"):
        os.remove("save.txt")
    with open("save.txt", "w") as save:
        save.write(f"{inteligencia}\n{nivel}\n{agilidade}\n{forca}\n{vida}\n{evolucao}\n{energia}\n{fome}\n{base}")

def load_game():
    global inteligencia, nivel, agilidade, forca, vida, evolucao, energia, fome

    if os.path.exists("save.txt"):
        with open("save.txt", "r") as load:
            lines = load.readlines()
            if len(lines) == 9:
                try:
                    inteligencia, nivel, agilidade, forca, vida, evolucao, energia, fome = map(int, lines)
                except ValueError:
                    print("Erro ao carregar dados do arquivo. Certifique-se de que os dados são válidos.")
            else:
                print("Erro: O arquivo não tem o número esperado de linhas.")
    else:
        print("Erro: O arquivo 'save.txt' não foi encontrado.")

if __name__ == '__main__':
    menu_cursor = 0
    main_menu()