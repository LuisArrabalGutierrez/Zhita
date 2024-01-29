import tkinter
import mysql.connector
from GUI.login_window import login_window
from sql.functions_sql import log_account,log_location,log_profile


def create_account_window(cnx,ventana_principal):

    cursor = cnx.cursor()
    

        
    ####INTERFAZ####
    

    ancho_pantalla = ventana_principal.winfo_screenwidth()
    alto_pantalla = ventana_principal.winfo_screenheight()
    nuevo_ancho = ancho_pantalla
    nuevo_alto = alto_pantalla


    account_window = tkinter.Toplevel(ventana_principal)
    account_window.title("Create Account")
    account_window.geometry(f"{nuevo_ancho}x{nuevo_alto}+{nuevo_ancho // 2}+{nuevo_alto // 2}")
    account_window.configure(bg="black")

    ####Label Crear cuenta####
    label_create_account = tkinter.Label(account_window, text="Create Account", bg="black", fg="pink")
    label_create_account.place(x="100", y="50", anchor="center",width=200, height=50)
    
    ####Label ID usuario####
    label_id = tkinter.Label(account_window, text="user ID", bg="black", fg="pink")
    label_id.place(x="100", y="100", anchor="center")
    entry_id = tkinter.Entry(account_window)
    entry_id.place(x="100", y="150", anchor="center")
    

    ####Label Nombre####
    label_name = tkinter.Label(account_window, text="Name", bg="black", fg="pink")
    label_name.place(x="100", y="200", anchor="center")
    entry_name = tkinter.Entry(account_window)
    entry_name.place(x="100", y="250", anchor="center")

    ####Label Apellido####
    label_surname = tkinter.Label(account_window, text="Surname", bg="black", fg="pink")
    label_surname.place(x="100", y="300", anchor="center")
    entry_surname = tkinter.Entry(account_window)
    entry_surname.place(x="100", y="350", anchor="center")

    ####Label Email####
    label_email = tkinter.Label(account_window, text="E-mail", bg="black", fg="pink")
    label_email.place(x="100", y="400", anchor="center")
    entry_email = tkinter.Entry(account_window)
    entry_email.place(x="100", y="450", anchor="center")

    ####Label Password####
    label_password = tkinter.Label(account_window, text="Password", bg="black", fg="pink")
    label_password.place(x="100", y="500", anchor="center")
    entry_password = tkinter.Entry(account_window)
    entry_password.place(x="100", y="550", anchor="center")

    ####Label Telefono####
    label_phone = tkinter.Label(account_window, text="Telephone", bg="black", fg="pink")
    label_phone.place(x="100", y="600", anchor="center")
    entry_phone = tkinter.Entry(account_window)
    entry_phone.place(x="100", y="650", anchor="center")

    ####Label Ciudad####
    label_city = tkinter.Label(account_window, text="City", bg="black", fg="pink")
    label_city.place(x="500", y="100", anchor="center")
    entry_city = tkinter.Entry(account_window)
    entry_city.place(x="500", y="150", anchor="center")

    ####Label Pais####
    label_country = tkinter.Label(account_window, text="Country", bg="black", fg="pink")
    label_country.place(x="500", y="200", anchor="center")
    entry_country = tkinter.Entry(account_window)
    entry_country.place(x="500", y="250", anchor="center")

    ####Label Calle####
    label_street = tkinter.Label(account_window, text="Street", bg="black", fg="pink")
    label_street.place(x="500", y="300", anchor="center")
    entry_street = tkinter.Entry(account_window)
    entry_street.place(x="500", y="350", anchor="center")

    ####Label Provincia####
    label_province = tkinter.Label(account_window, text="Province", bg="black", fg="pink")
    label_province.place(x="500", y="400", anchor="center")
    entry_province = tkinter.Entry(account_window)
    entry_province.place(x="500", y="450", anchor="center")

    ####Label Genero, entrada 'M' o 'F'####
    label_genre = tkinter.Label(account_window, text="Genre ('M' o 'F')", bg="black", fg="pink")
    label_genre.place(x="500", y="500", anchor="center")
    entry_genre = tkinter.Entry(account_window)
    entry_genre.place(x="500", y="550", anchor="center")

    ####Label Edad####
    label_age = tkinter.Label(account_window, text="Age", bg="black", fg="pink")
    label_age.place(x="500", y="600", anchor="center")
    entry_age = tkinter.Entry(account_window)
    entry_age.place(x="500", y="650", anchor="center")

    ####Label Descripcion####
    label_description = tkinter.Label(account_window, text="Description", bg="black", fg="pink", width="60", height="20")
    label_description.place(x="900", y="100", anchor="center")
    entry_description = tkinter.Entry(account_window)
    entry_description.place(x="900", y="150", anchor="center")

    ####Function create account####
    def create_account():
        user_id = entry_id.get()
        name = entry_name.get()
        surname = entry_surname.get()
        email = entry_email.get()
        password = entry_password.get()
        telephone = entry_phone.get()

        city= entry_city.get()
        country = entry_country.get()
        street = entry_street.get()
        province = entry_province.get()

        genre = entry_genre.get()
        age = entry_age.get()
        description = entry_description.get()

        try:
            log_account(cursor,user_id, name, surname, email, password, telephone)
            log_location(cursor,user_id, city, country, street, province)
            log_profile(cursor,user_id,genre,age,description)
            cnx.commit()
            account_window.destroy()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            


        #account_window.destroy()
        cursor.close()
        login_window(cnx,ventana_principal)
        

        
    ####Boton Crear cuenta####
    button_create_account = tkinter.Button(account_window, text="Create Account", bg="black", fg="white", borderwidth=0, relief="flat",command=lambda: create_account())

    button_create_account.place(x="100", y="700", anchor="center", width="200", height="50")


    account_window.mainloop()
    
    