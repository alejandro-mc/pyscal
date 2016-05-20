#parser.py
#Alejandro Morejon Cortina 2016

import scanner as sc
import sys

#try parsing test file


#required datastructures
symbtab = []      #symbol table this is very ineficient MUST CHANGE
lhs = ''
next_address=0    #memory address pointer
ip =0             #instruction pointer for now it's going to hold the index of the entry
                  #in the instruction list
instructions = [] #this instruction list is temporary eventually should write directly to bin


def addNewInstruction(instruction):
    '''
    instruction is of the form ["operation","parameter"]
    '''
    global ip
    global instructions
    instructions.append(instruction)
    ip += 1 #increment must change to the actual opcode size when dealing with real instructions

def write_instructions_to_file():
    global instructions
    for instruction in instructions:
      print(instruction)

def Program():
  global fi
  global instructions
  #import pdb; pdb.set_trace()
  sc.get_token(fi)
  #import pdb; pdb.set_trace()
  if sc.__CURRENT_TOKEN__ == ["keyword","program"]:
    match(["keyword","program"])
    match(["identifier",""])
    #import pdb; pdb.set_trace()
    match(["semicolon",";"])
    declarations()
    match(["keyword","begin"])#program begins
    #import pdb; pdb.set_trace()
    statements()
    match(["keyword","endprog"])#program ends
    addNewInstruction(["halt",""])#produce opcode to halt the program
    write_instructions_to_file()

def declarations():
    var_declarations()

def var_declarations():
    global next_address
    #import pdb; pdb.set_trace()
    if sc.__CURRENT_TOKEN__ == ["keyword","var"]:
      match(["keyword","var"])
    else:
      #import pdb;pdb.set_trace()
      #begin()
      return

    while True: #add variable names to the symbol table
      #import pdb; pdb.set_trace()
      if sc.__CURRENT_TOKEN__[0] == "identifier":
        new_symbtab_entry = {"name" : sc.__CURRENT_TOKEN__[1],
                             "type" : "empty",
                             "value": 0,
                             "address": next_address}
        symbtab.append(new_symbtab_entry)
        next_address += 4
        match(["identifier",""])
      #import pdb; pdb.set_trace()
      if sc.__CURRENT_TOKEN__ == ["comma",","]:
        match(["comma",","])
      #import pdb; pdb.set_trace()
      if sc.__CURRENT_TOKEN__ == ["colon",":"]:
        match(["colon",":"])
        break
    
    #add integer variable types
    if sc.__CURRENT_TOKEN__ == ["keyword","integer"]:
      for entry in symbtab:
        if entry['type'] == 'empty':
          entry['type'] = 'integer'
      match(["keyword","integer"])
    #add real varable types
    if sc.__CURRENT_TOKEN__ == ["keyword","real"]:
      for entry in symbtab:
        if entry['type'] == 'empty':
          entry['type'] = 'real'

    if sc.__CURRENT_TOKEN__ == ["semicolon",";"]:
      match(["semicolon",";"])

    var_declarations()

def begin():
  if sc.__CURRENT_TOKEN__ == ["keyword","begin"]:
    match(["keyword","begin"])
    while sc.__CURRENT_TOKEN__ != ["keyword","end"]:
      statements()


def statements():
  while True:
      statement()
      if sc.__CURRENT_TOKEN__ == ["keyword","endprog"]:
        return

def statement():
    global lhs

    if sc.__CURRENT_TOKEN__ == ["keyword","if"]:
      if_statement()
    #so far identifier is only found at the begining of asignments or array idexing
    if sc.__CURRENT_TOKEN__[0] == "identifier":
      lhs = sc.__CURRENT_TOKEN__[1]#save the identifier name
      match(["identifier",""])
      if sc.__CURRENT_TOKEN__ == ["opassign",":="]:
        match(["opassign",":="])
        Lexp()

        #after the code produced by Exp is evaluated
        #we must put the result from the top of the stack
        #in the correct mem location
        opstring = ["pop" , list(filter(lambda x: x['name'] == lhs,symbtab))[0]['address']]
        addNewInstruction(opstring)
        match(["semicolon",";"])


