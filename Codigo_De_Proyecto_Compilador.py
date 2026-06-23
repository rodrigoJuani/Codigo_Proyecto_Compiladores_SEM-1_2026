import re
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
                tokens.append((101, '+'))
                i += 1

            elif c == '-':
                tokens.append((102, '-'))
                i += 1

            elif c == '*':
                tokens.append((103, '*'))
                i += 1

            elif c == '/':
                tokens.append((104, '/'))
                i += 1

            elif c == '=':
                if i+1 < n and codigo[i+1] == '=':
                    tokens.append((110, '=='))
                    i += 2
                else:
                    tokens.append((105, '='))
                    i += 1

            elif c == '<':
                if i+1 < n and codigo[i+1] == '=':
                    tokens.append((108, '<='))
                    i += 2
                elif i+1 < n and codigo[i+1] == '<':
                    tokens.append((115, '<<'))
                    i += 2
                else:
                    tokens.append((106, '<'))
                    i += 1

            elif c == '>':
                if i+1 < n and codigo[i+1] == '=':
                    tokens.append((109, '>='))
                    i += 2
                elif i+1 < n and codigo[i+1] == '>':
                    tokens.append((114, '>>'))
                    i += 2
                else:
                    tokens.append((107, '>'))
                    i += 1

            elif c == '!':
                if i+1 < n and codigo[i+1] == '=':
                    tokens.append((111, '!='))
                    i += 2
                else:
                    errores.append(f"ERROR: operador ! inválido en posición {i}")
                    i += 1

            elif c == '&':
                if i+1 < n and codigo[i+1] == '&':
                    tokens.append((112, '&&'))
                    i += 2
                else:
                    errores.append(f"ERROR: operador & inválido en posición {i}")
                    i += 1

            elif c == '|':
                if i+1 < n and codigo[i+1] == '|':
                    tokens.append((113, '||'))
                    i += 2
                else:
                    errores.append(f"ERROR: operador | inválido en posición {i}")
                    i += 1

            elif c == '(':
                tokens.append((116, '('))
                i += 1

            elif c == ')':
                tokens.append((117, ')'))
                i += 1

            elif c == '{':
                tokens.append((118, '{'))
                i += 1

            elif c == '}':
                tokens.append((119, '}'))
                i += 1

            elif c == ';':
                tokens.append((120, ';'))
                i += 1

            elif c == ',':
                tokens.append((121, ','))
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
                    tokens.append((10, 'int'))
                elif lexema == "float":
                    tokens.append((11, 'float'))
                elif lexema == "void":
                    tokens.append((12, 'void'))
                elif lexema == "if":
                    tokens.append((20, 'if'))
                elif lexema == "else":
                    tokens.append((21, 'else'))
                elif lexema == "while":
                    tokens.append((22, 'while'))
                elif lexema == "for":
                    tokens.append((23, 'for'))
                elif lexema == "return":
                    tokens.append((24, 'return'))
                elif lexema == "cin":
                    tokens.append((25, 'cin'))
                elif lexema == "cout":
                    tokens.append((26, 'cout'))
                else:
                    tokens.append((1000, lexema))

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
                tokens.append((2000, lexema))
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
                    tokens.append((3000, lexema))

                lexema = ""
                estado = 0
                continue

        # =====================
        # CADENA
        # =====================
        elif estado == 4:

            if c == '"':
                tokens.append((4000, '"' + lexema + '"'))
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



# ==========================================
# ANALIZADOR SEMÁNTICO 
# ==========================================

RESERVADAS = {
    "int", "float", "void", "if", "else", "while", "for", "return", "cin", "cout"
}

TIPOS_NUMERICOS = {"int", "float"}
OPERADORES_ARIT = {"+", "-", "*", "/", "%", "^"}
OPERADORES_REL = {"<", ">", "<=", ">=", "==", "!="}
OPERADORES_LOG = {"&&", "||"}
OPERADORES_SEM = OPERADORES_ARIT | OPERADORES_REL | OPERADORES_LOG

