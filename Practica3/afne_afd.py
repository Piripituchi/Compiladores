#!/usr/bin/env python3
'''
Modulo:   afne_afd.py
Autor:    Jesus Eduardo Angeles Hernandez
Fecha:    2021/10/11

Descripcion: Este codigo carga desde un archivo un AFN-E y lo convierte en un AFD usando el metodo
             de contruccion de subconjuntos.
             Este codigo fue desarrollado como parte de la 3ra practica de la asignatura 
             Compiladores en la Escuela Superior de Computo del IPN durante el semestre 2022/1.
'''
__author__ = "Jesus Eduardo Angeles Hernandez"
__email__ = "jeduardohdez98@gmail.com"
__status__= "Terminado"

#-----------------------------LIBRERIAS NECESARIAS----------------------------------

import re #Usaremos los metodos de esta libreria para poder manejar la informacion de los achivos de texto que se proporcionen
import sys #Usaremos esta libreria para leer los argumentos de la entrada al correr el programa
import pprint #Usaremos esta libreria para imprimir con un formato mas entendible los diccionarios que forman la tabla de transicion.

#-----------------------------CLASES----------------------------------

class Automata: #Clase Automata

    def __init__(self,Estados,Sigma,inicial,Finales,delta): #Constructor de la clase Automata
        self.Estados=Estados # Conjunto de estados del automata
        self.Sigma=Sigma # Alfabeto del automata
        self.inicial=inicial # Estado inicial
        self.Finales=Finales # Conjunto de estados finales/de aceptacion
        self.delta=delta # Diccionario que representa la tabla de transicion

    def transicion(self,estado,caracter): # Toma un estado y un caracter de la entrada y regresa el estado o estados posibles
        if caracter not in self.Sigma:
            return estado,False # Si el caracter no esta en el alfabeto, no hace ninguna transicion y regresa una bandera de False
        if (estado,caracter) in self.delta.keys(): #Revisa si existe una transicion con el estado y simbolo en el diccionario de transiciones 
            estados_sig=self.delta[(estado,caracter)] # Consulta en la tabla de transiciones
            return estados_sig,True # Regresa el o los estados siguiente y una bandera de True

        return estado,False # Regresa el estado ingresado sin cambios y una bandera de False ya que no se encontro transicion

    def cerradura_Epsilon(self,estado_actual): # Toma una lista de estados y regresa una lista con los estados y todos los estados a los que se podra llegar con E (Cerradura Epsilon)
        temp=estado_actual
        for q in estado_actual:
            if (q,'E') in self.delta.keys(): #Si el estado tiene una trancision con E
                temp = set().union(temp, self.delta[(q,'E')]) # Agrega la transicion a la lista y usa set(). para evitar estados duplicados
        if temp==estado_actual: # SI la lista de estados inicial y la lista obtenida despues de consultar las transiciones E son iguales, siginifica que no se encontraron nuevas transiciones y podemos dejar de buscar
            return temp # regresamos la ultima lista
        else: # Si las listas son diferentes significa que se encontraron y agregaron transiciones
            return self.cerradura_Epsilon(temp) # Lanazamos el metodo nuevamente para buscar transiciones sobre la nueva lista de estados
    
    def mover_A(self,estadoactual,sigma): # Toma una lista de estados y devuelve un conjunto de estados alcanzables desde ese estado con un simbolo dado
        temp=[] # lista de estados alcanzables
        for q in estadoactual: # Iteramos la lista dada
            estadosig,FLAG=self.transicion(q,sigma) # Obtenemos la transicion para el elemento q de la lista
            if not FLAG: #Si la bandera obtenida de la transicion es falsa
                continue # No agrega ningun estado a la lista de estados alcanzables
            temp.extend(estadosig) #Agrega el estado alcanzado con q y sigma a la lista de estados alcanzables
        return set(temp) #devuelve el conjunto obtenido de estados alcanzables

    def ir_A(self,estadoactual,sigma): # Toma un conjunto de estados y devuelve un conjunto de los estados hacia los cuales existe transicion con un simobolo
        return self.cerradura_Epsilon(self.mover_A(estadoactual,sigma)) # Devuelve el conjunto resultado de aplicar los metodos Mover_A y cerradura_E en ese orden

    def construccion_Subconjuntos(self): #Convierte el automata AFN-E definido en los atributos del objeto en un automata AFD
        inicial_afd=self.cerradura_Epsilon(set(self.inicial)) #Crea el primer estado a partir del estado inicial del automata
        estados_afd=[] #Lista que utilizaremos para guardar los estados nuevos encontrados e iterarlos
        finales_afd=[] #Lista que utilizaremos para guardar los estados finales del AFD
        transiciones_afd={} # Diccionario que utilizaremos para guardar la tabla de transicion obtenida
        new_nombres={} # Diccionario con el que reenombraremos los nuevos estados
        letra=0 #Inidice para renombrar nuevos estados usando letras del abcdario en mayuscula
        estados_afd.append(inicial_afd) #Agregamos el estado obtenido a la lista de estados a iterar
        new_nombres.setdefault(chr(65),inicial_afd) #Agregamos al diccionario el nuevo nombre del estado, convirtiendo el decimal 65 a ascci A y el estado al que corresponde
        for q in estados_afd: #iteramons la lista de estados obtenidos
            for s in self.Sigma: #iteramos los simbolos del alfabeto
                new_estado=self.ir_A(q,s) # Aplicamos la funcion ir_A sobre el estado q con el simbolo s
                if new_estado == set(): # Si el nuevo estado, es un conjunto vacio, lo descartamos
                    continue
                if new_estado not in estados_afd: # Si el estado obtenido de ir_A no esta en la lista de estados encontrados
                    estados_afd.append(new_estado) #Lo agregamos a la lista de estados encontrados
                    letra=letra+1 # Aumentamos el indice del nombre de los nuevos estados
                    new_nombres.setdefault(chr(65+letra),new_estado) #Agregamos al diccionario el nuevo nombre del estado y el estado al que corresponde
                transiciones_afd.setdefault((get_key(q,new_nombres),s),get_key(new_estado,new_nombres)) #Agregamos a la tabla de transicion, el estado actual renombrado, el simbolo y el estado alcanzado renombrado
        for f in self.Finales: #iteramos la lista de estados finales del automata AFN-E
            for e in new_nombres.values(): #Iteramos la lista de estados nuevos obtenidos
                if f in e: #Si el estado f de la lista de estados finales es un elemento del estado e
                    finales_afd.append(get_key(e,new_nombres)) #Agregamos el estado renombrado a la lista de nuevos estados finales
                    continue # Si un estado al menos un estado de f esta en el nuevo estado e, el estado forma parte de los nuevos estados finales y no hace falta comprobar con los demas estados finales
        self.Estados=list(new_nombres.keys()) #modificamos los estados del automata por los nuevos obtenidos
        self.inicial=get_key(inicial_afd,new_nombres) # Modificamos el estado inicial del automata por el nuevo obtenido
        self.Finales=list(finales_afd) # Modificamos los estados finales del automata por los obtenidos
        self.delta=transiciones_afd #Modificamos la tabla de transiciones del automata por la nueva obtenida
    
    def print_Automata(self): #Imprimimos la 5-tupla del automata
        print("Estados: "+' , '.join(self.Estados)) #imprime la lista de estados
        print("Alfabeto: "+' , '.join(self.Sigma)) #imprime el alfabeto del automata
        print("Inicial: "+self.inicial) #imprime el estado inicial del automata
        print("Finales: "+' , '.join(self.Finales)) #imprime la lista de estados finales del automata
        print("Tabla de transicion:") 
        pprint.pprint(self.delta) #imprime la tabla de transicion del automata


