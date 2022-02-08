%{
#include "prac5.tab.h"
%}
DIGITO [0-9]
NUM ("-")?[1-9]{DIGITO}*
DEC ("-")?(0|{NUM}+)"."{DIGITO}+
M [Mm][Oo][Dd]
%%

{M}	{
	printf("Modulo\n");
	return (MOD);
	}

"("|")"	{
	printf("Signo parentesis %s\n",yytext);
	return (yytext[0]);
	}

","	{
	printf("coma %s\n",yytext);
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

"+"|"-"|"*"|"/"	{
	printf("Signo op %s\n",yytext);
	return (yytext[0]);
	}
"\n" {
	printf("Salto de linea\n");
	return (yytext[0]);
	}
%%