def lexico(codigo):

    codigo = codigo + " "
    i = 0
    n = len(codigo)

    estado = 0
    lexema = ""

    tokens = []
    errores = []

    while i < n:

        c = codigo[i]

        # =====================
        # ESTADO INICIAL
        # =====================
        if estado == 0:

            if c.isspace():
                i += 1
                continue

            elif c.isalpha() or c == "_":
                lexema = c
                estado = 1
                i += 1
                continue

            elif c.isdigit():
                lexema = c
                estado = 2
                i += 1
                continue

            elif c == '"':
                lexema = ""
                estado = 4
                i += 1
                continue

            elif c == '+':
                tokens.append(101)
                i += 1

            elif c == '-':
                tokens.append(102)
                i += 1

            elif c == '*':
                tokens.append(103)
                i += 1

            elif c == '/':
                tokens.append(104)
                i += 1

            elif c == '=':
                if i+1 < n and codigo[i+1] == '=':
                    tokens.append(110)
                    i += 2
                else:
                    tokens.append(105)
                    i += 1

            elif c == '<':
                if i+1 < n and codigo[i+1] == '=':
                    tokens.append(108)
                    i += 2
                elif i+1 < n and codigo[i+1] == '<':
                    tokens.append(115)
                    i += 2
                else:
                    tokens.append(106)
                    i += 1

            elif c == '>':
                if i+1 < n and codigo[i+1] == '=':
                    tokens.append(109)
                    i += 2
                elif i+1 < n and codigo[i+1] == '>':
                    tokens.append(114)
                    i += 2
                else:
                    tokens.append(107)
                    i += 1

            elif c == '!':
                if i+1 < n and codigo[i+1] == '=':
                    tokens.append(111)
                    i += 2
                else:
                    errores.append(f"ERROR: operador ! inválido en posición {i}")
                    i += 1

            elif c == '&':
                if i+1 < n and codigo[i+1] == '&':
                    tokens.append(112)
                    i += 2
                else:
                    errores.append(f"ERROR: operador & inválido en posición {i}")
                    i += 1

            elif c == '|':
                if i+1 < n and codigo[i+1] == '|':
                    tokens.append(113)
                    i += 2
                else:
                    errores.append(f"ERROR: operador | inválido en posición {i}")
                    i += 1

            elif c == '(':
                tokens.append(116)
                i += 1

            elif c == ')':
                tokens.append(117)
                i += 1

            elif c == '{':
                tokens.append(118)
                i += 1

            elif c == '}':
                tokens.append(119)
                i += 1

            elif c == ';':
                tokens.append(120)
                i += 1

            elif c == ',':
                tokens.append(121)
                i += 1

            else:
                errores.append(f"ERROR: símbolo desconocido '{c}' en posición {i}")
                i += 1

        # =====================
        # IDENTIFICADOR
        # =====================
        elif estado == 1:

            if c.isalnum() or c == "_":
                lexema += c
                i += 1
                continue
            else:

                if lexema == "int":
                    tokens.append(10)
                elif lexema == "float":
                    tokens.append(11)
                elif lexema == "void":
                    tokens.append(12)
                elif lexema == "if":
                    tokens.append(20)
                elif lexema == "else":
                    tokens.append(21)
                elif lexema == "while":
                    tokens.append(22)
                elif lexema == "for":
                    tokens.append(23)
                elif lexema == "return":
                    tokens.append(24)
                elif lexema == "cin":
                    tokens.append(25)
                elif lexema == "cout":
                    tokens.append(26)
                else:
                    tokens.append(1000)

                lexema = ""
                estado = 0
                continue

        # =====================
        # ENTERO
        # =====================
        elif estado == 2:

            if c.isdigit():
                lexema += c
                i += 1
                continue

            elif c == '.':
                lexema += c
                estado = 3
                i += 1
                continue
            elif c.isalpha() or c == "_":
                lexema += c
                i += 1

                # consumir todo el lexema inválido para reportarlo completo
                while i < n and (codigo[i].isalnum() or codigo[i] == "_"):
                    lexema += codigo[i]
                    i += 1

                errores.append(f"ERROR léxico: número inválido '{lexema}' en posición {i - len(lexema)}")
                lexema = ""
                estado = 0
                continue

            else:
                tokens.append(2000)
                lexema = ""
                estado = 0
                continue
            

        # =====================
        # REAL
        # =====================
        elif estado == 3:

            if c.isdigit():
                lexema += c
                i += 1
                continue

            else:
                # validar que no termine en punto
                if lexema[-1] == '.':
                    errores.append(f"ERROR: número real inválido '{lexema}'")
                else:
                    tokens.append(3000)

                lexema = ""
                estado = 0
                continue

        # =====================
        # CADENA
        # =====================
        elif estado == 4:

            if c == '"':
                tokens.append(4000)
                lexema = ""
                estado = 0
                i += 1
            else:
                lexema += c
                i += 1

    # =====================
    # VALIDACIÓN FINAL
    # =====================

    if estado == 4:
        errores.append("ERROR: cadena sin cerrar")

    return tokens, errores
