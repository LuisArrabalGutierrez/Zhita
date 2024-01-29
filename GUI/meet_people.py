import tkinter
import mysql.connector
import threading

from sql.functions_sql import select_user_usertable,select_user_profiletable,check_matchs
from functions.map import open_map, get_my_location, profiles_location
from GUI.conversation_window import open_conversation_window

def meet_people(cnx,email, password,window):
    try:
        cursor = cnx.cursor()

        user = select_user_usertable(cursor,email,password)

        if user:
            id_user = user[0]
            
            profile = select_user_profiletable(cursor,id_user)

            if not profile:
                print("No hay perfil")  

            
            meet_people_window(cnx,profile,window)
            
            
           
        else:
            print("No hay usuario")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

######################################################


#profile is the tuple with the profile data from PerfilUsuario
def meet_people_window(cnx,profile,window):
    
    
    cursor=cnx.cursor()
    
    meet_people_view= tkinter.Tk()
    
    ancho_pantalla = meet_people_view.winfo_screenwidth()
    alto_pantalla = meet_people_view.winfo_screenheight()
    nuevo_ancho = ancho_pantalla
    nuevo_alto = alto_pantalla

    meet_people_view.geometry(f"{nuevo_ancho}x{nuevo_alto}+{nuevo_ancho // 2}+{nuevo_alto // 2}")
    meet_people_view.title("Meet People")
    meet_people_view.configure(bg="black")

    

    ####Footer Frame####
    footer_frame = tkinter.Frame(meet_people_view, bg="black", width=ancho_pantalla, height=100)
    footer_frame.place(x=0, y=alto_pantalla - 50, anchor="sw")

    ####MAP BUTTON####
    map_button = tkinter.Button(footer_frame, text="Map", bg="black", fg="white", command=lambda: open_map(cursor, profile),font=("Arial", 15))
    map_button.place(relx=0.95, rely=0.5, anchor="e")

    ####Conversation BUTTON####
    conversation_button = tkinter.Button(footer_frame, text="Conversation", bg="black", fg="white", command=lambda: open_conversation_window(cnx,profile,meet_people_view),font=("Arial", 15))
    conversation_button.place(relx=0.5, rely=0.5, anchor="center")

    ####HOME BUTTON####
    home_button = tkinter.Button(footer_frame, text="Home", bg="black", fg="white",font=("Arial", 15))
    home_button.place(relx=0.05, rely=0.5, anchor="w")

    ####PROFILES FRAME####
    profiles_frame = tkinter.Frame(meet_people_view, bg="grey",width=600, height=800)
    profiles_frame.place(x=ancho_pantalla/2 , y=alto_pantalla/2-100, anchor="center")


    #check if there are matchs
    threading.Thread(target=check_matchs_periodic).start()


    # first i get my user, then i get my location, then i get the profiles in my location
    my_user=profile[0]
    #return city,province,country
    my_location = get_my_location(cursor,my_user)
    #return profiles from PerfilUsuario in my location
    profiles_names = profiles_location(cursor,my_location,my_user)
    
    current_profile_index = 0

    #-----------------------------------------------

    def no_more_profiles():
            
            no_profiles_frame = tkinter.Frame(meet_people_view, bg="grey", width=1000, height=1000)
            no_profiles_frame.place(x=ancho_pantalla//2-100 , y=alto_pantalla//2-100, anchor="center")
            no_profiles_label = tkinter.Label(no_profiles_frame, text="No more profiles in this location", font=("Arial", 20))
            no_profiles_label.pack(pady=10)
            profiles_frame.destroy()


    # Función para actualizar las etiquetas de perfil
    def update_profile_labels(current_profile_index):
        
        

        #.........................................
            
        if current_profile_index == len(profiles_names):
            no_more_profiles()
            return
            

        current_profile = profiles_names[current_profile_index]

        # Limpiar cualquier widget anterior en el frame de perfiles
        for widget in profiles_frame.winfo_children():
            widget.destroy()

        # Etiquetas para mostrar información del perfil actual
        label_description = tkinter.Label(profiles_frame, text=f"Name: {current_profile[0]}", font=("Arial", 10))
        label_description.pack(pady=10)

        label_description = tkinter.Label(profiles_frame, text=f"Description: {current_profile[1]}", font=("Arial", 8))
        label_description.pack(pady=10)

        # Botones para aceptar o rechazar
        accept_button = tkinter.Button(profiles_frame, text="❤️", borderwidth=0, relief="flat",command=lambda: show_next_profile(accept=True))
        accept_button.pack(side="left", padx=20)

        decline_button = tkinter.Button(profiles_frame, text="❌", borderwidth=0, relief="flat",command=lambda: show_next_profile(accept=False))
        decline_button.pack(side="right", padx=20)

    #------------------------------------------------
    if profiles_names:
        update_profile_labels(current_profile_index)
    else:
        # Mostrar algún mensaje o acción cuando no hay perfiles en esta ubicación
        print("No hay perfiles en esta ubicación UPDATE_PROFILE_LABELS.")

    #--------------------------------------------------
    def show_next_profile(accept=True):
        nonlocal current_profile_index

        my_user_id = profile[0]
        
        # Verificar si hay más perfiles
        if current_profile_index < len(profiles_names):
            current_profile_id = profiles_names[current_profile_index][0]

            
            # Comprobar si ya existe una entrada en la tabla Aceptados
            cursor.execute(f"SELECT * FROM Aceptados WHERE ID_Usuario = '{my_user_id}' AND ID_Usuario2 = '{current_profile_id}'")
            user_accepted = cursor.fetchone()

            if user_accepted:
                print(f"El perfil con ID {current_profile_id} ya ha sido aceptado anteriormente.")
                current_profile_index += 1
                return
                # Puedes tomar acciones adicionales aquí si es necesario
            else:
                if accept:
                    # Comprobar si el perfil ya ha sido aceptado
                    cursor.execute(f"SELECT * FROM Aceptados WHERE ID_Usuario = '{my_user}' AND ID_Usuario2 = '{current_profile_id}'")
                    user_accepted = cursor.fetchone()

                    if user_accepted:
                        print(f"Ya aceptado el perfil con ID {current_profile_id}")
                        # Puedes tomar acciones adicionales aquí si es necesario
                    else:
                        print(f"Aceptado el perfil con ID {current_profile_id}")
                        cursor.execute(f"INSERT INTO Aceptados (ID_Usuario,ID_Usuario2) VALUES ('{my_user}','{current_profile_id}')")
                        cnx.commit()
                else:
                    print(f"Rechazado el perfil con ID {current_profile_id}")
                    # Aquí puedes realizar acciones adicionales si el perfil es rechazado

                current_profile_index += 1
                # Actualizar la interfaz gráfica con el próximo perfil
                update_profile_labels(current_profile_index)
        else:
            print("No hay perfiles en esta ubicación SHOW_NEXT_PROFILE.")
            no_more_profiles()


    #łast window open, to close it
    window.destroy()
   
    meet_people_view.mainloop()

#####################################################

def check_matchs_periodic():
    # Crear una nueva conexión en este hilo
    config = {
        "user": "admin",
        "password": "Ll488433",
        "host": "matchapp.cbgmo2ki0s6l.eu-west-2.rds.amazonaws.com",
        "port": 3306,
        "database": "MATCHAPP"
    }
    cnx = mysql.connector.connect(**config)
    cursor=cnx.cursor()
    try:
        check_matchs(cursor)
    finally:
        # Asegurarse de cerrar la conexión
        
        cnx.close()
    
    # Programar la ejecución periódica
    threading.Timer(30, check_matchs_periodic).start()
