import argparse,os,sys
def k():
	if os.name=='nt':
		import msvcrt as D;A=D.getch()
		try:return A.decode('utf-8')
		except:return A
	import tty,termios as B;C=sys.stdin.fileno();E=B.tcgetattr(C)
	try:tty.setraw(C);A=sys.stdin.read(1)
	finally:B.tcsetattr(C,B.TCSADRAIN,E)
	return A
a=argparse.ArgumentParser()
a.add_argument('--file')
a.add_argument('--output')
a=a.parse_args()
c=''
f=a.file
o=a.output
if f:
	for x in open(f,encoding='UTF-8').read():c+=x.strip()
else:
	x=k()
	while x!='\n':c+=x;x=k()
if o:C=''
def p(t,e='\n'):
	global C,o
	if o:C+=t+e
	else:print(t,end=e)
def t(x,n):
	global i;A=' '*i
	if x=='+':p(f"{A}mem[pointer]+={n}")
	if x=='-':p(f"{A}mem[pointer]-={n}")
	if x=='>':p(f"{A}pointer+={n}")
	if x=='<':p(f"{A}pointer-={n}")
	if x=='[':
		if n>1:t('[',n-1)
		p(f"{A}while not mem[pointer]==0:");i+=1
	if x==']':
		if n>1:t(']',n-1)
		i-=1
	if x==',':
		if n>1:t(',',n-1)
		p(f"{A}mem[pointer]=ord(k())")
	if x=='.':
		if n==1:p(f"{A}p(chr(mem[pointer]))")
		else:p(f"{A}p(chr(mem[pointer])*{n})")
p('\nimport os\nimport sys\nimport argparse\n\nparser = argparse.ArgumentParser()\nparser.add_argument(\'--file\')\nparser.add_argument(\'--output\')\nargs = parser.parse_args()\n\ndef k():\n # Windows platform\n if os.name == \'nt\':\n  import msvcrt\n  # msvcrt.getch() blocks until a key is pressed, returning a byte string\n  char = msvcrt.getch()\n  try:\n   return char.decode(\'utf-8\')\n  except UnicodeDecodeError:\n   return char\n\n # Unix/Linux/macOS platform\n else:\n  import tty\n  import termios\n  fd = sys.stdin.fileno()\n  old_settings = termios.tcgetattr(fd)\n  try:\n   # Set the terminal to raw mode to catch single characters instantly\n   tty.setraw(sys.stdin.fileno())\n   char = sys.stdin.read(1)\n  finally:\n   # Always reset terminal settings back to normal\n   termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)\n  return char\ncode: str = ""\nfile = args.file\noutput = args.output\nfile_index = 0\ndef modKey():\n global file_index\n global code\n file_index += 1\n return code[file_index-1]\n \n\nif file:\n for line in open(file,encoding="UTF-8").read():\n   line: str\n   code += line\n key = modKey\n\nif output:\n global CODE\n CODE:str = ""\ndef p(text):\n global output\n global CODE\n if output:\n  CODE += text\n else:\n  print(text,end='',flush=True)\n')
p('mem=[0]*1024')
p('pointer=0')
i=0
n=1
l=None
for x in c:
	if x==l:n+=1
	else:t(l,n);l=x;n=1
t(l,n)
p('\nif output:open(output,"w").write(CODE)')
if o:open(o,'w').write(C)
