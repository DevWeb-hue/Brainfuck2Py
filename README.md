# Zanebrain Compiler

A Brainfuck-to-Python compiler designed to eventually be simple enough to be rewritten in Zanebrain itself.

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
