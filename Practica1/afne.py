#!/usr/bin/env python3
'''
Modulo:   afne.py
Autor:    Jesus Eduardo Angeles Hernandez
Fecha:    2021/10/01

Descripcion: Este codigo carga desde un archivo un AFN-E que es capaz de verificar si las
             cadenas igresadas por el usuario son parte o no del lenguaje que describe el 
             automata proporcionado, ademas de eso emplea un metodo similar al Panic Mode
             para manejo de errores.
             Este codigo fue desarrollado como parte de la 1er - 2da practica de la asignatura 
             Compiladores en la Escuela Superior de Computo del IPN durante el semestre 2022/1.
'''
__author__ = "Jesus Eduardo Angeles Hernandez"
__email__ = "jeduardohdez98@gmail.com"
__status__= "Terminado"

#-----------------------------LIBRERIAS NECESARIAS----------------------------------

import re #Usaremos los metodos de esta libreria para poder manejar la informacion de los achivos de texto que se proporcionen
import sys #Usaremos esta libreria para leer los argumentos de la entrada al correr el programa

#-----------------------------CLASES----------------------------------

class Automata: #Clase Automata

    def __init__(self,Estados,Sigma,inicial,Finales,delta): #Constructor de la clase Automata
        self.Estados=Estados # Conjunto de estados del automata
        self.Sigma=Sigma # Alfabeto del automata
        self.inicial=inicial # Estado inicial
        self.Finales=Finales # Conjunto de estados finales/de aceptacion
        self.delta=delta # Diccionario que representa la tabla de transicion

    def completarAutomata(self): #Completa el automata agregando el estado de error
        for s in self.Sigma: 
            for q in self.Estados:
                if (q,s) not in self.delta.keys():
                    self.delta.setdefault((q,s),['\u03F4']) # Para cada estado que no tengan definida una transicion con un simbolo de Sigma, se crea dicha transicion al estado de error
            self.delta.setdefault(('\u03F4',s),['\u03F4']) # Por cada simbolo de Sigma se crea su transicion desde el estado de error a el estado de error
        return

    def transicion(self,estado,caracter): # Toma un estado y un caracter de la entrada y regresa el estado o estados posibles
        if caracter not in self.Sigma:
            return estado,False # Si el caracter no esta en el alfabeto, no hace ninguna transicion y regresa una bandera de False
        estados_sig=self.delta[(estado,caracter)] # Consulta en la tabla de transiciones
        return estados_sig,True # Regresa el o los estados siguiente y una bandera de True

    def transicionesEpsilon(self,estado_actual): # Toma una lista de estados y regresa una lista con los estados y todos los estados a los que se podra llegar con E (Cerradura Epsilon)
        temp=estado_actual
        for q in estado_actual:
            if (q,'E') in self.delta.keys(): #Si el estado tiene una trancision con E
                temp = list(set().union(temp, self.delta[(q,'E')])) # Agrega la transicion a la lista y usa set(). para evitar estados duplicados
        if temp==estado_actual: # SI la lista de estados inicial y la lista obtenida despues de consultar las transiciones E son iguales, siginifica que no se encontraron nuevas transiciones y podemos dejar de buscar
            return temp # regresamos la ultima lista
        else: # Si las listas son diferentes significa que se encontraron y agregaron transiciones
            return self.transicionesEpsilon(temp) # Lanazamos el metodo nuevamente para buscar transiciones sobre la nueva lista de estados

    def validarCadena(self,cadena): #Tomamos una cadena y validamos si es parte de un automata
        estado_act=list(self.inicial) # Iniciamos la lista de estados con el estado inicial
        errores=[] # Lista para guardar los carcateres detectados como error
        temp=[] 
        transiciones=[] # Lista para guardar las listas de estados resultados de la transicion
        FLAG=True
        for c in cadena: # Iteramos la cadena de entrada
            temp=estado_act
            estado_act= self.transicionesEpsilon(temp) # Agregamos los estados alcanzados con E
            temp=[] # Limpiamos temp[] para guardar ahi los estados siguientes
            for q in estado_act: # Iteramos la lista de los estados actuales
                estado_sig,FLAG=self.transicion(q,c) # Obtenemos el estado siguiente correspondiente a (q,c)
                if estado_sig==['\u03F4']: #Si el estado siguiente es el simbolo de Omega mayuscula (estado de error), descartamos ese estado
                    continue
                if not FLAG: # Si la bandera es False, es decir el simbolo no pertenece al alfabeto, lo guardamos para indicar el error
                    errores.append(c)
                temp.extend(estado_sig) # Si el estado siguiente no es un estado de error, lo agregamos a la lista de estados siguientes obtenidos
            transiciones.append(estado_act) # Agregamos a las transiciones posibles la lista de estados origen
            transiciones.append(temp) # Agregamos a las transiciones posibles la lista de estados destino
            estado_act=temp # Pasamos a la lista de estados destino obtenidos a los estados actuales
        if len((set(estado_act) & set(self.Finales))) > 0: # Si la interseccion entre la ultima lista de estados y el conjunto de estados finales es < 0, existe uno o mas caminos posibles
            if errores: # Si se detecta que existieron errores.
                print("\n"+self.inicial+" - (E) -> "+"[ "+",".join(transiciones[0])+" ]") #Imprime el estado inicial y sus transiciones posibles con E
                i=0 # Contador de los indices de la cadena de entrada
                for t in range(0,len(transiciones)-1): # Recorremos la lista de estados por los que se paso
                    if(t%2==0): #Si el modulo a 2 del indice de la lista de estados transitados es 0, quiere decir que esa fue una transicion con lectura de un simbolo de la cadena
                        if cadena[i] in errores:
                            c="Manejo de error: "+cadena[i] #Si el simbolo leido esta en la lista de simbolos detectados como errores lo indica
                        else:
                            c=cadena[i] #Si el simbolo lido no esta en la lista de errores, lo imprime como una transicion normal
                        i+=1 #Aumentamos el indice de la cadena
                    else:
                        c='E' #Si el modulo a 2 del indice es diferente de cero, quiere decir que esa fue una transicion E
                    print("[ "+",".join(transiciones[t])+" ]"+" - "+c+" -> "+"[ "+",".join(transiciones[t+1])+" ]") # Imprime la lista de estados atuales, el simbolo que se uso y la lista de transicion posibles
                return str(cadena+" si esta en el lenguaje.")
            print("\n"+self.inicial+" - (E) -> "+"[ "+",".join(transiciones[0])+" ]") #Imprime el estado inicial y sus transiciones posibles con E
            i=0 # Contador de los indices de la cadena de entrada
            for t in range(0,len(transiciones)-1): # Recorremos la lista de estados por los que se paso
                if(t%2==0): #Si el modulo a 2 del indice de la lista de estados transitados es 0, quiere decir que esa fue una transicion con lectura de un simbolo de la cadena
                    c=cadena[i] #Si el simbolo lido no esta en la lista de errores, lo imprime como una transicion normal
                    i+=1 #Aumentamos el indice de la cadena
                else:
                    c='E'#Si el modulo a 2 del indice es diferente de cero, quiere decir que esa fue una transicion E
                print("[ "+",".join(transiciones[t])+" ]"+" - "+c+" -> "+"[ "+",".join(transiciones[t+1])+" ]") # Imprime la lista de estados atuales, el simbolo que se uso y la lista de transicion posibles
            return str(cadena+" si esta en el lenguaje")
        else: #Si la interseccion es 0, no llegamos a un estado de aceptacion y la cadena no es valida, no imprimos las transiciones
            return str("Cadena: "+cadena+" no es valida")    

