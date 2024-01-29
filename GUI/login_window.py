import tkinter
import mysql.connector
from tkinter import messagebox
from GUI.meet_people import meet_people
from sql.functions_sql import log_login


def login_window(cnx,ventana):

    login_window_view= tkinter.Toplevel(ventana)
    ancho_pantalla = login_window_view.winfo_screenwidth()
    alto_pantalla = login_window_view.winfo_screenheight()
    nuevo_ancho = 1920
    nuevo_alto = 1080

    
    
    def login():

        email=entry_email.get()
        password=entry_password.get()

       
        cursor = cnx.cursor()
            

        if log_login(cursor, email, password):
            login_window_view.destroy()

            meet_people(cnx,email, password,login_window_view)
            

                
        else:
            messagebox.showerror("Error","Email o contraseña incorrectos")

       
        
        cursor.close()


    
    ####INTERFAZ####
    login_window_view.geometry(f"{nuevo_ancho}x{nuevo_alto}+{nuevo_ancho // 2}+{nuevo_alto // 2}")
    login_window_view.title("Login")
    login_window_view.configure(bg="black")

    
    ####Label Login####
    label_login = tkinter.Label(login_window_view, text="Login", bg="black", fg="pink", font=(20))
    label_login.place(x=nuevo_alto/2 + 400 , y= "100", anchor="center") 

    ####Label email####
    label_email = tkinter.Label(login_window_view, text="Email", bg="black", fg="pink")
    label_email.place(x=nuevo_alto/2 + 400, y="200", anchor="center")
    entry_email = tkinter.Entry(login_window_view)
    entry_email.place(x=nuevo_alto/2 + 400, y="250", anchor="center")
    
    ####Label password####
    label_password = tkinter.Label(login_window_view, text="Password", bg="black", fg="pink")
    label_password.place(x=nuevo_alto/2 + 400, y="400", anchor="center")
    entry_password = tkinter.Entry(login_window_view)
    entry_password.place(x=nuevo_alto/2 + 400, y="450", anchor="center")

    ####Boton login####
    login_button = tkinter.Button(login_window_view, text="Login", bg="black", fg="white",borderwidth=0, relief="flat", command=lambda: login())
    login_button.place(x=nuevo_alto/2 + 400, y="500", anchor="center")

    #ventana.destroy()
    ventana.withdraw()
    login_window_view.mainloop()