PRECEDENCIA = {
    "||": 1,
    "&&": 2,
    "==": 3, "!=": 3, "<": 3, ">": 3, "<=": 3, ">=": 3,
    "+": 4, "-": 4,
    "*": 5, "/": 5, "%": 5,
    "^": 6,
}

tablaSimbolos = {}
tablaFunciones = {}


def limpiar_semantico():
    tablaSimbolos.clear()
    tablaFunciones.clear()


def token_codigo(tok):
    return tok[0] if isinstance(tok, tuple) else tok


def token_lexema(tok):
    if isinstance(tok, tuple) and len(tok) > 1:
        return tok[1]
    return str(tok)


def _es_identificador(lexema):
    return bool(re.fullmatch(r"[A-Za-z_]\w*", lexema)) and lexema not in RESERVADAS


def _es_entero(tok):
    return re.fullmatch(r"\d+", tok) is not None


def _es_real(tok):
    return re.fullmatch(r"\d+\.\d+", tok) is not None


def _es_cadena(tok):
    return re.fullmatch(r'"[^"]*"', tok, flags=re.S) is not None


def _tipo_literal(tok):
    if _es_entero(tok):
        return "int"
    if _es_real(tok):
        return "float"
    if _es_cadena(tok):
        return "cadena"
    return None


def _buscar_en_ambitos(nombre, ambitos):
    for ambito in reversed(ambitos):
        if nombre in ambito:
            return True, ambito[nombre]
    return False, None


def registrarVariable(nombre, tipo, ambito):
    if nombre in ambito:
        return False, f"ERROR SEMÁNTICO: '{nombre}' ya fue declarada en este ámbito"
    ambito[nombre] = tipo
    return True, ""


def extraer_parametros(lista_texto):
    if isinstance(lista_texto, str):
        texto = lista_texto.strip()
    else:
        texto = " ".join(token_lexema(t) for t in lista_texto).strip()

    if not texto:
        return []

    params = []
    for p in [x.strip() for x in texto.split(",") if x.strip()]:
        m = re.match(r"^(int|float|void)\s+([A-Za-z_]\w*)$", p)
        if m:
            params.append((m.group(2), m.group(1)))
        else:
            m2 = re.match(r"^([A-Za-z_]\w*)$", p)
            if m2:
                params.append((m2.group(1), "int"))
    return params


def _tokenizar_expresion(texto):
    patron = r'"[^"]*"|<=|>=|==|!=|&&|\|\||[A-Za-z_]\w*|\d+\.\d+|\d+|[()+\-*/%^<>]'
    return re.findall(patron, texto)


def segmentar_tokens(tokens):
    chunks = []
    actual = []
    depth = 0

    for tok in tokens:
        cod = token_codigo(tok)
        if cod == 116:
            depth += 1
            actual.append(tok)
            continue
        if cod == 117:
            depth = max(0, depth - 1)
            actual.append(tok)
            continue
        if cod == 120 and depth == 0:
            if actual:
                chunks.append(actual)
                actual = []
            chunks.append([tok])
            continue
        if cod in (118, 119) and depth == 0:
            if actual:
                chunks.append(actual)
                actual = []
            chunks.append([tok])
            continue
        actual.append(tok)

    if actual:
        chunks.append(actual)
    return chunks


def _tokens_a_lexemas(tokens):
    return [token_lexema(t) for t in tokens]


def infijo_a_prefijo(tokens):
    if isinstance(tokens, str):
        lex = _tokenizar_expresion(tokens)
    else:
        lex = _tokens_a_lexemas(tokens)

    inv = list(reversed(lex))
    for i, t in enumerate(inv):
        if t == "(":
            inv[i] = ")"
        elif t == ")":
            inv[i] = "("

    salida = []
    pila = []
    for tok in inv:
        if tok == "(":
            pila.append(tok)
        elif tok == ")":
            while pila and pila[-1] != "(":
                salida.append(pila.pop())
            if pila and pila[-1] == "(":
                pila.pop()
        elif tok in OPERADORES_SEM:
            while pila and pila[-1] in OPERADORES_SEM and (
                PRECEDENCIA[pila[-1]] > PRECEDENCIA[tok] or
                (PRECEDENCIA[pila[-1]] == PRECEDENCIA[tok] and tok != "^")
            ):
                salida.append(pila.pop())
            pila.append(tok)
        else:
            salida.append(tok)

    while pila:
        salida.append(pila.pop())

    return list(reversed(salida))


