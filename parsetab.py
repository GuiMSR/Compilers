
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'initrightASSIGNleftANDrightNOTnonassocLOWEREQUALLOWER_EQUALleftPLUSMINUSleftTIMESDIVrightISNULLUMINUSrightPOWleftDOTAND ASSIGN BOOL CLASS COLON COMMA DIV DO DOT ELSE EQUAL EXTENDS FALSE IF IN INT32 INTEGER_LITERAL ISNULL LBRACE LET LOWER LOWER_EQUAL LPAR MINUS NEW NOT OBJECT_IDENTIFIER PLUS POW RBRACE RPAR SELF SEMICOLON STRING THEN TIMES TRUE TYPE_IDENTIFIER UNIT WHILE string_literalinit : programprogram : program class\n                    | classclass : field\n                | methodclass : CLASS errorclass : expression\n                | TYPE_IDENTIFIER\n                | blockclass : CLASS new_class_scope class-body\n                | CLASS new_class_scope EXTENDS TYPE_IDENTIFIER class-bodynew_class_scope : TYPE_IDENTIFIERclass-body : LBRACE class-body-in RBRACEclass-body : LBRACE class-body-in errorclass-body-in : class-body-in fieldclass-body-in : class-body-in methodclass-body-in : field : OBJECT_IDENTIFIER COLON type SEMICOLON\n                | OBJECT_IDENTIFIER COLON type ASSIGN expression SEMICOLONmethod : new_method LPAR formals RPAR COLON type blocknew_method : OBJECT_IDENTIFIERnew_variables_scope :type : TYPE_IDENTIFIER\n                | INT32\n                | BOOL\n                | STRING\n                | UNIT formals : formal\n                | formals COMMA formal\n                | formal : OBJECT_IDENTIFIER COLON typeblock : LBRACE check_block new_variables_scope inblock RBRACEcheck_block :inblock : inblock SEMICOLON expression\n                | expression\n                |inblock : inblock error expression : new_variables_scope IF expression THEN expression\n                    | new_variables_scope IF expression THEN expression ELSE expressionexpression : WHILE expression DO expressionexpression : LET let_type IN expression\n                    | LET let_type ASSIGN expression IN expressionlet_type : OBJECT_IDENTIFIER COLON typeexpression : OBJECT_IDENTIFIER ASSIGN expressionexpression : NOT expression check_bool\n                    | MINUS expression check_int %prec UMINUScheck_int :check_bool :expression : ISNULL expressionexpression : expression PLUS expression\n                  | expression MINUS expression\n                  | expression TIMES expression\n                  | expression DIV expression\n                  | expression EQUAL expression\n                  | expression LOWER_EQUAL expression\n                  | expression LOWER expression\n                  | expression POW expression\n                  | expression AND expressionexpression : OBJECT_IDENTIFIER LPAR args RPAR\n                    | expression DOT OBJECT_IDENTIFIER LPAR args RPARexpression : NEW TYPE_IDENTIFIERexpression : OBJECT_IDENTIFIERexpression : SELFexpression : literalexpression : LPAR RPARexpression : LPAR expression RPARexpression : LPAR expression error\n                    | error expression RPARexpression : blockexpression : error\n                    | IF expression THEN expression SEMICOLON errorargs : args COMMA expression\n                | expression\n                |literal : literal_integer\n                | literal_string\n                | boolean-literalliteral_string : string_literalliteral_integer : INTEGER_LITERALboolean-literal : TRUE \n                        | FALSE'
    
