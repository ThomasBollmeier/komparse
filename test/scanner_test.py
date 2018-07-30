import sys
sys.path.insert(0, "../src")
from komparse import (Grammar, Scanner, StringStream)

code = """
-- Search for user 'drbolle'
SELECT * FROM users where name="Dr. #"Bolle#"";
"""

print(code)
print()

g = Grammar(case_sensitive = False)\
    .add_comment("--", "\n")\
    .add_string('"', '"', escape='#', name="DOUBLE_QUOTED")\
    .add_keyword("SELECT")\
    .add_keyword("FROM")\
    .add_keyword("WHERE")\
    .add_token("ASTERISK", r"\*")\
    .add_token("ASSIGN", "=")\
    .add_token("SEMICOLON", ";")\
    .add_token("ID", "[a-zA-Z_][a-zA-Z_0-9]*")\

scanner = Scanner(StringStream(code), g)

while scanner.has_next():
    token = scanner.advance()
    print(token)



