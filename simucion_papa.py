"""Juego de la papa caliente usando una cola FIFO y una ventana con Tkinter."""

import tkinter as tk
import random

NOMBRES = ["Valentina", "Juan", "Sebastian", "Maria"]
PASES = 2


class Cola:
    """Cola FIFO (First In, First Out): el primero que entra es el primero en salir."""

    def __init__(self):
        """Crea una lista vacía para guardar los jugadores."""
        self.datos = []

    def enqueue(self, nombre):
        """Agrega un jugador al final de la cola, al principio de la lista."""
        self.datos.insert(0, nombre)

    def dequeue(self):
        """Retira al jugador del frente de la cola, al final de la lista."""
        return self.datos.pop()

    def size(self):
        """Devuelve la cantidad de jugadores que quedan."""
        return len(self.datos)

    def fila(self):
        """Devuelve una copia invertida de la lista para mostrar los turnos."""
        return self.datos[::-1]


def papa_caliente(nombres, pases):
    """Calcula las jugadas y las guarda para mostrarlas en la animación.

    Recibe los nombres de los jugadores y la cantidad de pases por ronda.
    En cada pase, el primero de la cola pasa al final.
    Después de los pases, se elimina al que queda en el frente.
    Devuelve los pasos del juego, incluyendo al ganador.
    """
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
    """Muestra los movimientos de los jugadores en la ventana.

    pasos contiene las jugadas, turno indica la jugada actual y cuadro
    indica el avance del movimiento. Se usa after para continuar
    la animación y al terminar se activa otra vez el botón.
    """
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
    """Mezcla una copia de los nombres y empieza la animación del juego.

    Desactiva el botón mientras se juega. El orden cambia al azar,
    aunque una misma persona puede volver a ganar.
    """
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
