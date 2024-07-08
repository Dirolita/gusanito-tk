import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class JuegoGusanito:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Gusanito")
        self.ancho_celda = 25
        self.largo_tablero = 25
        self.velocidad = 100
        self.canvas = tk.Canvas(self.root, width=self.ancho_celda * self.largo_tablero, height=self.ancho_celda * self.largo_tablero)
        self.canvas.pack()
        self.gusanito = [[4, 3], [4, 4], [4, 5]]
        self.direccion = "Right"
        self.color_gusanito = "green"
        self.comida = self.generar_comida()
        self.puntuacion = 0
        self.nombre_gusanito = "Gusanito"
        self.puntuaciones = []
        self.juego_activo = False
        self.fondo_img = None
        self.cargar_fondo("bk.jpg")
        self.root.bind("<Key>", self.cambiar_direccion)
        self.root.bind("<Return>", self.reiniciar_juego)
        self.mostrar_menu()

    def cargar_fondo(self, ruta):
        try:
            self.fondo_img = tk.PhotoImage(file=ruta)
        except tk.TclError:
            print(f"No se pudo cargar el archivo {ruta}. Usando fondo de color predeterminado.")
            self.fondo_img = None

    def mostrar_menu(self):
        self.canvas.delete("all")
        if self.fondo_img:
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.fondo_img)
        else:
            self.canvas.create_rectangle(0, 0, self.ancho_celda * self.largo_tablero, self.ancho_celda * self.largo_tablero, fill="lightblue")
        self.canvas.create_text(self.ancho_celda * self.largo_tablero // 2, 100, text="Juego de Gusanito", font=("Helvetica", 24), fill="white")
        boton_iniciar = tk.Button(self.root, text="Iniciar Juego", command=self.pedir_datos_iniciales, width=20, font=("Helvetica", 12))
        self.canvas.create_window(self.ancho_celda * self.largo_tablero // 2, 150, window=boton_iniciar)
        boton_instrucciones = tk.Button(self.root, text="Instrucciones", command=self.mostrar_instrucciones, width=20, font=("Helvetica", 12))
        self.canvas.create_window(self.ancho_celda * self.largo_tablero // 2, 200, window=boton_instrucciones)
        boton_puntuacion = tk.Button(self.root, text="Ver Puntuación", command=self.mostrar_puntuacion, width=20, font=("Helvetica", 12))
        self.canvas.create_window(self.ancho_celda * self.largo_tablero // 2, 250, window=boton_puntuacion)

    def pedir_datos_iniciales(self):
        self.nombre_gusanito = simpledialog.askstring("Nombre del Gusanito", "¿Cuál es el nombre de tu gusanito?", parent=self.root) or "Gusanito"
        self.color_gusanito = simpledialog.askstring("Color del Gusanito", "¿Cuál es el color de tu gusanito?", parent=self.root) or "green"
        self.iniciar_juego()

    def iniciar_juego(self):
        self.gusanito = [[4, 3], [4, 4], [4, 5]]
        self.direccion = "Right"
        self.comida = self.generar_comida()
        self.puntuacion = 0
        self.juego_activo = True
        self.actualizar_juego()

    def cambiar_direccion(self, event):
        if self.juego_activo:
            key = event.keysym
            if key == "Up" and self.direccion != "Down":
                self.direccion = "Up"
            elif key == "Down" and self.direccion != "Up":
                self.direccion = "Down"
            elif key == "Left" and self.direccion != "Right":
                self.direccion = "Left"
            elif key == "Right" and self.direccion != "Left":
                self.direccion = "Right"

    def actualizar_juego(self):
        self.mover_gusanito()
        self.dibujar_gusanito()
        if self.detectar_colision():
            self.mostrar_mensaje("¡Game Over! Presiona 'Enter' para jugar de nuevo o espera para volver al menú.")
        else:
            self.root.after(self.velocidad, self.actualizar_juego)

    def mover_gusanito(self):
        cabeza = self.gusanito[0][:]
        if self.direccion == "Up":
            cabeza[1] -= 1
        elif self.direccion == "Down":
            cabeza[1] += 1
        elif self.direccion == "Left":
            cabeza[0] -= 1
        elif self.direccion == "Right":
            cabeza[0] += 1

        self.gusanito.insert(0, cabeza)
        if cabeza == self.comida:
            self.comida = self.generar_comida()
            self.puntuacion += 10
        else:
            self.gusanito.pop()

    def generar_comida(self):
        while True:
            comida = [random.randint(0, self.largo_tablero - 1), random.randint(0, self.largo_tablero - 1)]
            if comida not in self.gusanito:
                return comida

    def detectar_colision(self):
        cabeza = self.gusanito[0]
        if cabeza[0] < 0 or cabeza[0] >= self.largo_tablero or cabeza[1] < 0 or cabeza[1] >= self.largo_tablero:
            self.guardar_puntuacion()
            return True
        if cabeza in self.gusanito[1:]:
            self.guardar_puntuacion()
            return True
        return False

    def dibujar_gusanito(self):
        self.canvas.delete("all")
        if self.fondo_img:
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.fondo_img)
        else:
            self.canvas.create_rectangle(0, 0, self.ancho_celda * self.largo_tablero, self.ancho_celda * self.largo_tablero, fill="lightblue")

        for segmento in self.gusanito:
            x1, y1 = segmento[0] * self.ancho_celda, segmento[1] * self.ancho_celda
            x2, y2 = x1 + self.ancho_celda, y1 + self.ancho_celda
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color_gusanito, outline="white")

        x1, y1 = self.comida[0] * self.ancho_celda, self.comida[1] * self.ancho_celda
        x2, y2 = x1 + self.ancho_celda, y1 + self.ancho_celda
        self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="white")

    def mostrar_mensaje(self, mensaje):
        self.juego_activo = False
        self.canvas.create_text(self.ancho_celda * self.largo_tablero // 2, self.ancho_celda * self.largo_tablero // 2, text=mensaje, font=("Helvetica", 20), fill="white")
        self.root.after(5000, self.mostrar_menu)

    def reiniciar_juego(self, event=None):
        if not self.juego_activo:
            self.pedir_datos_iniciales()

    def mostrar_instrucciones(self):
        instrucciones = (
            "Instrucciones del Juego:\n\n"
            "- Usa las flechas del teclado para mover el gusanito.\n"
            "- Come la comida roja para crecer y ganar puntos.\n"
            "- No choques contra las paredes o contra tu propio cuerpo.\n"
            "- Puedes reiniciar el juego presionando 'Enter'.\n"
            "- En cada partida, podrás ingresar el nombre y color de tu gusanito."
        )
        messagebox.showinfo("Instrucciones", instrucciones)

    def guardar_puntuacion(self):
        self.puntuaciones.append((self.nombre_gusanito, self.puntuacion))

    def mostrar_puntuacion(self):
        if self.puntuaciones:
            score_text = "Puntuaciones:\n"
            for nombre, puntaje in self.puntuaciones:
                score_text += f"{nombre}: {puntaje}\n"
            messagebox.showinfo("Puntuaciones", score_text)
        else:
            messagebox.showinfo("Puntuaciones", "No hay puntuaciones guardadas aún.")

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoGusanito(root)
    root.mainloop()





