import sys
sys.path.append("../src")
from komparse import *

code = """
SELECT * FROM select where name='drbolle';
"""

print(code)
print()

sql = Grammar(case_sensitive = False)\
    .add_comment("(*", "*)")\
    .add_comment("--", "\n")\
    .add_keyword("SELECT")\
    .add_keyword("FROM")\
    .add_keyword("WHERE")\
    .add_token("ASTERISK", r"\*")\
    .add_token("ASSIGN", "=")\
    .add_token("SEMICOLON", ";")\
    .add_token("ID", "[a-zA-Z_][a-zA-Z_0-9]*")\
    .add_token("STRING", "'[^']*'")

sql.rule('select',
         Sequence(
            TokenType('SELECT'),
            Rule('field_list', 'fields'),
            TokenType('FROM'),
            TokenType('ID', 'table'),
            Optional(Rule('where_clause', 'where')),
            TokenType('SEMICOLON')),
        is_root=True)
@sql.ast_transform('select')
def select(ast):
    ret = Ast('select_stmt')
    ret.add_children_by_id(ast, 'fields')
    ret.add_children_by_id(ast, 'table')
    ret.add_children_by_id(ast, 'where')
    return ret

sql.rule('field_list', TokenType('ASTERISK'))
@sql.ast_transform('field_list')
def field_list(ast):
    children = ast.get_children()
    if len(children) == 1 and children[0].name == 'ASTERISK':
        return Ast("all_fields")
    else:
        return ast

sql.rule('where_clause',
         Sequence(
            TokenType('WHERE'),
            Rule('conditions')))
@sql.ast_transform('where_clause')
def where_clause(ast):
    return ast.find_children_by_name('conditions')[0]
    
sql.rule('conditions',
         Sequence(
            TokenType('ID', 'field'),
            TokenType('ASSIGN'),
            OneOf(
                TokenType('ID', 'expr'),
                TokenType('STRING', 'expr'))))
@sql.ast_transform('conditions')
def condition(ast):
    ret = Ast('conditions')
    cond = Ast('condition')
    ret.add_child(cond)
    cond.add_children_by_id(ast, 'field')
    cond.add_children_by_id(ast, 'expr')
    return ret


sql_parser = Parser(sql)

ast = sql_parser.parse(code)
if ast:
    print(ast.to_xml())
else:
    print(sql_parser.error())



