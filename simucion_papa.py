import tkinter as tk
import random

NOMBRES = ["Valentina", "Juan", "Sebastian", "Maria"]
PASES = 2


class Cola:
    # Una cola normal: el primero que llega es el primero en salir

    def __init__(self):
        # Empezamos con una lista vacía
        self.datos = []

    def enqueue(self, nombre):
        # Mete a alguien al principio de la lista
        self.datos.insert(0, nombre)

    def dequeue(self):
        # Saca al que está al final de la lista
        return self.datos.pop()

    def size(self):
        # Cuenta cuántos quedan jugando
        return len(self.datos)

    def fila(self):
        # Da vuelta la lista para ver el orden real de los turnos
        return self.datos[::-1]


def papa_caliente(nombres, pases):
    # Esta es la lógica del juego para armar la lista de jugadas
    if not nombres or pases < 1:
        raise ValueError("Se necesita al menos un nombre y un pase.")
    cola = Cola()
    for nombre in nombres:
        cola.enqueue(nombre)

    pasos = [(cola.fila(), "inicio", "Empieza " + nombres[0] + ".")]
    while cola.size() > 1:
        for i in range(pases):
            fila = cola.fila()
            nombre = cola.dequeue()
            cola.enqueue(nombre)
            pasos.append((fila, "pase", f"Pase {i + 1}: {nombre} le pasa la papa a {fila[1]}."))
        fila = cola.fila()
        eliminado = cola.dequeue()
        pasos.append((fila, "sale", "Sale " + eliminado + "."))

    ganador = cola.dequeue()
    pasos.append(([ganador], "fin", "¡Gana " + ganador + "!"))
    return pasos


def animar(pasos, turno=0, cuadro=0):
    # Esta función dibuja la animación en la pantalla cuadrito por cuadrito
    fila, accion, mensaje = pasos[turno]
    lienzo.delete("all")
    lienzo.create_text(12, 17, anchor="w", text=mensaje, font=("Arial", 12))
    for i in range(len(fila)):
        x, y = 60 + 110 * i, 84
        if i > 0:
            x -= 11 * cuadro                 # Hace que los de atrás caminen hacia adelante
        elif accion == "pase":
            x += 11 * cuadro * (len(fila) - 1)
            if 0 < cuadro < 10:
                y = 46                       # Hace que el que pasa la papa salte por arriba
        elif accion == "sale":
            y += 9 * cuadro                  # Hace que el eliminado se caiga hacia abajo
        lienzo.create_rectangle(x - 48, y - 15, x + 48, y + 15, fill="#f9e2b3")
        lienzo.create_text(x, y, text=fila[i], font=("Arial", 12))

    if accion == "fin":
        boton.config(state="normal")
    elif accion == "inicio" or cuadro == 10:
        lienzo.after(750, animar, pasos, turno + 1, 0)
    else:
        lienzo.after(50, animar, pasos, turno, cuadro + 1)


def jugar():
    # Mezcla los nombres para que sea al azar y arranca la animación
    boton.config(state="disabled")
    jugadores = NOMBRES.copy()
    random.shuffle(jugadores)
    animar(papa_caliente(jugadores, PASES))


if __name__ == "__main__":
    # Configuración de la ventanita de Tkinter (labels, botones y el lienzo)
    ventana = tk.Tk()
    ventana.title("La papa caliente")
    tk.Label(ventana, text="Cola de jugadores: el frente está a la izquierda").pack(pady=6)
    lienzo = tk.Canvas(ventana, width=max(360, 110 * len(NOMBRES) + 10), height=120, bg="white")
    lienzo.pack()
    lienzo.create_text(12, 45, anchor="w", text=f"Al jugar se sortea el orden. Pases por ronda: {PASES}")
    boton = tk.Button(ventana, text="Jugar", command=jugar)
    boton.pack(pady=5)
    ventana.mainloop()