def _compatibles_asignacion(tipo_destino, tipo_origen):
    if tipo_destino == "desconocido" or tipo_origen == "desconocido":
        return True
    if tipo_destino == tipo_origen:
        return True
    if tipo_destino == "float" and tipo_origen == "int":
        return True
    return False


def _validar_operacion(op, izq_tipo, der_tipo, errores, contexto="expresión"):
    if izq_tipo == "desconocido" or der_tipo == "desconocido":
        return "desconocido"

    if op in OPERADORES_ARIT:
        if izq_tipo not in TIPOS_NUMERICOS or der_tipo not in TIPOS_NUMERICOS:
            errores.append(f"ERROR SEMÁNTICO: operación aritmética inválida '{op}' entre '{izq_tipo}' y '{der_tipo}' en {contexto}")
            return "desconocido"
        if op == "/" or izq_tipo == "float" or der_tipo == "float":
            return "float"
        return "int"

    if op in OPERADORES_REL:
        if izq_tipo not in TIPOS_NUMERICOS or der_tipo not in TIPOS_NUMERICOS:
            errores.append(f"ERROR SEMÁNTICO: comparación inválida '{op}' entre '{izq_tipo}' y '{der_tipo}' en {contexto}")
            return "desconocido"
        return "bool"

    if op in OPERADORES_LOG:
        if izq_tipo == "cadena" or der_tipo == "cadena":
            errores.append(f"ERROR SEMÁNTICO: operación lógica inválida '{op}' con cadenas en {contexto}")
            return "desconocido"
        return "bool"

    return "desconocido"


def _generar_expresion(expr_tokens, ambitos, errores, temp_inicial, contexto):
    prefijo = infijo_a_prefijo(expr_tokens)
    cuartetos = []
    temp = temp_inicial

    def recorrer(it):
        nonlocal temp
        tok = next(it)
        if tok in OPERADORES_SEM:
            op1_ref, op1_tipo = recorrer(it)
            op2_ref, op2_tipo = recorrer(it)
            res_tipo = _validar_operacion(tok, op1_tipo, op2_tipo, errores, contexto)
            res_ref = f"T{temp}"
            temp += 1
            cuartetos.append((tok, op1_ref, op2_ref, res_ref))
            return res_ref, res_tipo
        lit_tipo = _tipo_literal(tok)
        if lit_tipo is not None:
            return tok, lit_tipo
        if _es_identificador(tok):
            ok, tipo = _buscar_en_ambitos(tok, ambitos)
            if not ok:
                errores.append(f"ERROR SEMÁNTICO: identificador no declarado '{tok}' en {contexto}")
                return tok, "desconocido"
            return tok, tipo
        return tok, "desconocido"

    if not prefijo:
        return [], "desconocido", "", temp

    ref, tipo = recorrer(iter(prefijo))
    return cuartetos, tipo, ref, temp


def _partir_condicion_for(tokens):
    partes = []
    actual = []
    depth = 0
    for tok in tokens:
        cod = token_codigo(tok)
        if cod == 116:
            depth += 1
        elif cod == 117:
            depth = max(0, depth - 1)
        if cod == 120 and depth == 0:
            partes.append(actual)
            actual = []
        else:
            actual.append(tok)
    partes.append(actual)
    while len(partes) < 3:
        partes.append([])
    return partes[:3]

