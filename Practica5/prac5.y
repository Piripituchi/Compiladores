%{
    //#include <smath.h>
%}
/* Declaraciones BISON */
%union{
	int entero;
    double decimal;
}

%token <entero> ENTERO
%token <decimal> DECIMAL
%token MOD
%type <entero> exp
%type <decimal> des

%left '+'
%left '-'
%left '*'
%left '/'

/* Gramática */
%%

input: /* cadena vacía */
	| input line
;

line:	'\n'
	| exp '\n' { printf ("\tresultado: %d\n", $1); }
    | des '\n' { printf ("\tresultado: %f\n", $1); }
;

exp:	ENTERO { $$ = $1; }
    | exp '+' exp { $$ = $1 + $3; }
    | exp '-' exp { $$ = $1 - $3; }
    | exp '*' exp { $$ = $1 * $3; }
    | exp '/' exp { $$ = $1 / $3; }
    | MOD'(' exp ',' exp ')' { $$ = $3 % $5; }
;

des:	DECIMAL { $$ = $1; }
	| des '+' des { $$ = $1 + $3; }
    | des '-' des { $$ = $1 - $3; }
    | des '*' des { $$ = $1 * $3; }
    | des '/' des { $$ = $1 / $3; }
;

%%

int main(){
	yyparse();
}

yyerror (char *s){
	printf("--%s--\n", s);
}

int yywrap(){
	return 1;
}
