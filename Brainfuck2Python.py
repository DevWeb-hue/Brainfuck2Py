# a brainfuck compiler capible of being written in brainfuck.
import argparse;import os;import sys
def key():
 if os.name=='nt':
  import msvcrt;char=msvcrt.getch()
  try:return char.decode('utf-8')
  except UnicodeDecodeError:return char
 else:
  import tty;import termios;fd=sys.stdin.fileno();old_settings=termios.tcgetattr(fd)
  try:tty.setraw(sys.stdin.fileno());char = sys.stdin.read(1)
  finally:termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return char
parser = argparse.ArgumentParser()
parser.add_argument('--file')
parser.add_argument('--output')
args = parser.parse_args()



# usage:
#  python brainfuck_compiler.py --file program.bf --output program.py
code: str = ""
file = args.file
output = args.output
if file:
 for line in open(file,encoding="UTF-8").read():
   line: str
   cleaned = line.strip()
   code += cleaned
else:
 char = key()
 while not char == "\n":
  code += char
  char = key()
if output:
 global CODE
 CODE:str = ""



def p(text,end="\n"):
 global output
 global CODE
 if output:
  CODE += text + end
 else:
  print(text,end=end)


def translate(char,amount):
 global indentation
 indent=" "*indentation
 if char == "+":
  p(f"{indent}mem[pointer]+={amount}")
 if char == "-":
  p(f"{indent}mem[pointer]-={amount}")
 if char == "[":
  if amount > 1:
   translate("[",amount-1)
  p(f"{indent}while not mem[pointer]==0:")
  indentation += 1
 if char == ".":
  if amount == 1:
   p(f"{indent}p(chr(mem[pointer]))")
  else:
   p(f"{indent}p(chr(mem[pointer])*{amount})")
 if char == ",":
  if amount > 1:
   translate(",",amount-1)
  p(f"{indent}mem[pointer]=ord(key())") #ord('a')
 if char == "]":
  if amount > 1:
   translate("]",amount-1)
  indentation -= 1
 if char == ">":
  p(f"{indent}pointer+={amount}")
 if char == "<":
  p(f"{indent}pointer-={amount}")


p("""
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file')
parser.add_argument('--output')
args = parser.parse_args()

def key():
 # Windows platform
 if os.name == 'nt':
  import msvcrt
  # msvcrt.getch() blocks until a key is pressed, returning a byte string
  char = msvcrt.getch()
  try:
   return char.decode('utf-8')
  except UnicodeDecodeError:
   return char

 # Unix/Linux/macOS platform
 else:
  import tty
  import termios
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
   # Set the terminal to raw mode to catch single characters instantly
   tty.setraw(sys.stdin.fileno())
   char = sys.stdin.read(1)
  finally:
   # Always reset terminal settings back to normal
   termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return char
code: str = ""
file = args.file
output = args.output
file_index = 0
def modKey():
 global file_index
 global code
 file_index += 1
 return code[file_index-1]
 

if file:
 for line in open(file,encoding="UTF-8").read():
   line: str
   code += line
 key = modKey

if output:
 global CODE
 CODE:str = ""
def p(text):
 global output
 global CODE
 if output:
  CODE += text
 else:
  print(text,end='',flush=True)
""")

p("mem = [0 for _ in range(1024)]")
p("pointer = 0")
indentation:int = 0
amount = 1
last = None
for char in code:
 if char == last:
  amount += 1
 else:
  translate(last, amount)
  last = char
  amount = 1
translate(last, amount)
last = char
p("""
if output:
 open(output, "w").write(CODE)
""")
if output:
 open(output, "w").write(CODE)
