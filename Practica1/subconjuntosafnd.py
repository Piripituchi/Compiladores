

import re
import sys
from itertools import chain,combinations

def conjunto_potencia(Estados):
    return list(chain.from_iterable(combinations(Estados,r) for r in range(len(Estados)+1)))

def finales_prima(Ep,Finales):
    Fp=[]
    for estado in Ep:
        for e in estado:
            if e in Finales:
                Fp.append(estado)
                break
    return Fp

def delta_prima(Ep,Sigma,delta):
    dp={}
    for estado in Ep:
        for s in Sigma:
            estado_sig=[]
            for e in estado:
                if (e,s) not in delta.keys():
                    continue
                for e_sig in delta[(e,s)]:
                    if e_sig not in estado_sig:
                        estado_sig.append(e_sig)
            estado_sig.sort()
            dp.setdefault((estado,s),tuple(estado_sig))
    return dp

class Automata:

    def __init__(self,Estados,Sigma,inicial,Finales,delta):
        self.Estados=Estados
        self.Sigma=Sigma
        self.inicial=inicial
        self.Finales=Finales
        self.delta=delta
        self.Ep=conjunto_potencia(self.Estados)
        self.Fp=finales_prima(self.Ep,self.Finales)
        self.dp=delta_prima(self.Ep,self.Sigma,self.delta)


    def transicion(self,estado,caracter):
        if caracter not in self.Sigma:
            return estado,False
        if (estado,caracter) not in self.dp.keys():
            return '\u03F4',False
        estado_sig=self.dp[(estado,caracter)]
        print("  Transicion (", estado,",",caracter,")  ->", estado_sig)
        return estado_sig,True

    def validarCadena(self,cadena):
        estado=self.inicial
        errores=[]
        for c in range(0,len(cadena)):
            estado,FLAG=self.transicion(estado,cadena[c])
            if estado=='\u03F4' and not FLAG:
                break
            if not FLAG:
                errores.append(cadena[c])
        if estado in self.Fp:
            if errores:
                return str(cadena+" si esta en el lenguaje, se aplico manejo de error para "+','.join(errores))
            return str(cadena+" si esta en el lenguaje")
        else:
            return str("Cadena: "+cadena+" no es valida")
            

def leerAfd(archivo):
    estados=list(''.join(re.split(',|\n',archivo.readline())))
    sigma=list(''.join(re.split(',|\n',archivo.readline())))
    inicial=(''.join(archivo.readline().splitlines()),)
    finales=list(''.join(re.split(',|\n',archivo.readline())))
    transiciones=re.split(',|\n',archivo.read())
    dic_transiciones={}
    for i in range(0,len(transiciones),3):
        if(transiciones[i],transiciones[i+1]) in dic_transiciones.keys():
            dic_transiciones.setdefault((transiciones[i],transiciones[i+1]),dic_transiciones[(transiciones[i],transiciones[i+1])].append(transiciones[i+2]))
        else:
            dic_transiciones.setdefault((transiciones[i],transiciones[i+1]),list(transiciones[i+2]))
    return estados,sigma,inicial,finales,dic_transiciones


if __name__ == "__main__":
    if len(sys.argv)==2 and sys.argv[1].endswith('.txt'):
        f=open(sys.argv[1],'r')
        Estados,Sigma,Inicial,Finales,delta=leerAfd(f)
        f.close()
        automata=Automata(Estados,Sigma,Inicial,Finales,delta)
        try:
            while True:
                cadena=input('Ingrese cadena a evaluar por el automata: ')
                valido=automata.validarCadena(cadena)
                print(valido)
                print("\n Presione ^C para terminar")
        except:
            print("\nFin del programa")
    else:
        print("Error: Entrada incorrecta ")
        print("Ejemplo: $ python prac1.py prueba.txt")