#ANALIZADOR SINTACTICO
def parsear(tokens):

    if tokens and isinstance(tokens[0], tuple):
        tokens = [t[0] for t in tokens]

    parser = _Parser(tokens)
    ok, mensaje = parser.programa()

    if ok and parser.fin():
        return "VÁLIDO"
    if ok and not parser.fin():
        return f"ERROR SINTÁCTICO: símbolo inesperado '{parser.actual()}' en la posición {parser.i}"
    return mensaje

#_ es una convencion de pyhon que indica que la clase es privada es decir solo debe ser usada dentro de este modulo
class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def actual(self):
        if self.i < len(self.tokens):
            return self.tokens[self.i]
        return None

    def fin(self):
        return self.i >= len(self.tokens)

    def avanzar(self):
        self.i += 1

    def coincidir(self, esperado):
        if self.actual() == esperado:
            self.avanzar()
            return True, ""
        return False, f"ERROR SINTÁCTICO: se esperaba '{esperado}' y se encontró '{self.actual()}' en la posición {self.i}"
    
#representa el simbolo inicial de la gramatica.Unprograma es simplemente una secuencia de sentecias,asi que delega el analisis a instrucciones
    def programa(self):
        # Un programa es una secuencia de sentencias.
        ok, msg = self.instrucciones()
        if not ok:
            return False, msg
        return True, ""

    def instrucciones(self):
        # Una o más sentencias dentro del programa o bloque
        if self.fin() or self.actual() == 119:  # '}'
            return False, f"ERROR SINTÁCTICO: se esperaba una sentencia en la posición {self.i}"

        while not self.fin() and self.actual() != 119:
            ok, msg = self.sentencia()
            if not ok:
                return False, msg
        return True, ""

    def sentencia(self):
        t = self.actual()

        if t == 1000:  # id -> asignación;
            ok, msg = self.asignacion()
            if not ok:
                return False, msg
            ok, msg = self.coincidir(120)  # ;
            if not ok:
                return False, msg
            return True, ""

        if t == 25:  # cin
            return self.lectura()

        if t == 26:  # cout
            return self.escritura()

        if t in (10, 11, 12):  # tipo -> declaración o función
            # Si después del id viene '(' entonces es función; si no, declaración.
            if self.i + 2 < len(self.tokens) and self.tokens[self.i + 1] == 1000 and self.tokens[self.i + 2] == 116:
                return self.funcion()
            return self.declaracion()

        if t == 20:  # if
            return self.condicional_if()

        if t == 22:  # while
            return self.ciclo_while()

        if t == 23:  # for
            return self.ciclo_for()

        if t == 24:  # return
            return self.sentencia_return()

        if t == 118:  # bloque directo
            return self.bloque()

        return False, f"ERROR SINTÁCTICO: sentencia no válida con token '{t}' en la posición {self.i}"

