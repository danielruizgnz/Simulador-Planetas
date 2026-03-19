import math
import pygame

class CuerpoCeleste:
    G = 6.67428e-11
    UA = 149.6e6 * 1000
    ESCALA_BASE = 200 / UA     
    TIMESTEP = 3600 * 24  

    def __init__(self, x, y, radio, color, masa, nombre, vel_y=0, vel_x=0):
        self.x = x
        self.y = y
        self.radio = radio
        self.color = color
        self.masa = masa
        self.nombre = nombre
        self.orbita = []
        self.vel_x = vel_x
        self.vel_y = vel_y

    def dibujar(self, ventana, ancho, alto, zoom, despl_x, despl_y, tierra=None):
        escala = self.ESCALA_BASE * zoom
        
        # --- TRUCO VISUAL PARA LA LUNA ---
        x_dibujo, y_dibujo = self.x, self.y
        
        if self.nombre == "Luna" and tierra:
            # vector Tierra -> Luna
            dx = self.x - tierra.x
            dy = self.y - tierra.y
            distancia_real = math.sqrt(dx**2 + dy**2)
            
            if distancia_real > 0:
                # exageración visual
                factor_exageracion = 15 
                # Nueva posición visual exagerada
                x_dibujo = tierra.x + (dx / distancia_real) * (distancia_real * factor_exageracion)
                y_dibujo = tierra.y + (dy / distancia_real) * (distancia_real * factor_exageracion)


        # coordenadas de dibujo calculadas
        x = x_dibujo * escala + ancho / 2 + despl_x
        y = y_dibujo * escala + alto / 2 + despl_y

        # Estela
        if len(self.orbita) > 2:
            puntos_dibujo = []
            limite = 200 if self.nombre == "Luna" else 1000
            for p in self.orbita[-limite:]:
                px = p[0] * escala + ancho / 2 + despl_x
                py = p[1] * escala + alto / 2 + despl_y
                puntos_dibujo.append((px, py))
            pygame.draw.lines(ventana, self.color, False, puntos_dibujo, 1)

        radio_visual = max(1, int(self.radio * math.sqrt(zoom)))

        if self.nombre == "Sol":
            for r in range(1, 4):
                s = pygame.Surface((radio_visual*10, radio_visual*10), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 255, 0, 70//r), (radio_visual*5, radio_visual*5), radio_visual * r * 2)
                ventana.blit(s, (x - radio_visual*5, y - radio_visual*5))

        pygame.draw.circle(ventana, self.color, (int(x), int(y)), radio_visual)

        if self.nombre == "Saturno":
            rect_anillo = pygame.Rect(0, 0, radio_visual * 4, radio_visual * 1.2)
            rect_anillo.center = (int(x), int(y))
            pygame.draw.ellipse(ventana, (180, 160, 140), rect_anillo, 2)
        
        if zoom > 0.08:
            fuente = pygame.font.SysFont("Arial", max(10, int(12 * math.sqrt(zoom))))
            texto = fuente.render(self.nombre, True, (255, 255, 255))
            ventana.blit(texto, (x - texto.get_width()/2, y + radio_visual + 3))

    def actualizar_posicion(self, todos, dt):
        total_fx = total_fy = 0
        for cuerpo in todos:
            if self == cuerpo: continue
            dx = cuerpo.x - self.x
            dy = cuerpo.y - self.y
            distancia = math.sqrt(dx**2 + dy**2)
            if distancia < 1000: continue # Evitar división por cero o distancias absurdas
            
            fuerza = self.G * self.masa * cuerpo.masa / distancia**2
            angulo = math.atan2(dy, dx)
            total_fx += math.cos(angulo) * fuerza
            total_fy += math.sin(angulo) * fuerza

        self.vel_x += total_fx / self.masa * dt
        self.vel_y += total_fy / self.masa * dt
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt