

CREATE TABLE PerfilUsuario (
    ID_Usuario VARCHAR(20) PRIMARY KEY REFERENCES USUARIO(id_usuario),
    Descripcion VARCHAR(500),
    Genero CHAR(1) CHECK (Genero IN ('M', 'F')),
    Edad INT
);

CREATE TABLE Ubicacion(
    ----
    Ciudad VARCHAR(20) ,
    Pais VARCHAR(20),
    Calle VARCHAR(20),
    Provincia VARCHAR(20),
    ---- ALL HAVE TO REFERENCE EACH VAIABLE FROM USUARIO
    ID_Usuario VARCHAR(20) REFERENCES PerfilUsuario(ID_Usuario),
    PRIMARY KEY(Ciudad,Pais,Calle,ID_Usuario)
);



ALTER TABLE USUARIO ADD FOREIGN KEY (Ciudad) REFERENCES Ubicacion(Ciudad);
ALTER TABLE USUARIO ADD FOREIGN KEY (Pais) REFERENCES Ubicacion(Pais);
ALTER TABLE USUARIO ADD FOREIGN KEY (Calle) REFERENCES Ubicacion(Calle);
ALTER TABLE USUARIO ADD FOREIGN KEY (Provincia) REFERENCES Ubicacion(Provincia);


CREATE TABLE Aceptados(
    ID_Usuario VARCHAR(20) REFERENCES USUARIO(ID_Usuario),
    ID_Usuario2 VARCHAR(20) REFERENCES USUARIO(ID_Usuario),
    PRIMARY KEY(ID_Usuario, ID_Usuario2)
);


CREATE TABLE Mensaje(
    ID_USUARIO VARCHAR(20) NOT NULL,
    MensajeID INT NOT NULL PRIMARY KEY,
    Contenido TEXT NOT NULL,
    Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_USUARIO) REFERENCES USUARIO(ID_Usuario)

);

CREATE TABLE Conversacion(
    ID_Usuario VARCHAR(20) NOT NULL,
    ID_Usuario2 VARCHAR(20) NOT NULL,
    ID_Conversacion INT NOT NULL PRIMARY KEY,
    FOREIGN KEY (ID_Usuario) REFERENCES USUARIO(ID_Usuario),
    FOREIGN KEY (ID_Usuario2) REFERENCES USUARIO(ID_Usuario)
);

CREATE TABLE MensajeConversacion(
    ID_Conversacion INT NOT NULL,
    MensajeID INT NOT NULL,
    FOREIGN KEY (ID_Conversacion) REFERENCES Conversacion(ID_Conversacion),
    FOREIGN KEY (MensajeID) REFERENCES Mensaje(MensajeID)
);


CREATE TABLE Matchs (
    ID_Match INT PRIMARY KEY ,
    ID_Usuario VARCHAR(20) NOT NULL,
    ID_Usuario2 VARCHAR(20) NOT NULL,
    FOREIGN KEY (ID_Usuario) REFERENCES USUARIO(id_usuario),
    FOREIGN KEY (ID_Usuario2) REFERENCES USUARIO(id_usuario)
);
--ALTER TABLE Matchs 
--MODIFY COLUMN ID_Match INT AUTO_INCREMENT;

--ALTER TABLE Mensaje
--ADD COLUMN ID_Recibe VARCHAR(20) NOT NULL,
--ADD FOREIGN KEY (ID_Recibe) REFERENCES USUARIO(id_usuario);


--CREATE TABLE MensajeIdGlobal (
 --   id INT PRIMARY KEY AUTO_INCREMENT
--);

-- to solve the problem with the primary key of mensajes
-- this primary key will be being auto incremented and i'll 
-- take this id and then the message will be inserted with this id ,
-- i'll insert thee last id and the id will be incremented for the next message 



-- Eliminar todos los registros de la tabla Aceptados
DELETE FROM Aceptados;



-- Eliminar todos los registros de la tabla Matchs
DELETE FROM Matchs;
-- Eliminar todos los registros de la tabla Mensaje
DELETE FROM Mensaje;
-- Eliminar todos los registros de la tabla Conversacion
DELETE FROM Conversacion;

-- Eliminar todos los registros de la tabla MensajeConversacion
DELETE FROM MensajeConversacion;

-- Eliminar todos los registros de la tabla MensajeIdGlobal
DELETE FROM MensajeIdGlobal;

-- Eliminar todos los registros de la tabla PerfilUsuario
DELETE FROM PerfilUsuario;

-- Eliminar todos los registros de la tabla USUARIO
DELETE FROM USUARIO;

-- Eliminar todos los registros de la tabla Ubicacion
DELETE FROM Ubicacion;

