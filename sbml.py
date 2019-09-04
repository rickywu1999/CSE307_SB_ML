import time
functions = {}
stack = []
variables = {}

def copy_variables(copy):
    variables.clear()
    for x in copy.keys():
        variables[x] = copy[x]

class SemanticException(Exception):
    pass

class SyntaxException(Exception):
    pass

class Node:
    def __init__(self):
        print("init node")
    def evaluate(self):
        return 0
    def execute(self):
        return 0
    
# -----------------
# EXPRESSIONS NODES
# -----------------

class NumberNode(Node):
    def __init__(self, v1, v2):
        if (isinstance(v2,str)):
            if('.' in v2 or 'e' in v2 or 'E' in v2):
                self.value = float(v2)
            else:
                self.value = int(v2)
        else:
            x = v2.evaluate()
            if (isinstance(x,(int,float))):
                if (v1 == '+'):
                    self.value = x
                else:
                    self.value = -x
            else:
                raise SemanticException
    def evaluate(self):
        return self.value

class StringNode(Node):
    def __init__(self, v):
        self.value = v[1:-1]
    def evaluate(self):
        return self.value

class BooleanNode(Node):
    def __init__(self, v):
        if (v == 'True'):
            self.value = True
        else:
            self.value = False
    def evaluate(self):
        return self.value

class VariableNode(Node):
    def __init__(self, v):
        self.value = v
    def evaluate(self):
        if self.value in variables:
           return variables[self.value]
        else:
            raise SemanticException
    def getname(self):
        return self.value

class PrintNode(Node):
    def __init__(self, v):
        self.value = v
    def evaluate(self):
        x = self.value.evaluate()
        if (x is None):
            raise SemanticException()
        elif (isinstance(self.value,StringNode)):
            print(x)
        elif (isinstance(x,str)):
            print('\''+x+'\'')
        else :
            print(x)

class NotNode(Node):
    def __init__(self, v1):
        self.v1 = v1
    def evaluate(self):
        x = self.v1.evaluate()
        if (isinstance(x,bool)):
            return not x
        else:
            raise SemanticException

