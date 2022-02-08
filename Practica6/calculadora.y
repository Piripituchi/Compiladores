%{
    #include <math.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include "listasl.c"
    struct ListaL* tabla;
    struct ListaL* aux=NULL;
    char buffer[31];
    union tipo u;
%}
/* Declaraciones BISON */
%union{
	int entero;
    float decimal;
    char *variable;
    char *cadena;
    char *tipo;
}

%token <entero> ENTERO
%token VAR
%token <decimal> DECIMAL
%token <cadena> CAD
%token POT
%token <tipo> T_DOUBLE
%token <tipo> T_INT
%token <tipo> T_STRING
%token IGUAL
%type <variable> VAR
%type <entero> exp
%type <decimal> des
%type <cadena> cad

%left '+'
%left '-'
%left '*'
%left '/'
%left ';'
%left '%'
%left IGUAL

/* Gramática */
%%

input: /* cadena vacía */
	| input line
;

line:	'\n'
	| exp '\n' { printf ("\tresultado: %d\n", $1); }
    | des '\n' { printf ("\tresultado: %f\n", $1); }
    | dec '\n' { printf ("\tDeclaracion\n"); }
    | cad '\n' { printf ("\tresultado: %s\n", $1); }
;

exp:	ENTERO { $$ = $1; }
    | exp '+' exp { $$ = $1 + $3; }
    | exp '-' exp { $$ = $1 - $3; }
    | exp '*' exp { $$ = $1 * $3; }
    | exp '/' exp { $$ = $1 / $3; }
    | exp '%' exp { $$ = $1 % $3; }
    | POT "(" exp "," exp ")" {$$ = pow($3,$5);} 
    | VAR {
        aux=buscarListaL (tabla, $1);
        $$=aux->dato.entero;}
;

des:	DECIMAL { $$ = $1; }
	| des '+' des { $$ = $1 + $3; }
    | des '-' des { $$ = $1 - $3; }
    | des '*' des { $$ = $1 * $3; }
    | des '/' des { $$ = $1 / $3; }
    | des '%' des { $$ = fmod($1,$3); }
    | POT "(" des "," des ")" {$$ = powf($3,$5);}
    | VAR {
        aux=buscarListaL (tabla, $1);
        $$=aux->dato.dec;}
;

cad:    CAD { $$ = $1; }
    | cad '+' cad {
                     strcat($1,$3);
                     strcpy($$,$1);
                     printf ("\tresultado: %s\n", $$);
                     }
    | VAR {
        aux=buscarListaL (tabla, $1);
        strcpy($$,aux->dato.cadena);}
;

dec:    T_INT VAR ';' {

                     u.entero=0;
                     insertarListaL (&tabla, u, $2, $1);
                     }
    | T_DOUBLE VAR ';' {

                     u.dec=0;
                     insertarListaL (&tabla, u, $2, $1);
                     }
    
    | T_STRING VAR ';' {

                     strcpy(u.cadena," ");
                     insertarListaL (&tabla, u, $2, $1);
                     }

    | T_INT VAR IGUAL exp ';' {
                             
                             u.entero=$4;
                             insertarListaL (&tabla, u, $2, $1);
                             }
    | T_DOUBLE VAR IGUAL des ';'
                             {
                             
                             u.dec=$4;
                             insertarListaL (&tabla, u, $2, $1);
                             }

    | T_STRING VAR IGUAL cad ';'
                             {
                             strcpy(u.cadena,$4);
                             insertarListaL (&tabla, u, $2, $1);
                             }

    | VAR IGUAL exp ';'
                             {
                             aux=buscarListaL (tabla, $1);
                             aux->dato.entero=$3;
                             }
    | VAR IGUAL des ';'
                             {
                             aux=buscarListaL (tabla, $1);
                             aux->dato.dec=$3;
                             }

    | VAR IGUAL cad ';'
                             {
                             aux=buscarListaL (tabla, $1);
                             strcpy(aux->dato.cadena,$3);
                             }
;

%%

int main(){
    tabla=(struct ListaL *)NULL;
	yyparse();
}

yyerror (char *s){
	printf("--%s--\n", s);
}

int yywrap(){
	return 1;
}
