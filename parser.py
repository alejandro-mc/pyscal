#parser.py
#Alejandro Morejon Cortina 2016

import scanner as sc
import sys
import pickle

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
    #i=0
    #for instruction in instructions:
    #  print(i,instruction)
    #  i+=1
    for var in symbtab:
        if var['type'] == "array":
           for i in range(var['lo'],var['hi'] + 1):
               instructions.append(var['value'])
        if var['type'] == "integer":
           instructions.append(var['value'])
    with open('executable','wb') as ex:
         pickle.dump(instructions,ex)

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
    #import pdb; pdb.set_trace()
    match(["keyword","begin"])#program begins
    statements()
    match(["keyword","end"])#program ends
    match(["dot","."])
    addNewInstruction(["halt",""])#produce opcode to halt the program
    write_instructions_to_file()

def declarations():
    var_declarations()

def var_declarations():
    global next_address
    global symbtab

    tmpsymbtab =[]
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
                             "address": 0}#we don't know what type it is so don't know
                                          #the address either
        tmpsymbtab.append(new_symbtab_entry)
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
      for entry in tmpsymbtab:
        if entry['type'] == 'empty':
          entry['type'] = 'integer'
          entry['address'] = next_address
          next_address +=1
      match(["keyword","integer"])
    #add real varable types
    if sc.__CURRENT_TOKEN__ == ["keyword","real"]:
      for entry in tmpsymbtab:
        if entry['type'] == 'empty':
           entry['type'] = 'real'
    #add array types
    lo  = 0
    hi  = 0
    if sc.__CURRENT_TOKEN__ == ["keyword","array"]:
       match(["keyword","array"])
       match(["leftbracket", "["])
       if sc.__CURRENT_TOKEN__[0] == "unsigned int":
          lo = int(sc.__CURRENT_TOKEN__[1])
          match(["unsigned int",""])

       match(["oprange",".."])
       if sc.__CURRENT_TOKEN__[0] == "unsigned int":
          hi = int(sc.__CURRENT_TOKEN__[1])
          match(["unsigned int",""])
       #import pdb;pdb.set_trace()
       match(["rightbracket", "]"])

       match(["keyword","of"])

       if sc.__CURRENT_TOKEN__ == ["keyword","integer"]:
          for entry in tmpsymbtab:
              entry['type']         = "array"
              entry['element_type'] = "integer"
              entry['lo']           = lo
              entry['hi']           = hi
              entry['address']      = next_address
              next_address = next_address + (hi -  lo + 1)
          match(["keyword","integer"])
    
    match(["semicolon",";"])

    symbtab = symbtab + tmpsymbtab

    var_declarations()

def begin():
    match(["keyword","begin"])
    statements()
    match(["keyword","end"])
    match(["semicolon",";"])


def statements():
    while sc.__CURRENT_TOKEN__ != ["keyword","end"]:
          statement()

def statement():
    global lhs

    if sc.__CURRENT_TOKEN__ == ["keyword","if"]:
       if_statement()
       return
    if sc.__CURRENT_TOKEN__ == ["keyword","while"]:
       while_stat()
       return
    if sc.__CURRENT_TOKEN__ == ["keyword","do"]:
       do_while_stat()
       return
    if sc.__CURRENT_TOKEN__ == ["keyword","repeat"]:
       repeat_stat()
       return
    if sc.__CURRENT_TOKEN__ == ["keyword","for"]:
       fordo_stat()
       return
    if sc.__CURRENT_TOKEN__ == ["keyword","begin"]:
       begin()
       return
    #so far identifier is only found at the begining of asignments or array idexing
    if sc.__CURRENT_TOKEN__[0] == "identifier":

       lhs = sc.__CURRENT_TOKEN__[1]#save the identifier name
       match(["identifier",""])
       symbtab_entry = list(filter(lambda x: x['name'] == lhs, symbtab))[0]
       identifiertype = symbtab_entry['type']
       if identifiertype == 'array':
          match(["leftbracket","["])
          Exp()
          match(["rightbracket","]"])

       if sc.__CURRENT_TOKEN__ == ["opassign",":="]:
          match(["opassign",":="])
          if identifiertype == 'array':
             #normalize
             addNewInstruction(["pushi",symbtab_entry['lo']])
             addNewInstruction(["sub",""])

             #compute offset not needed for our stack machine 
             #we don't multiply here because integer takes one
             #memory address in our stack machine

             #compute address
             addNewInstruction(["pushi",symbtab_entry['address']])
             addNewInstruction(["add",""])

             #now the address is at the top of the stack

          Lexp()

          #after the code produced by Exp is evaluated
          #we must put the result from the top of the stack
          #in the correct mem location
          if identifiertype == 'array':
             #at this point the value of Lexp will be
             #at the top of the stack
             #and the address will be below
             addNewInstruction(["put",""])#puts the value in the mem address
          else:
             addNewInstruction(["pop" , symbtab_entry['address']])

          match(["semicolon",";"])


def if_statement():
  global ip
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

def while_stat():
  global ip
  global instructions
  match(["keyword","while"])

  #we have to excute the condition severa times
  #so let's save that memory location so we can jmp to later
  conditionaddress = ip
  #next we can parse and generate the code for the condition
  Lexp()

  #if the condition is not true we would like to
  #jump to the end of the while statement so we must save
  #we don't know where to jump yet so save the pointer to add it ater
  hole1 = ip  
  addNewInstruction(["jfalse",""])
  match(["keyword","do"])
  #import pdb; pdb.set_trace()
  statement()
  #add jump to begening
  addNewInstruction(["jmp",conditionaddress])
  #patch hole1
  instructions[hole1][1] = ip

