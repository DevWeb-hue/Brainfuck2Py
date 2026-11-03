# Zanebrain Compiler

A Brainfuck-to-Python compiler designed to eventually be simple enough to be rewritten in Zanebrain itself.

One side effect of Zanebrain's design is that it works well as a sandboxed programming language.

Zanebrain programs compile into a very small subset of Python and cannot directly create classes, execute arbitrary Python code, import modules, access the filesystem, or interact with the operating system.

Programs operate primarily on:

- Integers
- Arrays
- A stack
- Input streams
- Output streams

File access is intentionally restricted.

Input is only available through the `--file` argument, which exposes a single file (through ints) to the program.

Output is only available through the `--output` argument, which writes to a single destination (rather than to terminal). ONLY when the 'program' halts, never through any zanebrain compiled code (writting to file is once at the very end of generated python).

This means a Zanebrain program cannot decide what files to open, what files to create, or what locations to access. Those choices are made outside the language by whoever runs the program.

If you are particularly paranoid about security, you can inspect or compile the raw Zanebrain source itself. The language is intentionally small enough that understanding every possible operation is practical.

### Security Notes

Zanebrain restricts what programs can do, but it does not automatically prevent:

- Infinite loops
- Excessive memory usage
- Excessive output
- Extremely long runtimes

Programs should still be executed with sensible limits when used in untrusted environments.
BUT if program taking too long, you can close it, it won't corrupt any files! Meaning all that any hackers or malicious programmers have,
are infinite loops, and an uncapped stack that can only be appended ints, one at a time. So if the program takes too long, just close it!

### Custom Compilers

Zanebrain intentionally has very strict limitations.

If you wish to avoid these restrictions, Zanebrain may not be the language you are looking for.

However, the compiler itself is written in Python and is designed to be easy to understand and modify. If you want additional features such as networking, graphics, audio, filesystem access, larger memory models, or other capabilities, simply copy the compiler, add your own opcodes, and have fun.

Keep in mind that many of Zanebrain's safety properties come from what the compiler refuses to generate. Every new opcode increases the amount of trust required in the compiler implementation and may introduce new security risks.

For this reason, custom Zanebrain compilers should be treated as separate languages with separate security guarantees.

In short:

- Trust the compiler, not just the source code.
- More opcodes = more power.
- More power = more opportunities for bugs and vulnerabilities.
- If security matters, inspect both the Zanebrain source and the compiler being used.

Compile Zanebrain source:
(I have Brainfuck2Python.py as bcs.py on my computer B.C.S aka be cau se)
```bash
python bcs.py --file program.zb --output program.py
```

Run the generated program:

```bash
python program.py
```

Run with file input:

```bash
python program.py --file test.txt
```

Write output to a file:

```bash
python program.py --output result.txt
```

---

## Differences From Brainfuck

Unlike traditional Brainfuck implementations, Zanebrain uses full Python integers.

This means:

```brainfuck
+
```

can increase forever.

```brainfuck
-
```

can go negative.

There is no 0-255 wrapping.

As a result:

```brainfuck
[-]
```

does **not** always clear a cell.

Example:

```text
Cell = -5

[-]
```

becomes:

```text
-5
-6
-7
-8
...
```

and never reaches zero.

To make programming practical with signed integers, Zanebrain adds several new opcodes.

---

## Opcode Reference

| Opcode | Description |
|----------|----------|
| `+` | Increment cell |
| `-` | Decrement cell |
| `>` | Move pointer right |
| `<` | Move pointer left |
| `[` | Loop while current cell is nonzero |
| `]` | End loop |
| `,` | Read character |
| `.` | Output character |

### Zanebrain Extensions

#### `()`

Run-once-if-zero blocks.

```brainfuck
(
    code here
)
```

Equivalent to:

```python
if mem[pointer] == 0:
```

Useful when `[-]` cannot be relied upon.

---

#### `/`

Clear current cell.

```brainfuck
/
```

Equivalent to:

```python
mem[pointer] = 0
```

---

#### `_`

Invert sign.

```brainfuck
_
```

Examples:

```text
5  -> -5
-5 -> 5
```

---

#### `|`

Clamp negative values to zero.

```brainfuck
|
```

Examples:

```text
5  -> 5
0  -> 0
-5 -> 0
```

---

#### `$`

Push current cell onto the stack.

```brainfuck
$
```

Equivalent to:

```python
stack.append(mem[pointer])
```

---

#### `#`

Pop from stack.

```brainfuck
#
```

Equivalent to:

```python
mem[pointer] = stack.pop()
```

---

#### `*`

Store stack length.

```brainfuck
*
```

Equivalent to:

```python
mem[pointer] = len(stack)
```

Useful for counters, sentinels, and file processing.

---

#### `@`

Relative jump.

```brainfuck
@
```

Equivalent to:

```python
pointer += mem[pointer]
```

Example:

```text
cell = 5

@
```

moves the pointer 5 cells to the right.

---

#### `O`

Return pointer to origin.

```brainfuck
O
```

Equivalent to:

```python
pointer = 0
```

Useful for large memory structures and sentinel-based algorithms.

---

## File Input Format

When a generated program is run using:

```bash
python program.py --file test.txt
```

the input stream becomes:

```text
[length, byte1, byte2, byte3, ...]
```

Example:

```text
File:
abc
```

becomes:

```text
[3, 97, 98, 99]
```

inside the program.

The file length is provided first, making it possible to build sentinels, counters, bounded loops, and memory layouts without relying on EOF detection.

---

# Membrane

Membrane is a transpiler that expands macros and shorthand syntax into Zanebrain.

Compile a Membrane file:

```bash
python membrane_compiler.py --file program.mb --output program.zb
```

Compile the resulting Zanebrain:

```bash
python bcs.py --file program.zb --output program.py
```

Run it:

```bash
python program.py
```

Full pipeline:

```bash
python membrane_compiler.py --file program.mb --output program.zb

python bcs.py --file program.zb --output program.py

python program.py --file test.txt
```

---

## Membrane Features

### Macros

Define:

```membrane
macro:next:>;
```

Use:

```membrane
next next next
```

Expands to:

```brainfuck
>>>
```

---

### Instruction Counts

```membrane
+10
```

Expands to:

```brainfuck
++++++++++
```

Likewise:

```membrane
>20
```

becomes:

```brainfuck
>>>>>>>>>>>>>>>>>>>>
```

---

### Repetition

```membrane
hello*5
```

Expands to:

```membrane
hello hello hello hello hello
```

---

## Example

```membrane
macro:move:[->+<];

+++++
move
```

Expands to:

```brainfuck
+++++[->+<]
```

before being compiled by Zanebrain.

---

## Example: Sentinel-Based File Reader

```membrane
macro:move:[->+<];
macro:sentenal:[move - move + >];

>, sentenal O > [,.>]
```

For a file containing:

```text
a b c
```

Output:

```text
a b c
```

This uses the file length to build a bounded sentinel region and then reads exactly that many characters without relying on EOF detection.

---

## Design Goals

Zanebrain aims to remain close to Brainfuck while adding enough features to make real programs practical.

Major goals include:

- Signed integer arithmetic
- Stack support
- Relative jumps
- Macro expansion through Membrane
- Self-hosting compiler experiments
- File processing without EOF dependence
- Sentinel-based memory structures

---


Happy frickn coding!
