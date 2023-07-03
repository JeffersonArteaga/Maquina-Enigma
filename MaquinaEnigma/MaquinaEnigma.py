#Jefferson David Arteaga - Jense David Martinez Gramaticas y lenguajes formales

#Esta es mi prueba con git

import random
import copy
import os

#Esta funcion me permite saber en que Sistema opertaivo se esta ejecutando el programa para ejecutar cls o clear
def clear():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == ("ce", "nt", "dos"):
        os.system ("cls")

#Esta funcion pide caracter por caracter la palabra clave de la maquina enigma y las retorna en una lista
def generar_palabra_clave(simbolos,lista_rotores):
    lista_palabra_clave = []
    palabra_clave = ""
    for i in range(0,len(lista_rotores)):
        kw = input(f"Ingrese el caracter inicial para el rotor {i+1}: ")
        palabra_clave = palabra_clave + kw
        lista_palabra_clave.append(simbolos.index(kw))
    print(f"\nLa palabra clave ha usar es: {palabra_clave}")
    #print(lista_palabra_clave)
    return lista_palabra_clave

#Esta funcion genera el reflector de la maquina enigma en una lista y la retorna en una lista
def generar_reflector():
    lista = []
    for i in range(99,-1,-1):
       lista.append(i)
    return lista

#Esta funcion genera en una lista de lista la configuracion original de los rotores y retorna la lista de listas
def generar_lista_rotores():
    n = int(input("Ingrese la cantidad de rotores que desea generar: "))
    lista_de_rotores = [[] for i in range(n)]
    for i in range(n):
        numeros_usados = set()
        for j in range(100):
            numero = random.randint(0, 99)
            while ((numero in numeros_usados) or (numero == j)):
                numero = random.randint(0, 99)
            numeros_usados.add(numero)
            lista_de_rotores[i].append(numero)
    print("Se han generado {} rotores y el reflector...\n".format(n))
    return lista_de_rotores

#Esta funcion recibe el valor de la posicion que salga del ultimo rotor de la maquina y retorna la conexion que tenga este valor en el reflector
def reflectar(reflector,x):
    return reflector[x]


#Esta funcion recibe la configuracion de un rotor y desplaza las posiciones del rotor el numero de veces que ese rotor haya hecho un click y
#retorna una lista con el valor actualizado de sus posiciones
def config_rotor(pos_rotor,lista_rotor):
    rotor_configurado = [None] * len(lista_rotor)
    for i in range(len(lista_rotor)):
        nueva_posicion = (i + pos_rotor) % len(lista_rotor)
        rotor_configurado[nueva_posicion] = lista_rotor[i]
    return rotor_configurado

#Esta funcion recibe la lista con la configuracion original de los rotores y desplaza los valores de posicion en cada rotor el numero de veces que sea necesario
#para adecuarse a la palabra clave ingresada y devuelve en una lista la configuracion de los rotores actualizada
def config_maquina(lista_keyword,lista_rotores):
    maquina_configurada = []
    for rotor in lista_rotores:
        nueva_config = [None] * len(rotor)
        for i in range(len(rotor)):
            nueva_posicion = (i + lista_keyword[lista_rotores.index(rotor)]) %len(rotor)
            nueva_config[nueva_posicion] = rotor[i]
        maquina_configurada.append(nueva_config)
    return maquina_configurada

#Esta funcion sirve para realizar los clicks necesarios en cada rotor
def contador_clicks(lista_clicks):
    lista_clicks[0]+= 1
    for j in range(1,len(lista_clicks)):
        if (lista_clicks[0] % (10 ** j) == 0):
            lista_clicks[j] += 1
    pass

#Esta funcion se encarga de recibir un caracter y lo retorna encriptado
def enigma(x,lista_maquina_config, lista_clicks, lista_reflector):
    for rotor in lista_maquina_config:
        rotor_click = config_rotor(lista_clicks[lista_maquina_config.index(rotor)],rotor)
        x = rotor_click[x % len(rotor)]
        lista_maquina_config[lista_maquina_config.index(rotor)] = rotor_click
    x_reflectado = reflectar(lista_reflector,x)
    for pos in range(len(lista_maquina_config)-1,-1,-1):
        x_reflectado = lista_maquina_config[pos].index((x_reflectado) % len(lista_maquina_config[pos]))
    return x_reflectado

#Esta funcion se encarga de leer el archivo .txt que se va a encriptar
def leer_archivo(filename):
    with open(filename, 'r') as f:
        contenido = f.read()
        lista_caracteres = list(contenido)
        return lista_caracteres

def main():
    try:
        print(" Jefferson David Arteaga - Jense David Martinez \n               Maquina enigma")
        input("Presione enter para continuar...")
        simbolos = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]\^_`abcdefghijklmnopqrstuvwxyz{|}~°¡¿Ññ'''
        lista_rotores = generar_lista_rotores()
        lista_reflector = generar_reflector()
        confirmacion = "SI"
        
        while (confirmacion != "NO"):
            lista_keyword = generar_palabra_clave(simbolos,lista_rotores)
            lista_maquina_config = config_maquina(lista_keyword,lista_rotores)
            opcion = 0
            while ((opcion > 2) or (opcion <= 0)):
                print("\nOpciones de encriptacion\n\n1. Encriptar fichero \n2. Encriptar palabra ingresada por teclado")
                print("\n\n(Si desea desencriptar un mensaje ingreso anteriormente,\ncopie el mensaje encriptado, ingrese la misma palabra clave \ny despues seleccione la opcion 2)")
                opcion = int(input("Ingrese la opcion que desea: "))

            if (opcion == 1):
                mensaje_a_encriptar = leer_archivo('texto.txt')
                elemento_a_eliminar = "\n"
                while elemento_a_eliminar in mensaje_a_encriptar:
                    mensaje_a_encriptar.remove(elemento_a_eliminar)
                print(mensaje_a_encriptar)

            elif (opcion == 2):
                mensaje_a_encriptar = input("Ingrese el mensaje que desea encriptar: ")

            lista_mensaje_encriptado = []
            mensaje_encriptado = ""
            lista_clicks = [0] * len(lista_rotores)
            for caracter in mensaje_a_encriptar:       
                contador_clicks(lista_clicks)
                x = simbolos.index(caracter)
                caracter_encriptado = enigma(x, lista_maquina_config, lista_clicks, lista_reflector)
                lista_mensaje_encriptado.append(simbolos[caracter_encriptado])
                mensaje_encriptado = mensaje_encriptado + simbolos[caracter_encriptado]
            #print(lista_clicks)
            print(f"\nEl mensaje encriptado es (Tomar en cuenta todos los caracteres que esten dentro de []): [{mensaje_encriptado}]")
            #print(lista_mensaje_encriptado)
            for i in range(len(lista_clicks)):
                print(f"\nEl rotor {i+1} hizo {lista_clicks[i]} clicks")

            confirmacion = input("\n¿Desea encriptar otro mensaje?[SI/NO]: ")
    except:
        print("Ingrese los datos correctamente")
        input()
    
main()

