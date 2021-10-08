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
__status__= "Pruebas"

#-----------------------------LIBRERIAS NECESARIAS----------------------------------

import re #Usaremos los metodos de esta libreria para poder manejar la informacion de los achivos de texto que se proporcionen
import sys #Usaremos esta libreria para leer los argumentos de la entrada al correr el programa
import pprint

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
        if (estado,caracter) in self.delta.keys():
            estados_sig=self.delta[(estado,caracter)] # Consulta en la tabla de transiciones
            return estados_sig,True # Regresa el o los estados siguiente y una bandera de True

        return estado,False # Regresa el o los estados siguiente y una bandera de True

    def cerradura_Epsilon(self,estado_actual): # Toma una lista de estados y regresa una lista con los estados y todos los estados a los que se podra llegar con E (Cerradura Epsilon)
        temp=estado_actual
        for q in estado_actual:
            if (q,'E') in self.delta.keys(): #Si el estado tiene una trancision con E
                temp = set().union(temp, self.delta[(q,'E')]) # Agrega la transicion a la lista y usa set(). para evitar estados duplicados
        if temp==estado_actual: # SI la lista de estados inicial y la lista obtenida despues de consultar las transiciones E son iguales, siginifica que no se encontraron nuevas transiciones y podemos dejar de buscar
            return temp # regresamos la ultima lista
        else: # Si las listas son diferentes significa que se encontraron y agregaron transiciones
            return self.cerradura_Epsilon(temp) # Lanazamos el metodo nuevamente para buscar transiciones sobre la nueva lista de estados
    
    def mover_A(self,estadoactual,sigma):
        temp=[]
        for q in estadoactual:
            estadosig,FLAG=self.transicion(q,sigma)
            if not FLAG:
                continue
            temp.extend(estadosig)
        return set(temp)

    def ir_A(self,estadoactual,sigma):
        return self.cerradura_Epsilon(self.mover_A(estadoactual,sigma))

    def construccion_Subconjuntos(self):
        inicial_afd=self.cerradura_Epsilon(set(self.inicial))
        estados_afd=[]
        finales_afd=[]
        transiciones_afd={}
        new_nombres={}
        letra=0
        estados_afd.append(inicial_afd)
        new_nombres.setdefault(chr(65),inicial_afd)
        for q in estados_afd:
            for s in self.Sigma:
                new_estado=self.ir_A(q,s)
                if new_estado not in estados_afd:
                    estados_afd.append(new_estado)
                if new_estado == set():
                    continue
                if new_estado not in new_nombres.values():
                    letra=letra+1
                    new_nombres.setdefault(chr(65+letra),new_estado)
                #print(get_key(q,new_nombres)+" , "+s+" -> "+get_key(new_estado,new_nombres))
                transiciones_afd.setdefault((get_key(q,new_nombres),s),get_key(new_estado,new_nombres))
        for f in self.Finales:
            for e in new_nombres.values():
                if f in e:
                    finales_afd.append(get_key(e,new_nombres))
                    continue
        self.Estados=list(new_nombres.keys())
        self.inicial=get_key(inicial_afd,new_nombres) # Estado inicial
        self.Finales=list(finales_afd) # Conjunto de estados finales/de aceptacion
        self.delta=transiciones_afd
    
    def print_Automata(self):
        print("Estados: "+' , '.join(self.Estados))
        print("Alfabeto: "+' , '.join(self.Sigma))
        print("Inicial: "+self.inicial)
        print("Finales: "+' , '.join(self.Finales))
        print("Tabla de transicion:")
        pprint.pprint(self.delta)


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

def get_key(val,dic):
    for key, value in dic.items():
        if val == value:
            return key
#-----------------------------MAIN----------------------------------

if __name__ == "__main__":
    if len(sys.argv)==2 and sys.argv[1].endswith('.txt'): #Si la entrada contiene 2 argumentos y el segundo es un archivo .txt, se ejecuta el programa
        f=open(sys.argv[1],'r') # Abre el archivo con el nombre que se dio en el segundo argumento
        Estados,Sigma,Inicial,Finales,delta=leerAutomata(f) # Lee el automata del archivo y asigna lo leido a las variables correspondientes
        f.close() # Cierra el archivo
        automata=Automata(Estados,Sigma,Inicial,Finales,delta) #Construye el automata con los valores proporcionados
        print("\n\t Automata Leido:\n")
        automata.print_Automata()
        automata.construccion_Subconjuntos()
        print("\n\t Automata Resultante:\n")
        automata.print_Automata()
        # print("Estados: "+' , '.join(automata.Estados))
        # print("Alfabeto: "+' , '.join(automata.Sigma))
        # print("Inicial: "+automata.inicial)
        # print("Alfabeto: "+' , '.join(automata.Finales))
        # print("Tabla de transicion:")
        # pprint.pprint(automata.delta)
    else: #Si la entrada no contiene 2 argumentos y el segundo no es un archivo .txt, no puede ejecutarse el programa e imprime un mensaje de error
        print("Error: Entrada incorrecta ")
        print("Ejemplo de entrada correcta: $ python afne.py automata.txt") # ejemplo de entrada correcta