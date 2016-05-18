#parser.py
#Alejandro Morejon Cortina 2016

import scanner as sc

#try parsing test file


#required datastructures
symbtab = []
lhs = ''
next_address=0

def Program():
  global fi
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
    print("halt")#produce opcode to halt the program


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
  global lhs

  while True:
    #so far identifier is only found at the begining of asignments or array idexing
    if sc.__CURRENT_TOKEN__[0] == "identifier":
      lhs = sc.__CURRENT_TOKEN__[1]#save the identifier name
      match(["identifier",""])
      if sc.__CURRENT_TOKEN__ == ["opassign",":="]:
        match(["opassign",":="])
        Exp()
        #after the code produced by Exp is evaluated
        #we must put the result from the top of the stack
        #in the correct mem location
        opstring = "pop %d" % list(filter(lambda x: x['name'] == lhs,symbtab))[0]['address']
        print(opstring)
        match(["semicolon",";"])
      if sc.__CURRENT_TOKEN__ == ["keyword","endprog"]:
        return


#for now will only parse arithmetic expression
#def Goal():
#    global fi
#    #import pdb; pdb.set_trace()
#    sc.get_token(fi)
#    match(["keyword","program"])
#    Exp();
#    match(["keyword","end"])
    
def Exp():
    Term()
    Eprime()

def Eprime():
    if sc.__CURRENT_TOKEN__ == ["opplus","+"]:
       match(["opplus","+"])
       Term()
       print("opadd")
       Eprime()
    elif sc.__CURRENT_TOKEN__ == ["opminus","-"]:
       mathc(["opminus","-"])
       Term()
       print("opsub")
       Eprime()
 
def Term():
    Fact()
    Tprime()

def Tprime():
    if sc.__CURRENT_TOKEN__ == ["opmul","*"]:
       match(["opmul","*"])
       Fact()
       print("opmul")
       Tprime()
    elif sc.__CURRENT_TOKEN__ == ["keyword","div"]:
       match(["keyword","div"])
       Fact()
       print("opdiv")
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
    opstring = "push %d" % id_address
    print(opstring)  

def Lit():#only numerical literals for now
    opstring = "pushi %s" % sc.__CURRENT_TOKEN__[1]
    print(opstring)

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
  with open('test1.psc','r') as inputfile:
    fi = inputfile
    Program()

#sart parsing
#Program()
#fi.close()
