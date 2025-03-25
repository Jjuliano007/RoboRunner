import pygame
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 400
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("RoboRunner")

# Carregar imagem de fundo
fundo = pygame.image.load("assets/fabrica.png")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

# Sons
coletar_som = pygame.mixer.Sound("assets/bateria.wav")
colisao_som = pygame.mixer.Sound("assets/erro.wav")
pygame.mixer.music.load("assets/musica_fundo.mp3")
pygame.mixer.music.play(-1)

# Robô
robo_img = pygame.image.load("assets/robo.png")
robo_x, robo_y = 100, ALTURA - 70
robo_vel = 5
pulo = False
pulo_contador = 10

# Bateria
bateria_img = pygame.image.load("assets/bateria.png")
bateria_x = random.randint(200, LARGURA - 40)
bateria_y = ALTURA - 70

# Obstáculo (laser)
laser_img = pygame.image.load("assets/laser.png")
laser_x = LARGURA
laser_y = ALTURA - 70
laser_vel = 5

# Pontuação
pontos = 0
fonte = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Loop principal
ejogando = True
while ejogando:
    clock.tick(30)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejogando = False

    # Movimento do robô
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and robo_x > 0:
        robo_x -= robo_vel
    if teclas[pygame.K_RIGHT] and robo_x < LARGURA - 40:
        robo_x += robo_vel
    if teclas[pygame.K_SPACE] and not pulo:
        pulo = True

    # Pulo do robô
    if pulo:
        robo_y -= (pulo_contador * abs(pulo_contador)) * 0.5
        pulo_contador -= 1
        if pulo_contador < -10:
            pulo = False
            pulo_contador = 10

    # Movimento do laser
    laser_x -= laser_vel
    if laser_x < -40:
        laser_x = LARGURA

    # Coleta de bateria
    if abs(robo_x - bateria_x) < 30 and abs(robo_y - bateria_y) < 30:
        pontos += 1
        coletar_som.play()
        bateria_x = random.randint(200, LARGURA - 40)

    # Colisão com laser
    if abs(robo_x - laser_x) < 30 and abs(robo_y - laser_y) < 30:
        pontos = max(0, pontos - 1)
        colisao_som.play()
        laser_x = LARGURA

    # Atualizar tela
    TELA.blit(fundo, (0, 0))
    TELA.blit(robo_img, (robo_x, robo_y))
    TELA.blit(bateria_img, (bateria_x, bateria_y))
    TELA.blit(laser_img, (laser_x, laser_y))
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))
    TELA.blit(texto_pontos, (10, 10))
    pygame.display.update()

pygame.quit()