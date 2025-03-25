#!/usr/bin/env python3
import ply.yacc as yacc
from src.lexer import CLexer

class CParser:
    def __init__(self):
        self.lexer = CLexer()
        self.tokens = self.lexer.tokens
        self.lexer.build()
        self.parser = yacc.yacc(module=self)
        
    def parse(self, text):
        return self.parser.parse(text, lexer=self.lexer.lexer)
    
    # Operator precedence rules (lowest to highest)
    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MUL', 'DIV'),
        ('right', 'UMINUS'),   # Precedence for unary minus
    )

    # Grammar rules
    def p_program(self, p):
        'program : function'
        p[0] = p[1]
    
    def p_function(self, p):
        'function : TYPE IDENTIFIER LPAREN RPAREN LBRACE statements RBRACE'
        p[0] = ('FUNCTION', p[2], p[6])
    
    def p_statements(self, p):
        '''statements : statement
                      | statements statement'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
    
    def p_statement(self, p):
        '''statement : variable_declaration
                     | assignment_statement
                     | return_statement'''
        p[0] = p[1]
    
    def p_variable_declaration(self, p):
        'variable_declaration : TYPE IDENTIFIER SEMICOLON'
        p[0] = ('VAR_DECL', p[1], p[2])
    
    def p_assignment_statement(self, p):
        'assignment_statement : IDENTIFIER ASSIGN expression SEMICOLON'
        p[0] = ('ASSIGN', p[1], p[3])
    
    def p_return_statement(self, p):
        'return_statement : RETURN expression SEMICOLON'
        p[0] = ('RETURN', p[2])
    
    def p_expression(self, p):
        '''expression : expression PLUS term
                      | expression MINUS term
                      | term'''
        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '+':
            p[0] = ('BINOP', '+', p[1], p[3])
        elif p[2] == '-':
            p[0] = ('BINOP', '-', p[1], p[3])
    
    def p_term(self, p):
        '''term : term MUL factor
                | term DIV factor
                | factor'''
        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '*':
            p[0] = ('BINOP', '*', p[1], p[3])
        elif p[2] == '/':
            p[0] = ('BINOP', '/', p[1], p[3])
    
    def p_factor(self, p):
        '''factor : INTEGER
                | IDENTIFIER
                | LPAREN expression RPAREN
                | MINUS factor %prec UMINUS'''
        if len(p) == 2:
            if isinstance(p[1], int):
                p[0] = ('INTEGER', p[1])
            else:
                p[0] = ('VARIABLE', p[1])
        elif p[1] == '-':
            p[0] = ('UNARYOP', '-', p[2])
        else:
            p[0] = p[2]

    
    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}', line {p.lineno}, position {p.lexpos}")
        else:
            print("Syntax error at EOF")