#include <stdlib.h>
#include <stdio.h>
#include <string.h>

union tipo{
    double dec;
    int entero;
    char cadena[20];
};

struct ListaL
{
  union tipo dato;
  char nombre[20];
  struct ListaL *siguiente;
  char tip[10];
};

void
insertarListaL (struct ListaL **lista, union tipo dato, char nombre[20], char tipo[10])
{
  struct ListaL *aux = NULL;
  aux = (struct ListaL *) malloc (sizeof (struct ListaL));
  aux->siguiente = (*lista);
  if (strcmp("int",tipo)==0)
  {
    aux->dato.entero = dato.entero;
  }
  if (strcmp("double",tipo)==0)
  {
    aux->dato.dec = dato.dec;
  }
  if (strcmp("string",tipo)==0)
  {
    strcpy(aux->dato.cadena,dato.cadena);
  }
  strcpy(aux->nombre,nombre);
  (*lista) = aux;
}

struct ListaL *
buscarListaL (struct ListaL *lista, char nombre[20])
{
  while (lista)
    {
      if (strcmp(nombre,lista->nombre) == 0)
	{
	  return lista;
	}
      lista = lista->siguiente;
    }
  return NULL;
}
