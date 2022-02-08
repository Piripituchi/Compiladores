%{
#include "calculadora.tab.h"
%}
DIGITO [0-9]
MAYUS [A-Z]
MINUS [a-z]
NUM ("-")?[1-9]{DIGITO}*
DEC ("-")?(0|{NUM}+)"."{DIGITO}+
NOMBRE (_*({MAYUS}|{MINUS})({MAYUS}|{MINUS}|{DIGITO}|_)*) 
CADENA "\"".*"\""
P [P][o][w]
%%

{CADENA}	{
	printf("Cadena %s\n",yytext);
	yylval.cadena=strdup(yytext);
	return (CAD);
	}

{P}	{
	printf("Potencia \n");
	return (POT);
	}

"double"	{
	printf("Tipo de varible %s\n",yytext);
	yylval.tipo=strdup(yytext);
	return (T_DOUBLE);
	}

"int"	{
	printf("Tipo de varible %s\n",yytext);
	yylval.tipo=strdup(yytext);
	return (T_INT);
	}

"string"	{
	printf("Tipo de varible %s\n",yytext);
	yylval.tipo=strdup(yytext);
	return (T_STRING);
	}	

{NOMBRE}	{
	printf("Varible %s\n",yytext);
	yylval.variable=strdup(yytext);
	return (VAR);
	}


"("|")"	{
	printf("Signo parentesis %s\n",yytext);
	return (yytext[0]);
	}

","	{
	printf("coma %s\n",yytext);
	return (yytext[0]);
	}

";"	{
	printf("fin de expresion %s\n",yytext);
	return (yytext[0]);
	}

{NUM}	{
	printf("Numero entero %s\n",yytext);
	yylval.entero = atoi(yytext);
	return (ENTERO);
	}

{DEC}	{
	printf("Numero decimal %s\n",yytext);
	yylval.decimal = atof(yytext);
	return (DECIMAL);
	}

"+"|"-"|"*"|"/"|"%"	{
	printf("Signo op %s\n",yytext);
	return (yytext[0]);
	}

"="	{
	printf("Igual \n");
	return (IGUAL);
	}

"\n" {
	printf("Salto de linea\n");
	return (yytext[0]);
	}
%%