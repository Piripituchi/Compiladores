#ifndef __LISTAS_LIGADAS__
#define __LISTAS_LIGADAS__

#include <stdlib.h>
#include <stdio.h>

union tipo{
    double dec;
    int entero;
    char cadena[20];
};

struct ListaL
{
  union tipo dato;
  char nombre[20]
  struct ListaL *siguiente;
};

void insertarListaL (struct ListaL **, union tipo);

void mostrarListaL (struct ListaL *);

struct ListaL *buscarListaL (struct ListaL *, union tipo);

void eliminarListaL (struct ListaL **, int);

#endif