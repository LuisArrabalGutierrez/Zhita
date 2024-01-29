import tkinter as tk
from PIL import ImageTk, Image
from GUI.create_account import create_account_window  
from GUI.login_window import login_window
import mysql.connector
from GUI.fonts.fonts import bg_color

def on_window_configure(event):
    img_frame.configure(width=ventana.winfo_width() * 0.4)
    empty_frame.configure(width=ventana.winfo_width() * 0.6)

####Conexion BD####
####CONECTAR A bd####
config = {
    "user": "admin",
    "password": "Ll488433",
    "host": "matchapp.cbgmo2ki0s6l.eu-west-2.rds.amazonaws.com",
    "port": 3306,
    "database": "MATCHAPP"
}
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")

####INTERFAZ####
ventana = tk.Tk()
ventana.title("Zhita")

ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
nuevo_ancho = ancho_pantalla
nuevo_alto = alto_pantalla

ventana.geometry(f"{nuevo_ancho}x{nuevo_alto}+{nuevo_ancho // 2}+{nuevo_alto // 2}")

# Cargar la imagen desde un archivo (asegúrate de que la ruta sea correcta)
zhita_img = Image.open("./images/zhita.png")
zhita_img = ImageTk.PhotoImage(zhita_img)


# Frame para la imagen
img_frame = tk.Frame(ventana, bd=0, height=alto_pantalla * 0.4, relief=tk.SOLID, bg="grey")
img_frame.pack(side="top", expand=tk.YES, fill=tk.BOTH)

# Label para la imagen
label_zhita = tk.Label(img_frame, image=zhita_img, bg="black")
label_zhita.pack(fill=tk.BOTH, expand=tk.YES)

# Frame vacío para ocupar el espacio restante a la izquierda
empty_frame = tk.Frame(ventana, height=alto_pantalla * 0.6, bg="black")
empty_frame.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

####CREATE ACCOUNT BUTTON####
create_account_button = tk.Button(ventana, text="Create Account", bg="black", fg="white", command=lambda: create_account_window(cnx, ventana))
create_account_button.place(relx=0.5, rely=0.7, anchor="center")

####LOGIN BUTTON####
login_button = tk.Button(ventana, text="Login Account", bg="black", fg="white", command=lambda: login_window(cnx, ventana))
login_button.place(relx=0.5, rely=0.8, anchor="center")

ventana.bind("<Configure>", on_window_configure)
ventana.mainloop()

####CERRAR CONEXION####
cnx.close()