class TupleNode(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    def evaluate(self):
        x = self.v1.evaluate()
        y = self.v2.evaluate()
        return (x,y)

class TupleNodeAdd(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    def evaluate(self):
        y = self.v2.evaluate()
        return self.v1.evaluate() + (y,)

class TupleIndexNode(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    def evaluate(self):
        x = self.v1.evaluate()
        y = self.v2.evaluate()
        if (isinstance(x,(int)) and isinstance(y,tuple)):
            if (x > 0 and x <= len(y)):
                return y[x-1]
            else:
                raise SemanticException
        else:
            raise SemanticException

class EmptyTupleNode(Node):		
    def __init__(self):		
        pass				
    def evaluate(self):		
        return ()

class ListNode(Node):
    def __init__(self, v1):
        self.v1 = v1
    def evaluate(self):
        x = self.v1.evaluate()
        return [x]
    def getname(self):
        if not isinstance(self.v1,VariableNode):
            return SemanticError
        else:
            return [self.v1.getname()]

class ListNodeAdd(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    def evaluate(self):
        y = self.v2.evaluate()
        return self.v1.evaluate() + [y]
    def getname(self):
        if not isinstance(self.v2,VariableNode):
            return SemanticError
        else:
            return self.v1.getname() + [self.v2.getname()]

class EmptyListNode(Node):		
    def __init__(self):		
        pass			
    def evaluate(self):		
        return []

class ListIndexNode(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    def evaluate(self):
        x = self.v1.evaluate()
        y = self.v2.evaluate()
        if (isinstance(x,(list,str)) and isinstance(y,list)):
            if (len(y) == 1):
                y = y[0];
                if (y < len(x)):
                    return x[y]
                else:
                    return SemanticException
            else:
                raise SyntaxException
        else:
            raise SemanticException

class BopNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op
    def evaluate(self):
        x = self.v1.evaluate()
        y = self.v2.evaluate()
            
        if (self.op == '::'):
            if (isinstance(y,list)):
                return [x] + y
            else:
                raise SemanticException
        elif (self.op == 'in'):
            if (isinstance(x,str) and isinstance(y,str)):
                return x in y
            elif (isinstance(y,list)):
                return x in y
            else:
                raise SemanticException
        elif (isinstance(x,str) and isinstance(y,str)):
            if (self.op == '+'):
                return x + y
            elif (self.op == '>'):
                return x > y
            elif (self.op == '>='):
                return x >= y
            elif (self.op == '<'):
                return x < y
            elif (self.op == '<='):
                return x <= y
            elif (self.op == '=='):
                return x == y
            elif (self.op == '<>'):
                return x != y
            else:
                raise SemanticException
        elif (isinstance(x,list) and isinstance(y,list)):
            if (self.op == '+'):
                return x + y
            else:
                raise SemanticException
        elif (isinstance(x,bool) and isinstance(y,bool)):
            if (self.op == 'andalso'):
                return x and y
            elif (self.op == 'orelse'):
                return x or y
            else:
                raise SemanticException
        elif (isinstance(x,(int,float)) and isinstance(y,(int,float))):
            if (self.op == '+'):
                return x + y
            elif (self.op == '-'):
                return x - y
            elif (self.op == '*'):
                return x * y
            elif (self.op == '/'):
                if (y == 0):
                    raise SemanticError
                else:
                    return x / y
            elif (self.op == '**'):
                return x ** y
            elif (self.op == 'div'):
                if (isinstance(x,float) or isinstance(y,float)):
                    raise SemanticException
                else:
                    if (y == 0):
                        raise SemanticException
                    else:
                        return x // y
            elif (self.op == 'mod'):
                if (isinstance(x,float) or isinstance(y,float)):
                    raise SemanticException
                else:
                    if (y == 0):
                        raise SemanticException
                    else:
                        return x % y
            elif (self.op == '>'):
                return x > y
            elif (self.op == '>='):
                return x >= y
            elif (self.op == '<'):
                return x < y
            elif (self.op == '<='):
                return x <= y
            elif (self.op == '=='):
                return x == y
            elif (self.op == '<>'):
                return x != y
            else:
                raise SemanticException
        else:
            raise SemanticException

#-----------------------------------------------
#-----------------------------------------------

# ----------------
# STATEMENTS NODES
# ----------------

class BlockNode(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    def evaluate(self):
        if self.v1 is not 0:
            self.v1.evaluate()
        if self.v2 is not 0:
            self.v2.evaluate()

class CodeNode(Node):
    def __init__(self, v1):
        self.v1 = v1
    def evaluate(self):
        self.v1.evaluate()
        
class AssignmentNode(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    def evaluate(self):
        x = self.v2.evaluate()
        variables[self.v1.getname()] = x

class ArrayAssignmentNode(Node):
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
    def evaluate(self):
        if not isinstance(self.v1,VariableNode):
            raise SemanticException
        name = self.v1.getname()
        value = self.v1.evaluate()
        if not isinstance(value,(str,list)):
            raise SemanticException
        indexList = self.v2.evaluate()
        if len(indexList) is not 1:
            raise SemanticException
        index = indexList[0]
        x = self.v3.evaluate()
        variables[name][index] = x

class IfNode(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    def evaluate(self):
        x = self.v1.evaluate()
        if isinstance(x,bool):
            if x is True:
                if self.v2 is not 0:
                    self.v2.evaluate()
        else:
            return SemanticException

class IfElseNode(Node):
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
    def evaluate(self):
        x = self.v1.evaluate()
        if isinstance(x,bool):
            if x is True:
                if self.v2 is not 0:
                    self.v2.evaluate()
            else:
                if self.v3 is not 0:
                    self.v3.evaluate()
        else:
            return SemanticException

class WhileNode(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    def evaluate(self):
        x = self.v1.evaluate()
        if isinstance(x,bool):
            while x is True:
                if self.v2 is not 0:
                    self.v2.evaluate()
                
                x = self.v1.evaluate()
                if not isinstance(x, bool):
                    raise SemanticException
        else:
            return SemanticException

# ------------
# FUNCTIONS
# ------------

class AllNode(Node):
    def __init__(self,functions,main):
        self.functions = functions
        self.main = main
    def evaluate(self):
        self.functions.evaluate()
        self.main.evaluate()

class FunctionListNode(Node):
    def __init__(self,flist,fun):
        self.flist = flist
        self.fun = fun
    def evaluate(self):
        self.flist.evaluate()
        self.fun.evaluate()
        
class FunctionNode(Node):
    def __init__(self,name,arguments,block,expr):
        self.name = name.getname()
        if arguments is not 0:
            self.arguments = arguments.getname()
        else:
            self.arguments = 0
        self.block = block
        self.expr = expr
    def evaluate(self):
        if self.name in functions:
            return SemanticException
        else:
            functions[self.name] = self
    def getargs(self):
        return self.arguments
    def getblock(self):
        return self.block
    def getexpr(self):
        return self.expr

class CallFunctionNode(Node):
    def __init__(self,name,arguments):
        self.name = name.getname()
        self.arguments = arguments
    def evaluate(self):
        if self.name not in functions:
            return SemanticException
        function = functions[self.name]
        args1 = function.getargs()
        if self.arguments is not 0:
            args2 = self.arguments.evaluate()
        else:
            args2 = []
        if args1 is 0:
            args1 = []
        if len(args1) != len(args2):
            return SemanticException
        stack.append(dict(variables))
        variables.clear()
        for x in range(len(args1)):
            variables[args1[x]] = args2[x]
        function.getblock().evaluate()
        ret = function.getexpr().evaluate()
        copy_variables(stack.pop())
        return ret
        
            
reserved = {
    'print'    : 'PRINT',
    'andalso'  : 'ANDALSO',
    'orelse'   : 'ORELSE',
    'div'      : 'DIV',
    'mod'      : 'MOD',
    'not'      : 'NOT',
    'in'       : 'IN',
    'True'     : 'TRUE',
    'False'    : 'FALSE',
    'if'       : 'IF',
    'while'    : 'WHILE',
    'else'     : 'ELSE',
    'fun'      : 'FUN'
}

tokens = [
    'LPAREN', 'RPAREN', 'POUND',
    'NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EXPONENT',
    'STRING',
    'LT','LTE','GT','GTE','EQ','NEQ',
    'LBRACKET','RBRACKET','COMMA',
    'APPEND',
    'EMPTYLIST','EMPTYTUPLE',
    'SEMICOLON',
    'LCURLY','RCURLY',
    'VARIABLE' , 'EQUAL'
    ] + list(reserved.values())

# Tokens
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_EXPONENT = r'\*\*'
t_LT       = r'<'
t_LTE      = r'<='
t_EQ       = r'=='
t_NEQ      = r'<>'
t_GT       = r'>'
t_GTE      = r'>='
t_LBRACKET = r'\['
t_RBRACKET = r']'
t_COMMA    = r','
t_APPEND   = r'::'
t_POUND    = r'\#'
t_SEMICOLON= r'\;'
t_RCURLY   = r'\}'
t_LCURLY   = r'\{'
t_EQUAL    = r'\='

def t_VARIABLE(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    t.type = reserved.get(t.value,'VARIABLE')
    if t.type is 'VARIABLE':
        t.value = VariableNode(t.value)
    if t.type is 'TRUE' or t.type is 'FALSE':
        t.value = BooleanNode(t.value)
    return t

def t_STRING(t):
    r'\"((\\\")|[^\"])*\"|\'((\\\')|[^\'])*\''
    t.value = StringNode(t.value)
    return t

def t_NUMBER(t):
    r'(\d*(\d\.|\.\d)\d*|\d+)([Ee][+-]?\d+)?'
    try:
        t.value = NumberNode('+',t.value)
    except ValueError:
        print("Number value too large %d", t.value)
        t.value = 0
    return t

def t_EMPTYLIST(t):		
    r'\[\]'		
    t.value = EmptyListNode()		
    return t

def t_EMPTYTUPLE(t):		
    r'\(\)'		
    t.value = EmptyTupleNode()		
    return t		

# Ignored characters
t_ignore = " \t\n"

def t_error(t):
    raise SyntaxException()
    
# Build the lexer
import ply.lex as lex
lex.lex(debug = 0)

# Parsing rules
precedence = (
    ('left','ORELSE'),
    ('left','ANDALSO'),
    ('left','NOT'),
    ('left','EQ','NEQ','LT','LTE','GT','GTE'),
    ('right','APPEND'),
    ('left','IN'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE','DIV','MOD'),
    ('right','EXPONENT'),
    ('left','LBRACKET','RBRACKET','POUND'),
    ('left','LPAREN','RPAREN'),
    )

# ----------------
# FUNCTION PARSING
# ----------------

def p_all_lines(t):
    '''all_lines : functionlist main_lines
    '''
    t[0] = AllNode(t[1],t[2])

def p_all_lines2(t):
    '''all_lines : main_lines
    '''
    t[0] = t[1]

def p_function_list(t):
    '''functionlist : functionlist function
    '''
    t[0] = FunctionListNode(t[1],t[2])

def p_function_list2(t):
    '''functionlist : function
    '''
    t[0] = t[1]

def p_function(t):
    '''function : FUN VARIABLE LPAREN list RPAREN EQUAL bigblock expression SEMICOLON
    '''
    t[0] = FunctionNode(t[2],t[4],t[7],t[8])

def p_function2(t):
    '''function : FUN VARIABLE EMPTYTUPLE EQUAL bigblock expression SEMICOLON
    '''
    t[0] = FunctionNode(t[2],0,t[5],t[6])

def p_call_function(t):
    '''call_fun : VARIABLE LPAREN list RPAREN
    '''
    t[0] = CallFunctionNode(t[1],t[3])

def p_call_function2(t):
    '''call_fun : VARIABLE EMPTYTUPLE
    '''
    t[0] = CallFunctionNode(t[1],0)
# ------------------
# STATEMENTS PARSING
# ------------------

def p_main_lines(t):
    '''main_lines : bigblock
    '''
    t[0] = CodeNode(t[1])

def p_bigblock(t):
    '''bigblock : LCURLY block RCURLY
    '''
    t[0] = t[2]

def p_bigblock2(t):
    ''' bigblock : LCURLY RCURLY
    '''
    t[0] = BlockNode(0,0)
    
def p_block(t):
    '''block : block statement
    '''
    t[0] = BlockNode(t[1],t[2])

def p_block2(t):
    '''block : statement
    '''
    t[0] = t[1]

def p_assignment(t):
    '''assignment : VARIABLE EQUAL expression SEMICOLON
    '''
    t[0] = AssignmentNode(t[1],t[3])

def p_assignment2(t):
    '''assignment : VARIABLE biglist EQUAL expression SEMICOLON
    '''
    t[0] = ArrayAssignmentNode(t[1],t[2],t[4])

def p_if_else(t):
    '''if_else_statement : IF LPAREN expression RPAREN bigblock ELSE bigblock
    '''
    t[0] = IfElseNode(t[3],t[5],t[7])

def p_if_statement(t):
    '''if_statement : IF LPAREN expression RPAREN bigblock
    '''
    t[0] = IfNode(t[3],t[5])

def p_while_statement(t):
    '''while_statement : WHILE LPAREN expression RPAREN bigblock
    '''
    t[0] = WhileNode(t[3],t[5])

def p_statement(t):
    '''statement : assignment
                 | print_smt
                 | if_statement
                 | if_else_statement
                 | while_statement
                 | bigblock
                 | call_fun SEMICOLON
    '''
    t[0] = t[1]

# -------------------
# EXPRESSIONS PARSING
# -------------------
def p_print_smt(t):
    """
    print_smt : PRINT LPAREN expression RPAREN SEMICOLON
    """
    t[0] = PrintNode(t[3])

def p_parenthesis(t):
    '''expression : LPAREN expression RPAREN
    '''
    t[0] = t[2]

def p_pound(t):
    '''poundexp : POUND expression
    '''
    t[0] = t[2]
    
def p_tupleindex(t):
    '''expression : poundexp bigtuple
    '''
    t[0] = TupleIndexNode(t[1],t[2])

def p_tupleindex2(t):
    '''expression : poundexp LPAREN expression RPAREN
    '''
    t[0] = TupleIndexNode(t[1],t[3])

def p_tupleParen(t):
    '''bigtuple : LPAREN bigtuple RPAREN
    '''
    t[0] = t[2]

def p_emptytuple(t):		
    '''bigtuple : EMPTYTUPLE
    '''		
    t[0] = t[1]

def p_bigtuple(t):
    '''bigtuple : LPAREN tuple RPAREN
    '''
    t[0] = t[2]

def p_tuple(t):
    '''tuple : expression COMMA expression
    '''
    t[0] = TupleNode(t[1],t[3])

def p_tuple2(t):
    '''tuple : tuple COMMA expression
    '''
    t[0] = TupleNodeAdd(t[1],t[3])

def p_brackets(t):
    '''expression : expression biglist
    '''
    t[0] = ListIndexNode(t[1],t[2])

def p_biglist(t):
    '''biglist : LBRACKET list RBRACKET
    '''
    t[0] = t[2]

def p_emptyList(t):		
    '''biglist : EMPTYLIST		
    '''		
    t[0] = t[1]

def p_lists(t):
    '''list : expression
    '''
    t[0] = ListNode(t[1])

def p_lists2(t):
    '''list : list COMMA expression
    '''
    t[0] = ListNodeAdd(t[1],t[3])

def p_notop(t):
    '''expression : NOT expression
    '''
    t[0] = NotNode(t[2])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EXPONENT expression
                  | expression DIV expression
                  | expression MOD expression
                  | expression LT expression
                  | expression LTE expression
                  | expression GT expression
                  | expression GTE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression ANDALSO expression
                  | expression ORELSE expression
                  | expression APPEND expression
                  | expression IN expression
    '''
    t[0] = BopNode(t[2], t[1], t[3])

def p_expression_factor(t):
    '''expression : factor'''
    t[0] = t[1]

def p_unary(t):
    '''unary : MINUS expression
    '''
    t[0] = NumberNode(t[1],t[2])

def p_factor_number(t):
    '''factor : NUMBER
              | STRING
              | TRUE
              | FALSE
              | biglist
              | bigtuple
              | unary
              | VARIABLE
              | call_fun
    '''
    t[0] = t[1]

#-----------------------------------------------
#-----------------------------------------------

def p_error(t):
    raise SyntaxException()

import ply.yacc as yacc
yacc.yacc(debug = 0)

import sys

if (len(sys.argv) != 2):
    sys.exit("invalid arguments")
fd = open(sys.argv[1], 'r')
code = fd.read();

try:
    lex.input(code)
    while True:
        token = lex.token()
        if not token: break
        #print(token)
    ast = yacc.parse(code)
    ast.evaluate()
except SemanticException:
    print("SEMANTIC ERROR")
except SyntaxException:
    print("SYNTAX ERROR")
