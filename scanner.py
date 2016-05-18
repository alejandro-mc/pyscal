#scannner.py
#tokenizes Pascal code

import sys


#if __name__ == "__main__":


__CURRENT_TOKEN__ = []

__CURRENT_STATE__ = "initial"

__CURRENT_TOKEN_NAME__ = ""

__SPECIAL_CHARACTERS__ = [
"+",
"-",
"=",
"!",
"*",
"/",
".",
",",
";",
":",
"^",
"<",
">",
"|",
"'",
"(",
")",
"{",
"}",
"[",
"]"
]


__RESERVED_KEYWORDS__ = [
 "div",
 "mod",
 "nil",
 "in",
 "if",
 "then",
 "else",
 "case",
 "of",
 "repeat",
 "until",
 "while",
 "do",
 "for",
 "to",
 "downto",
 "begin",
 "end",
 "endprog",
 "with",
 "goto",
 "const",
 "var",
 "type",
 "array",
 "record",
 "set",
 "file",
 "function",
 "procedure",
 "label",
 "packed",
 "program",
 "writeln",
 "integer",
 "real"
]


def is_pecial_char(string):
    global __SPECIAL_CHARACTERS__
    return __SPECIAL_CHARACTERS__.count(string) > 0
        

def is_keyword(string):
    global __RESERVED_KEYWORDS__
    return __RESERVED_KEYWORDS__.count(string.lower()) > 0

def state_action_initial(character):
    global __CURRENT_STATE__
    global __CURRENT_TOKEN_NAME__
    character = character.lower()
    if character.isalpha():
       __CURRENT_STATE__ = "identifier"
       __CURRENT_TOKEN_NAME__ += character
       return 0#change1
    elif character.isdigit():
         __CURRENT_STATE__ = "unsigned int"
         __CURRENT_TOKEN_NAME__ += character
         return 0#change1
    elif character == "'":
         __CURRENT_STATE__ = "string"
         return 0#change1
    elif character == "{":
         __CURRENT_STATE__ = "comment"
         return 0#change1
    elif "!:<>.".count(character) > 0:
         __CURRENT_STATE__ = "twocharsymb"
         __CURRENT_TOKEN_NAME__ = character
         return 0 #change1
    elif character == "(":
         return ["leftparen", "("]
    elif character == ")":
         return ["rightparen",")"]
    elif character == "+":
         return ["opplus","+"]
    elif character == "-":
         return ["opminus","-"]
    elif character == "*":
         return ["opmul","*"]
    elif character == "=":
         return ["opeq","="]
    elif character == ";":
         return ["semicolon",";"]
    elif character == ",":
         return ["comma",","]
    else:
         return 0
    
def state_action_identifier(character):

    global __CURRENT_STATE__
    global __CURRENT_TOKEN_NAME__
    character = character.lower()
    if character.isalpha() | character.isdigit():
       __CURRENT_TOKEN_NAME__ += character
       return 0#change1
    else:
       temp = __CURRENT_TOKEN_NAME__
       __CURRENT_STATE__ = "initial"
       __CURRENT_TOKEN_NAME__ = ""

       if is_keyword(temp):
          return ["keyword",temp]

       else:  
          return ["identifier",temp]

def state_action_unsigned_int(character):
    
    global __CURRENT_STATE__
    global __CURRENT_TOKEN_NAME__

    if character.isdigit():
       __CURRENT_TOKEN_NAME__ += character
       return 0#change1
    elif character == ".":
       __CURRENT_STATE__ = "unsigned real"
       __CURRENT_TOKEN_NAME__ += character
       return 0#change
    elif character.isalpha():
       __CURRENT_STATE__ = "error"
       return 0 #change
    else:
       temp = __CURRENT_TOKEN_NAME__
       __CURRENT_TOKEN_NAME__ = ""
       __CURRENT_STATE__ = "initial"
       return ["unsigned int",temp]

def state_action_unsigned_real(character):
    global __CURRENT_STATE__
    global __CURRENT_TOKEN_NAME__

    if character.isdigit():
       __CURRENT_TOKEN_NAME__ += character
       return 0#change
    elif character.isalpha():
       __CURRENT_STATE__ = "error"
       return 0 #change
    else: 
       temp = __CURRENT_TOKEN_NAME__
       __CURRENT_TOKEN_NAME__ = ""
       __CURRENT_STATE__ = "initial"
       return ["unsigned real",temp]

