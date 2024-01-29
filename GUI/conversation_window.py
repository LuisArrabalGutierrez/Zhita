import tkinter
import mysql.connector
from functions.map import open_map


def open_conversation_window(cnx, profile, window):
    conversation_window = tkinter.Tk()
    conversation_window.title("Conversation")
    ancho_pantalla = conversation_window.winfo_screenwidth()
    alto_pantalla = conversation_window.winfo_screenheight()
    conversation_window.geometry(f"{ancho_pantalla}x{alto_pantalla}+{ancho_pantalla // 2}+{alto_pantalla // 2}")
    conversation_window.configure(bg="black")

    # Last window open, to close it
    window.destroy()

    # Frame for the conversation with the user
    my_user = profile[0]

    cursor = cnx.cursor()
    cursor.execute(f"SELECT * FROM Conversacion WHERE ID_Usuario='{my_user}' OR ID_Usuario2='{my_user}'")
    conversations = cursor.fetchall()

    # Frame para la conversación
    conversation_frame = tkinter.Frame(conversation_window, bg="black", height=alto_pantalla * 0.9, width=ancho_pantalla)
    conversation_frame.pack(side="top", fill="both", expand=True)


    # For all conversations make a frame
    for i in range(len(conversations)):
        name = conversations[i][0]

        each_conversation_frame = tkinter.Frame(conversation_frame, bg="grey", height=300, width=ancho_pantalla)
        each_conversation_frame.pack(side="top", fill="both", pady=0.5)
        conversation_name = tkinter.Button(each_conversation_frame, text=name, bg="white", fg="black", font=("Arial", 15),
                                           command=lambda n=name, c_id=conversations[i][2]: open_messages(cnx, profile, n, c_id))
        conversation_name.pack(side="top", fill="both", padx=0.5)

    # Footer Frame
    footer_frame = tkinter.Frame(conversation_window, bg="black", height=alto_pantalla * 0.1, width=ancho_pantalla)
    footer_frame.pack(side="bottom", fill="both")

    # Map Button
    map_button = tkinter.Button(footer_frame, text="Map", bg="black", fg="white", command=lambda: open_map(cnx.cursor(), profile), font=("Arial", 15))
    map_button.place(relx=0.95, rely=0.5, anchor="e")

    # Conversation Button
    conversation_button = tkinter.Button(footer_frame, text="Conversation", bg="black", fg="white", font=("Arial", 15))
    conversation_button.place(relx=0.5, rely=0.5, anchor="center")

    # Home Button
    from GUI.meet_people import meet_people_window
    home_button = tkinter.Button(footer_frame, text="Home", bg="black", fg="white", command=lambda: meet_people_window(cnx, profile, conversation_window), font=("Arial", 15))
    home_button.place(relx=0.05, rely=0.5, anchor="w")

    conversation_window.mainloop()


