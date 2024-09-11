import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})"

class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.tokens = self.tokenize()

    def tokenize(self):
        token_specification = [
            ('NUMBER',    r'\d+(\.\d*)?'),
            ('WORD',      r'\b\w+\b'),
            ('OP',        r'[+\-*/]'),
            ('PAREN',     r'[()]'),
            ('STRING',    r'\".*?\"|\'.*?\''),
            ('PUNCT',     r'[^\w\s]'),
            ('SKIP',      r'\s+'),
            ('MISMATCH',  r'.'),
        ]
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        get_token = re.compile(tok_regex).match

        tokens = []
        pos = 0

        while pos < len(self.text):
            match = get_token(self.text, pos)
            if match:
                typ = match.lastgroup
                val = match.group(typ)
                if typ == 'MISMATCH':
                    raise RuntimeError(f'Unexpected character: {val}')
                elif typ != 'SKIP':
                    tokens.append(Token(typ, val))
                pos = match.end()
            else:
                raise RuntimeError(f'Error tokenizing at position {pos}')
        return tokens

    def count_token_type(self, token_type):
        return sum(1 for token in self.tokens if token.type == token_type)

    def extract_token_values(self, token_type):
        return [token.value for token in self.tokens if token.type == token_type]

    def categorize_tokens(self):
        categories = {'NUMBERS': [], 'WORDS': [], 'OPERATORS': [], 'PARENTHESIS': [], 'STRINGS': [], 'PUNCTUATION': []}
        for token in self.tokens:
            if token.type == 'NUMBER':
                categories['NUMBERS'].append(token.value)
            elif token.type == 'WORD':
                categories['WORDS'].append(token.value)
            elif token.type == 'OP':
                categories['OPERATORS'].append(token.value)
            elif token.type == 'PAREN':
                categories['PARENTHESIS'].append(token.value)
            elif token.type == 'STRING':
                categories['STRINGS'].append(token.value)
            elif token.type == 'PUNCT':
                categories['PUNCTUATION'].append(token.value)
        return categories

    def display_tokens(self):
        for token in self.tokens:
            print(token)

def main():
    text = input("Enter text to be tokenized: ")
    tokenizer = Tokenizer(text)
    
    print("\nTokens:")
    tokenizer.display_tokens()
    
    print("\nCategorized Tokens:")
    categories = tokenizer.categorize_tokens()
    for category, tokens in categories.items():
        print(f"{category}: {tokens}")

    print("\nToken Count by Type:")
    for token_type in ['NUMBER', 'WORD', 'OP', 'PAREN', 'STRING', 'PUNCT']:
        print(f"{token_type}: {tokenizer.count_token_type(token_type)}")

if __name__ == "__main__":
    main()