#-----------------------------METODOS----------------------------------

def leerAutomata(archivo): # lee un archivo txt y toma el automata que viene descrito
    estados=set(re.split(',|\n',archivo.readline())) #lee la primera linea y crea on lo leido la lista de estados
    sigma=set(''.join(re.split(',|\n',archivo.readline()))) #lee la segunda linea y crea la lista del alfabeto del automata
    inicial=''.join(archivo.readline().splitlines()) # lee la tercera linea que contiene el estado inicial
    finales=set(re.split(',|\n',archivo.readline())) #lee la cuarta linea y crea la lista de estados finales
    transiciones=re.split(',|\n',archivo.read()) #lee desde la quinta linea hasta el final del archivo y organiza todos los elementos en una lista
    dic_transiciones={} # inicializa el diccionario que contendra la tabla de transiciones
    for i in range(0,len(transiciones),3): #recorre los elementos de la lista para encontrar estado, caracter y transicion
        if(transiciones[i],transiciones[i+1]) in dic_transiciones.keys(): #si el par (estado, caracter) ya esta definido en el diccionario, agrega a la lista de transicion el caracter [t+2]
            dic_transiciones.setdefault((transiciones[i],transiciones[i+1]),dic_transiciones[(transiciones[i],transiciones[i+1])].add(transiciones[i+2]))
        else: #si el par (estado, caracter) aun no esta definido, crea la lista de transicion
            dic_transiciones.setdefault((transiciones[i],transiciones[i+1]),{transiciones[i+2]})
    return estados,sigma,inicial,finales,dic_transiciones #regresa conjunto de estados, alfabeto, estado inicial, conjunto de estados finales, tabla de transiciones

def get_key(val,dic): # dado un valor y un diccionario obtiene la llave del valor en el diccionario
    for key, value in dic.items(): #itera el diccionario
        if val == value: #si el valor ingresado es igual con el valor del diccionario
            return key  #devuelve la llave de ese valor

#-----------------------------MAIN----------------------------------

if __name__ == "__main__":
    if len(sys.argv)==2 and sys.argv[1].endswith('.txt'): #Si la entrada contiene 2 argumentos y el segundo es un archivo .txt, se ejecuta el programa
        f=open(sys.argv[1],'r') # Abre el archivo con el nombre que se dio en el segundo argumento
        Estados,Sigma,Inicial,Finales,delta=leerAutomata(f) # Lee el automata del archivo y asigna lo leido a las variables correspondientes
        f.close() # Cierra el archivo
        automata=Automata(Estados,Sigma,Inicial,Finales,delta) #Construye el automata con los valores proporcionados
        print("\n\t Automata Leido:\n")
        automata.print_Automata() #imprime la 5-tupla del AFN-E leido del archivo pasado como argumento con el que fue creado el objeto automata
        automata.construccion_Subconjuntos() #Convertimos el AFN-E en un AFD
        print("\n\t Automata Resultante:\n")
        automata.print_Automata() #Imprime la 5-tupla del automata resultante
    else: #Si la entrada no contiene 2 argumentos y el segundo no es un archivo .txt, no puede ejecutarse el programa e imprime un mensaje de error
        print("Error: Entrada incorrecta ")
        print("Ejemplo de entrada correcta: $ python afne.py automata.txt") # ejemplo de entrada correcta