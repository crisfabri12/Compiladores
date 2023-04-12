import re

regex_patterns = [
    ("STRING", r'"(?:\\.|[^"])*"'),
    ("INTEGER", r"0|[1-9][0-9]*"),
    ("KEYWORD", r"\b(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield|int|bool|float)\b"),
    ("DELIMITER", r"\(|\)|\[|\]|\{|\}|\,"),
    ("OPERATOR", r"\+|\-|\*|\/\/|\%|<|>|<=|>=|==|!=|=|and|or|\:"),
    ('ID', r'[a-zA-Z]([a-zA-Z0-9_]*[a-zA-Z0-9])?'),
    ("NEWLINE", r"\n"),
    ("WHITESPACE", r"\s+")
]

regex_combined = "|".join("(?P<%s>%s)" % pair for pair in regex_patterns)
token_regex = re.compile(regex_combined)
def tokenize(code):
    """
    Tokeniza un código fuente y devuelve una lista de tokens.
    """
    tokens = []
    index = 0
    line = 1
    while index < len(code):
        # Obtener el siguiente carácter sin mover el puntero
        c = peekchar(code, index)
        
        if c is None:
            break
        
        # Si es un espacio en blanco, mover el puntero y continuar
        if c.isspace():
            getchar(code, index)
            if c == "\n":
                line += 1
            
            
        # Obtener el token actual
        match = token_regex.match(code, index)
        if match:
            token_type = match.lastgroup
            token_value = match.group(token_type)
            if token_type == "STRING":
                # Eliminar las comillas dobles que rodean el valor del string
                token_value = token_value[1:-1]
            elif token_type == "INTEGER":
                # Convertir el valor del entero en un entero de Python
                token_value = int(token_value)
            elif token_type == "KEYWORD":
                # Clasificar la palabra clave como "KEY"
                token_type = "KEY"
            elif token_type == "DELIMITER":
                # Clasificar todos los operadores y delimitadores como "DELIM"
                
                if token_value == '(':
                    token_type = "OPEN_PAR"
                elif token_value == ')':
                    token_type = "CLO_PAR" 
                else:    
                    token_type = "DELIM"       
            elif token_type == "OPERATOR":
                token_type = "OP"
            elif token_type == "ID":
                # Clasificar el ID como "ID"
                token_type = "ID"
            
            
            # Agregar el token a la lista
            token = (token_type, token_value, line, index)
            tokens.append(token)
            
            # Mover el puntero
            index += len(str(token_value)) if isinstance(token_value, str) else 1
        
        else:
            print(f"Error de sintaxis en la línea {line}, espacio {index}")
            index += 1
        
    return tokens

    
def getchar(code, index):
    """
    Devuelve el carácter en el índice dado del código fuente y la posición del siguiente carácter.
    Si el índice está fuera de los límites del código fuente, devuelve None.
    """
    

    if index < 0 or index >= len(code):
        return None
    else:
        return code[index], index + 1


def peekchar(code, index):
    """
    Devuelve el carácter en el índice dado del código fuente sin mover el puntero de posición.
    Si el índice está fuera de los límites del código fuente, devuelve None.
    """
    if index < 0 or index >= len(code):
        return None
    else:
        return code[index]

def main():
    filename = "texto.txt"
    with open(filename, 'r') as file:
        input_str = file.read()

    input_str = re.sub(r'#.*', '', input_str)

    tokens = tokenize(input_str)
    espacio = 0
    for token in tokens:
        token_type, token_value, line, index = token
        if token_type == "NEWLINE":
            print(f"DEBUG SCAN - {token_type} [ ]     found at ({line}:{index}) ")
        elif token_type == "WHITESPACE":
            espacio += 1
        else:
            print(f"DEBUG SCAN - {token_type}  [ {token_value} ]     found at ({line}:{index})")

if __name__ == '__main__':
    main()