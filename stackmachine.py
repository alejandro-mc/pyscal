import sys
import pickle

ip           = 0
stack        = []
static       = 0
program      = []

def add():
	global stack
	global ip
	b = stack.pop()
	a = stack.pop()
	stack.append(a+b)
	ip +=1

def sub():
	global stack
	global ip
	b = stack.pop()
	a = stack.pop()
	stack.append(a - b)
	ip += 1

def mul():
	global stack
	global ip
	b = stack.pop()
	a = stack.pop()
	stack.append(a * b)
	ip += 1


def div():
	global stack
	global ip
	b = stack.pop()
	a = stack.pop()
	stack.append(a / b)
	ip +=1

def geq():
	global stack
	global ip
	b = stack.pop()
	a = stack.pop()
	stack.append(a >= b)
	ip+=1

def gtr():
	global stack
	global ip
	b = stack.pop()
	a = stack.pop()
	stack.append(a > b)
	ip+=1


def leq():
	global stack
	global ip
	b = stack.pop()
	a = stack.pop()
	stack.append(a <= b)
	ip+=1

def less():
	global stack
	global ip
	b = stack.pop()
	a = stack.pop()
	stack.append(a < b)
	ip+=1


def push():
    global stack
    global ip
    global program
    global static

    memaddress = program[ip][1]#gets the address parameter 
    stack.append(program[memaddress + static])
    ip+=1

def pushi():
	global stack
	global ip
	global program

	value = program[ip][1]#get the inmediate parameter
	stack.append(value)
	ip+=1

def pop():
	global stack
	global ip
	global program
	global static

	memaddress = program[ip][1]#get address parameter
	program[memaddress + static] = stack.pop()
	ip+=1

def put():
    global stack
    global ip
    global program
    global static

    value      = stack.pop()
    memaddress = stack.pop() 
    program[memaddress + static] = value
    ip+=1

def emit():
    global stack
    global ip
    global program
    global static

    memaddress = stack.pop() 
    stack.append(program[memaddress + static])
    ip+=1



def jmp():
	global stack
	global ip
	global program
	global static

	memaddress = program[ip][1]#get address parameter
	ip = memaddress	

def jfalse():
	global stack
	global ip
	global program

	memaddress = program[ip][1]#get address parameter
	if not stack.pop():
	   ip = memaddress
	else:
	   ip+=1

def jtrue():
	global stack
	global ip
	global program

	memaddress = program[ip][1]#get address parameter
	if stack.pop():
	   ip = memaddress
	else:
	   ip+=1

def noop():
	return

#instruction dispatcher
executeInstruction = {
'add'    : add,
'sub'    : sub,
'mul'    : mul,
'div'    : div,
'gtr'    : gtr,
'geq'    : geq,
'leq'    : leq,
'less'   : less,
'push'   : push,
'pushi'  : pushi,
'pop'    : pop,
'put'    : put,
'emit'   : emit,
'jmp'    : jmp,
'jfalse' : jfalse,
'jtrue'  : jtrue,
'noop'	 : noop
}


def main():
	global stack
	global memory
	global program
	global static
	#statick memory goes at the end
	#of the executable
	#so everytime we access a memory
	#location we must off set it

    #the following finds this location
	while program[static][0] != 'halt':
		  static+=1
	static +=1

	#import pdb; pdb.set_trace()
	#execute the program
	#print("~~~~~~~~~~~~~~~Executable~~~~~~~~~~~~~~~")
	#for i in program:
	#	print(i)
	#return
	while program[ip][0] != 'halt':
		  #execute instruction
		  executeInstruction[program[ip][0]]()
		  #import pdb; pdb.set_trace()


	#at the end print the stack
	print("~~~~~~~~~~~~~~~~STACK~~~~~~~~~~~~~~")
	for i in stack:
		print(i)

	print("~~~~~~~~~~~~~~~Executable~~~~~~~~~~~~~~~")
	for i in program:
		print(i)



if __name__ == "__main__":
   if (len(sys.argv) < 2):
   	  print("Too few parameters")
   	  print("Usage:python stackmachine.py <executable file>")
   else:
   	  with open(sys.argv[1],'rb') as fi:
   	  	   program = pickle.load(fi)
   	  	   main()