def if_statement():
  match(["keyword","if"])
  Lexp() #first we must evaluate the logical expression
         #when the expression is evaluated the result will be at the top of the stack
  match(["keyword","then"])
  #then we will jump to some address if the result is not true
  hole1 = ip #but first we must save ip because we don't know the jump address yet
  addNewInstruction(["jfalse",""]) #once we know the address we will add the parameter
  statement()

  #after the first statement we could have an else
  if sc.__CURRENT_TOKEN__ == ["keyword","else"]:
     match(["keyword","else"])

     #if there is an else the current instruction will be a jmp so we must
     #skip it that's why we have ip + 1
     instructions[hole1][1] = ip + 1

     #as before this is a jump forward so we must save the instruction
     #pointer to add the jump address later
     hole2 = ip
     addNewInstruction(["jmp",""])
     statement()
     instructions[hole2][1] = ip
  else:
     #if there is no else the program can continue executing
     #from the current instruction 
     instructions[hole1][1] = ip



    
######################
#EXPRESSION PARSING
######################

#GRAMMAR (Fixed to void left recursion)
# L  -> E L'
# L' -> < E L' | > E L' ....
# E  -> T E'
# E' -> + T E' | - T E' ...
# T  -> F T'
# T' -> * F T' | div F T' ...


def Lexp():
    Exp()
    Lprime()

def Lprime():
    if sc.__CURRENT_TOKEN__ == ["opless","<"]:
       match(["opless","<"])
       Exp()
       addNewInstruction(["less",""])
       Lprime()
    elif sc.__CURRENT_TOKEN__ == ["opgreater",">"]:
       match(["opgreater",">"])
       Exp()
       addNewInstruction(["greater",""])
       Lprime()
    elif sc.__CURRENT_TOKEN__ == ["opeq","="]:
       match(["opeq","="])
       Exp()
       addNewInstruction(["eq",""])
       Lprime()
    #must add the other cases later


def Exp():
    Term()
    Eprime()

def Eprime():
    if sc.__CURRENT_TOKEN__ == ["opplus","+"]:
       match(["opplus","+"])
       Term()
       addNewInstruction(["opadd",""])
       Eprime()
    elif sc.__CURRENT_TOKEN__ == ["opminus","-"]:
       mathc(["opminus","-"])
       Term()
       addNewInstruction(["opsub",""])
       Eprime()
 
def Term():
    Fact()
    Tprime()

def Tprime():
    if sc.__CURRENT_TOKEN__ == ["opmul","*"]:
       match(["opmul","*"])
       Fact()
       addNewInstruction(["opmul",""])
       Tprime()
    elif sc.__CURRENT_TOKEN__ == ["keyword","div"]:
       match(["keyword","div"])
       Fact()
       addNewInstruction(["opdiv",""])
       Tprime()

def Fact():
    if sc.__CURRENT_TOKEN__[0] == "identifier":
       Id()
       match(sc.__CURRENT_TOKEN__) 
    elif sc.__CURRENT_TOKEN__[0] == "unsigned int":
       Lit()#will push int literal to stack
       match(sc.__CURRENT_TOKEN__)

def Id():
    #lookup identifier in the symbol table
    id_address = list(filter(lambda x: x['name'] == sc.__CURRENT_TOKEN__[1],symbtab))[0]['address']
    opstring = ["push" , id_address]
    addNewInstruction(opstring)  

def Lit():#only numerical literals for now
    oppair = ["pushi" , sc.__CURRENT_TOKEN__[1]]
    addNewInstruction(oppair)

def match(token):
    global fi

    if token == ["keyword","endprog"]:
      if sc.__CURRENT_TOKEN__ == token:
        return
      else:
        print("an error occured")

    if token[0] == "identifier" and sc.__CURRENT_TOKEN__[0] == "identifier":
      sc.get_token(fi)
      return

    if sc.__CURRENT_TOKEN__ != token:
       print("an error occured")
       return
    else:
       sc.get_token(fi)

if __name__ == "__main__":
  global fi
  with open(sys.argv[1],'r') as inputfile:
    fi = inputfile
    Program()

#sart parsing
#Program()
#fi.close()
