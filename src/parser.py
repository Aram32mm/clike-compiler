#!/usr/bin/env python3
"""
CParser: A PLY-based parser for a C-like language.
Generates an Abstract Syntax Tree (AST) from source code.
"""

import pprint
import ply.yacc as yacc
from src.lexer import CLexer

# ============================================
# Abstract Syntax Tree (AST) Node Formats
# ============================================
# ('FUNCTION', name, parameters, statements)
# ('PARAM', type, name)
# ('VAR_DECL', type, name)
# ('VAR_DECL_INIT', type, name, expression)
# ('ARRAY_DECL', type, name, size)
# ('ASSIGN', name, expression)
# ('ARRAY_ASSIGN', name, index_expr, value_expr)
# ('RETURN', expression)
# ('IF', condition, then_stmt)
# ('IF_ELSE', condition, then_stmt, else_stmt)
# ('WHILE', condition, body_stmt)
# ('FOR', init_stmt, condition_expr, update_stmt, body_stmt)
# ('BLOCK', list_of_statements)
# ('CALL', function_name, list_of_argument_exprs)
# ('ARRAY_ACCESS', array_name, index_expr)
# ('BINOP', operator, left_expr, right_expr)
# ('UNARYOP', operator, expression)
# ('INTEGER', value) / ('FLOAT', value) / ('CHAR', value) / ('STRING', value)
# ('VARIABLE', name)
# ('EMPTY',)


