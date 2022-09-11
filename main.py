import pygame, random

# Inicializamos ventana
pygame.init()
ancho_screen = 850
alto_screen = 480
screen = pygame.display.set_mode((ancho_screen, alto_screen))
pygame.display.set_caption("MI PEQUEÑO JUEGO")
clock = pygame.time.Clock()


class Personaje(pygame.sprite.Sprite):
    def __init__(self, x, y, fuente, limite):
        super().__init__()
        self.x = x
        self.y = y
        fuente += "/"

        # Atributos para animacion movimiento
        self.va_izq = False
        self.va_der = False
        self.contador_pasos = 0

        self.camina_derecha = [
            pygame.image.load("img/" + fuente + "R1.png"),
            pygame.image.load("img/" + fuente + "R2.png"),
            pygame.image.load("img/" + fuente + "R3.png"),
            pygame.image.load("img/" + fuente + "R4.png"),
            pygame.image.load("img/" + fuente + "R5.png"),
            pygame.image.load("img/" + fuente + "R6.png"),
            pygame.image.load("img/" + fuente + "R7.png"),
            pygame.image.load("img/" + fuente + "R8.png"),
            pygame.image.load("img/" + fuente + "R9.png"),
        ]
        self.camina_izquierda = [
            pygame.image.load("img/" + fuente + "L1.png"),
            pygame.image.load("img/" + fuente + "L2.png"),
            pygame.image.load("img/" + fuente + "L3.png"),
            pygame.image.load("img/" + fuente + "L4.png"),
            pygame.image.load("img/" + fuente + "L5.png"),
            pygame.image.load("img/" + fuente + "L6.png"),
            pygame.image.load("img/" + fuente + "L7.png"),
            pygame.image.load("img/" + fuente + "L8.png"),
            pygame.image.load("img/" + fuente + "L9.png"),
        ]

        self.quieto = pygame.image.load("img/" + fuente + "standing.png")
        self.ancho = self.quieto.get_width()
        self.alto = self.quieto.get_height()
        self.velocidad = 5
        self.impulso_salto = 10
        self.saltar = False
        self.camino = [self.x, limite]
        self.salud = 10
        self.zona_impacto = (self.x + 15, self.y + 10, 30, 50)

    def dibujar(self, cuadro):
        if self.contador_pasos + 1 > 27:
            self.contador_pasos = 0

        if self.va_izq:
            cuadro.blit(
                self.camina_izquierda[self.contador_pasos // 3],
                (self.x, self.y),
            )
            self.contador_pasos += 1
        elif self.va_der:
            cuadro.blit(
                self.camina_derecha[self.contador_pasos // 3],
                (self.x, self.y),
            )
            self.contador_pasos += 1
        else:
            cuadro.blit(self.quieto, (self.x, self.y))

        pygame.draw.rect(cuadro, (255, 0, 0), (self.x + 5, self.y - 20, 50, 10))
        pygame.draw.rect(
            cuadro,
            (0, 128, 0),
            (self.x + 5, self.y - 20, 50 - (5 * (10 - self.salud)), 10),
        )

        self.zona_impacto = (self.x + 15, self.y + 10, 30, 50)
        pygame.draw.rect(cuadro, (255, 0, 0), self.zona_impacto, 2)

    def movimiento(self, k, iz, de, ar, ab, salta):
        if k[iz] and self.x >= self.velocidad:
            self.x -= self.velocidad
            # Control de animacion
            self.va_izq = True
            self.va_der = False

        elif k[de] and self.x <= ancho_screen - self.ancho - self.velocidad:
            self.x += self.velocidad
            self.va_der = True
            self.va_izq = False
        else:
            self.va_der = False
            self.va_izq = False
            self.contador_pasos = 0

        if self.saltar == True:
            if self.impulso_salto >= -10:
                if self.impulso_salto < 0:
                    self.y += (self.impulso_salto**2) * 0.5
                else:
                    self.y -= (self.impulso_salto**2) * 0.5
                self.impulso_salto -= 1
            else:
                self.saltar = False
                self.impulso_salto = 10
        else:
            if k[ar] and self.y >= self.velocidad:
                self.y -= self.velocidad

            if k[ab] and self.y <= alto_screen - self.alto - self.velocidad:
                self.y += self.velocidad

            if k[salta]:
                self.saltar = True
                self.va_der = False
                self.va_izq = False
                self.contador_pasos = 0

    def movimiento_auto(self):
        if self.velocidad > 0:
            if self.x + self.velocidad < self.camino[1]:
                self.x += self.velocidad
                self.va_der = True
                self.va_izq = False
            else:
                self.velocidad *= -1
                self.contador_pasos = 0
        else:
            if self.x - self.velocidad > self.camino[0]:
                self.x += self.velocidad
                self.va_der = False
                self.va_izq = True
            else:
                self.velocidad *= -1
                self.contador_pasos = 0

    def se_encuentra_con(self, alguien):
        R1_ab = self.zona_impacto[1] + self.zona_impacto[3]
        R1_ar = self.zona_impacto[1]
        R1_iz = self.zona_impacto[0]
        R1_de = self.zona_impacto[0] + self.zona_impacto[2]
        R2_ab = alguien.zona_impacto[1] + alguien.zona_impacto[3]
        R2_ar = alguien.zona_impacto[1]
        R2_iz = alguien.zona_impacto[0]
        R2_de = alguien.zona_impacto[0] + alguien.zona_impacto[2]

        return R1_de > R2_iz and R1_iz < R2_de and R1_ar < R2_ab and R1_ab > R2_ar


def repintar_cuadro_juego():
    # screen.fill((225, 69, 20))
    screen.blit(imagen_fondo, (0, 0))

    # dibujo personaje
    heroe.dibujar(screen)
    villano.dibujar(screen)

    pygame.display.update()


# Funcion principal

repetir = True  # Variable para controlar las repeticiones del juego completo en todas sus ventanas

# ciclo de repeticion de todo el juego
while repetir:

    # Iniciliacion de elementos del juego
    imagen_fondo = pygame.image.load("img/bg0.jpg")

    # Musica del juego
    ruta_musica = "snd/dubstep.mp3"
    musica_fondo = pygame.mixer.music.load(ruta_musica)
    # pygame.mixer.music.play(-1)

    # Creacion del personaje Heroe
    heroe = Personaje(
        int(ancho_screen // 2), int(alto_screen // 2), "heroe", ancho_screen
    )
    # Creacion del personaje villano
    villano = Personaje(0, int(alto_screen // 2), "villano", ancho_screen // 2)
    # Sección del juego
    esta_jugando = True
    while esta_jugando:
        clock.tick(27)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Evento de movimiento de personaje
        teclas = pygame.key.get_pressed()

        heroe.movimiento(
            teclas,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_SPACE,
        )
        impacto = heroe.se_encuentra_con(villano)
        print(impacto)
        villano.movimiento_auto()
        repintar_cuadro_juego()

pygame.quit()