def analizar_semantico(codigo):
    limpiar_semantico()
    tokens, errores_lexicos = lexico(codigo)
    if errores_lexicos:
        return {
            "tabla_simbolos": tablaSimbolos,
            "tabla_funciones": tablaFunciones,
            "cuartetos": [],
            "errores": errores_lexicos[:]
        }

    errores = []
    cuartetos = []
    ambitos = [tablaSimbolos]
    pila_funciones = []
    pendiente_funcion = None
    pendientes_else = []   # <-- NUEVO: guarda if pendientes de else
    temp = 1

    chunks = segmentar_tokens(tokens)
    i = 0
    while i < len(chunks):
        chunk = chunks[i]
        cod0 = token_codigo(chunk[0]) if chunk else None
        lex = _tokens_a_lexemas(chunk)

        if len(chunk) == 1 and cod0 == 120:
            i += 1
            continue

        if len(chunk) == 1 and cod0 == 119:
            if len(ambitos) > 1:
                ambitos.pop()
            if pila_funciones and len(ambitos) == 1:
                pila_funciones.pop()
            i += 1
            continue

        if len(chunk) == 1 and cod0 == 118:
            nuevo = {}
            ambitos.append(nuevo)
            if pendiente_funcion is not None:
                nombre_func, retorno, params = pendiente_funcion
                tablaFunciones[nombre_func] = {"retorno": retorno, "parametros": params}
                for nombre_param, tipo_param in params:
                    ok, msg = registrarVariable(nombre_param, tipo_param, ambitos[-1])
                    if not ok:
                        errores.append(msg)
                pila_funciones.append(nombre_func)
                pendiente_funcion = None
            i += 1
            continue

        m_func = re.match(r"^(int|float|void)\s+([A-Za-z_]\w*)\s*\((.*?)\)$", " ".join(lex))
        if m_func and i + 1 < len(chunks) and len(chunks[i + 1]) == 1 and token_codigo(chunks[i + 1][0]) == 118:
            pendiente_funcion = (m_func.group(2), m_func.group(1), extraer_parametros(m_func.group(3)))
            i += 1
            continue

        m_decl = re.match(r"^(int|float|void)\s+([A-Za-z_]\w*)\s*(?:=\s*(.+))?$", " ".join(lex))
        if m_decl:
            tipo, nombre, expr_txt = m_decl.group(1), m_decl.group(2), m_decl.group(3)
            if nombre in RESERVADAS:
                errores.append(f"ERROR SEMÁNTICO: no se puede usar la palabra reservada '{nombre}' como identificador")
                i += 1
                continue
            if tipo == "void":
                errores.append(f"ERROR SEMÁNTICO: la variable '{nombre}' no puede ser de tipo void")
                i += 1
                continue
            ok, msg = registrarVariable(nombre, tipo, ambitos[-1])
            if not ok:
                errores.append(msg)
            if expr_txt is None:
                cuartetos.append(("DECL", tipo, "", nombre))
            else:
                expr_tokens = _tokenizar_expresion(expr_txt)
                c, tipo_expr, ref, temp = _generar_expresion(expr_tokens, ambitos, errores, temp, f"inicialización de '{nombre}'")
                cuartetos.extend(c)
                if tipo_expr != "desconocido" and not _compatibles_asignacion(tipo, tipo_expr):
                    errores.append(f"ERROR SEMÁNTICO: no se puede asignar '{tipo_expr}' a variable '{nombre}' de tipo '{tipo}'")
                cuartetos.append(("=", ref or expr_txt, "", nombre))
            i += 1
            continue

        m_asig = re.match(r"^([A-Za-z_]\w*)\s*=\s*(.+)$", " ".join(lex))
        if m_asig:
            nombre, expr_txt = m_asig.group(1), m_asig.group(2)
            ok, tipo_var = _buscar_en_ambitos(nombre, ambitos)
            if not ok:
                errores.append(f"ERROR SEMÁNTICO: variable no declarada '{nombre}' en asignación")
                tipo_var = "desconocido"
            expr_tokens = _tokenizar_expresion(expr_txt)
            c, tipo_expr, ref, temp = _generar_expresion(expr_tokens, ambitos, errores, temp, f"asignación a '{nombre}'")
            cuartetos.extend(c)
            if tipo_expr != "desconocido" and not _compatibles_asignacion(tipo_var, tipo_expr):
                errores.append(f"ERROR SEMÁNTICO: no se puede asignar '{tipo_expr}' a variable '{nombre}' de tipo '{tipo_var}'")
            cuartetos.append(("=", ref or expr_txt, "", nombre))
            i += 1
            continue

        if cod0 == 25:
            ids = [token_lexema(t) for t in chunk if token_codigo(t) == 1000]
            for nombre in ids:
                ok, _ = _buscar_en_ambitos(nombre, ambitos)
                if not ok:
                    errores.append(f"ERROR SEMÁNTICO: variable no declarada '{nombre}' en cin")
                cuartetos.append(("READ", nombre, "", ""))
            i += 1
            continue

        if cod0 == 26:
            partes = []
            actual = []
            for tok in chunk[1:]:
                if token_codigo(tok) in (115, 114):
                    if actual:
                        partes.append(actual)
                        actual = []
                else:
                    actual.append(tok)
            if actual:
                partes.append(actual)
            for parte in partes:
                expr_txt = " ".join(_tokens_a_lexemas(parte))
                c, tipo_expr, ref, temp = _generar_expresion(parte, ambitos, errores, temp, f"salida '{expr_txt}'")
                cuartetos.extend(c)
                cuartetos.append(("WRITE", ref or expr_txt, "", ""))
            i += 1
            continue

        if cod0 == 24:
            expr_tokens = chunk[1:]
            c, tipo_expr, ref, temp = _generar_expresion(expr_tokens, ambitos, errores, temp, "return")
            cuartetos.extend(c)
            cuartetos.append(("RETURN", ref or " ".join(_tokens_a_lexemas(expr_tokens)), "", ""))
            i += 1
            continue

        if cod0 == 20:
            kw = token_lexema(chunk[0]).upper()
            cond = []
            seen = False
            for tok in chunk[1:]:
                if token_codigo(tok) == 116:
                    seen = True
                    continue
                if token_codigo(tok) == 117:
                    break
                if seen:
                    cond.append(tok)
            c, tipo_cond, ref, temp = _generar_expresion(cond, ambitos, errores, temp, f"condición de {kw}")
            cuartetos.extend(c)
            cuartetos.append((kw, ref or " ".join(_tokens_a_lexemas(cond)), "", ""))

            pendientes_else.append(True)   # <-- NUEVO: este if puede tener else
            i += 1
            continue

        if cod0 == 21:
            if not pendientes_else:
                errores.append("ERROR SEMÁNTICO: 'else' sin un 'if' previo")
            else:
                pendientes_else.pop()
                cuartetos.append(("ELSE", "", "", ""))  # <-- NUEVO: reconocer else
            i += 1
            continue

        if cod0 == 22:
            kw = token_lexema(chunk[0]).upper()
            cond = []
            seen = False
            for tok in chunk[1:]:
                if token_codigo(tok) == 116:
                    seen = True
                    continue
                if token_codigo(tok) == 117:
                    break
                if seen:
                    cond.append(tok)
            c, tipo_cond, ref, temp = _generar_expresion(cond, ambitos, errores, temp, f"condición de {kw}")
            cuartetos.extend(c)
            cuartetos.append((kw, ref or " ".join(_tokens_a_lexemas(cond)), "", ""))
            i += 1
            continue

        if cod0 == 23:
            inner = []
            seen = False
            for tok in chunk[1:]:
                if token_codigo(tok) == 116:
                    seen = True
                    continue
                if token_codigo(tok) == 117:
                    break
                if seen:
                    inner.append(tok)
            init, cond, update = _partir_condicion_for(inner)

            if init:
                init_txt = " ".join(_tokens_a_lexemas(init))
                m = re.match(r"^([A-Za-z_]\w*)\s*=\s*(.+)$", init_txt)
                if m:
                    nombre, expr_txt = m.group(1), m.group(2)
                    ok, tipo_var = _buscar_en_ambitos(nombre, ambitos)
                    if not ok:
                        errores.append(f"ERROR SEMÁNTICO: variable no declarada '{nombre}' en for (inicialización)")
                        tipo_var = "desconocido"
                    expr_tokens = _tokenizar_expresion(expr_txt)
                    c, tipo_expr, ref, temp = _generar_expresion(expr_tokens, ambitos, errores, temp, f"for-inicialización de '{nombre}'")
                    cuartetos.extend(c)
                    if tipo_expr != "desconocido" and not _compatibles_asignacion(tipo_var, tipo_expr):
                        errores.append(f"ERROR SEMÁNTICO: no se puede asignar '{tipo_expr}' a variable '{nombre}' de tipo '{tipo_var}'")
                    cuartetos.append(("=", ref or expr_txt, "", nombre))

            if cond:
                c, tipo_cond, ref, temp = _generar_expresion(cond, ambitos, errores, temp, "condición de for")
                cuartetos.extend(c)
                cuartetos.append(("FOR_COND", ref or " ".join(_tokens_a_lexemas(cond)), "", ""))

            if update:
                upd_txt = " ".join(_tokens_a_lexemas(update))
                m = re.match(r"^([A-Za-z_]\w*)\s*=\s*(.+)$", upd_txt)
                if m:
                    nombre, expr_txt = m.group(1), m.group(2)
                    ok, tipo_var = _buscar_en_ambitos(nombre, ambitos)
                    if not ok:
                        errores.append(f"ERROR SEMÁNTICO: variable no declarada '{nombre}' en for (actualización)")
                        tipo_var = "desconocido"
                    expr_tokens = _tokenizar_expresion(expr_txt)
                    c, tipo_expr, ref, temp = _generar_expresion(expr_tokens, ambitos, errores, temp, f"for-actualización de '{nombre}'")
                    cuartetos.extend(c)
                    if tipo_expr != "desconocido" and not _compatibles_asignacion(tipo_var, tipo_expr):
                        errores.append(f"ERROR SEMÁNTICO: no se puede asignar '{tipo_expr}' a variable '{nombre}' de tipo '{tipo_var}'")
                    cuartetos.append(("=", ref or expr_txt, "", nombre))

            cuartetos.append(("FOR", "", "", ""))
            i += 1
            continue

        errores.append(f"ERROR SEMÁNTICO: sentencia no reconocida -> {' '.join(lex)}")
        i += 1

    return {
        "tabla_simbolos": tablaSimbolos,
        "tabla_funciones": tablaFunciones,
        "cuartetos": cuartetos,
        "errores": errores
    }

