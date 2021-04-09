
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'initrightASSIGNleftANDrightNOTnonassocLOWEREQUALLOWER_EQUALleftPLUSMINUSleftTIMESDIVrightISNULLUMINUSrightPOWleftDOTAND ASSIGN BOOL CLASS COLON COMMA DIV DO DOT ELSE EQUAL EXTENDS FALSE IF IN INT32 INTEGER_LITERAL ISNULL LBRACE LET LOWER LOWER_EQUAL LPAR MINUS NEW NOT OBJECT_IDENTIFIER PLUS POW RBRACE RPAR SELF SEMICOLON STRING THEN TIMES TRUE TYPE_IDENTIFIER UNIT WHILE string_literalinit : programprogram : program class\n                    | classclass : field\n                | methodclass : CLASS errorclass : expression\n                | TYPE_IDENTIFIER\n                | blockclass : CLASS new_class_scope class-body\n                | CLASS new_class_scope EXTENDS TYPE_IDENTIFIER class-bodynew_class_scope : TYPE_IDENTIFIERclass-body : LBRACE class-body-in RBRACEclass-body : LBRACE class-body-in errorclass-body-in : class-body-in fieldclass-body-in : class-body-in methodclass-body-in : field : OBJECT_IDENTIFIER COLON type SEMICOLON\n                | OBJECT_IDENTIFIER COLON type ASSIGN expression SEMICOLONmethod : OBJECT_IDENTIFIER new_variables_scope LPAR formals RPAR COLON type blocknew_variables_scope :type : TYPE_IDENTIFIER\n                | INT32\n                | BOOL\n                | STRING\n                | UNIT formals : formal\n                | formals COMMA formal\n                | formal : OBJECT_IDENTIFIER COLON typeblock : LBRACE new_variables_scope inblock RBRACEinblock : inblock SEMICOLON expression\n                | expression\n                |inblock : inblock error expression : IF expression THEN expression\n                    | IF expression THEN expression ELSE expressionexpression : WHILE expression DO expressionexpression : LET OBJECT_IDENTIFIER COLON type IN expression\n                    | LET OBJECT_IDENTIFIER COLON type ASSIGN expression IN expressionexpression : OBJECT_IDENTIFIER ASSIGN expressionexpression : NOT expression\n                    | MINUS expression %prec UMINUS\n                    | ISNULL expressionexpression : expression PLUS expression\n                  | expression MINUS expression\n                  | expression TIMES expression\n                  | expression DIV expression\n                  | expression EQUAL expression\n                  | expression LOWER_EQUAL expression\n                  | expression LOWER expression\n                  | expression POW expression\n                  | expression AND expressionexpression : OBJECT_IDENTIFIER LPAR args RPAR\n                    | expression DOT OBJECT_IDENTIFIER LPAR args RPARexpression : NEW TYPE_IDENTIFIERexpression : OBJECT_IDENTIFIERexpression : SELFexpression : literalexpression : LPAR RPARexpression : LPAR expression RPARexpression : LPAR expression error\n                    | error expression RPARexpression : blockexpression : error\n                    | IF expression THEN expression SEMICOLON errorargs : args COMMA expression\n                | expression\n                |literal : INTEGER_LITERAL\n                | string_literal\n                | boolean-literalboolean-literal : TRUE \n                        | FALSE'
    
