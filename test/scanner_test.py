import sys
import os
src_path = os.path.dirname(__file__)
src_path += os.sep + ".." + os.sep + "src"
sys.path.insert(0, src_path)
from komparse import (Grammar, Scanner, StringStream)


def test_sql():
    code = """
    -- Search for user 'drbolle'
    SELECT * FROM users where name="Dr. #"Bolle#" is our ###"One#"";
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


def test_nested_comments():

    g = Grammar(case_sensitive=False) \
        .add_comment("--", "\n") \
        .add_comment("(*", "*)", nestable=True) \
        .add_string('"', '"', escape='#', name="DOUBLE_QUOTED") \
        .add_keyword("SELECT") \
        .add_keyword("FROM") \
        .add_keyword("WHERE") \
        .add_token("ASTERISK", r"\*") \
        .add_token("ASSIGN", "=") \
        .add_token("SEMICOLON", ";") \
        .add_token("ID", "[a-zA-Z_][a-zA-Z_0-9]*") \

    code = """
    (* Search (* for *)user 'drbolle' *)
    SELECT * FROM users where name="Dr. #"Bolle#" is our ###"One#"";
    """
    print(code)
    print()

    scanner = Scanner(StringStream(code), g)

    while scanner.has_next():
        token = scanner.advance()
        print(token)


if __name__ == "__main__":
    #test_sql()
    test_nested_comments()



