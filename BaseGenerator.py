import random
import string
import json
import os.path
from pathlib import Path


class UserGenerator:
    def __init__(self, TOTAL, SEC):# TOTAL hace referencia a la cantidad de Usuarios que deseamos Generar, SEC se refiere a la cantidad de caracteré de la contraseña que se genera
        self.total = TOTAL
        self.sec = SEC
        self.characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
        self.character= list(string.ascii_letters + string.digits)
        self.listName = ["Marcos", "Antonia", "Juanjo", "Maria", "Pablo", "Gonzalo", "Adrian", "David", "Cristina",
                    "Ana", "Lucia", "Alvaro", "Pedro", "Laura", "Mercedes", "Clara", "Paula", "Alverto"]

    #Funcion que genera usuarios y contraseñas de forma aleatoria
    def generateName (self):

        password = ""
        shuffle = self.characters
        random.shuffle(shuffle)
        name = self.listName[random.randint(0, len(self.listName) - 1)]+str(random.randint(0,999))
        for e in range(self.sec):
            password = password + shuffle[e]
        return [str(name), str(password)]

    #Funcion que genera por cada usuario un numero aleatorio de listas dentro de una rango de 10 y un numero aleatorio de videos en un rango de 25
    def GenerateList (self):
        shuffle = self.character
        random.shuffle(shuffle)
        playlists={}
        for i in range(random.randint(1, 10)):
            playlists["Playlist"+str(i+1)]=[]
            for e in range(random.randint(1, 25)):
                shuffle = self.character
                random.shuffle(shuffle)
                code=""
                for e in range(10):
                   code += shuffle[e]
                playlists["Playlist" + str(i+1)].append("https://www.youtube.com/watch?v="+str(code))
        return playlists

    #Funcion que crea todos los datos
    def creation (self):
        for i in range(self.total):
            x = self.generateName()
            p = self.GenerateList()
            cosa = {
                "User": x[0],
                "Password": x[1],
                "Lists": p
            }
            try:#Carga constantemente los datos del json para reescribirlos y volcarlos de nuevo al json
                with open("Users.json", "r+") as file:
                    data = json.load(file)

                    # convert data to list if not
                    if type(data) is dict:
                        data = [data]

                    # append new item to data lit
                    data.append(cosa)

                    # write list to file
                    with open('Users.json', 'w') as outfile:
                        json.dump(data, outfile, indent=4)
            except: #En caso de jason vacio no carga el contenido sino que vuelca directamente los datos al json
                with open('Users.json', 'w') as outfile:
                    json.dump(cosa, outfile, indent=4)

    #funcion que vacia el json deseado para evitar acumulación entre pruebas, actualmente inusable
    def clear (self,json):

        if os.path.exists(self.my_file):
            os.remove(self.my_file)
        if not os.path.exists(self.my_file):  # si no existe lo creamos
            file = open(os.path.join(self.directory, json), "w")
            file.close()






