# Constants
DIGITS = '0123456789'

# Tokens
TK_INT = "INT"
TK_FLOAT = "FLOAT"
TK_OTHER = "OTHER"

TK_KEYWORDS = "KEYWORDS"
KEYWORD_LIST = ["int", "float", "bool", "if", "else", "then", "do", "while", "for", "and", "or", "function"]

TK_SEPARATORS = "SEPARATOR"
SEPARATOR_LIST = ["'", "(", ")", "{", "}", "[", "]", ",", ".", ":", ";", " "]

TK_OPERATORS = "OPERATOR"
OPERATOR_LIST = ["+", "-", "*", "/", "<", ">", "=", "%", "^" ]

TK_IDENTIFIER = "IDENTIFIER"
TK_COMMENT = "COMMENT"

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


# Lexer

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in '\t':
                self.advance()
            elif self.current_char in '\n':
                self.advance()
            elif self.current_char == " ":
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in OPERATOR_LIST:
                tokens.append(self.make_operator())
            elif self.current_char in SEPARATOR_LIST:
                tokens.append(self.make_separator())
            elif self.current_char.isalpha():
                tokens.append(self.make_keyword())
            elif self.current_char == "!":
                tokens.append(self.make_comment())
            else:
                tokens.append(self.make_other())
                self.advance()

        return tokens, None

    #PROJECT 2

        # Expression Function:
            # expression = number (aka identifier aka terminal)
            # expression = terminal AND operator AND  terminal
            # expression = separator AND expression AND separator

            # removing left-recursion: 
                # if expression = expression AND terminal
                    # do Expression Prime function
                    # do Terminal Function
                    # if not end of stack, receieve error-message
        
        # Expression Prime function
            # if token is + or -:
                # do lexer function AND terminal function AND expression prime func again

        # Terminal Function
            # if token is identifier:
                # do lexer function (to verify it's an identifier. IF anything else: error)

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TK_INT, int(num_str))
        elif dot_count == 1:
            return Token(TK_FLOAT, float(num_str))
        elif dot_count > 1:
            return Token(TK_OTHER, str(num_str))

    def make_operator(self):
        op_str = ''
        while self.current_char is not None and self.current_char in OPERATOR_LIST:
            op_str += self.current_char
            self.advance()
        return Token(TK_OPERATORS, op_str)

    def make_separator(self):
        sep_counter = 0
        sep_str = ''
        while self.current_char is not None and self.current_char in SEPARATOR_LIST and sep_counter < 1:
            sep_str += self.current_char
            sep_counter += 1
            self.advance()
            if self.current_char == ' ':
                break
        return Token(TK_SEPARATORS, sep_str)

    def make_keyword(self):
        key_str = ''
        while self.current_char != ' ' and self.current_char not in SEPARATOR_LIST and self.current_char not in OPERATOR_LIST:
            key_str += self.current_char
            self.advance()
            if self.current_char is None:
                break
        if key_str in KEYWORD_LIST:
            return Token(TK_KEYWORDS, key_str)
        else:
            return Token(TK_IDENTIFIER, key_str)

    def make_other(self):
        other_str = ''
        while self.current_char is not None:
            other_str += self.current_char
            self.advance()
        return Token(TK_OTHER, other_str)

    def make_comment(self):
        comment_str = ''
        while self.current_char is not None:
            comment_str += self.current_char
            self.advance()
        return Token(TK_COMMENT, comment_str)

# Run
# while (fahr < upper) { a = 23.00 }
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()

    return tokens, error
