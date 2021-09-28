

import re
import sys


class Automata:

    def __init__(self,Estados,Sigma,inicial,Finales,delta):
        self.Estados=Estados
        self.Sigma=Sigma
        self.inicial=inicial
        self.Finales=Finales
        self.delta=delta

    def completarAutomata(self):
        for s in self.Sigma:
            for q in self.Estados:
                if (q,s) not in self.delta.keys():
                    self.delta.setdefault((q,s),['\u03F4'])
                    self.delta.setdefault(('\u03F4',s),['\u03F4'])
        return


    def transicion(self,estado,caracter):
        if caracter not in self.Sigma:
            return estado,False
        # if self.delta[(estado,caracter)]=='\u03F4':
        #     return '\u03F4',False
        estados_sig=self.delta[(estado,caracter)]
        #print("  Transicion (", estado,",",caracter,")  ->  ", estados_sig)
        return estados_sig,True

    def transicionesEpsilon(self,estado_actual):
        aux=False
        temp=estado_actual
        #print(estado_actual)
        for q in estado_actual:
            if (q,'E') in self.delta.keys():
                temp = list(set().union(temp, self.delta[(q,'E')]))
                #print(temp)
                aux=True
        
        if temp==estado_actual:
            return temp
        else:
            return self.transicionesEpsilon(temp)
        
        

    def validarCadena(self,cadena):
        estado_act=list(self.inicial)
        errores=[]
        temp=[]
        FLAG=True
        for c in cadena:
            temp=estado_act
            # print(estado_act)
            # for q in estado_act:
            #     if (q,'E') in self.delta.keys():
            #         temp = list(set().union(temp, self.delta[(q,'E')]))
            estado_act=self.transicionesEpsilon(temp)
            # print(estado_act)
            temp=[]
            for q in estado_act:
                if q=='\u03F4':
                    continue
                estado_sig,FLAG=self.transicion(q,c)
                if not FLAG:
                    errores.append(c)
                temp.extend(estado_sig)
            estado_act=temp  
        if len((set(estado_act) & set(self.Finales))) > 0:
            if errores:
                return str(cadena+" si esta en el lenguaje, se aplico manejo de error para "+','.join(set(errores)))
            return str(cadena+" si esta en el lenguaje")
        else:
            return str("Cadena: "+cadena+" no es valida")
            

def leerAfd(archivo):
    estados=re.split(',|\n',archivo.readline())
    sigma=list(''.join(re.split(',|\n',archivo.readline())))
    inicial=''.join(archivo.readline().splitlines())
    finales=re.split(',|\n',archivo.readline())
    transiciones=re.split(',|\n',archivo.read())
    dic_transiciones={}
    for i in range(0,len(transiciones),3):
        if(transiciones[i],transiciones[i+1]) in dic_transiciones.keys():
            dic_transiciones.setdefault((transiciones[i],transiciones[i+1]),dic_transiciones[(transiciones[i],transiciones[i+1])].append(transiciones[i+2]))
        else:
            dic_transiciones.setdefault((transiciones[i],transiciones[i+1]),[transiciones[i+2]])
    return estados,sigma,inicial,finales,dic_transiciones


if __name__ == "__main__":
    if len(sys.argv)==2 and sys.argv[1].endswith('.txt'):
        f=open(sys.argv[1],'r')
        Estados,Sigma,Inicial,Finales,delta=leerAfd(f)
        f.close()
        automata=Automata(Estados,Sigma,Inicial,Finales,delta)
        automata.completarAutomata()
        try:
            while True:
                cadena=input('Ingrese cadena a evaluar por el automata: ')
                valido=automata.validarCadena(cadena)
                print(valido)
                print("\n Presione ^C para terminar")
        except:
            print("\nFin del programa")
        # cadena=input('Ingrese cadena a evaluar por el automata: ')
        # valido=automata.validarCadena(cadena)
        # print(valido)
        # print("\n Presione ^C para terminar")
    else:
        print("Error: Entrada incorrecta ")
        print("Ejemplo de entrada correcta: $ python prac1.py prueba.txt")