#-----------------------------METODOS----------------------------------

def leerAfd(archivo): # lee un archivo txt y toma el automata que viene descrito
    estados=re.split(',|\n',archivo.readline()) #lee la primera linea y crea on lo leido la lista de estados
    sigma=list(''.join(re.split(',|\n',archivo.readline()))) #lee la segunda linea y crea la lista del alfabeto del automata
    inicial=''.join(archivo.readline().splitlines()) # lee la tercera linea que contiene el estado inicial
    finales=re.split(',|\n',archivo.readline()) #lee la cuarta linea y crea la lista de estados finales
    transiciones=re.split(',|\n',archivo.read()) #lee desde la quinta linea hasta el final del archivo y organiza todos los elementos en una lista
    dic_transiciones={} # inicializa el diccionario que contendra la tabla de transiciones
    for i in range(0,len(transiciones),3): #recorre los elementos de la lista para encontrar estado, caracter y transicion
        if(transiciones[i],transiciones[i+1]) in dic_transiciones.keys(): #si el par (estado, caracter) ya esta definido en el diccionario, agrega a la lista de transicion el caracter [t+2]
            dic_transiciones.setdefault((transiciones[i],transiciones[i+1]),dic_transiciones[(transiciones[i],transiciones[i+1])].append(transiciones[i+2]))
        else: #si el par (estado, caracter) aun no esta definido, crea la lista de transicion
            dic_transiciones.setdefault((transiciones[i],transiciones[i+1]),[transiciones[i+2]])
    return estados,sigma,inicial,finales,dic_transiciones #regresa conjunto de estados, alfabeto, estado inicial, conjunto de estados finales, tabla de transiciones

#-----------------------------MAIN----------------------------------

if __name__ == "__main__":
    if len(sys.argv)==2 and sys.argv[1].endswith('.txt'): #Si la entrada contiene 2 argumentos y el segundo es un archivo .txt, se ejecuta el programa
        f=open(sys.argv[1],'r') # Abre el archivo con el nombre que se dio en el segundo argumento
        Estados,Sigma,Inicial,Finales,delta=leerAfd(f) # Lee el automata del archivo y asigna lo leido a las variables correspondientes
        f.close() # Cierra el archivo
        automata=Automata(Estados,Sigma,Inicial,Finales,delta) #Construye el automata con los valores proporcionados
        automata.completarAutomata() # Completa el automata creando el estado de error
        try:
            while True: # Mientras el usuario no decida finalizar el programa
                cadena=input('Ingrese cadena a evaluar por el automata: ') # Lee la cadena de la entrada
                valido=automata.validarCadena(cadena) # Pasa la cadena del automata para su validacion
                print(valido) # Imprimir el resultado de la validacion
                print("\n Presione ^C para terminar") #Instruccion para finalizar el automata "Ctrl + C" (Interrupcion)
        except: # Cuando ocurra la interrupcion indica que es el fin del programa
            print("\nFin del programa")
    else: #Si la entrada no contiene 2 argumentos y el segundo no es un archivo .txt, no puede ejecutarse el programa e imprime un mensaje de error
        print("Error: Entrada incorrecta ")
        print("Ejemplo de entrada correcta: $ python prac1.py prueba.txt") # ejemplo de entrada correxta