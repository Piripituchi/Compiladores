
import re

class Afd:

    def __init__(self,Estados,Sigma,Inicial,Finales,delta):
        self.Estados=Estados
        self.Sigma=Sigma
        self.Inicial=Inicial
        self.Finales=Finales
        self.delta=delta

    def transicion(self,estado,caracter):
        if caracter not in self.Sigma:
            pass
        if (estado,caracter) not in self.delta.keys():
            return '',False
        estado_sig=self.delta[(estado,caracter)]
        return estado_sig,True

def leerAfd(archivo):
    estados=list(''.join(re.split(',|\n',archivo.readline())))
    sigma=list(''.join(re.split(',|\n',archivo.readline())))
    inicial=''.join(archivo.readline().splitlines())
    finales=list(''.join(re.split(',|\n',archivo.readline())))
    transiciones=re.split(',|\n',archivo.read())
    dic_transiciones={}
    for i in range(0,len(transiciones),3):
        dic_transiciones.setdefault((transiciones[i],transiciones[i+1]),transiciones[i+2])
    for s in sigma:
        for q in estados:
            if (q,s) not in dic_transiciones.keys():
                dic_transiciones.setdefault((q,s),'\u03F4')
        dic_transiciones.setdefault(('\u03F4',s),'\u03F4')
    return estados,sigma,inicial,finales,dic_transiciones

# for cadena in w1:
#     estado=s
#     for c in cadena:
#         estado,STATUS=transicion(estado,c)
#         if not STATUS:
#             break
#     if STATUS and estado in F:
#         print(cadena, "si esta en el lenguaje")
#     else:
#         print(cadena, "no esta en el lenguaje")

if __name__ == "__main__":
    f=open('/home/eduardo/Documentos/Compiladores/Practica1/prueba.txt','r')
    a,b,c,d,e=leerAfd(f)
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    f.close()