def open_messages(cnx, profile, name, conver_id):
    messages_window = tkinter.Tk()
    messages_window.title("Messages")
    ancho_pantalla = messages_window.winfo_screenwidth()
    alto_pantalla = messages_window.winfo_screenheight()

    messages_window.geometry(f"{ancho_pantalla}x{alto_pantalla}+{ancho_pantalla // 2}+{alto_pantalla // 2}")
    messages_window.configure(bg="black")

    def load_messages(cursor, conver_id, my_id, user_name):
        query = f"SELECT * FROM MensajeConversacion WHERE ID_Conversacion='{conver_id}'"
        cursor.execute(query)
        messages_conversation = cursor.fetchall()

        for message_conversation in messages_conversation:
            message_id = message_conversation[1]

            query = f"SELECT * FROM Mensaje WHERE MensajeID='{message_id}'"
            cursor.execute(query)
            message = cursor.fetchone()

            id_send = message[0]
            id_receive = message[4]
            content = message[2]

            if id_send == my_id:
                sent_message = tkinter.Label(messages_frame, text=content, bg="black", fg="white", font=("Arial", 15), anchor="e",
                                             padx=0.5, pady=0.5, width=100)
                sent_message.pack(side="top", fill="both", expand=True)
            else:
                received_message = tkinter.Label(messages_frame, text=content, bg="black", fg="white", font=("Arial", 15),
                                                 anchor="w", padx=0.5, pady=0.5, width=100)
                received_message.pack(side="top", fill="both", expand=True)

    def send_message():
        cursor0 = cnx.cursor()
        cursor0.execute("INSERT INTO MensajeIdGlobal VALUES (NULL)")

        query0 = "SELECT * FROM MensajeIdGlobal ORDER BY id DESC LIMIT 1"
        cursor0.execute(query0)
        MensajeID = cursor0.fetchone()[0]
        cursor0.close()

        message = entry_message.get()
        cursor = cnx.cursor()

        query = "INSERT INTO Mensaje (ID_USUARIO, MensajeID, Contenido, Fecha, ID_Recibe) VALUES (%s, %s, %s, NOW(), %s)"
        data = (profile[0], MensajeID, message, name)

        cursor.execute(query, data)
        cnx.commit()
        cursor.close()

        cursor2 = cnx.cursor()
        query2 = "INSERT INTO MensajeConversacion (ID_Conversacion, MensajeID) VALUES (%s, %s)"
        data2 = (conver_id, MensajeID)

        cursor2.execute(query2, data2)
        cnx.commit()

        cursor2.close()

        entry_message.delete(0, tkinter.END)

    # Frame for the user info
    user_frame = tkinter.Frame(messages_window, bg="white", height=alto_pantalla * 0.1, width=ancho_pantalla)
    user_frame.pack(side="top", fill="both")

    # Footer Frame
    footer_frame = tkinter.Frame(messages_window, bg="black", height=alto_pantalla * 0.1, width=ancho_pantalla)
    footer_frame.pack(side="bottom", fill="both")

    # Map Button
    map_button = tkinter.Button(footer_frame, text="Map", bg="black", fg="white", command=lambda: open_map(cnx.cursor(), profile), font=("Arial", 15))
    map_button.place(relx=0.95, rely=0.5, anchor="e")

    # Conversation Button
    conversation_button = tkinter.Button(footer_frame, text="Conversation", command=lambda: close_window(messages_window), bg="black", fg="white", font=("Arial", 15))
    conversation_button.place(relx=0.5, rely=0.5, anchor="center")

    # Home Button
    from GUI.meet_people import meet_people_window
    home_button = tkinter.Button(footer_frame, text="Home", bg="black", fg="white", command=lambda: meet_people_window(cnx, profile, messages_window), font=("Arial", 15))
    home_button.place(relx=0.05, rely=0.5, anchor="w")


    # Get user_name from the parameter
    user_name = name
    user_label = tkinter.Label(user_frame, text=user_name, bg="white", fg="black", font=("Arial", 15))
    user_label.place(relx=0.5, rely=0.5, anchor="w")

    # sent_messages_frame
    new_height = (messages_window.winfo_height() * 0.8)
    messages_frame = tkinter.Frame(messages_window, bg="grey", height=f"{new_height}", width=ancho_pantalla)
    messages_frame.pack(side="top", fill="both", expand=True)


    # Frame for the text to send
    text_frame = tkinter.Frame(messages_window, bg="grey", height=alto_pantalla * 0.1, width=ancho_pantalla)
    text_frame.pack(side="bottom", fill="both",)
    entry_message = tkinter.Entry(text_frame, bg="white", fg="black", font=("Arial", 15))
    entry_message.place(relx=0.5, rely=0.5, anchor="w")

    # Send Button
    send_button = tkinter.Button(text_frame, text="Send", command=lambda: send_message(), bg="black", fg="white", font=("Arial", 15))
    send_button.place(relx=0.95, rely=0.5, anchor="e")
   
    load_messages(cnx.cursor(), conver_id, my_id=profile[0], user_name=user_name)

    
    messages_window.mainloop()


def close_window(window):
    window.destroy()

 