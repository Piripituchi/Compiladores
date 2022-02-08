ESPACIO [^\s]
MAYUS [A-Z]
MINUS [a-z]
DIGITO [0-9]
NOMBRE (_*({MAYUS}|{MINUS})({MAYUS}|{MINUS}|{DIGITO}|_)*) 
RESERVADAS (auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|typedef|union|unsigned|void|volatile|while)
DECIMAL ("+"|"-")?(0|{ENTERO}+)"."{DIGITO}+
ENTERO ("+"|"-")?[1-9]{DIGITO}*
POTENCIA (({ENTERO}|{DECIMAL})"^"({ENTERO}|{DECIMAL}))
SUMA (({ENTERO}|{DECIMAL})"+"({ENTERO}|{DECIMAL}))
RESTA (({ENTERO}|{DECIMAL})"-"({ENTERO}|{DECIMAL}))
MULTIPLICACION (({ENTERO}|{DECIMAL})"*"({ENTERO}|{DECIMAL}))
DIVICION (({ENTERO}|{DECIMAL})"/"({ENTERO}|{DECIMAL}))
MODULO ([Mm][Oo][Dd]"("({ENTERO}|{DECIMAL})","({ENTERO}|{DECIMAL})")")
%%
{RESERVADAS} {printf("Palabra reservada: %s\n",yytext);}
{NOMBRE} {printf("Nombre de variable correcto: %s\n",yytext);}
{POTENCIA} {printf("Potencia: %s\n",yytext);}
{SUMA} {printf("Suma: %s\n",yytext);}
{RESTA} {printf("Resta: %s\n",yytext);}
{MULTIPLICACION} {printf("Multiplicacion: %s\n",yytext);}
{DIVICION} {printf("Divicion: %s\n",yytext);}
{MODULO} {printf("Modulo: %s\n",yytext);}
{ENTERO} {printf("Numero entero: %s\n",yytext);}
{DECIMAL} {printf("Numero decimal: %s\n",yytext);}

