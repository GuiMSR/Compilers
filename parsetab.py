
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ASSIGN COLON COMMA COMMENTS DIV DOT EQUAL INTEGER_ERROR INTEGER_LITERAL LBRACE LOWER LOWER_EQUAL LPAR Lexicalerror MINUS OBJECT_IDENTIFIER PLUS POW RBRACE RPAR SEMICOLON SPACES TIMES TYPE_IDENTIFIER string_literalexpression : expression PLUS termexpression : expression MINUS termexpression : termterm : term TIMES factorterm : term DIV factorterm : factorfactor : INTEGER_LITERALfactor : LPAR expression RPAR'
    
_lr_action_items = {'INTEGER_LITERAL':([0,5,6,7,8,9,],[4,4,4,4,4,4,]),'LPAR':([0,5,6,7,8,9,],[5,5,5,5,5,5,]),'$end':([1,2,3,4,11,12,13,14,15,],[0,-3,-6,-7,-1,-2,-4,-5,-8,]),'PLUS':([1,2,3,4,10,11,12,13,14,15,],[6,-3,-6,-7,6,-1,-2,-4,-5,-8,]),'MINUS':([1,2,3,4,10,11,12,13,14,15,],[7,-3,-6,-7,7,-1,-2,-4,-5,-8,]),'RPAR':([2,3,4,10,11,12,13,14,15,],[-3,-6,-7,15,-1,-2,-4,-5,-8,]),'TIMES':([2,3,4,11,12,13,14,15,],[8,-6,-7,8,8,-4,-5,-8,]),'DIV':([2,3,4,11,12,13,14,15,],[9,-6,-7,9,9,-4,-5,-8,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,5,],[1,10,]),'term':([0,5,6,7,],[2,2,11,12,]),'factor':([0,5,6,7,8,9,],[3,3,3,3,13,14,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> expression PLUS term','expression',3,'p_expression_plus','parserFile.py',52),
  ('expression -> expression MINUS term','expression',3,'p_expression_minus','parserFile.py',56),
  ('expression -> term','expression',1,'p_expression_term','parserFile.py',60),
  ('term -> term TIMES factor','term',3,'p_term_times','parserFile.py',64),
  ('term -> term DIV factor','term',3,'p_term_div','parserFile.py',68),
  ('term -> factor','term',1,'p_term_factor','parserFile.py',72),
  ('factor -> INTEGER_LITERAL','factor',1,'p_factor_num','parserFile.py',76),
  ('factor -> LPAR expression RPAR','factor',3,'p_factor_expr','parserFile.py',80),
]