_lr_action_items = {'CLASS':([0,2,3,4,5,7,8,9,10,11,20,21,23,24,25,26,27,28,29,33,34,49,54,55,56,57,59,62,63,64,65,66,67,68,69,70,71,79,83,84,93,98,100,101,103,106,107,108,123,124,128,129,130,134,135,],[6,6,-3,-4,-5,-65,-7,-8,-9,-57,-58,-59,-70,-71,-72,-73,-74,-2,-6,-57,-64,-60,-42,-43,-44,-56,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,-18,-54,-36,-38,-31,-11,-13,-14,-55,-19,-37,-66,-39,-20,-40,]),'TYPE_IDENTIFIER':([0,2,3,4,5,6,7,8,9,10,11,19,20,21,23,24,25,26,27,28,29,33,34,45,49,54,55,56,57,59,60,62,63,64,65,66,67,68,69,70,71,79,83,84,87,93,98,100,101,103,106,107,108,114,123,124,126,128,129,130,134,135,],[9,9,-3,-4,-5,31,-65,-7,-8,-9,-57,57,-58,-59,-70,-71,-72,-73,-74,-2,-6,-57,-64,74,-60,-42,-43,-44,-56,-10,90,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,74,-18,-54,-36,-38,-31,-11,-13,-14,74,-55,-19,74,-37,-66,-39,-20,-40,]),'OBJECT_IDENTIFIER':([0,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,20,21,22,23,24,25,26,27,28,29,33,34,35,36,37,38,39,40,41,42,43,44,46,48,49,54,55,56,57,58,59,61,62,63,64,65,66,67,68,69,70,71,79,80,83,84,85,86,91,92,93,94,98,99,100,101,103,104,106,107,108,109,110,116,118,120,121,123,124,128,129,130,133,134,135,],[11,11,-3,-4,-5,33,-7,-8,-9,-57,33,33,33,53,33,33,33,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,-57,-64,33,33,33,33,33,33,33,33,33,72,33,33,-60,-42,-43,-44,-56,33,-10,-17,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,95,-61,-62,33,33,111,33,-18,33,-54,33,-36,-38,-31,33,-11,-13,-14,-15,-16,95,33,33,33,-55,-19,-37,-66,-39,33,-20,-40,]),'IF':([0,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,33,34,35,36,37,38,39,40,41,42,43,46,48,49,54,55,56,57,58,59,62,63,64,65,66,67,68,69,70,71,79,83,84,85,86,92,93,94,98,99,100,101,103,104,106,107,108,118,120,121,123,124,128,129,130,133,134,135,],[13,13,-3,-4,-5,13,-7,-8,-9,-57,13,13,13,13,13,13,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,-57,-64,13,13,13,13,13,13,13,13,13,13,13,-60,-42,-43,-44,-56,13,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,13,13,13,-18,13,-54,13,-36,-38,-31,13,-11,-13,-14,13,13,13,-55,-19,-37,-66,-39,13,-20,-40,]),'WHILE':([0,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,33,34,35,36,37,38,39,40,41,42,43,46,48,49,54,55,56,57,58,59,62,63,64,65,66,67,68,69,70,71,79,83,84,85,86,92,93,94,98,99,100,101,103,104,106,107,108,118,120,121,123,124,128,129,130,133,134,135,],[14,14,-3,-4,-5,14,-7,-8,-9,-57,14,14,14,14,14,14,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,-57,-64,14,14,14,14,14,14,14,14,14,14,14,-60,-42,-43,-44,-56,14,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,14,14,14,-18,14,-54,14,-36,-38,-31,14,-11,-13,-14,14,14,14,-55,-19,-37,-66,-39,14,-20,-40,]),'LET':([0,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,33,34,35,36,37,38,39,40,41,42,43,46,48,49,54,55,56,57,58,59,62,63,64,65,66,67,68,69,70,71,79,83,84,85,86,92,93,94,98,99,100,101,103,104,106,107,108,118,120,121,123,124,128,129,130,133,134,135,],[15,15,-3,-4,-5,15,-7,-8,-9,-57,15,15,15,15,15,15,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,-57,-64,15,15,15,15,15,15,15,15,15,15,15,-60,-42,-43,-44,-56,15,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,15,15,15,-18,15,-54,15,-36,-38,-31,15,-11,-13,-14,15,15,15,-55,-19,-37,-66,-39,15,-20,-40,]),'NOT':([0,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,33,34,35,36,37,38,39,40,41,42,43,46,48,49,54,55,56,57,58,59,62,63,64,65,66,67,68,69,70,71,79,83,84,85,86,92,93,94,98,99,100,101,103,104,106,107,108,118,120,121,123,124,128,129,130,133,134,135,],[16,16,-3,-4,-5,16,-7,-8,-9,-57,16,16,16,16,16,16,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,-57,-64,16,16,16,16,16,16,16,16,16,16,16,-60,-42,-43,-44,-56,16,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,16,16,16,-18,16,-54,16,-36,-38,-31,16,-11,-13,-14,16,16,16,-55,-19,-37,-66,-39,16,-20,-40,]),'MINUS':([0,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,32,33,34,35,36,37,38,39,40,41,42,43,46,48,49,50,51,52,54,55,56,57,58,59,62,63,64,65,66,67,68,69,70,71,79,82,83,84,85,86,89,92,93,94,98,99,100,101,103,104,106,107,108,113,117,118,120,121,122,123,124,128,129,130,131,133,134,135,],[17,17,-3,-4,-5,17,36,-8,-9,-57,17,17,17,17,17,17,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,36,-57,-64,17,17,17,17,17,17,17,17,17,17,17,-60,36,36,36,36,-43,-44,-56,17,-10,-63,-45,-46,-47,-48,36,36,36,-52,36,36,36,-61,-62,17,17,36,17,-18,17,-54,17,36,36,-31,17,-11,-13,-14,36,36,17,17,17,36,-55,-19,36,-66,36,36,17,-20,36,]),'ISNULL':([0,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,33,34,35,36,37,38,39,40,41,42,43,46,48,49,54,55,56,57,58,59,62,63,64,65,66,67,68,69,70,71,79,83,84,85,86,92,93,94,98,99,100,101,103,104,106,107,108,118,120,121,123,124,128,129,130,133,134,135,],[18,18,-3,-4,-5,18,-7,-8,-9,-57,18,18,18,18,18,18,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,-57,-64,18,18,18,18,18,18,18,18,18,18,18,-60,-42,-43,-44,-56,18,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,18,18,18,-18,18,-54,18,-36,-38,-31,18,-11,-13,-14,18,18,18,-55,-19,-37,-66,-39,18,-20,-40,]),'NEW':([0,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,33,34,35,36,37,38,39,40,41,42,43,46,48,49,54,55,56,57,58,59,62,63,64,65,66,67,68,69,70,71,79,83,84,85,86,92,93,94,98,99,100,101,103,104,106,107,108,118,120,121,123,124,128,129,130,133,134,135,],[19,19,-3,-4,-5,19,-7,-8,-9,-57,19,19,19,19,19,19,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,-57,-64,19,19,19,19,19,19,19,19,19,19,19,-60,-42,-43,-44,-56,19,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,19,19,19,-18,19,-54,19,-36,-38,-31,19,-11,-13,-14,19,19,19,-55,-19,-37,-66,-39,19,-20,-40,]),'SELF':([0,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,33,34,35,36,37,38,39,40,41,42,43,46,48,49,54,55,56,57,58,59,62,63,64,65,66,67,68,69,70,71,79,83,84,85,86,92,93,94,98,99,100,101,103,104,106,107,108,118,120,121,123,124,128,129,130,133,134,135,],[20,20,-3,-4,-5,20,-7,-8,-9,-57,20,20,20,20,20,20,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,-57,-64,20,20,20,20,20,20,20,20,20,20,20,-60,-42,-43,-44,-56,20,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,20,20,20,-18,20,-54,20,-36,-38,-31,20,-11,-13,-14,20,20,20,-55,-19,-37,-66,-39,20,-20,-40,]),'LPAR':([0,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,33,34,35,36,37,38,39,40,41,42,43,46,47,48,49,54,55,56,57,58,59,62,63,64,65,66,67,68,69,70,71,72,79,83,84,85,86,92,93,94,98,99,100,101,103,104,106,107,108,111,118,120,121,123,124,128,129,130,133,134,135,],[12,12,-3,-4,-5,12,-7,-8,-9,48,12,12,12,12,12,12,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,48,-64,12,12,12,12,12,12,12,12,12,12,80,12,-60,-42,-43,-44,-56,12,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,92,-41,-61,-62,12,12,12,-18,12,-54,12,-36,-38,-31,12,-11,-13,-14,-21,12,12,12,-55,-19,-37,-66,-39,12,-20,-40,]),'error':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,33,34,35,36,37,38,39,40,41,42,43,46,48,49,50,54,55,56,57,58,59,61,62,63,64,65,66,67,68,69,70,71,79,83,84,85,86,88,89,91,92,93,94,98,99,100,101,103,104,105,106,107,108,109,110,118,119,120,121,122,123,124,128,129,130,133,134,135,],[7,7,-3,-4,-5,29,7,-7,-8,-9,-57,7,7,7,7,7,7,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,-57,-64,7,7,7,7,7,7,7,7,7,7,7,-60,84,-42,-43,-44,-56,7,-10,-17,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,7,7,105,-33,108,7,-18,7,-54,7,-36,-38,-31,7,-35,-11,-13,-14,-15,-16,7,129,7,7,-32,-55,-19,-37,-66,-39,7,-20,-40,]),'LBRACE':([0,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37,38,39,40,41,42,43,46,48,49,54,55,56,57,58,59,62,63,64,65,66,67,68,69,70,71,74,75,76,77,78,79,83,84,85,86,90,92,93,94,98,99,100,101,103,104,106,107,108,118,120,121,123,124,128,129,130,132,133,134,135,],[22,22,-3,-4,-5,22,-7,-8,-9,-57,22,22,22,22,22,22,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,61,-12,-57,-64,22,22,22,22,22,22,22,22,22,22,22,-60,-42,-43,-44,-56,22,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-22,-23,-24,-25,-26,-41,-61,-62,22,22,61,22,-18,22,-54,22,-36,-38,-31,22,-11,-13,-14,22,22,22,-55,-19,-37,-66,-39,22,22,-20,-40,]),'INTEGER_LITERAL':([0,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,33,34,35,36,37,38,39,40,41,42,43,46,48,49,54,55,56,57,58,59,62,63,64,65,66,67,68,69,70,71,79,83,84,85,86,92,93,94,98,99,100,101,103,104,106,107,108,118,120,121,123,124,128,129,130,133,134,135,],[23,23,-3,-4,-5,23,-7,-8,-9,-57,23,23,23,23,23,23,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,-57,-64,23,23,23,23,23,23,23,23,23,23,23,-60,-42,-43,-44,-56,23,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,23,23,23,-18,23,-54,23,-36,-38,-31,23,-11,-13,-14,23,23,23,-55,-19,-37,-66,-39,23,-20,-40,]),'string_literal':([0,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,33,34,35,36,37,38,39,40,41,42,43,46,48,49,54,55,56,57,58,59,62,63,64,65,66,67,68,69,70,71,79,83,84,85,86,92,93,94,98,99,100,101,103,104,106,107,108,118,120,121,123,124,128,129,130,133,134,135,],[24,24,-3,-4,-5,24,-7,-8,-9,-57,24,24,24,24,24,24,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,-57,-64,24,24,24,24,24,24,24,24,24,24,24,-60,-42,-43,-44,-56,24,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,24,24,24,-18,24,-54,24,-36,-38,-31,24,-11,-13,-14,24,24,24,-55,-19,-37,-66,-39,24,-20,-40,]),'TRUE':([0,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,33,34,35,36,37,38,39,40,41,42,43,46,48,49,54,55,56,57,58,59,62,63,64,65,66,67,68,69,70,71,79,83,84,85,86,92,93,94,98,99,100,101,103,104,106,107,108,118,120,121,123,124,128,129,130,133,134,135,],[26,26,-3,-4,-5,26,-7,-8,-9,-57,26,26,26,26,26,26,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,-57,-64,26,26,26,26,26,26,26,26,26,26,26,-60,-42,-43,-44,-56,26,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,26,26,26,-18,26,-54,26,-36,-38,-31,26,-11,-13,-14,26,26,26,-55,-19,-37,-66,-39,26,-20,-40,]),'FALSE':([0,2,3,4,5,7,8,9,10,11,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,33,34,35,36,37,38,39,40,41,42,43,46,48,49,54,55,56,57,58,59,62,63,64,65,66,67,68,69,70,71,79,83,84,85,86,92,93,94,98,99,100,101,103,104,106,107,108,118,120,121,123,124,128,129,130,133,134,135,],[27,27,-3,-4,-5,27,-7,-8,-9,-57,27,27,27,27,27,27,-58,-59,-21,-70,-71,-72,-73,-74,-2,-6,-57,-64,27,27,27,27,27,27,27,27,27,27,27,-60,-42,-43,-44,-56,27,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,27,27,27,-18,27,-54,27,-36,-38,-31,27,-11,-13,-14,27,27,27,-55,-19,-37,-66,-39,27,-20,-40,]),'$end':([1,2,3,4,5,7,8,9,10,11,20,21,23,24,25,26,27,28,29,33,34,49,54,55,56,57,59,62,63,64,65,66,67,68,69,70,71,79,83,84,93,98,100,101,103,106,107,108,123,124,128,129,130,134,135,],[0,-1,-3,-4,-5,-65,-7,-8,-9,-57,-58,-59,-70,-71,-72,-73,-74,-2,-6,-57,-64,-60,-42,-43,-44,-56,-10,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,-18,-54,-36,-38,-31,-11,-13,-14,-55,-19,-37,-66,-39,-20,-40,]),'PLUS':([7,8,10,11,20,21,23,24,25,26,27,32,33,34,49,50,51,52,54,55,56,57,62,63,64,65,66,67,68,69,70,71,79,82,83,84,89,98,100,101,103,113,117,122,123,128,129,130,131,135,],[-65,35,-64,-57,-58,-59,-70,-71,-72,-73,-74,35,-57,-64,-60,35,35,35,35,-43,-44,-56,-63,-45,-46,-47,-48,35,35,35,-52,35,35,35,-61,-62,35,-54,35,35,-31,35,35,35,-55,35,-66,35,35,35,]),'TIMES':([7,8,10,11,20,21,23,24,25,26,27,32,33,34,49,50,51,52,54,55,56,57,62,63,64,65,66,67,68,69,70,71,79,82,83,84,89,98,100,101,103,113,117,122,123,128,129,130,131,135,],[-65,37,-64,-57,-58,-59,-70,-71,-72,-73,-74,37,-57,-64,-60,37,37,37,37,-43,-44,-56,-63,37,37,-47,-48,37,37,37,-52,37,37,37,-61,-62,37,-54,37,37,-31,37,37,37,-55,37,-66,37,37,37,]),'DIV':([7,8,10,11,20,21,23,24,25,26,27,32,33,34,49,50,51,52,54,55,56,57,62,63,64,65,66,67,68,69,70,71,79,82,83,84,89,98,100,101,103,113,117,122,123,128,129,130,131,135,],[-65,38,-64,-57,-58,-59,-70,-71,-72,-73,-74,38,-57,-64,-60,38,38,38,38,-43,-44,-56,-63,38,38,-47,-48,38,38,38,-52,38,38,38,-61,-62,38,-54,38,38,-31,38,38,38,-55,38,-66,38,38,38,]),'EQUAL':([7,8,10,11,20,21,23,24,25,26,27,32,33,34,49,50,51,52,54,55,56,57,62,63,64,65,66,67,68,69,70,71,79,82,83,84,89,98,100,101,103,113,117,122,123,128,129,130,131,135,],[-65,39,-64,-57,-58,-59,-70,-71,-72,-73,-74,39,-57,-64,-60,39,39,39,39,-43,-44,-56,-63,-45,-46,-47,-48,None,None,None,-52,39,39,39,-61,-62,39,-54,39,39,-31,39,39,39,-55,39,-66,39,39,39,]),'LOWER_EQUAL':([7,8,10,11,20,21,23,24,25,26,27,32,33,34,49,50,51,52,54,55,56,57,62,63,64,65,66,67,68,69,70,71,79,82,83,84,89,98,100,101,103,113,117,122,123,128,129,130,131,135,],[-65,40,-64,-57,-58,-59,-70,-71,-72,-73,-74,40,-57,-64,-60,40,40,40,40,-43,-44,-56,-63,-45,-46,-47,-48,None,None,None,-52,40,40,40,-61,-62,40,-54,40,40,-31,40,40,40,-55,40,-66,40,40,40,]),'LOWER':([7,8,10,11,20,21,23,24,25,26,27,32,33,34,49,50,51,52,54,55,56,57,62,63,64,65,66,67,68,69,70,71,79,82,83,84,89,98,100,101,103,113,117,122,123,128,129,130,131,135,],[-65,41,-64,-57,-58,-59,-70,-71,-72,-73,-74,41,-57,-64,-60,41,41,41,41,-43,-44,-56,-63,-45,-46,-47,-48,None,None,None,-52,41,41,41,-61,-62,41,-54,41,41,-31,41,41,41,-55,41,-66,41,41,41,]),'POW':([7,8,10,11,20,21,23,24,25,26,27,32,33,34,49,50,51,52,54,55,56,57,62,63,64,65,66,67,68,69,70,71,79,82,83,84,89,98,100,101,103,113,117,122,123,128,129,130,131,135,],[-65,42,-64,-57,-58,-59,-70,-71,-72,-73,-74,42,-57,-64,-60,42,42,42,42,42,42,-56,-63,42,42,42,42,42,42,42,42,42,42,42,-61,-62,42,-54,42,42,-31,42,42,42,-55,42,-66,42,42,42,]),'AND':([7,8,10,11,20,21,23,24,25,26,27,32,33,34,49,50,51,52,54,55,56,57,62,63,64,65,66,67,68,69,70,71,79,82,83,84,89,98,100,101,103,113,117,122,123,128,129,130,131,135,],[-65,43,-64,-57,-58,-59,-70,-71,-72,-73,-74,43,-57,-64,-60,43,43,43,-42,-43,-44,-56,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,43,43,-61,-62,43,-54,43,43,-31,43,43,43,-55,43,-66,43,43,43,]),'DOT':([7,8,10,11,20,21,23,24,25,26,27,32,33,34,49,50,51,52,54,55,56,57,62,63,64,65,66,67,68,69,70,71,79,82,83,84,89,98,100,101,103,113,117,122,123,128,129,130,131,135,],[-65,44,-64,-57,-58,-59,-70,-71,-72,-73,-74,44,-57,-64,-60,44,44,44,44,44,44,-56,-63,44,44,44,44,44,44,44,44,44,44,44,-61,-62,44,-54,44,44,-31,44,44,44,-55,44,-66,44,44,44,]),'RPAR':([7,12,20,21,23,24,25,26,27,32,33,34,48,49,50,54,55,56,57,62,63,64,65,66,67,68,69,70,71,74,75,76,77,78,79,80,81,82,83,84,92,96,97,98,100,101,103,112,117,123,125,127,128,129,130,135,],[-65,49,-58,-59,-70,-71,-72,-73,-74,62,-57,-64,-69,-60,83,-42,-43,-44,-56,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-22,-23,-24,-25,-26,-41,-29,98,-68,-61,-62,-69,115,-27,-54,-36,-38,-31,123,-67,-55,-30,-28,-37,-66,-39,-40,]),'THEN':([7,20,21,23,24,25,26,27,33,34,49,51,54,55,56,57,62,63,64,65,66,67,68,69,70,71,79,83,84,98,100,101,103,123,128,129,130,135,],[-65,-58,-59,-70,-71,-72,-73,-74,-57,-64,-60,85,-42,-43,-44,-56,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,-54,-36,-38,-31,-55,-37,-66,-39,-40,]),'DO':([7,20,21,23,24,25,26,27,33,34,49,52,54,55,56,57,62,63,64,65,66,67,68,69,70,71,79,83,84,98,100,101,103,123,128,129,130,135,],[-65,-58,-59,-70,-71,-72,-73,-74,-57,-64,-60,86,-42,-43,-44,-56,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,-54,-36,-38,-31,-55,-37,-66,-39,-40,]),'COMMA':([7,20,21,23,24,25,26,27,33,34,48,49,54,55,56,57,62,63,64,65,66,67,68,69,70,71,74,75,76,77,78,79,80,81,82,83,84,92,96,97,98,100,101,103,112,117,123,125,127,128,129,130,135,],[-65,-58,-59,-70,-71,-72,-73,-74,-57,-64,-69,-60,-42,-43,-44,-56,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-22,-23,-24,-25,-26,-41,-29,99,-68,-61,-62,-69,116,-27,-54,-36,-38,-31,99,-67,-55,-30,-28,-37,-66,-39,-40,]),'RBRACE':([7,20,21,22,23,24,25,26,27,33,34,49,54,55,56,57,58,61,62,63,64,65,66,67,68,69,70,71,79,83,84,88,89,91,93,98,100,101,103,105,109,110,122,123,124,128,129,130,134,135,],[-65,-58,-59,-21,-70,-71,-72,-73,-74,-57,-64,-60,-42,-43,-44,-56,-34,-17,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,103,-33,107,-18,-54,-36,-38,-31,-35,-15,-16,-32,-55,-19,-37,-66,-39,-20,-40,]),'SEMICOLON':([7,20,21,22,23,24,25,26,27,33,34,49,54,55,56,57,58,62,63,64,65,66,67,68,69,70,71,73,74,75,76,77,78,79,83,84,88,89,98,100,101,103,105,113,122,123,128,129,130,135,],[-65,-58,-59,-21,-70,-71,-72,-73,-74,-57,-64,-60,-42,-43,-44,-56,-34,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,93,-22,-23,-24,-25,-26,-41,-61,-62,104,-33,-54,119,-38,-31,-35,124,-32,-55,-37,-66,-39,-40,]),'ELSE':([7,20,21,23,24,25,26,27,33,34,49,54,55,56,57,62,63,64,65,66,67,68,69,70,71,79,83,84,98,100,101,103,123,128,129,130,135,],[-65,-58,-59,-70,-71,-72,-73,-74,-57,-64,-60,-42,-43,-44,-56,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-41,-61,-62,-54,118,-38,-31,-55,-37,-66,-39,-40,]),'IN':([7,20,21,23,24,25,26,27,33,34,49,54,55,56,57,62,63,64,65,66,67,68,69,70,71,74,75,76,77,78,79,83,84,98,100,101,102,103,123,128,129,130,131,135,],[-65,-58,-59,-70,-71,-72,-73,-74,-57,-64,-60,-42,-43,-44,-56,-63,-45,-46,-47,-48,-49,-50,-51,-52,-53,-22,-23,-24,-25,-26,-41,-61,-62,-54,-36,-38,120,-31,-55,-37,-66,-39,133,-40,]),'COLON':([11,53,95,111,115,],[45,87,114,45,126,]),'ASSIGN':([11,33,73,74,75,76,77,78,102,],[46,46,94,-22,-23,-24,-25,-26,121,]),'EXTENDS':([30,31,],[60,-12,]),'INT32':([45,87,114,126,],[75,75,75,75,]),'BOOL':([45,87,114,126,],[76,76,76,76,]),'STRING':([45,87,114,126,],[77,77,77,77,]),'UNIT':([45,87,114,126,],[78,78,78,78,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'init':([0,],[1,]),'program':([0,],[2,]),'class':([0,2,],[3,28,]),'field':([0,2,91,],[4,4,109,]),'method':([0,2,91,],[5,5,110,]),'expression':([0,2,7,12,13,14,16,17,18,35,36,37,38,39,40,41,42,43,46,48,58,85,86,92,94,99,104,118,120,121,133,],[8,8,32,50,51,52,54,55,56,63,64,65,66,67,68,69,70,71,79,82,89,100,101,82,113,117,122,128,130,131,135,]),'block':([0,2,7,12,13,14,16,17,18,35,36,37,38,39,40,41,42,43,46,48,58,85,86,92,94,99,104,118,120,121,132,133,],[10,10,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,134,34,]),'literal':([0,2,7,12,13,14,16,17,18,35,36,37,38,39,40,41,42,43,46,48,58,85,86,92,94,99,104,118,120,121,133,],[21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,]),'boolean-literal':([0,2,7,12,13,14,16,17,18,35,36,37,38,39,40,41,42,43,46,48,58,85,86,92,94,99,104,118,120,121,133,],[25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,]),'new_class_scope':([6,],[30,]),'new_variables_scope':([11,22,111,],[47,58,47,]),'class-body':([30,90,],[59,106,]),'type':([45,87,114,126,],[73,102,125,132,]),'args':([48,92,],[81,112,]),'inblock':([58,],[88,]),'class-body-in':([61,],[91,]),'formals':([80,],[96,]),'formal':([80,116,],[97,127,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> init","S'",1,None,None,None),
  ('init -> program','init',1,'p_init','parserFile.py',91),
  ('program -> program class','program',2,'p_program','parserFile.py',95),
  ('program -> class','program',1,'p_program','parserFile.py',96),
  ('class -> field','class',1,'p_field_method_error','parserFile.py',103),
  ('class -> method','class',1,'p_field_method_error','parserFile.py',104),
  ('class -> CLASS error','class',2,'p_class_error','parserFile.py',110),
  ('class -> expression','class',1,'p_general_class_error','parserFile.py',115),
  ('class -> TYPE_IDENTIFIER','class',1,'p_general_class_error','parserFile.py',116),
  ('class -> block','class',1,'p_general_class_error','parserFile.py',117),
  ('class -> CLASS new_class_scope class-body','class',3,'p_class','parserFile.py',123),
  ('class -> CLASS new_class_scope EXTENDS TYPE_IDENTIFIER class-body','class',5,'p_class','parserFile.py',124),
  ('new_class_scope -> TYPE_IDENTIFIER','new_class_scope',1,'p_new_class_scope','parserFile.py',135),
  ('class-body -> LBRACE class-body-in RBRACE','class-body',3,'p_class_body','parserFile.py',141),
  ('class-body -> LBRACE class-body-in error','class-body',3,'p_class_braces_error','parserFile.py',145),
  ('class-body-in -> class-body-in field','class-body-in',2,'p_class_body_field','parserFile.py',150),
  ('class-body-in -> class-body-in method','class-body-in',2,'p_class_body_method','parserFile.py',155),
  ('class-body-in -> <empty>','class-body-in',0,'p_class_body_empty','parserFile.py',160),
  ('field -> OBJECT_IDENTIFIER COLON type SEMICOLON','field',4,'p_field','parserFile.py',164),
  ('field -> OBJECT_IDENTIFIER COLON type ASSIGN expression SEMICOLON','field',6,'p_field','parserFile.py',165),
  ('method -> OBJECT_IDENTIFIER new_variables_scope LPAR formals RPAR COLON type block','method',8,'p_method','parserFile.py',174),
  ('new_variables_scope -> <empty>','new_variables_scope',0,'p_new_variables_scope','parserFile.py',179),
  ('type -> TYPE_IDENTIFIER','type',1,'p_type','parserFile.py',185),
  ('type -> INT32','type',1,'p_type','parserFile.py',186),
  ('type -> BOOL','type',1,'p_type','parserFile.py',187),
  ('type -> STRING','type',1,'p_type','parserFile.py',188),
  ('type -> UNIT','type',1,'p_type','parserFile.py',189),
  ('formals -> formal','formals',1,'p_formals','parserFile.py',193),
  ('formals -> formals COMMA formal','formals',3,'p_formals','parserFile.py',194),
  ('formals -> <empty>','formals',0,'p_formals','parserFile.py',195),
  ('formal -> OBJECT_IDENTIFIER COLON type','formal',3,'p_formal','parserFile.py',204),
  ('block -> LBRACE new_variables_scope inblock RBRACE','block',4,'p_block','parserFile.py',209),
  ('inblock -> inblock SEMICOLON expression','inblock',3,'p_block_inside','parserFile.py',215),
  ('inblock -> expression','inblock',1,'p_block_inside','parserFile.py',216),
  ('inblock -> <empty>','inblock',0,'p_block_inside','parserFile.py',217),
  ('inblock -> inblock error','inblock',2,'p_block_error','parserFile.py',226),
  ('expression -> IF expression THEN expression','expression',4,'p_if','parserFile.py',231),
  ('expression -> IF expression THEN expression ELSE expression','expression',6,'p_if','parserFile.py',232),
  ('expression -> WHILE expression DO expression','expression',4,'p_while','parserFile.py',239),
  ('expression -> LET OBJECT_IDENTIFIER COLON type IN expression','expression',6,'p_let','parserFile.py',243),
  ('expression -> LET OBJECT_IDENTIFIER COLON type ASSIGN expression IN expression','expression',8,'p_let','parserFile.py',244),
  ('expression -> OBJECT_IDENTIFIER ASSIGN expression','expression',3,'p_assign','parserFile.py',253),
  ('expression -> NOT expression','expression',2,'p_unary_operators','parserFile.py',257),
  ('expression -> MINUS expression','expression',2,'p_unary_operators','parserFile.py',258),
  ('expression -> ISNULL expression','expression',2,'p_unary_operators','parserFile.py',259),
  ('expression -> expression PLUS expression','expression',3,'p_binary_operators','parserFile.py',263),
  ('expression -> expression MINUS expression','expression',3,'p_binary_operators','parserFile.py',264),
  ('expression -> expression TIMES expression','expression',3,'p_binary_operators','parserFile.py',265),
  ('expression -> expression DIV expression','expression',3,'p_binary_operators','parserFile.py',266),
  ('expression -> expression EQUAL expression','expression',3,'p_binary_operators','parserFile.py',267),
  ('expression -> expression LOWER_EQUAL expression','expression',3,'p_binary_operators','parserFile.py',268),
  ('expression -> expression LOWER expression','expression',3,'p_binary_operators','parserFile.py',269),
  ('expression -> expression POW expression','expression',3,'p_binary_operators','parserFile.py',270),
  ('expression -> expression AND expression','expression',3,'p_binary_operators','parserFile.py',271),
  ('expression -> OBJECT_IDENTIFIER LPAR args RPAR','expression',4,'p_object_call','parserFile.py',276),
  ('expression -> expression DOT OBJECT_IDENTIFIER LPAR args RPAR','expression',6,'p_object_call','parserFile.py',277),
  ('expression -> NEW TYPE_IDENTIFIER','expression',2,'p_new_type','parserFile.py',284),
  ('expression -> OBJECT_IDENTIFIER','expression',1,'p_expression_object','parserFile.py',288),
  ('expression -> SELF','expression',1,'p_expression_self','parserFile.py',292),
  ('expression -> literal','expression',1,'p_expression_literal','parserFile.py',296),
  ('expression -> LPAR RPAR','expression',2,'p_par_alone','parserFile.py',300),
  ('expression -> LPAR expression RPAR','expression',3,'p_par_expression','parserFile.py',304),
  ('expression -> LPAR expression error','expression',3,'p_par_error','parserFile.py',308),
  ('expression -> error expression RPAR','expression',3,'p_par_error','parserFile.py',309),
  ('expression -> block','expression',1,'p_expression_block','parserFile.py',314),
  ('expression -> error','expression',1,'p_expression_error','parserFile.py',318),
  ('expression -> IF expression THEN expression SEMICOLON error','expression',6,'p_expression_error','parserFile.py',319),
  ('args -> args COMMA expression','args',3,'p_args','parserFile.py',327),
  ('args -> expression','args',1,'p_args','parserFile.py',328),
  ('args -> <empty>','args',0,'p_args','parserFile.py',329),
  ('literal -> INTEGER_LITERAL','literal',1,'p_literal','parserFile.py',338),
  ('literal -> string_literal','literal',1,'p_literal','parserFile.py',339),
  ('literal -> boolean-literal','literal',1,'p_literal','parserFile.py',340),
  ('boolean-literal -> TRUE','boolean-literal',1,'p_boolean_literal','parserFile.py',344),
  ('boolean-literal -> FALSE','boolean-literal',1,'p_boolean_literal','parserFile.py',345),
]