def _codigo_visual_operacion(op):
    mapa = {
        'DECL': 5,
        'READ': 25,
        'WRITE': 35,
        'RETURN': 151,
        '=': 150,
        'FOR': 300,
        'FOR_COND': 301,
        '+': 401,
        '-': 402,
        '*': 403,
        '/': 404,
        '%': 405,
        '^': 406,
        '<': 410,
        '>': 411,
        '<=': 412,
        '>=': 413,
        '==': 414,
        '!=': 415,
        '&&': 416,
        '||': 417,
    }
    return mapa.get(op, op)


def _normalizar_visual(valor):
    if valor in ('', [], (), {}):
        return None
    return valor


def imprimir_cuartetos(cuartetos):
    for i, (op, a1, a2, r) in enumerate(cuartetos, start=1):
        op_v = _codigo_visual_operacion(op)
        a1_v = _normalizar_visual(a1)
        a2_v = _normalizar_visual(a2)
        r_v = _normalizar_visual(r)
        print(f"{i}: ({op_v!r}, {a1_v!r}, {a2_v!r}, {r_v!r})")


def ejecutar_analisis(codigo):
    tokens, errores_lexicos = lexico(codigo)
    print('TOKENS:', tokens)
    print('ERRORES LÉXICOS:', errores_lexicos)

    if errores_lexicos:
        print('No se analiza sintáctica ni semánticamente por errores léxicos.')
        return

    resultado_sintactico = parsear(tokens)
    print('RESULTADO SINTÁCTICO:', resultado_sintactico)

    if resultado_sintactico != 'VÁLIDO':
        return

    sem = analizar_semantico(codigo)

    if sem['errores']:
        print('\nERRORES SEMÁNTICOS:')
        for e in sem['errores']:
            print('-', e)
        return

    print('\nVálido')
    imprimir_cuartetos(sem['cuartetos'])


if __name__ == '__main__':
    codigo_prueba = '''int a;
int b;
int c;
int d;
int e;
float f;
f = (a + b) * c - d / e;
'''
    ejecutar_analisis(codigo_prueba)
