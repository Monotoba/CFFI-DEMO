# Python CFFI Demo

[![Tests](https://github.com/Monotoba/CFFI-DEMO/actions/workflows/tests.yml/badge.svg)](https://github.com/Monotoba/CFFI-DEMO/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![C](https://img.shields.io/badge/C-C99-blue)
[![License](https://img.shields.io/badge/License-BSD--2--Clause-blue)](LICENSE)

Learn how to call compiled C functions from Python using CFFI. This small companion
project for [CodeRancher](https://www.coderancher.us/) demonstrates integers, floating
point values, strings, arrays, structures, booleans, matrix multiplication, and text
file I/O. The C source also includes a callback example; the Python demo does not
invoke it yet.

## Quick start (Linux or macOS)

Requires Python 3.10+, a C compiler (`cc`, GCC, or Clang), and a shell. Run from the
repository directory:

```sh
git clone https://github.com/Monotoba/CFFI-DEMO.git
cd CFFI-DEMO
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Compile on Linux:

```sh
cc -std=c99 -Wall -Wextra -fPIC -shared -o example.so example.c
```

Compile on macOS:

```sh
cc -std=c99 -Wall -Wextra -fPIC -dynamiclib -o example.dylib example.c
```

Generate the input file, then run:

```sh
python data_gen.py
python main.py > demo-output.txt
```

The generator writes 100,000 values to `data.txt`. The demo prints its examples and
reads those values, then writes `output.txt`. Redirecting the output avoids printing
100,000 lines in your terminal. Files are read/written relative to your current
directory; the compiled library is loaded relative to `main.py`.

The matrix result is `[[30, 24, 18], [84, 69, 54], [138, 114, 90]]`.
Missing, short, or malformed input raises an error before output is written.

## Run tests

```sh
python -m unittest discover -s tests -v
```

Tests compile the actual library with compiler warnings treated as errors and check
scalar calls, structures, matrix results, greeting boundaries, file round trips,
error handling, and imports from another directory. CI runs Linux/macOS with Python
3.10, 3.12, and 3.13 and also exercises the complete generated-data demo.

## Scope and limitations

This is an educational demo. Windows build/loading support is not implemented.
The greeting uses a shared static 50-byte buffer and rejects names longer than 41
UTF-8 bytes; concurrent use is not supported. C integer arithmetic has native bounds.
Text output uses six decimal places, so file round trips are not lossless for every
floating point value. Callers of the C functions must provide valid pointers and
matching array dimensions.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports should include your OS, Python
and compiler versions, commands, and expected/actual results. Useful next additions
include a tested Python callback example and documented Windows compiler support.

## License

Original project code is licensed under [BSD-2-Clause](LICENSE). Retain its copyright
notice and license terms when redistributing. Linked articles have their own terms.