#Analiza una asignación simple: `identificador = expresión`. No consume el `;` final (eso lo hace `sentencia`).
    def asignacion(self):
        ok, msg = self.coincidir(1000)#Espera un identificador (`1000`).
        if not ok:
            return False, msg #Si falla, propaga error.
        ok, msg = self.coincidir(105)  # =
        if not ok:
            return False, msg
        ok, msg = self.exp()#Analiza la expresión del lado derecho llamando a `exp()`.
        if not ok:
            return False, msg#Si `exp()` falla, propaga error.
        return True, ""

#Analiza una sentencia de entrada: `cin >> id >> id ... ;`.
    def lectura(self):
        ok, msg = self.coincidir(25)  # Consume cin
        if not ok:
            return False, msg #Si falla, propaga error.
        ok, msg = self.coincidir(114)  # >>
        if not ok:
            return False, msg
        ok, msg = self.coincidir(1000)#Consume el primer identificador.
        if not ok:
            return False, msg
        while not self.fin() and self.actual() == 115:#Mientras haya tokens y el actual sea `115`  El bucle permite múltiples `>> id`.
            self.avanzar()#Consume el `>>` (token `115`).
            ok, msg = self.coincidir(1000)#Consume el siguiente identificador.
            if not ok:
                return False, msg
        ok, msg = self.coincidir(120)  #Después del bucle, espera el punto y coma ;
        if not ok:
            return False, msg
        return True, ""

#Analiza `cout << expresión << expresión ... ;`.
    def escritura(self):
        ok, msg = self.coincidir(26)  # cout
        if not ok:
            return False, msg
        ok, msg = self.coincidir(115)  # <<
        if not ok:
            return False, msg
        ok, msg = self.exp()#Analiza la primera expresión.
        if not ok:
            return False, msg#Si `exp()` falla, propaga error.
        while not self.fin() and self.actual() == 114:#Mientras haya tokens y el actual sea `114`
            self.avanzar() #consume el operador 114
            ok, msg = self.exp()#Analiza la siguiente expresión.
            if not ok:
                return False, msg
        ok, msg = self.coincidir(120)  # espera ;
        if not ok:
            return False, msg
        return True, ""

#Analiza una declaración de variable: `tipo id [= expresión] ;`.
    def declaracion(self):
        ok, msg = self.tipo()#Llama a `tipo()` para consumir uno de los tipos (`int`, `float`, `char`).
        if not ok:
            return False, msg
        ok, msg = self.coincidir(1000)#Consume el identificador.
        if not ok:
            return False, msg
        if not self.fin() and self.actual() == 105:#Si no se ha llegado al final y el token actual es `105` (`=`), entonces hay inicialización.
            self.avanzar()#Consume el `=`.
            ok, msg = self.exp()#Analiza la expresión de inicialización.
            if not ok:
                return False, msg
        ok, msg = self.coincidir(120)  # ;
        if not ok:
            return False, msg
        return True, ""

#Analiza `if (condicion) bloque [else bloque]`.
    def condicional_if(self):
        ok, msg = self.coincidir(20)  # if
        if not ok:
            return False, msg
        ok, msg = self.coincidir(116)  # (
        if not ok:
            return False, msg
        ok, msg = self.condicion() #Analiza la condición dentro del paréntesis.
        if not ok:
            return False, msg
        ok, msg = self.coincidir(117)  # )
        if not ok:
            return False, msg
        ok, msg = self.bloque() #Analiza el bloque del `if`.
        if not ok:
            return False, msg
        if not self.fin() and self.actual() == 21:  # Si hay más tokens y el actual es `21` (`else`), procesa la parte `else`.
            self.avanzar()#Consume `else`.
            ok, msg = self.bloque()#Analiza el bloque del `else`.
            if not ok:
                return False, msg
        return True, ""

#Analiza `while (condicion) bloque`.
    def ciclo_while(self):
        ok, msg = self.coincidir(22)#Consume `while`.
        if not ok:
            return False, msg
        ok, msg = self.coincidir(116)#Consume `(`.
        if not ok:
            return False, msg
        ok, msg = self.condicion()#Analiza la condición.
        if not ok:
            return False, msg
        ok, msg = self.coincidir(117)#Consume `)`.
        if not ok:
            return False, msg
        return self.bloque()#Analiza el bloque y retorna su resultado (que ya es una tupla `(ok, msg)`).

