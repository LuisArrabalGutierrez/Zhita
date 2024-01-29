
def log_account(cursor,user_id, name, surname, email, password, telephone):
    cursor.execute(f"INSERT INTO USUARIO (id_usuario, nombre, apellido, email, contrasena, Telefono) VALUES ('{user_id}', '{name}', '{surname}', '{email}', '{password}', '{telephone}')")

def log_location(cursor,user_id, city, country, street, province):
    cursor.execute(f"INSERT INTO Ubicacion (id_usuario, Ciudad, Pais, Calle, Provincia) VALUES ('{user_id}', '{city}', '{country}', '{street}', '{province}')")
    cursor.execute(f"UPDATE USUARIO SET Ciudad = '{city}', Pais = '{country}', Calle = '{street}', Provincia = '{province}' WHERE ID_Usuario = '{user_id}'")
    cursor.execute("COMMIT")

def log_profile(cursor,user_id,genre,age,description):
    cursor.execute(f"INSERT INTO PerfilUsuario (ID_Usuario, Genero, Edad, Descripcion) VALUES ('{user_id}', '{genre}', '{age}', '{description}')")
    cursor.execute("COMMIT")
    
def log_login(cursor, email, password):
    cursor.execute(f"SELECT * FROM USUARIO WHERE email='{email}' AND contrasena='{password}'")
    return cursor.fetchone()

def select_user_usertable(cursor,email,password):
    cursor.execute( f"SELECT id_usuario FROM USUARIO WHERE email = '{email}' AND contrasena = '{password}'")
    return cursor.fetchone()

def select_user_profiletable(cursor,id_user):
    cursor.execute(f"SELECT * FROM PerfilUsuario WHERE ID_Usuario = '{id_user}'")
    return cursor.fetchone()


def check_matchs(cursor):
    
    query = "INSERT INTO Matchs (ID_Usuario, ID_Usuario2) SELECT a.ID_Usuario, a.ID_Usuario2 FROM Aceptados a WHERE NOT EXISTS (SELECT 1 FROM Matchs m WHERE (m.ID_Usuario = a.ID_Usuario AND m.ID_Usuario2 = a.ID_Usuario2) OR (m.ID_Usuario = a.ID_Usuario2 AND m.ID_Usuario2 = a.ID_Usuario))"
    cursor.execute(query)

    id_match=cursor.lastrowid

    cursor.execute("COMMIT")

    

    create_conversation(cursor,id_match)
    

def create_conversation(cursor, id_match):
    try:
        # Obtener los usuarios asociados al ID_Match
        query_get_users = f"SELECT ID_Usuario, ID_Usuario2 FROM Matchs WHERE ID_Match = {id_match}"
        cursor.execute(query_get_users)
        users = cursor.fetchone()

      
        
        if users:
            # Crear la tupla en la tabla Conversacion
            query_create_conversation = f"INSERT INTO Conversacion (ID_Usuario, ID_Usuario2, ID_Conversacion) VALUES ('{users[0]}', '{users[1]}', {id_match})"
            cursor.execute(query_create_conversation)
            cursor.execute("COMMIT")
            print("Conversación creada")
        else:
            print("No se ha podido crear la conversacion")
    
    except Exception as e:
        print(f"Error al crear la conversación: {e}")


