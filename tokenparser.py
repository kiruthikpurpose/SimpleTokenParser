import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})"

def tokenize(text):
    token_specification = [
        ('NUMBER', r'\d+(\.\d*)?'),
        ('WORD',   r'\b\w+\b'),
        ('PUNCT',  r'[^\w\s]'),
        ('SKIP',   r'\s+'),
    ]
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    get_token = re.compile(tok_regex).match

    tokens = []
    pos = 0

    while pos < len(text):
        match = get_token(text, pos)
        if match:
            typ = match.lastgroup
            if typ != 'SKIP':
                val = match.group(typ)
                tokens.append(Token(typ, val))
            pos = match.end()
        else:
            raise RuntimeError(f'Unexpected character: {text[pos]}')
    return tokens

def main():
    text = input("Enter text to be tokenized: ")
    tokens = tokenize(text)
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()
