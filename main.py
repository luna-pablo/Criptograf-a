from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from BaseGenerator import UserGenerator
import json

"""
Nota:
Para generar un nuevo caso de prueba es necesario borrar
Todos los jsons.
"""


#Se genera los usuarios, 10 usuarios, y cada contraseña personal ocupa 45 caracteres
x= UserGenerator(10,45)

x.creation()

list_of_playlist_passwords=[] #Lista usada para la automatización de autentificación de contraseñas de cifrado simetrico. En un caso real esto no sería necesario

#Función que encripta la contraseña del usuario
def encryptPassword(Password):
    b =bytes(Password, "utf-8")
    h_obj = SHA256.new()
    h_obj.update(b)
    new_pass = h_obj.hexdigest()
    return new_pass

#Función que encripta las listas de reproducciones del usuario
def encryptList(key,list):

    new_dict = {}


    for i in list:
        new_list = []
        cipher_encrypt = AES.new(key, AES.MODE_CFB)
        iv = cipher_encrypt.iv
        iv_h=iv.hex()
        for e in list[i]:
            data = e.encode("utf-8")
            cipher_bytes = cipher_encrypt.encrypt(data)
            cipher_bytes_h=cipher_bytes.hex() #El paso a hexadecimal es para almacenar los datos en el json ya que el formato "bytes" es incompatible
            new_list.append(cipher_bytes_h)
        new_list.append(iv_h)
        new_dict[i] = new_list

    return new_dict

#Función que desencripta las listas de reproducciones del usuario en base al almacenemiento de contraseñas automático
def decryptList(key, list):

    new_dict = {}
    for i in list:
        iv_h = list[i].pop()
        iv=bytes.fromhex(iv_h)
        new_list = []
        cipher_decrypt = AES.new(key, AES.MODE_CFB, iv=iv)
        for e_h in list[i]:
            e=bytes.fromhex(e_h)
            deciphered_bytes = cipher_decrypt.decrypt(e)
            deciphered_str = deciphered_bytes.decode("UTF-8")
            new_list.append(deciphered_str)
        new_dict[i] = new_list



    return(new_dict)

##Función que llama a las funciones de encriptado de cada usuario y las guarda en un json
def Encrypt ():
    new_data=[]
    with open("Users.json", "r+") as file: #Carga en data los datos de los Usuarios iniciales
        data = json.load(file)
        if type(data) is dict:
            data = [data]
        #Recorre la lista de datos y los encripta por Usuario
        for i in data:
            Name= i["User"]
            Password= i["Password"]
            Lists = i["Lists"]
            key = get_random_bytes(32)
            print("Contraseña del Usuraio",Name,":",key) #Esta es la forma practica de darle al usuario su contraseña
            list_of_playlist_passwords.append(key)
            encry_pass=encryptPassword(Password)
            encry_lists=encryptList(key,Lists)
            new_data.append({"User":Name,"Password":encry_pass,"Lists":encry_lists})

        #Los datos encriptados los guarda aqui
        with open ("EncryUser.json", "w") as outfile:
            json.dump(new_data, outfile, indent=4)

##Función que llama a las funciones de desencriptado de cada usuario y las guarda en un json
def DeEncrypt ():
    new_data=[]
    with open("EncryUser.json", "r+") as file: #Carga en data los datos de los Usuarios Encriptados
        data = json.load(file)
        if type(data) is dict:
            data = [data]
        #Recorre la lista de datos encriptados y los desencripta por Usuario
        for i in data:
            Name= i["User"]
            Password= i["Password"]
            Lists = i["Lists"]
            key = list_of_playlist_passwords.pop(0)
            deencry_lists=decryptList(key,Lists)
            new_data.append({"User":Name,"Password":Password,"Lists":deencry_lists})
        #Los datos desencriptados los guarda aqui
        with open ("DeEncryUser.json", "w") as outfile:
            json.dump(new_data, outfile, indent=4)
Encrypt()
DeEncrypt()

