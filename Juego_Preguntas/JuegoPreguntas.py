# Importamos los módulos necesarios
import tkinter
from PIL import Image, ImageTk
import sqlite3

# Base de Datos de Sqlite
# Conecta con la base de datos
conn = sqlite3.connect("Jugadores.db")
cursor = conn.cursor() # Creamos el cursor
cursor.execute("""CREATE TABLE IF NOT EXISTS jugadores(id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, puntuacion INTEGER DEFAULT 0)""")
conn.commit() # Se confirma la creación de la tabla

# Las preguntas y contador de respuestas dadas -------------------------------------------------------------------------------------------------
preguntas = [("¿Cuál es el villano principal de Fallout 1? \n A. El Maestro \n B. Frank Horrigan \n C. Harold", "A"),("¿Cuál es la mejor armadura de Fallout 1? \n A. Servoarmadura \n B. Escudo Gamma \n C. Armadura de Sierra Madre", "A"),("¿Qué vehículo consigues en Fallout 1? \n A. Una moto \n B. Un coche \n C. Ninguno", "C"),("¿Quién rompe el chip de agua? \n A. Se rompe solo \n B. El protagonista de Fallout 2 viajando en el tiempo \n C. El Supervisor", "B"),("¿Es posible ligar con Tandi en Shady Sands? \n A. Solo siendo hombre \n B. Solo siendo mujer \n C. No se puede, es menor", "C"),("¿Cuál es el mejor atributo de Fallout 1? \n A. Carisma \n B. Agilidad \n C. Fuerza", "B"),("¿Dónde tiene su guarida el Maestro? \n A. La Base Mariposa \n B. La Base Militar \n C. La Catedral", "C"),("¿Qué causa más daño en todo el juego? \n A. La Ametralladora Láser \n B. Un aliado disparandote por la espalda \n C. Un Sanguinario", "B"),("¿Cuántas cuerdas se necesitan para completar la historia? \n A. Tres \n B. Cinco \n C. Dos", "A"),("¿El morador del refugio canónicamente? \n A. Es virgen \n B. Es un cyborg \n C. Sacó el palo más corto", "C")]
respuestas = 0
# -----------------------------------------------------------------------------------------------------------------------------------------------------
# La fuente y color del texto
estilo_fuente = ("Courier", 18, "bold")
color_texto = "#00FF00"  # Verde fosforescente

# Las funciones del juego ------------------------------------------------------------------------------------------------------------------------------
# Para crear nuevas ventanas
def mostrar_pregunta(nombre_jugador):
    global preguntas
    global respuestas

    if respuestas >= len(preguntas):
        ventana_preguntas = tkinter.Toplevel()
        ventana_preguntas.title(f"FIN")
        ventana_preguntas.geometry("1520x1136")

        # Cargar la imagen
        imagen_original = Image.open("Media/HUD_Fallout.png")
        imagen_fondo = ImageTk.PhotoImage(imagen_original)
        ventana_preguntas.imagen_fondo = imagen_fondo

        # Se pone como fondo
        fondo = tkinter.Label(ventana_preguntas, image=imagen_fondo)
        fondo.place(x=0, y=0, relwidth=1, relheight=1)

        cursor.execute("SELECT puntuacion FROM jugadores WHERE nombre = ?", (nombre_jugador,))
        resultado = cursor.fetchone()

        texto_puntos = {f"Tu puntuación es: \n {nombre_jugador}: {resultado}"}

        puntuacion_display = tkinter.Label(ventana_preguntas, text=texto_puntos, font=estilo_fuente, fg=color_texto, bg="black"); puntuacion_display.pack()
        puntuacion_display.place(relx=0.90, rely=0.3, anchor="e")
    
    else:
        ventana_preguntas = tkinter.Toplevel()
        ventana_preguntas.title(f"Pregunta {respuestas + 1}")
        ventana_preguntas.geometry("1520x1136")

        # Cargar la imagen
        imagen_original = Image.open("Media/HUD_Fallout.png")
        imagen_fondo = ImageTk.PhotoImage(imagen_original)
        ventana_preguntas.imagen_fondo = imagen_fondo

        # Se pone como fondo
        fondo = tkinter.Label(ventana_preguntas, image=imagen_fondo)
        fondo.place(x=0, y=0, relwidth=1, relheight=1)

        pregunta_display = tkinter.Label(ventana_preguntas, text=preguntas[respuestas][0], font=estilo_fuente, fg=color_texto, bg="black"); pregunta_display.pack()
        pregunta_display.place(relx=0.90, rely=0.3, anchor="e")

        def responder(eleccion):
            global respuestas
            global preguntas
            if eleccion == preguntas[respuestas][1]:
                print("Correcto")
                cursor.execute('update jugadores set puntuacion = puntuacion + 10 where nombre = ?', (nombre_jugador,))
                conn.commit()
            else:
                print("Incorrecto")
            ventana_preguntas.destroy()
            respuestas += 1
            mostrar_pregunta(nombre_jugador)

        boton_1 = tkinter.Button(ventana_preguntas, text="A", font=estilo_fuente, fg=color_texto, bg="black", command=lambda: responder('A')); boton_1.pack()
        boton_1.place(relx=0.70, rely=0.4, anchor="e")
        boton_2 = tkinter.Button(ventana_preguntas, text="B", font=estilo_fuente, fg=color_texto, bg="black", command=lambda: responder('B')); boton_2.pack()
        boton_2.place(relx=0.70, rely=0.5, anchor="e")
        boton_3 = tkinter.Button(ventana_preguntas, text="C", font=estilo_fuente, fg=color_texto, bg="black", command=lambda: responder('C')); boton_3.pack()
        boton_3.place(relx=0.70, rely=0.6, anchor="e")

# Verificar usuario
def verificar():
    nombre_jugador = nombre_introduccion.get()
    ventana.destroy()
    cursor.execute('INSERT INTO jugadores (nombre, puntuacion) values (?,?)', (nombre_jugador, 0))
    conn.commit()
    mostrar_pregunta(nombre_jugador)

# Creamos la ventana
ventana = tkinter.Tk()
ventana.title("Preguntas")
ventana.geometry('1520x1136')

# Cargar la imagen
imagen_original = Image.open("Media/HUD_Fallout.png")
imagen_fondo = ImageTk.PhotoImage(imagen_original)
ventana.imagen_fondo = imagen_fondo

# Se pone como fondo
fondo = tkinter.Label(ventana, image=imagen_fondo)
fondo.place(x=0, y=0, relwidth=1, relheight=1)

titulo = tkinter.Label(ventana, text="JUEGO DE PREGUNTAS", font=estilo_fuente, fg=color_texto, bg="black"); titulo.pack()
titulo.place(relx=0.75, rely=0.4, anchor="e")

nombre_introduccion = tkinter.Entry(ventana, font=estilo_fuente, fg=color_texto, insertbackground="#00FF00", bg="black"); nombre_introduccion.pack()
nombre_introduccion.place(relx=0.75, rely=0.5, anchor="e")

boton_verificar = tkinter.Button(ventana, text="Verificar", font=estilo_fuente, fg=color_texto, bg="black", command=verificar); boton_verificar.pack()
boton_verificar.place(relx=0.75, rely=0.6, anchor="e")

ventana.mainloop()