class CParser:
    start = 'program'

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.lexer = CLexer()
        self.tokens = self.lexer.tokens
        self.lexer.build()
        self.parser = yacc.yacc(module=self, debug=verbose)

    def parse(self, text):
        if self.verbose:
            print("\n📥 Parsing input:")
            print(text)
        result = self.parser.parse(text, lexer=self.lexer.lexer)
        if self.verbose:
            print("\n✅ Parse result:")
            pprint.pprint(result)
        return result

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NEQ'),
        ('left', 'LT', 'LE', 'GT', 'GE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MUL', 'DIV', 'MOD'),
        ('right', 'UMINUS'),
    )

    def p_program(self, p):
        '''program : function
                   | program function'''
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]
        if self.verbose:
            print("Reduced: program →", p[0])

    def p_function(self, p):
        'function : TYPE IDENTIFIER LPAREN parameters RPAREN LBRACE statements RBRACE'
        p[0] = ('FUNCTION', p[2], p[1], p[4], p[7])
        if self.verbose:
            print(f"Reduced: function → {p[1]} {p[2]}({p[4]}) {{...}}")

    def p_parameters(self, p):
        '''parameters : parameter
                      | parameters COMMA parameter
                      | empty'''
        if len(p) == 2 and p[1] is not None:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = []
        if self.verbose:
            print("Reduced: parameters →", p[0])

    def p_parameter(self, p):
        'parameter : TYPE IDENTIFIER'
        p[0] = ('PARAM', p[1], p[2])
        if self.verbose:
            print("Reduced: parameter →", p[0])

    def p_empty(self, p):
        'empty :'
        p[0] = None

    def p_statements(self, p):
        '''statements : statement
                      | statements statement
                      | empty'''
        if len(p) == 2:
            if p[1] is None:
                p[0] = []
            else:
                p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
        if self.verbose:
            print("Reduced: statements →", p[0])

    def p_statement(self, p):
        '''statement : variable_declaration
                     | assignment_statement
                     | return_statement
                     | if_statement
                     | while_statement
                     | break_statement
                     | continue_statement
                     | for_statement
                     | block_statement
                     | SEMICOLON'''
        if p.slice[1].type == 'SEMICOLON':
            p[0] = ('EMPTY',)
        else:
            p[0] = p[1]
        if self.verbose:
            print("Reduced: statement →", p[0])

    def p_block_statement(self, p):
        'block_statement : LBRACE statements RBRACE'
        p[0] = ('BLOCK', p[2])
        if self.verbose:
            print("Reduced: block_statement →", p[0])

    def p_for_statement(self, p):
        'for_statement : FOR LPAREN optional_expression SEMICOLON optional_expression SEMICOLON optional_expression RPAREN statement'
        p[0] = ('FOR', p[3], p[5], p[7], p[9])
        if self.verbose:
            print("Reduced: for_statement →", p[0])

    def p_variable_declaration(self, p):
        '''variable_declaration : TYPE IDENTIFIER SEMICOLON
                                 | TYPE MUL IDENTIFIER SEMICOLON
                                 | TYPE IDENTIFIER ASSIGN expression SEMICOLON
                                 | TYPE MUL IDENTIFIER ASSIGN expression SEMICOLON
                                 | TYPE IDENTIFIER LBRACKET INTEGER RBRACKET SEMICOLON'''
        if len(p) == 4:
            p[0] = ('VAR_DECL', p[1], p[2])
        elif len(p) == 5 and p.slice[2].type == 'MUL':
            p[0] = ('VAR_DECL', p[1] + '*', p[3]) 
        elif len(p) == 6:
            p[0] = ('VAR_DECL_INIT', p[1], p[2], p[4])
        elif len(p) == 7 and p.slice[2].type == 'MUL':
            p[0] = ('VAR_DECL_INIT', p[1] + '*', p[3], p[5])
        elif len(p) == 7:
            p[0] = ('ARRAY_DECL', p[1], p[2], p[4])
        if self.verbose:
            print("Reduced: variable_declaration →", p[0])

    def p_assignment_statement(self, p):
        'assignment_statement : IDENTIFIER ASSIGN expression SEMICOLON'
        p[0] = ('ASSIGN', p[1], p[3])
        if self.verbose:
            print("Reduced: assignment_statement →", p[0])
    
    def p_array_assignment_statement(self, p):
        'assignment_statement : IDENTIFIER LBRACKET expression RBRACKET ASSIGN expression SEMICOLON'
        p[0] = ('ARRAY_ASSIGN', p[1], p[3], p[6])

    def p_return_statement(self, p):
        'return_statement : RETURN expression SEMICOLON'
        p[0] = ('RETURN', p[2])
        if self.verbose:
            print("Reduced: return_statement →", p[0])

    def p_return_void(self, p):
        'return_statement : RETURN SEMICOLON'
        p[0] = ('RETURN', None)
        if self.verbose:
            print("Reduced: return_statement → ('RETURN', None)")

    def p_if_statement(self, p):
        '''if_statement : IF LPAREN expression RPAREN statement
                        | IF LPAREN expression RPAREN statement ELSE statement'''
        if len(p) == 6:
            p[0] = ('IF', p[3], p[5])
        else:
            p[0] = ('IF_ELSE', p[3], p[5], p[7])
        if self.verbose:
            print("Reduced: if_statement →", p[0])

    def p_while_statement(self, p):
        'while_statement : WHILE LPAREN expression RPAREN statement'
        p[0] = ('WHILE', p[3], p[5])
        if self.verbose:
            print("Reduced: while_statement →", p[0])

    def p_break_statement(self, p):
        'break_statement : BREAK SEMICOLON'
        p[0] = ('BREAK',)
        if self.verbose:
            print("Reduced: break_statement → BREAK")

    def p_continue_statement(self, p):
        'continue_statement : CONTINUE SEMICOLON'
        p[0] = ('CONTINUE',)
        if self.verbose:
            print("Reduced: continue_statement → CONTINUE")

    def p_argument_list(self, p):
        '''argument_list : expression
                         | argument_list COMMA expression
                         | empty'''
        if len(p) == 2 and p[1] is not None:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = []
        if self.verbose:
            print("Reduced: argument_list →", p[0])

    def p_expression(self, p):
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression MUL expression
                      | expression DIV expression
                      | expression MOD expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression LT expression
                      | expression LE expression
                      | expression GT expression
                      | expression GE expression
                      | expression AND expression
                      | expression OR expression
                      | IDENTIFIER ASSIGN expression
                      | IDENTIFIER LBRACKET expression RBRACKET
                      | IDENTIFIER LPAREN argument_list RPAREN
                      | LPAREN expression RPAREN
                      | MINUS expression %prec UMINUS
                      | IDENTIFIER
                      | INTEGER
                      | FLOAT
                      | CHAR
                      | STRING'''
        token_type = p.slice[1].type
        if len(p) == 2:
            if token_type == 'INTEGER':
                p[0] = ('INTEGER', p[1])
            elif token_type == 'FLOAT':
                p[0] = ('FLOAT', p[1])
            elif token_type == 'CHAR':
                p[0] = ('CHAR', p[1])
            elif token_type == 'STRING':
                p[0] = ('STRING', p[1])
            else:
                p[0] = ('VARIABLE', p[1])
        elif len(p) == 3:
            p[0] = ('UNARYOP', '-', p[2])
        elif len(p) == 4 and p[1] == '(':
            p[0] = p[2]
        elif len(p) == 4 and p.slice[2].type == 'ASSIGN':
            p[0] = ('ASSIGN', p[1], p[3])
        elif len(p) == 5 and p.slice[2].type == 'LPAREN':
            p[0] = ('CALL', p[1], p[3])
        elif len(p) == 5 and p.slice[2].type == 'LBRACKET':
            p[0] = ('ARRAY_ACCESS', p[1], p[3])
        else:
            p[0] = ('BINOP', p[2], p[1], p[3])
        if self.verbose:
            print("Reduced: expression →", p[0])
    
    def p_optional_expression(self, p):
        '''optional_expression : expression
                               | empty'''
        p[0] = p[1] if p[1] is not None else ('EMPTY',)

    def p_error(self, p):
        if p:
            print(f"❌ Syntax error at token '{p.type}' (value: '{p.value}') at line {p.lineno}, column {p.lexpos}")
            raise SyntaxError(f"Syntax error at token '{p.type}' (value: '{p.value}') at line {p.lineno}, column {p.lexpos}")

        else:
            print("❌ Syntax error at EOF")
            raise SyntaxError("Syntax error at EOF")