#Analiza `for (asignacion; condicion; asignacion) bloque`.
    def ciclo_for(self):
        ok, msg = self.coincidir(23)#Consume `for`.
        if not ok:
            return False, msg
        ok, msg = self.coincidir(116)#Consume `(`.
        if not ok:
            return False, msg

        ok, msg = self.asignacion()#Analiza la primera asignación (inicialización).
        if not ok:
            return False, msg
        ok, msg = self.coincidir(120)  # ;
        if not ok:
            return False, msg

        ok, msg = self.condicion()
        if not ok:
            return False, msg
        ok, msg = self.coincidir(120)  # ;
        if not ok:
            return False, msg

        ok, msg = self.asignacion()
        if not ok:
            return False, msg

        ok, msg = self.coincidir(117)#Espera `)`.
        if not ok:
            return False, msg
        
        ok, msg = self.bloque()
        if not ok:
            return False, msg
        return True, ""

#Analiza la definición de una función: `tipo id ( [parametros] ) bloque`.
    def funcion(self):
        ok, msg = self.tipo()
        if not ok:
            return False, msg
        ok, msg = self.coincidir(1000)#Consume el nombre de la función.
        if not ok:
            return False, msg
        ok, msg = self.coincidir(116)#Consume `(`.
        if not ok:
            return False, msg
        if not self.fin() and self.actual() != 117:#Si no hay final y el token actual no es `)`, entonces hay parámetros.
            ok, msg = self.parametros()
            if not ok:
                return False, msg
        ok, msg = self.coincidir(117)#Consume `)`.
        if not ok:
            return False, msg
        ok, msg = self.bloque()#Analiza el cuerpo de la función (bloque).
        if not ok:
            return False, msg
        return True, ""

#Analiza una lista de identificadores separados por comas: `id , id , ...`. (Nota: no maneja tipos en los parámetros, solo identificadores).
    def parametros(self):
        ok, msg = self.coincidir(1000)#Consume el primer parámetro (identificador).
        if not ok:
            return False, msg
        while not self.fin() and self.actual() == 121:#Mientras haya tokens y el actual sea `121` (`,`), repite.
            self.avanzar()#Consume la coma.
            ok, msg = self.coincidir(1000)#Consume el siguiente identificador.
            if not ok:
                return False, msg
        return True, ""
    
#Analiza un bloque entre llaves: `{ instrucciones }`. No permite bloque vacío.
    def bloque(self):
        ok, msg = self.coincidir(118)  #consume {
        if not ok:
            return False, msg

        if self.actual() == 119:#Si el token actual es `}` (es decir, no hay instrucciones), entonces bloque vacío.
            return False, f"ERROR SINTÁCTICO: el bloque no puede estar vacío en la posición {self.i}"

        ok, msg = self.instrucciones()#Analiza las instrucciones internas.
        if not ok:
            return False, msg

        ok, msg = self.coincidir(119)  # consume}
        if not ok:
            return False, msg
        return True, ""

#Analiza `return expresión ;`.
    def sentencia_return(self):
        ok, msg = self.coincidir(24)#Consume `return`.
        if not ok:
            return False, msg
        ok, msg = self.exp()#Analiza la expresión que sigue.
        if not ok:
            return False, msg
        ok, msg = self.coincidir(120)#Espera `;`
        if not ok:
            return False, msg
        return True, ""

