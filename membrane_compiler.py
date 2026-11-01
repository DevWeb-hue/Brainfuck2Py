# membrane transpiler
# python membrane_compiler.py --file membrane.mb --output program.bf
# python bcs.py --file program.bf --output program.py

import argparse;import os;import sys

def key():
 if os.name=='nt':
  import msvcrt;char=msvcrt.getch()
  try:return char.decode('utf-8')
  except UnicodeDecodeError:return char
 else:
  import tty;import termios;fd=sys.stdin.fileno();old_settings=termios.tcgetattr(fd)
  try:tty.setraw(sys.stdin.fileno());char=sys.stdin.read(1)
  finally:termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
  return char

parser=argparse.ArgumentParser()
parser.add_argument('--file')
parser.add_argument('--output')
args=parser.parse_args()

code=""
file=args.file
output=args.output

if file:
 code=open(file,encoding="UTF-8").read()
else:
 c=key()
 while c!="\n":
  code+=c
  c=key()

if output:
 CODE=""

def p(text,end="\n"):
 global output,CODE
 if output:
  CODE+=text+end
 else:
  print(text,end=end)

macros={}

i=0
while True:
 s=code.find("macro:",i)
 if s==-1:break

 n=code.find(":",s+6)
 if n==-1:break

 e=code.find(";",n+1)
 if e==-1:break

 name=code[s+6:n].strip()
 body=code[n+1:e].strip()

 macros[name]=body

 code=code[:s]+" "+code[e+1:]
 i=s

tokens=code.split()

def expand_counts(tok):
 if len(tok)<2:return tok

 if tok[0] in "+-<>":
  n=tok[1:]
  if n.isdigit():
   return tok[0]*int(n)

 return tok

changed=True
while changed:
 changed=False
 new=[]

 for tok in tokens:

  if "*" in tok:
   left,right=tok.rsplit("*",1)

   if right.isdigit():
    for _ in range(int(right)):
     new.append(left)
    changed=True
    continue

  if tok in macros:
   new.extend(macros[tok].split())
   changed=True
   continue

  tok2=expand_counts(tok)

  if tok2!=tok:
   changed=True

  new.append(tok2)

 tokens=new

result="".join(tokens)

p(result,"")

if output:
 open(output,"w",encoding="UTF-8").write(result)
