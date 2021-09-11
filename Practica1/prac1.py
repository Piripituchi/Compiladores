
import re

class Afd:

    def __init__(self,Estados,Sigma,Inicial,Finales,delta):
        self.Estados=Estados
        self.Sigma=Sigma
        self.Inicial=Inicial
        self.Finales=Finales
        self.delta=delta

    def transicion(self,estado,caracter):
        flag=True
        if caracter not in self.Sigma:
            pass
        if (estado,caracter):
            pass
        pass
    pass

def leerTxt(archivo):
    estados=list(''.join(re.split(',|\n',archivo.readline())))
    sigma=list(''.join(re.split(',|\n',archivo.readline())))
    inicial=''.join(archivo.readline().splitlines())
    finales=list(''.join(re.split(',|\n',archivo.readline())))
    transiciones=re.split(',|\n',archivo.read())
    dic_transiciones={}
    for i in range(0,len(transiciones),3):
        dic_transiciones.setdefault((transiciones[i],transiciones[i+1]),transiciones[i+2])
    return estados,sigma,inicial,finales,dic_transiciones

if __name__ == "__main__":
    f=open('/home/eduardo/Documentos/Compiladores/Practica1/prueba.txt','r')
    a,b,c,d,e=leerTxt(f)
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    f.close()