_lr_action_items = {'CLASS':([0,2,3,4,5,7,8,9,10,11,22,23,25,26,27,28,29,30,31,32,33,37,38,53,60,61,62,63,65,68,69,70,71,72,73,74,75,76,77,85,91,92,99,100,105,107,114,115,120,121,122,132,135,138,139,142,143,145,146,],[6,6,-3,-4,-5,-70,-7,-8,-9,-62,-63,-64,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,-65,-48,-47,-49,-61,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,-45,-46,-18,-59,-40,-41,-11,-13,-14,-38,-32,-60,-19,-71,-42,-20,-39,]),'TYPE_IDENTIFIER':([0,2,3,4,5,6,7,8,9,10,11,21,22,23,25,26,27,28,29,30,31,32,33,37,38,49,53,60,61,62,63,65,66,68,69,70,71,72,73,74,75,76,77,85,91,92,98,99,100,105,107,111,114,115,120,121,122,129,132,135,138,139,142,143,145,146,],[9,9,-3,-4,-5,35,-70,-7,-8,-9,-62,63,-63,-64,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,80,-65,-48,-47,-49,-61,-10,102,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,80,-45,-46,-18,-59,80,-40,-41,-11,-13,-14,80,-38,-32,-60,-19,-71,-42,-20,-39,]),'OBJECT_IDENTIFIER':([0,2,3,4,5,7,8,9,10,11,13,15,16,17,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,48,50,51,52,53,55,60,61,62,63,64,65,67,68,69,70,71,72,73,74,75,76,77,85,91,92,94,95,96,97,99,100,101,103,104,105,106,107,108,110,112,114,115,120,121,122,123,124,132,134,135,136,138,139,141,142,143,145,146,],[11,11,-3,-4,-5,37,-7,-8,-9,-62,37,37,37,59,37,37,37,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,37,37,37,37,37,37,37,37,37,78,37,37,90,-65,37,-48,-47,-49,-61,-22,-10,-17,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,37,37,37,37,-45,-46,37,125,37,-18,37,-59,37,90,37,-40,-41,-11,-13,-14,-15,-16,-38,37,-32,37,-60,-19,37,-71,-42,-20,-39,]),'WHILE':([0,2,3,4,5,7,8,9,10,11,13,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,50,51,53,55,60,61,62,63,64,65,68,69,70,71,72,73,74,75,76,77,85,91,92,94,95,96,97,99,100,101,104,105,106,107,108,112,114,115,120,121,122,132,134,135,136,138,139,141,142,143,145,146,],[16,16,-3,-4,-5,16,-7,-8,-9,-62,16,16,16,16,16,16,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,16,16,16,16,16,16,16,16,16,16,16,-65,16,-48,-47,-49,-61,-22,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,16,16,16,16,-45,-46,16,16,-18,16,-59,16,16,-40,-41,-11,-13,-14,-38,16,-32,16,-60,-19,16,-71,-42,-20,-39,]),'LET':([0,2,3,4,5,7,8,9,10,11,13,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,50,51,53,55,60,61,62,63,64,65,68,69,70,71,72,73,74,75,76,77,85,91,92,94,95,96,97,99,100,101,104,105,106,107,108,112,114,115,120,121,122,132,134,135,136,138,139,141,142,143,145,146,],[17,17,-3,-4,-5,17,-7,-8,-9,-62,17,17,17,17,17,17,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,17,17,17,17,17,17,17,17,17,17,17,-65,17,-48,-47,-49,-61,-22,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,17,17,17,17,-45,-46,17,17,-18,17,-59,17,17,-40,-41,-11,-13,-14,-38,17,-32,17,-60,-19,17,-71,-42,-20,-39,]),'NOT':([0,2,3,4,5,7,8,9,10,11,13,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,50,51,53,55,60,61,62,63,64,65,68,69,70,71,72,73,74,75,76,77,85,91,92,94,95,96,97,99,100,101,104,105,106,107,108,112,114,115,120,121,122,132,134,135,136,138,139,141,142,143,145,146,],[18,18,-3,-4,-5,18,-7,-8,-9,-62,18,18,18,18,18,18,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,18,18,18,18,18,18,18,18,18,18,18,-65,18,-48,-47,-49,-61,-22,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,18,18,18,18,-45,-46,18,18,-18,18,-59,18,18,-40,-41,-11,-13,-14,-38,18,-32,18,-60,-19,18,-71,-42,-20,-39,]),'MINUS':([0,2,3,4,5,7,8,9,10,11,13,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,36,37,38,39,40,41,42,43,44,45,46,47,50,51,53,54,55,56,57,60,61,62,63,64,65,68,69,70,71,72,73,74,75,76,77,85,87,91,92,93,94,95,96,97,99,100,101,104,105,106,107,108,112,113,114,115,116,119,120,121,122,127,128,132,134,135,136,138,139,141,142,143,144,145,146,],[19,19,-3,-4,-5,19,40,-8,-9,-62,19,19,19,19,19,19,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,40,-62,-69,19,19,19,19,19,19,19,19,19,19,19,-65,40,19,40,40,40,40,-49,-61,-22,-10,-68,-50,-51,-52,-53,40,40,40,-57,40,40,40,-66,-67,40,19,19,19,19,-45,-46,19,19,-18,19,-59,19,19,40,40,40,40,40,-11,-13,-14,40,40,40,19,-32,19,-60,-19,19,-71,40,40,-20,40,]),'ISNULL':([0,2,3,4,5,7,8,9,10,11,13,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,50,51,53,55,60,61,62,63,64,65,68,69,70,71,72,73,74,75,76,77,85,91,92,94,95,96,97,99,100,101,104,105,106,107,108,112,114,115,120,121,122,132,134,135,136,138,139,141,142,143,145,146,],[20,20,-3,-4,-5,20,-7,-8,-9,-62,20,20,20,20,20,20,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,20,20,20,20,20,20,20,20,20,20,20,-65,20,-48,-47,-49,-61,-22,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,20,20,20,20,-45,-46,20,20,-18,20,-59,20,20,-40,-41,-11,-13,-14,-38,20,-32,20,-60,-19,20,-71,-42,-20,-39,]),'NEW':([0,2,3,4,5,7,8,9,10,11,13,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,50,51,53,55,60,61,62,63,64,65,68,69,70,71,72,73,74,75,76,77,85,91,92,94,95,96,97,99,100,101,104,105,106,107,108,112,114,115,120,121,122,132,134,135,136,138,139,141,142,143,145,146,],[21,21,-3,-4,-5,21,-7,-8,-9,-62,21,21,21,21,21,21,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,21,21,21,21,21,21,21,21,21,21,21,-65,21,-48,-47,-49,-61,-22,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,21,21,21,21,-45,-46,21,21,-18,21,-59,21,21,-40,-41,-11,-13,-14,-38,21,-32,21,-60,-19,21,-71,-42,-20,-39,]),'SELF':([0,2,3,4,5,7,8,9,10,11,13,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,50,51,53,55,60,61,62,63,64,65,68,69,70,71,72,73,74,75,76,77,85,91,92,94,95,96,97,99,100,101,104,105,106,107,108,112,114,115,120,121,122,132,134,135,136,138,139,141,142,143,145,146,],[22,22,-3,-4,-5,22,-7,-8,-9,-62,22,22,22,22,22,22,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,22,22,22,22,22,22,22,22,22,22,22,-65,22,-48,-47,-49,-61,-22,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,22,22,22,22,-45,-46,22,22,-18,22,-59,22,22,-40,-41,-11,-13,-14,-38,22,-32,22,-60,-19,22,-71,-42,-20,-39,]),'LPAR':([0,2,3,4,5,7,8,9,10,11,12,13,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,50,51,53,55,60,61,62,63,64,65,68,69,70,71,72,73,74,75,76,77,78,85,91,92,94,95,96,97,99,100,101,104,105,106,107,108,112,114,115,120,121,122,125,132,134,135,136,138,139,141,142,143,145,146,],[13,13,-3,-4,-5,13,-7,-8,-9,51,52,13,13,13,13,13,13,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,51,-69,13,13,13,13,13,13,13,13,13,13,13,-65,13,-48,-47,-49,-61,-22,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,104,-44,-66,-67,13,13,13,13,-45,-46,13,13,-18,13,-59,13,13,-40,-41,-11,-13,-14,-21,-38,13,-32,13,-60,-19,13,-71,-42,-20,-39,]),'error':([0,2,3,4,5,6,7,8,9,10,11,13,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,50,51,53,54,55,60,61,62,63,64,65,67,68,69,70,71,72,73,74,75,76,77,85,91,92,94,95,96,97,99,100,101,103,104,105,106,107,108,112,114,115,118,119,120,121,122,123,124,132,133,134,135,136,137,138,139,141,142,143,144,145,146,],[7,7,-3,-4,-5,33,7,-7,-8,-9,-62,7,7,7,7,7,7,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,7,7,7,7,7,7,7,7,7,7,7,-65,92,7,-48,-47,-49,-61,-22,-10,-17,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,7,7,7,7,-45,-46,7,122,7,-18,7,-59,7,7,-40,-41,137,-35,-11,-13,-14,-15,-16,-38,142,7,-32,7,-37,-60,-19,7,-71,-42,-34,-20,-39,]),'IF':([0,2,3,4,5,7,8,9,10,11,13,14,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,50,51,53,55,60,61,62,63,64,65,68,69,70,71,72,73,74,75,76,77,85,91,92,94,95,96,97,99,100,101,104,105,106,107,108,112,114,115,120,121,122,132,134,135,136,138,139,141,142,143,145,146,],[15,15,-3,-4,-5,15,-7,-8,-9,-62,15,55,15,15,15,15,15,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,15,15,15,15,15,15,15,15,15,15,15,-65,15,-48,-47,-49,-61,-22,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,15,15,15,15,-45,-46,15,15,-18,15,-59,15,15,-40,-41,-11,-13,-14,-38,15,-32,15,-60,-19,15,-71,-42,-20,-39,]),'LBRACE':([0,2,3,4,5,7,8,9,10,11,13,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,34,35,37,38,39,40,41,42,43,44,45,46,47,50,51,53,55,60,61,62,63,64,65,68,69,70,71,72,73,74,75,76,77,80,81,82,83,84,85,91,92,94,95,96,97,99,100,101,102,104,105,106,107,108,112,114,115,120,121,122,132,134,135,136,138,139,140,141,142,143,145,146,],[24,24,-3,-4,-5,24,-7,-8,-9,-62,24,24,24,24,24,24,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,67,-12,-62,-69,24,24,24,24,24,24,24,24,24,24,24,-65,24,-48,-47,-49,-61,-22,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-23,-24,-25,-26,-27,-44,-66,-67,24,24,24,24,-45,-46,24,67,24,-18,24,-59,24,24,-40,-41,-11,-13,-14,-38,24,-32,24,-60,-19,24,24,-71,-42,-20,-39,]),'INTEGER_LITERAL':([0,2,3,4,5,7,8,9,10,11,13,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,50,51,53,55,60,61,62,63,64,65,68,69,70,71,72,73,74,75,76,77,85,91,92,94,95,96,97,99,100,101,104,105,106,107,108,112,114,115,120,121,122,132,134,135,136,138,139,141,142,143,145,146,],[28,28,-3,-4,-5,28,-7,-8,-9,-62,28,28,28,28,28,28,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,28,28,28,28,28,28,28,28,28,28,28,-65,28,-48,-47,-49,-61,-22,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,28,28,28,28,-45,-46,28,28,-18,28,-59,28,28,-40,-41,-11,-13,-14,-38,28,-32,28,-60,-19,28,-71,-42,-20,-39,]),'string_literal':([0,2,3,4,5,7,8,9,10,11,13,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,50,51,53,55,60,61,62,63,64,65,68,69,70,71,72,73,74,75,76,77,85,91,92,94,95,96,97,99,100,101,104,105,106,107,108,112,114,115,120,121,122,132,134,135,136,138,139,141,142,143,145,146,],[29,29,-3,-4,-5,29,-7,-8,-9,-62,29,29,29,29,29,29,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,29,29,29,29,29,29,29,29,29,29,29,-65,29,-48,-47,-49,-61,-22,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,29,29,29,29,-45,-46,29,29,-18,29,-59,29,29,-40,-41,-11,-13,-14,-38,29,-32,29,-60,-19,29,-71,-42,-20,-39,]),'TRUE':([0,2,3,4,5,7,8,9,10,11,13,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,50,51,53,55,60,61,62,63,64,65,68,69,70,71,72,73,74,75,76,77,85,91,92,94,95,96,97,99,100,101,104,105,106,107,108,112,114,115,120,121,122,132,134,135,136,138,139,141,142,143,145,146,],[30,30,-3,-4,-5,30,-7,-8,-9,-62,30,30,30,30,30,30,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,30,30,30,30,30,30,30,30,30,30,30,-65,30,-48,-47,-49,-61,-22,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,30,30,30,30,-45,-46,30,30,-18,30,-59,30,30,-40,-41,-11,-13,-14,-38,30,-32,30,-60,-19,30,-71,-42,-20,-39,]),'FALSE':([0,2,3,4,5,7,8,9,10,11,13,15,16,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,46,47,50,51,53,55,60,61,62,63,64,65,68,69,70,71,72,73,74,75,76,77,85,91,92,94,95,96,97,99,100,101,104,105,106,107,108,112,114,115,120,121,122,132,134,135,136,138,139,141,142,143,145,146,],[31,31,-3,-4,-5,31,-7,-8,-9,-62,31,31,31,31,31,31,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,31,31,31,31,31,31,31,31,31,31,31,-65,31,-48,-47,-49,-61,-22,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,31,31,31,31,-45,-46,31,31,-18,31,-59,31,31,-40,-41,-11,-13,-14,-38,31,-32,31,-60,-19,31,-71,-42,-20,-39,]),'$end':([1,2,3,4,5,7,8,9,10,11,22,23,25,26,27,28,29,30,31,32,33,37,38,53,60,61,62,63,65,68,69,70,71,72,73,74,75,76,77,85,91,92,99,100,105,107,114,115,120,121,122,132,135,138,139,142,143,145,146,],[0,-1,-3,-4,-5,-70,-7,-8,-9,-62,-63,-64,-75,-76,-77,-79,-78,-80,-81,-2,-6,-62,-69,-65,-48,-47,-49,-61,-10,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,-45,-46,-18,-59,-40,-41,-11,-13,-14,-38,-32,-60,-19,-71,-42,-20,-39,]),'PLUS':([7,8,10,11,22,23,25,26,27,28,29,30,31,36,37,38,53,54,56,57,60,61,62,63,68,69,70,71,72,73,74,75,76,77,85,87,91,92,93,99,100,107,113,114,115,116,119,127,128,132,135,138,142,143,144,146,],[-70,39,-69,-62,-63,-64,-75,-76,-77,-79,-78,-80,-81,39,-62,-69,-65,39,39,39,39,39,-49,-61,-68,-50,-51,-52,-53,39,39,39,-57,39,39,39,-66,-67,39,-45,-46,-59,39,39,39,39,39,39,39,39,-32,-60,-71,39,39,39,]),'TIMES':([7,8,10,11,22,23,25,26,27,28,29,30,31,36,37,38,53,54,56,57,60,61,62,63,68,69,70,71,72,73,74,75,76,77,85,87,91,92,93,99,100,107,113,114,115,116,119,127,128,132,135,138,142,143,144,146,],[-70,41,-69,-62,-63,-64,-75,-76,-77,-79,-78,-80,-81,41,-62,-69,-65,41,41,41,41,41,-49,-61,-68,41,41,-52,-53,41,41,41,-57,41,41,41,-66,-67,41,-45,-46,-59,41,41,41,41,41,41,41,41,-32,-60,-71,41,41,41,]),'DIV':([7,8,10,11,22,23,25,26,27,28,29,30,31,36,37,38,53,54,56,57,60,61,62,63,68,69,70,71,72,73,74,75,76,77,85,87,91,92,93,99,100,107,113,114,115,116,119,127,128,132,135,138,142,143,144,146,],[-70,42,-69,-62,-63,-64,-75,-76,-77,-79,-78,-80,-81,42,-62,-69,-65,42,42,42,42,42,-49,-61,-68,42,42,-52,-53,42,42,42,-57,42,42,42,-66,-67,42,-45,-46,-59,42,42,42,42,42,42,42,42,-32,-60,-71,42,42,42,]),'EQUAL':([7,8,10,11,22,23,25,26,27,28,29,30,31,36,37,38,53,54,56,57,60,61,62,63,68,69,70,71,72,73,74,75,76,77,85,87,91,92,93,99,100,107,113,114,115,116,119,127,128,132,135,138,142,143,144,146,],[-70,43,-69,-62,-63,-64,-75,-76,-77,-79,-78,-80,-81,43,-62,-69,-65,43,43,43,43,43,-49,-61,-68,-50,-51,-52,-53,None,None,None,-57,43,43,43,-66,-67,43,-45,-46,-59,43,43,43,43,43,43,43,43,-32,-60,-71,43,43,43,]),'LOWER_EQUAL':([7,8,10,11,22,23,25,26,27,28,29,30,31,36,37,38,53,54,56,57,60,61,62,63,68,69,70,71,72,73,74,75,76,77,85,87,91,92,93,99,100,107,113,114,115,116,119,127,128,132,135,138,142,143,144,146,],[-70,44,-69,-62,-63,-64,-75,-76,-77,-79,-78,-80,-81,44,-62,-69,-65,44,44,44,44,44,-49,-61,-68,-50,-51,-52,-53,None,None,None,-57,44,44,44,-66,-67,44,-45,-46,-59,44,44,44,44,44,44,44,44,-32,-60,-71,44,44,44,]),'LOWER':([7,8,10,11,22,23,25,26,27,28,29,30,31,36,37,38,53,54,56,57,60,61,62,63,68,69,70,71,72,73,74,75,76,77,85,87,91,92,93,99,100,107,113,114,115,116,119,127,128,132,135,138,142,143,144,146,],[-70,45,-69,-62,-63,-64,-75,-76,-77,-79,-78,-80,-81,45,-62,-69,-65,45,45,45,45,45,-49,-61,-68,-50,-51,-52,-53,None,None,None,-57,45,45,45,-66,-67,45,-45,-46,-59,45,45,45,45,45,45,45,45,-32,-60,-71,45,45,45,]),'POW':([7,8,10,11,22,23,25,26,27,28,29,30,31,36,37,38,53,54,56,57,60,61,62,63,68,69,70,71,72,73,74,75,76,77,85,87,91,92,93,99,100,107,113,114,115,116,119,127,128,132,135,138,142,143,144,146,],[-70,46,-69,-62,-63,-64,-75,-76,-77,-79,-78,-80,-81,46,-62,-69,-65,46,46,46,46,46,46,-61,-68,46,46,46,46,46,46,46,46,46,46,46,-66,-67,46,-45,-46,-59,46,46,46,46,46,46,46,46,-32,-60,-71,46,46,46,]),'AND':([7,8,10,11,22,23,25,26,27,28,29,30,31,36,37,38,53,54,56,57,60,61,62,63,68,69,70,71,72,73,74,75,76,77,85,87,91,92,93,99,100,107,113,114,115,116,119,127,128,132,135,138,142,143,144,146,],[-70,47,-69,-62,-63,-64,-75,-76,-77,-79,-78,-80,-81,47,-62,-69,-65,47,47,47,47,47,-49,-61,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,47,47,-66,-67,47,-45,-46,-59,47,47,47,47,47,47,47,47,-32,-60,-71,47,47,47,]),'DOT':([7,8,10,11,22,23,25,26,27,28,29,30,31,36,37,38,53,54,56,57,60,61,62,63,68,69,70,71,72,73,74,75,76,77,85,87,91,92,93,99,100,107,113,114,115,116,119,127,128,132,135,138,142,143,144,146,],[-70,48,-69,-62,-63,-64,-75,-76,-77,-79,-78,-80,-81,48,-62,-69,-65,48,48,48,48,48,48,-61,-68,48,48,48,48,48,48,48,48,48,48,48,-66,-67,48,-45,-46,-59,48,48,48,48,48,48,48,48,-32,-60,-71,48,48,48,]),'RPAR':([7,13,22,23,25,26,27,28,29,30,31,36,37,38,51,52,53,54,60,61,62,63,68,69,70,71,72,73,74,75,76,77,80,81,82,83,84,85,86,87,88,89,91,92,99,100,104,107,114,115,126,128,130,131,132,135,138,142,143,146,],[-70,53,-63,-64,-75,-76,-77,-79,-78,-80,-81,68,-62,-69,-74,-30,-65,91,-48,-47,-49,-61,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-23,-24,-25,-26,-27,-44,107,-73,109,-28,-66,-67,-45,-46,-74,-59,-40,-41,138,-72,-29,-31,-38,-32,-60,-71,-42,-39,]),'THEN':([7,22,23,25,26,27,28,29,30,31,37,38,53,56,60,61,62,63,68,69,70,71,72,73,74,75,76,77,85,91,92,93,99,100,107,114,115,132,135,138,142,143,146,],[-70,-63,-64,-75,-76,-77,-79,-78,-80,-81,-62,-69,-65,94,-48,-47,-49,-61,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,112,-45,-46,-59,-40,-41,-38,-32,-60,-71,-42,-39,]),'DO':([7,22,23,25,26,27,28,29,30,31,37,38,53,57,60,61,62,63,68,69,70,71,72,73,74,75,76,77,85,91,92,99,100,107,114,115,132,135,138,142,143,146,],[-70,-63,-64,-75,-76,-77,-79,-78,-80,-81,-62,-69,-65,95,-48,-47,-49,-61,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,-45,-46,-59,-40,-41,-38,-32,-60,-71,-42,-39,]),'COMMA':([7,22,23,25,26,27,28,29,30,31,37,38,51,52,53,60,61,62,63,68,69,70,71,72,73,74,75,76,77,80,81,82,83,84,85,86,87,88,89,91,92,99,100,104,107,114,115,126,128,130,131,132,135,138,142,143,146,],[-70,-63,-64,-75,-76,-77,-79,-78,-80,-81,-62,-69,-74,-30,-65,-48,-47,-49,-61,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-23,-24,-25,-26,-27,-44,108,-73,110,-28,-66,-67,-45,-46,-74,-59,-40,-41,108,-72,-29,-31,-38,-32,-60,-71,-42,-39,]),'SEMICOLON':([7,22,23,24,25,26,27,28,29,30,31,37,38,53,60,61,62,63,64,68,69,70,71,72,73,74,75,76,77,79,80,81,82,83,84,85,91,92,99,100,101,107,113,114,115,118,119,127,132,135,137,138,142,143,144,146,],[-70,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-62,-69,-65,-48,-47,-49,-61,-22,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,105,-23,-24,-25,-26,-27,-44,-66,-67,-45,-46,-36,-59,133,-40,-41,136,-35,139,-38,-32,-37,-60,-71,-42,-34,-39,]),'IN':([7,22,23,25,26,27,28,29,30,31,37,38,53,58,60,61,62,63,68,69,70,71,72,73,74,75,76,77,80,81,82,83,84,85,91,92,99,100,107,114,115,116,117,132,135,138,142,143,146,],[-70,-63,-64,-75,-76,-77,-79,-78,-80,-81,-62,-69,-65,96,-48,-47,-49,-61,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-23,-24,-25,-26,-27,-44,-66,-67,-45,-46,-59,-40,-41,134,-43,-38,-32,-60,-71,-42,-39,]),'RBRACE':([7,22,23,24,25,26,27,28,29,30,31,37,38,53,60,61,62,63,64,67,68,69,70,71,72,73,74,75,76,77,85,91,92,99,100,101,103,105,107,114,115,118,119,123,124,132,135,137,138,139,142,143,144,145,146,],[-70,-63,-64,-33,-75,-76,-77,-79,-78,-80,-81,-62,-69,-65,-48,-47,-49,-61,-22,-17,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,-45,-46,-36,121,-18,-59,-40,-41,135,-35,-15,-16,-38,-32,-37,-60,-19,-71,-42,-34,-20,-39,]),'ELSE':([7,22,23,25,26,27,28,29,30,31,37,38,53,60,61,62,63,68,69,70,71,72,73,74,75,76,77,85,91,92,99,100,107,114,115,132,135,138,142,143,146,],[-70,-63,-64,-75,-76,-77,-79,-78,-80,-81,-62,-69,-65,-48,-47,-49,-61,-68,-50,-51,-52,-53,-54,-55,-56,-57,-58,-44,-66,-67,-45,-46,-59,-40,-41,141,-32,-60,-71,-42,-39,]),'COLON':([11,59,90,109,125,],[49,98,111,129,49,]),'ASSIGN':([11,37,58,79,80,81,82,83,84,117,],[50,50,97,106,-23,-24,-25,-26,-27,-43,]),'EXTENDS':([34,35,],[66,-12,]),'INT32':([49,98,111,129,],[81,81,81,81,]),'BOOL':([49,98,111,129,],[82,82,82,82,]),'STRING':([49,98,111,129,],[83,83,83,83,]),'UNIT':([49,98,111,129,],[84,84,84,84,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'init':([0,],[1,]),'program':([0,],[2,]),'class':([0,2,],[3,32,]),'field':([0,2,103,],[4,4,123,]),'method':([0,2,103,],[5,5,124,]),'expression':([0,2,7,13,15,16,18,19,20,39,40,41,42,43,44,45,46,47,50,51,55,94,95,96,97,101,104,106,108,112,134,136,141,],[8,8,36,54,56,57,60,61,62,69,70,71,72,73,74,75,76,77,85,87,93,113,114,115,116,119,87,127,128,132,143,144,146,]),'block':([0,2,7,13,15,16,18,19,20,39,40,41,42,43,44,45,46,47,50,51,55,94,95,96,97,101,104,106,108,112,134,136,140,141,],[10,10,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,145,38,]),'new_method':([0,2,103,],[12,12,12,]),'new_variables_scope':([0,2,7,13,15,16,18,19,20,39,40,41,42,43,44,45,46,47,50,51,55,64,94,95,96,97,101,104,106,108,112,134,136,141,],[14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,101,14,14,14,14,14,14,14,14,14,14,14,14,]),'literal':([0,2,7,13,15,16,18,19,20,39,40,41,42,43,44,45,46,47,50,51,55,94,95,96,97,101,104,106,108,112,134,136,141,],[23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,]),'literal_integer':([0,2,7,13,15,16,18,19,20,39,40,41,42,43,44,45,46,47,50,51,55,94,95,96,97,101,104,106,108,112,134,136,141,],[25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,]),'literal_string':([0,2,7,13,15,16,18,19,20,39,40,41,42,43,44,45,46,47,50,51,55,94,95,96,97,101,104,106,108,112,134,136,141,],[26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,]),'boolean-literal':([0,2,7,13,15,16,18,19,20,39,40,41,42,43,44,45,46,47,50,51,55,94,95,96,97,101,104,106,108,112,134,136,141,],[27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,]),'new_class_scope':([6,],[34,]),'let_type':([17,],[58,]),'check_block':([24,],[64,]),'class-body':([34,102,],[65,120,]),'type':([49,98,111,129,],[79,117,131,140,]),'args':([51,104,],[86,126,]),'formals':([52,],[88,]),'formal':([52,110,],[89,130,]),'check_bool':([60,],[99,]),'check_int':([61,],[100,]),'class-body-in':([67,],[103,]),'inblock':([101,],[118,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> init","S'",1,None,None,None),
  ('init -> program','init',1,'p_init','classCheckerFile.py',107),
  ('program -> program class','program',2,'p_program','classCheckerFile.py',111),
  ('program -> class','program',1,'p_program','classCheckerFile.py',112),
  ('class -> field','class',1,'p_field_method_error','classCheckerFile.py',119),
  ('class -> method','class',1,'p_field_method_error','classCheckerFile.py',120),
  ('class -> CLASS error','class',2,'p_class_error','classCheckerFile.py',126),
  ('class -> expression','class',1,'p_general_class_error','classCheckerFile.py',131),
  ('class -> TYPE_IDENTIFIER','class',1,'p_general_class_error','classCheckerFile.py',132),
  ('class -> block','class',1,'p_general_class_error','classCheckerFile.py',133),
  ('class -> CLASS new_class_scope class-body','class',3,'p_class','classCheckerFile.py',139),
  ('class -> CLASS new_class_scope EXTENDS TYPE_IDENTIFIER class-body','class',5,'p_class','classCheckerFile.py',140),
  ('new_class_scope -> TYPE_IDENTIFIER','new_class_scope',1,'p_new_class_scope','classCheckerFile.py',152),
  ('class-body -> LBRACE class-body-in RBRACE','class-body',3,'p_class_body','classCheckerFile.py',169),
  ('class-body -> LBRACE class-body-in error','class-body',3,'p_class_braces_error','classCheckerFile.py',173),
  ('class-body-in -> class-body-in field','class-body-in',2,'p_class_body_field','classCheckerFile.py',178),
  ('class-body-in -> class-body-in method','class-body-in',2,'p_class_body_method','classCheckerFile.py',183),
  ('class-body-in -> <empty>','class-body-in',0,'p_class_body_empty','classCheckerFile.py',189),
  ('field -> OBJECT_IDENTIFIER COLON type SEMICOLON','field',4,'p_field','classCheckerFile.py',193),
  ('field -> OBJECT_IDENTIFIER COLON type ASSIGN expression SEMICOLON','field',6,'p_field','classCheckerFile.py',194),
  ('method -> new_method LPAR formals RPAR COLON type block','method',7,'p_method','classCheckerFile.py',212),
  ('new_method -> OBJECT_IDENTIFIER','new_method',1,'p_new_method','classCheckerFile.py',221),
  ('new_variables_scope -> <empty>','new_variables_scope',0,'p_new_variables_scope','classCheckerFile.py',233),
  ('type -> TYPE_IDENTIFIER','type',1,'p_type','classCheckerFile.py',237),
  ('type -> INT32','type',1,'p_type','classCheckerFile.py',238),
  ('type -> BOOL','type',1,'p_type','classCheckerFile.py',239),
  ('type -> STRING','type',1,'p_type','classCheckerFile.py',240),
  ('type -> UNIT','type',1,'p_type','classCheckerFile.py',241),
  ('formals -> formal','formals',1,'p_formals','classCheckerFile.py',245),
  ('formals -> formals COMMA formal','formals',3,'p_formals','classCheckerFile.py',246),
  ('formals -> <empty>','formals',0,'p_formals','classCheckerFile.py',247),
  ('formal -> OBJECT_IDENTIFIER COLON type','formal',3,'p_formal','classCheckerFile.py',256),
  ('block -> LBRACE check_block new_variables_scope inblock RBRACE','block',5,'p_block','classCheckerFile.py',268),
  ('check_block -> <empty>','check_block',0,'p_check_block','classCheckerFile.py',273),
  ('inblock -> inblock SEMICOLON expression','inblock',3,'p_block_inside','classCheckerFile.py',278),
  ('inblock -> expression','inblock',1,'p_block_inside','classCheckerFile.py',279),
  ('inblock -> <empty>','inblock',0,'p_block_inside','classCheckerFile.py',280),
  ('inblock -> inblock error','inblock',2,'p_block_error','classCheckerFile.py',289),
  ('expression -> new_variables_scope IF expression THEN expression','expression',5,'p_if','classCheckerFile.py',294),
  ('expression -> new_variables_scope IF expression THEN expression ELSE expression','expression',7,'p_if','classCheckerFile.py',295),
  ('expression -> WHILE expression DO expression','expression',4,'p_while','classCheckerFile.py',302),
  ('expression -> LET let_type IN expression','expression',4,'p_let','classCheckerFile.py',306),
  ('expression -> LET let_type ASSIGN expression IN expression','expression',6,'p_let','classCheckerFile.py',307),
  ('let_type -> OBJECT_IDENTIFIER COLON type','let_type',3,'p_let_type','classCheckerFile.py',314),
  ('expression -> OBJECT_IDENTIFIER ASSIGN expression','expression',3,'p_assign','classCheckerFile.py',319),
  ('expression -> NOT expression check_bool','expression',3,'p_unary_operators','classCheckerFile.py',323),
  ('expression -> MINUS expression check_int','expression',3,'p_unary_operators','classCheckerFile.py',324),
  ('check_int -> <empty>','check_int',0,'p_check_int','classCheckerFile.py',328),
  ('check_bool -> <empty>','check_bool',0,'p_check_bool','classCheckerFile.py',332),
  ('expression -> ISNULL expression','expression',2,'p_unary_isnull','classCheckerFile.py',336),
  ('expression -> expression PLUS expression','expression',3,'p_binary_operators','classCheckerFile.py',340),
  ('expression -> expression MINUS expression','expression',3,'p_binary_operators','classCheckerFile.py',341),
  ('expression -> expression TIMES expression','expression',3,'p_binary_operators','classCheckerFile.py',342),
  ('expression -> expression DIV expression','expression',3,'p_binary_operators','classCheckerFile.py',343),
  ('expression -> expression EQUAL expression','expression',3,'p_binary_operators','classCheckerFile.py',344),
  ('expression -> expression LOWER_EQUAL expression','expression',3,'p_binary_operators','classCheckerFile.py',345),
  ('expression -> expression LOWER expression','expression',3,'p_binary_operators','classCheckerFile.py',346),
  ('expression -> expression POW expression','expression',3,'p_binary_operators','classCheckerFile.py',347),
  ('expression -> expression AND expression','expression',3,'p_binary_operators','classCheckerFile.py',348),
  ('expression -> OBJECT_IDENTIFIER LPAR args RPAR','expression',4,'p_object_call','classCheckerFile.py',353),
  ('expression -> expression DOT OBJECT_IDENTIFIER LPAR args RPAR','expression',6,'p_object_call','classCheckerFile.py',354),
  ('expression -> NEW TYPE_IDENTIFIER','expression',2,'p_new_type','classCheckerFile.py',362),
  ('expression -> OBJECT_IDENTIFIER','expression',1,'p_expression_object','classCheckerFile.py',366),
  ('expression -> SELF','expression',1,'p_expression_self','classCheckerFile.py',370),
  ('expression -> literal','expression',1,'p_expression_literal','classCheckerFile.py',374),
  ('expression -> LPAR RPAR','expression',2,'p_par_alone','classCheckerFile.py',378),
  ('expression -> LPAR expression RPAR','expression',3,'p_par_expression','classCheckerFile.py',382),
  ('expression -> LPAR expression error','expression',3,'p_par_error','classCheckerFile.py',386),
  ('expression -> error expression RPAR','expression',3,'p_par_error','classCheckerFile.py',387),
  ('expression -> block','expression',1,'p_expression_block','classCheckerFile.py',392),
  ('expression -> error','expression',1,'p_expression_error','classCheckerFile.py',396),
  ('expression -> IF expression THEN expression SEMICOLON error','expression',6,'p_expression_error','classCheckerFile.py',397),
  ('args -> args COMMA expression','args',3,'p_args','classCheckerFile.py',405),
  ('args -> expression','args',1,'p_args','classCheckerFile.py',406),
  ('args -> <empty>','args',0,'p_args','classCheckerFile.py',407),
  ('literal -> literal_integer','literal',1,'p_literal','classCheckerFile.py',416),
  ('literal -> literal_string','literal',1,'p_literal','classCheckerFile.py',417),
  ('literal -> boolean-literal','literal',1,'p_literal','classCheckerFile.py',418),
  ('literal_string -> string_literal','literal_string',1,'p_literal_string','classCheckerFile.py',422),
  ('literal_integer -> INTEGER_LITERAL','literal_integer',1,'p_literal_integer','classCheckerFile.py',426),
  ('boolean-literal -> TRUE','boolean-literal',1,'p_boolean_literal','classCheckerFile.py',430),
  ('boolean-literal -> FALSE','boolean-literal',1,'p_boolean_literal','classCheckerFile.py',431),
]
