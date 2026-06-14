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
codigo = '''_c456y="_$%&123" '''
tokens, errores = lexico(codigo)

print(tokens)
print(errores)
