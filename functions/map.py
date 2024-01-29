

#for the map
import webbrowser
import mplleaflet
import requests
import folium


def get_coords(location):
    nominatim_endpoint = "https://nominatim.openstreetmap.org/search"
    direction = ', '.join([location[2], location[4], location[0], location[1]])
    print(direction)
    params = {
        "q": direction,  # Utiliza la dirección construida
        "format": "json"
    }

    response = requests.get(nominatim_endpoint, params=params)
    data = response.json()

    if response.status_code == 200 and data:
        location = data[0]
        print(location)
        return float(location["lat"]), float(location["lon"])
    else:
        print("Error")

def open_map(cursor,profile):

    id_user = profile[0]

    cursor.execute(f"SELECT * FROM Ubicacion WHERE ID_Usuario = '{id_user}'")
    location = cursor.fetchone()
    
    if location:
        coords=get_coords(location)
        
        if coords:
            map=folium.Map(location=coords, zoom_start=15)

            folium.Marker(
                location=coords,
                popup="You are here",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(map)
            
            map.save("./maps/map.html")
            webbrowser.open("./maps/map.html")

        else:
            print("No hay coordenadas")




def get_my_location(cursor,my_user):

    cursor.execute(f"SELECT * FROM Ubicacion WHERE ID_Usuario = '{my_user}'")
    
    my_location = cursor.fetchone()

    if(my_location):   
        my_city=my_location[0]
        my_country=my_location[1]
        my_province=my_location[4]

        
        return my_city,my_province, my_country
    
    else:
        print("No hay ubicacion")
        return None
    


def profiles_location(cursor,my_location,my_user):
    #my_location is a tuple with the location data from Ubicacion

    my_city=my_location[0]
    my_province=my_location[1]
    my_country=my_location[2]
    
    cursor.execute(f"SELECT * FROM Ubicacion WHERE Ciudad = '{my_city}' AND Pais = '{my_country}' AND Provincia = '{my_province}'")

    #all the tuples of the table Ubicacion in my location with their info
    #[('Madrid', 'España', 'Gran Via','Luis', 'Madrid')]
    #[('Madrid', 'España', 'Via Mayor','Javier', 'Madrid')]
    #.....
    tuples_location = cursor.fetchall()

    #array of tuples with the profiles in my location
    profiles_names = []

    for name in tuples_location:
        if name[3] != my_user:    
            #profiles_names.append(name[3])
            cursor.execute(f"SELECT * FROM PerfilUsuario WHERE ID_Usuario = '{name[3]}'")
            profile = cursor.fetchone()
            profiles_names.append(profile)
        

    return profiles_names
    
    