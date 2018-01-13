import sys
sys.path.append("../src")
from komparse import (Grammar, Scanner)

code = """
SELECT * FROM users where name="drbolle";
"""

print(code)
print()

g = Grammar(case_sensitive = False)\
    .add_comment("(*", "*)")\
    .add_comment("--", "\n")\
    .add_keyword("SELECT")\
    .add_keyword("FROM")\
    .add_keyword("WHERE")\
    .add_token("ASTERISK", r"\*")\
    .add_token("ASSIGN", "=")\
    .add_token("SEMICOLON", ";")\
    .add_token("ID", "[a-zA-Z_][a-zA-Z_0-9]*")\
    .add_token("STRING", '"[^"]*"')

token_stream = Scanner(g).find_tokens(code)

while token_stream.has_next():
    print(token_stream.advance())