def state_action_string(character):
 
    global __CURRENT_STATE__
    global __CURRENT_TOKEN_NAME__

    if character != "'":
       __CURRENT_TOKEN_NAME__ += character
       return 0 #change
    else:

       temp = __CURRENT_TOKEN_NAME__
       __CURRENT_TOKEN_NAME__ = ""
       __CURRENT_STATE__ = "initial"
       return ["string",temp]

def state_action_comment(character):
    
    global __CURRENT_STATE__
    global __CURRENT_TOKEN_NAME__

    if character == "}":
       __CURRENT_STATE__ = "initial"
       __CURRENT_TOKEN_NAME__ = ""
       return 0
    else:
       return 0 

def state_action_twocharsymb(character):

    global __CURRENT_STATE__
    global __CURRENT_TOKEN_NAME__

    if character == "=":
       if __CURRENT_TOKEN_NAME__ == ":":
          __CURRENT_STATE__ = "initial"
          __CURRENT_TOKEN_NAME__ = ""
          return ["opassign",":="]

       elif __CURRENT_TOKEN_NAME__ == "!":
            __CURRENT_STATE__ = "initial"
            __CURRENT_TOKEN_NAME__ = ""
            return ["opnoteq","!="]

       elif __CURRENT_TOKEN_NAME__ == "<":
            __CURRENT_STATE__ = "initial"
            __CURRENT_TOKEN_NAME__ = ""
            return ["opleq","<="]

       elif __CURRENT_TOKEN_NAME__ == ">":
            __CURRENT_STATE__ = "initial"
            __CURRENT_TOKEN_NAME__ = ""
            return ["opgeq",">="]

    elif character == ".":
         if __CURRENT_TOKEN_NAME__ == ".":
            __CURRENT_TOKEN_NAME__ = ""
            return ["oprange",".."]
         else:
            __CURRENT_STATE__ = "error"
            return 0
       
    else:
       if __CURRENT_TOKEN_NAME__ == "!":
          
          __CURRENT_STATE__ = "error"
          return 0 #change
          
       elif __CURRENT_TOKEN_NAME__ == "<":
            __CURRENT_STATE__ = "initial"
            __CURRENT_TOKEN_NAME__ = ""
            return ["opless","<"] 
       elif __CURRENT_TOKEN_NAME__ == ">":
            __CURRENT_STATE__ = "initial"
            __CURRENT_TOKEN_NAME__ = ""
            return ["opgreater",">"]  
       elif __CURRENT_TOKEN_NAME__ == ":":
            __CURRENT_STATE__ = "initial"
            __CURRENT_TOKEN_NAME__ = ""
            return ["colon",":"]

def state_action_error(character):
    return ["invalidtoken",""]


states = { 

"initial":state_action_initial,
"identifier":state_action_identifier,
"unsigned int":state_action_unsigned_int,
"unsigned real":state_action_unsigned_real,
"string":state_action_string,
"comment":state_action_comment,
"twocharsymb":state_action_twocharsymb,
"error":state_action_error,

}


#PRE: filein is a text file
#POST: returns the next character to be read in the file
def char_peek (filein):
    pos = filein.tell()
    char = filein.read(1)
    filein.seek(pos)
    return char
        


#PRE: filein is a text file
#POST: a file is written to the directory where python
#      file is 
#Implementation details
#token is of the form [tokentype,tokenname] 
def tokenize (filein,str_tokenfilename):
    #open output file for write
    file_out = open(str_tokenfilename,"w")
    while char_peek(filein) != "":
          token = states[__CURRENT_STATE__](filein.read(1))
          #if a new token was output write it to fie_out

#PRE: fi is  file object
def get_token(filein):
    global __CURRENT_STATE__
    global __CURRENT_TOKEN__
    token = 0
    while token == 0:
          pos = filein.tell()
          token = states[__CURRENT_STATE__](filein.read(1))
    if token[0] in ["keyword","identifier","unsigned int","unsigned real"]:
       filein.seek(pos)#reset file pointer for tokens that require
                       #look ahead 
    __CURRENT_TOKEN__ = token
    return token
