# membrane transpiler
# python membrane_compiler.py --file membrane.mb --output program.bf
# python bcs.py --file program.bf --output program.py
import argparse;import os;import sys;import re

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
 for c in open(file,encoding="UTF-8").read():
  code+=c
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

 name=code[s+6:n]
 body=code[n+1:e]

 macros[name]=body

 code=code[:s]+code[e+1:]
 i=s

def expand_counts(src):
 out=""
 i=0

 while i<len(src):
  c=src[i]

  if c in "+-<>":
   j=i+1
   n=""

   while j<len(src) and src[j].isdigit():
    n+=src[j]
    j+=1

   if n:
    out+=c*int(n)
    i=j
    continue

  out+=c
  i+=1

 return out

changed=True
while changed:
 old=code

 for name,body in macros.items():
  code=code.replace(name,body)

 code=expand_counts(code)

 changed=(code!=old)

p(code,"")

if output:
 open(output,"w",encoding="UTF-8").write(CODE)