def do_while_stat():
  global ip

  match(["keyword","do"])
  beginaddress = ip
  statement()
  match(["keyword","while"])
  Lexp()
  addNewInstruction(["jtrue",beginaddress])
  match(["semicolon",";"])


def repeat_stat():
  global ip

  match(["keyword","repeat"])
  beginaddress = ip

  #parse multiple satements until token until is found
  while True:
    if sc.__CURRENT_TOKEN__ == ["keyword","until"]:
      break

    statement()

  match(["keyword","until"])

  Lexp()

  addNewInstruction(["jfalse",beginaddress])

  match(["semicolon",";"])


# for <identifier> := <integer literal> to <integer literal> do <statement> ;
def fordo_stat():
    global next_address
    global ip

    match(["keyword","for"])
    #import pdb; pdb.set_trace()
    if sc.__CURRENT_TOKEN__[0] == "identifier":
       #add identifier to the symbol table
       control_var_address = next_address#save address to insert value later
       new_symbtab_entry = {"name" : sc.__CURRENT_TOKEN__[1],
                            "type" : "integer",
                            "value": 0,
                            "address": next_address}
       symbtab.append(new_symbtab_entry)
       next_address += 1
       match(["identifier",""])
    else:
       print("Error parsing for statement. Expected identifier")

    match(["opassign",":="])#may fail

    if sc.__CURRENT_TOKEN__[0] == "unsigned int":
       #assigm value 
       addNewInstruction(["pushi",int(sc.__CURRENT_TOKEN__[1])])
       addNewInstruction(["pop",control_var_address])

    match(["unsigned int",""])#may fail
    match(["keyword","to"])

    if sc.__CURRENT_TOKEN__[0] == "unsigned int":
       #save the value
       rangelimit = int(sc.__CURRENT_TOKEN__[1])

    #test condtition
    condition_address = ip
    addNewInstruction(["push",control_var_address])
    addNewInstruction(["pushi",rangelimit])
    addNewInstruction(["leq",""])

    hole1 = ip
    addNewInstruction(["jfalse",""])

    match(["unsigned int",""])
    match(["keyword","do"])

    #statements
    statement()

    #increment variable and return to begining
    addNewInstruction(["pushi",1])
    addNewInstruction(["push",control_var_address])
    addNewInstruction(["add",""])
    addNewInstruction(["pop",control_var_address])
    addNewInstruction(["jmp",condition_address])

    #patch hole
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
       addNewInstruction(["gtr",""])
       Lprime()
    elif sc.__CURRENT_TOKEN__ == ["opeq","="]:
       match(["opeq","="])
       Exp()
       addNewInstruction(["eq",""])
       Lprime()
    elif sc.__CURRENT_TOKEN__ == ["opleq","<="]:
       match(["opleq","<="])
       Exp()
       addNewInstruction(["leq",""])
       Lprime()
    elif sc.__CURRENT_TOKEN__ == ["opgeq",">="]:
       match(["opgeq",">="])
       Exp()
       addNewInstruction(["geq",""])
       Lprime()
    


def Exp():
    Term()
    Eprime()

def Eprime():
    if sc.__CURRENT_TOKEN__ == ["opplus","+"]:
       match(["opplus","+"])
       Term()
       addNewInstruction(["add",""])
       Eprime()
    elif sc.__CURRENT_TOKEN__ == ["opminus","-"]:
       match(["opminus","-"])
       Term()
       addNewInstruction(["sub",""])
       Eprime()
 
def Term():
    Fact()
    Tprime()

def Tprime():
    if sc.__CURRENT_TOKEN__ == ["opmul","*"]:
       match(["opmul","*"])
       Fact()
       addNewInstruction(["mul",""])
       Tprime()
    elif sc.__CURRENT_TOKEN__ == ["keyword","div"]:
       match(["keyword","div"])
       Fact()
       addNewInstruction(["div",""])
       Tprime()

def Fact():
    global symbtab
    if sc.__CURRENT_TOKEN__[0] == "identifier":
       symbtab_entry = list(filter(lambda x: x['name'] == sc.__CURRENT_TOKEN__[1], symbtab))[0]
       identifiertype = symbtab_entry['type']
       if identifiertype == 'array':
          arrayvar(symbtab_entry)
       else:
        Id()
        match(sc.__CURRENT_TOKEN__) 
    elif sc.__CURRENT_TOKEN__[0] == "unsigned int":
       Lit()#will push int literal to stack
       match(sc.__CURRENT_TOKEN__)

def arrayvar(entry):
    match(sc.__CURRENT_TOKEN__)#current token will be the variable name
    match(["leftbracket","["])
    Exp()
    match(["rightbracket","]"])

    #normalize
    addNewInstruction(["pushi",entry['lo']])
    addNewInstruction(["sub",""])

    #compute address
    addNewInstruction(["pushi",entry['address']])
    addNewInstruction(["add",""])

    #put value on the stack
    addNewInstruction(["emit",""])


def Id():
    #lookup identifier in the symbol table
    id_address = list(filter(lambda x: x['name'] == sc.__CURRENT_TOKEN__[1],symbtab))[0]['address']
    opstring = ["push" , id_address]
    addNewInstruction(opstring)  

def Lit():#only numerical literals for now
    oppair = ["pushi" , int(sc.__CURRENT_TOKEN__[1])]
    addNewInstruction(oppair)

def match(token):
    global fi

    if token == ["dot","."]:
      if sc.__CURRENT_TOKEN__ == token:
        return
      else:
        print("an error occured")

    if token[0] == "identifier" and sc.__CURRENT_TOKEN__[0] == "identifier":
      sc.get_token(fi)
      return
    if token[0] == "unsigned int" and sc.__CURRENT_TOKEN__[0] == "unsigned int":
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
