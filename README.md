# Simulador del Sistema Solar

Simulador orbital interactivo en Python utilizando Pygame. Se implementa una simulación de N-cuerpos con física de alta precisión para representar las órbitas de los principales planetas del sistema solar y la Luna.

## Características

- Física de Alta Precision: Implementa Sub-stepping (50 cálculos por frame) para mantener órbitas estables incluso a altas velocidades.
- Sistema Solar: Incluye el Sol, Mercurio, Tierra, Luna, Marte, Jupiter y Saturno (con anillos).
- Cámara Dinámica: Sistema de zoom y arrastre con el ratón.
- Seguimiento: Centrado automático de cámara en cuerpos celestes específicos.
- Efecto Parallax: Fondo de estrellas dinámico que reacciona al movimiento de la cámara.
- Control del Tiempo: Capacidad de acelerar, frenar o resetear el flujo del tiempo.

## Instalación

1. Tener Python instalado.
2. Instalar la libreria Pygame:
   pip install pygame
3. Ejecuta el simulador:
   python main.py

## Controles

- Zoom In / Out: Rueda del ratón
- Mover Cámara: Click izquierdo + Arrastrar
- Acelerar Tiempo: Flecha Arriba
- Frenar Tiempo: Flecha Abajo
- Resetear Tiempo: Tecla Espacio
- Seguir al Sol: Tecla S
- Seguir a la Tierra: Tecla T
- Seguir a la Luna: Tecla L
- Seguir a Marte: Tecla M
- Seguir a Júpiter: Tecla J
- Seguir a Saturno: Tecla A
- Liberar Cámara: Click izquierdo en punto vacío

## Notas sobre la Física

Este simulador utiliza la Ley de Gravitación Universal de Newton. Para resolver las ecuaciones de movimiento, se emplea una integracion numérica con 50 sub-pasos por cada frame renderizado. 

Escala Visual: Debido a la gran diferencia de escalas entre los radios de los planetas y sus distancias orbitales, se ha aplicado un factor de exageración visual a la distancia Tierra-Luna. Esto permite ver a la Luna orbitar claramente sin necesidad de hacer un zoom extremo que oculte a la Tierra.

## Estructura del Proyecto

- main.py: Punto de entrada del programa y bucle de renderizado.
- cuerpo.py: Lógica de la clase CuerpoCeleste y cálculos de fuerzas.

---