import pygame
import random
from cuerpo import CuerpoCeleste

pygame.init()

ANCHO, ALTO = 1200, 900
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulador Solar Completo: [S]ol, [T]ierra, [L]una, [M]arte, [J]úpiter, [Sat]urno")
FUENTE_UI = pygame.font.SysFont("Arial", 16, bold=True)

def main():
    reloj = pygame.time.Clock()
    estrellas = [(random.randint(0, ANCHO), random.randint(0, ALTO)) for _ in range(400)]

    zoom = 0.3
    despl_x, despl_y = 0, 0
    enfoque = None
    arrastrando = False
    ultima_pos_raton = (0, 0)
    SUBSTEPS = 50 

    # DEF DE SISTEMA
    sol = CuerpoCeleste(0, 0, 20, (255, 255, 0), 1.988 * 10**30, "Sol")
    
    mercurio = CuerpoCeleste(0.38 * CuerpoCeleste.UA, 0, 4, (170, 170, 170), 3.3 * 10**23, "Mercurio", vel_y=-47.4 * 1000)
    
    t_dist = -1 * CuerpoCeleste.UA
    t_vel_y = 29.78 * 1000
    tierra = CuerpoCeleste(t_dist, 0, 8, (50, 150, 255), 5.97 * 10**24, "Tierra", vel_y=t_vel_y)

    dist_luna = 384400 * 1000 
    luna = CuerpoCeleste(t_dist - dist_luna, 0, 2, (220, 220, 220), 7.34 * 10**22, "Luna", vel_y=t_vel_y + 1022)

    marte = CuerpoCeleste(-1.52 * CuerpoCeleste.UA, 0, 6, (200, 80, 80), 6.39 * 10**23, "Marte", vel_y=24.07 * 1000)
    
    jupiter = CuerpoCeleste(5.2 * CuerpoCeleste.UA, 0, 16, (210, 180, 140), 1.89 * 10**27, "Jupiter", vel_y=-13.07 * 1000)
    
    saturno = CuerpoCeleste(-9.5 * CuerpoCeleste.UA, 0, 14, (230, 200, 150), 5.68 * 10**26, "Saturno", vel_y=9.69 * 1000)

    lista_planetas = [sol, mercurio, tierra, luna, marte, jupiter, saturno]

    corriendo = True
    while corriendo:
        reloj.tick(60)
        VENTANA.fill((5, 5, 15))

        # EVENTOS
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: corriendo = False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 4: zoom *= 1.1
                if evento.button == 5: zoom /= 1.1
                if evento.button == 1:
                    arrastrando = True
                    enfoque = None
                    ultima_pos_raton = evento.pos
            
            if evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1: arrastrando = False
            
            if evento.type == pygame.MOUSEMOTION and arrastrando:
                dx, dy = evento.pos[0] - ultima_pos_raton[0], evento.pos[1] - ultima_pos_raton[1]
                despl_x += dx
                despl_y += dy
                ultima_pos_raton = evento.pos

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s: enfoque = sol
                if evento.key == pygame.K_t: enfoque = tierra
                if evento.key == pygame.K_l: enfoque = luna
                if evento.key == pygame.K_m: enfoque = marte
                if evento.key == pygame.K_j: enfoque = jupiter
                if evento.key == pygame.K_a: enfoque = saturno # A para saturno
                if evento.key == pygame.K_SPACE: CuerpoCeleste.TIMESTEP = 3600 * 24

        # Controles de tiempo
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]: CuerpoCeleste.TIMESTEP *= 1.05
        if teclas[pygame.K_DOWN]: CuerpoCeleste.TIMESTEP /= 1.05

        # FÍSICA
        dt_sub = CuerpoCeleste.TIMESTEP / SUBSTEPS
        for _ in range(SUBSTEPS):
            for p in lista_planetas:
                p.actualizar_posicion(lista_planetas, dt_sub)
        
        for p in lista_planetas:
            p.orbita.append((p.x, p.y))
            if len(p.orbita) > 1200: p.orbita.pop(0)

        # CÁMARA
        if enfoque:
            escala = CuerpoCeleste.ESCALA_BASE * zoom
            despl_x = -enfoque.x * escala
            despl_y = -enfoque.y * escala

        # DIBUJO
        for e in estrellas:
            ex = (e[0] + despl_x * 0.05) % ANCHO
            ey = (e[1] + despl_y * 0.05) % ALTO
            pygame.draw.circle(VENTANA, (150, 150, 150), (int(ex), int(ey)), 1)

        for p in lista_planetas:
            # referencia de la tierra al resto (solo para luna)
            p.dibujar(VENTANA, ANCHO, ALTO, zoom, despl_x, despl_y, tierra=tierra)

        # UI
        dias_seg = (CuerpoCeleste.TIMESTEP * 60) / (3600 * 24)
        txt = FUENTE_UI.render(f"Física x{SUBSTEPS} | Foco: {enfoque.nombre if enfoque else 'Libre'} | {dias_seg:.1f} d/s", True, (0, 255, 0))
        VENTANA.blit(txt, (20, 20))
        ayuda = FUENTE_UI.render("[S,T,L,M,J,A] Seguir | [Frenar/Acelerar] Flechas | [Rueda] Zoom", True, (200, 200, 200))
        VENTANA.blit(ayuda, (20, ALTO - 30))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()