#Analiza una condición que puede ser una expresión con operador relacional (`<`, `>`, `<=`, `>=`, `==`, `!=`) o una combinación
#  con operadores lógicos (`&&`, `||`). La gramática permite: `exp op_relacional exp` o `exp op_logico condicion`.
    def condicion(self):
        ok, msg = self.exp()#Primero analiza una expresión (el lado izquierdo).
        if not ok:
            return False, msg

        if not self.fin() and self.actual() in (106, 107, 108, 109, 110, 111):#Si no estamos al final y el token actual es uno de los 
            #operadores relacionales (106:`<`, 107:`>`, 108:`<=`, 109:`>=`, 110:`==`, 111:`!=`).
            self.avanzar()#Consume el operador.
            ok, msg = self.exp()#Analiza la expresión del lado derecho.
            if not ok:
                return False, msg
            return True, ""

        if not self.fin() and self.actual() in (112, 113):#Si el token actual es `112` (`&&`) o `113` (`||`).
            self.avanzar()#Consume el operador lógico.
            ok, msg = self.condicion()#Analiza recursivamente otra condición (la parte derecha).
            if not ok:
                return False, msg
            return True, ""

        #Si no se encontró ni relacional ni lógico, retorna error.
        return False, f"ERROR SINTÁCTICO: se esperaba operador relacional o lógico en la posición {self.i}"

#Analiza una expresión aritmética con suma y resta (`+`, `-`), con prioridad normal. Usa recursión para manejar la asociatividad por
#  izquierda (aunque en realidad la implementación es recursiva por derecha, pero en la práctica funciona para este nivel).
    def exp(self):
        ok, msg = self.termino()#Analiza un término (factor con multiplicación/división).
        if not ok:
            return False, msg
        if not self.fin() and self.actual() in (101, 102):#Si el token actual es `101` (`+`) o `102` (`-`).
            self.avanzar()#Consume el operador.
            ok, msg = self.exp()#Llama recursivamente a `exp()` para el resto de la expresión.
            if not ok:
                return False, msg
        return True, ""

#Analiza un término con multiplicación y división (`*`, `/`). Similar a `exp` pero para operadores de mayor prioridad.
    def termino(self):
        ok, msg = self.factor()#Analiza un factor (identificador, número, cadena, paréntesis).
        if not ok:
            return False, msg
        if not self.fin() and self.actual() in (103, 104):#Si el token es `103` (`*`) o `104` (`/`).
            self.avanzar()#Consume el operador.
            ok, msg = self.termino()#Llama recursivamente a `termino()` para la parte derecha.
            if not ok:
                return False, msg
        return True, ""

#Analiza los elementos básicos de una expresión: identificador, número entero, número real, cadena, o una subexpresión entre paréntesis.
    def factor(self):
        t = self.actual()#Guarda el token actual.
        if t in (1000, 2000, 3000, 4000):#Si es `1000` (id), `2000` (entero), `3000` (real), `4000` (cadena).
            self.avanzar()#Consume ese token.
            return True, ""
        if t == 116:#Si es `(`.
            self.avanzar()#Consume `(`.
            ok, msg = self.exp()#Analiza la expresión interna.
            if not ok:
                return False, msg
            ok, msg = self.coincidir(117)#Espera `)`.
            if not ok:
                return False, msg
            return True, ""
        #Si no es ninguno de los casos, retorna error.
        return False, f"ERROR SINTÁCTICO: factor no válido en la posición {self.i} (token '{t}')"

#Verifica que el token actual sea uno de los tipos de datos (`int`, `float`, `char`) y lo consume.
    def tipo(self):
        if self.actual() in (10, 11, 12):#if self.actual() in (10, 11, 12):
            self.avanzar()
            return True, ""
        #Si no es un tipo, retorna error.
        return False, f"ERROR SINTÁCTICO: se esperaba un tipo de dato en la posición {self.i}"

codigo = '''
while (x < 5) {
    x = x  1;
}


'''

# 1. LÉXICO
tokens, errores_lexicos = lexico(codigo)

print("TOKENS:", tokens)
print("ERRORES LÉXICOS:", errores_lexicos)

# 2. SI NO HAY ERRORES → SINTÁCTICO
if not errores_lexicos:
    resultado = parsear(tokens)   # función inicial del parser
    print("RESULTADO SINTÁCTICO:", resultado)
else:
    print("No se analiza sintácticamente por errores léxicos")