#!/usr/bin/env python3
# (-*-coding: utf-8-*-)

# =======================================
# Python Application to Demo Using CFFI
#    to call C functions from Python
# =======================================

__author__ = "Randall Morgan"
__copyright__ = "Copyright 2023, SensorNet"
__credits__ = ["Randall Morgan"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Randall Morgan"
__email__ = "rmorgan@sensornet.us"
__status__ = "Beta"

import cffi

ffi = cffi.FFI()
lib = ffi.dlopen(
    "./example.so"
)  # or "./example.dll" on Windows, or "./example.dylib" on macOS

# Add C function Signatures in ffi.cdef()
ffi.cdef(
    """
    int add(int x, int y);
    int sum(int *array, int length);
    float multiply(float x, float y);
    char* greet(char* name);
    void callback(int (*f)(int));
    typedef struct {
        int x;
        int y;
    } Point;
    Point move_point(Point p, int dx, int dy);
    bool is_even(int num);
    void matrix_multiply(double* A, double* B, double* C, int m, int n, int p);
    int read_file(char* filename, double* data, int size);
    int write_file(char* filename, double* data, int size);
"""
)


def add(x: int, y: int) -> int:
    return lib.add(x, y)


def mult(x: float, y: float) -> float:
    return lib.multiply(x, y)


def greet(name: str) -> str:
    b_string = name.encode()  # Note the name string must be converted to bytes.
    result = lib.greet(b_string)
    bstring = ffi.string(result)
    return bstring.decode("utf8")


def sum(arr: list[int]) -> int:
    # convert the Python list to a C array
    c_array = ffi.new("int[]", arr)

    # call the C function with the C array and the length of the array
    result = lib.sum(c_array, len(arr))

    # convert the result back to a Python int
    return int(result)


def move_point(p: dict[int, int], dx: int, dy: int) -> dict[int, int]:
    # Calling the move_point() function
    p = ffi.new("Point*", p)
    result = lib.move_point(p[0], dx, dy)
    return result


def is_even(x: bool) -> bool:
    result = lib.is_even(x)
    return bool(result)


def matrix_multiply():
    q = 3
    A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
    B = [[9.0, 8.0, 7.0], [6.0, 5.0, 4.0], [3.0, 2.0, 1.0]]
    C = [[0.0] * q for _ in range(q)]

    print("Matrix Multiply...")
    print(f"A: {A}\n\nB: {B}\n\nC: {C}\n\n")

    # Convert to C types
    _A = ffi.new("double[]", __builtins__.sum(A, []))
    _B = ffi.new("double[]", __builtins__.sum(B, []))
    _C = ffi.new("double[]", __builtins__.sum(C, []))

    m, n, p = 2, 2, 2

    lib.matrix_multiply(_A, _B, _C, m, n, p)
    C = [[_C[i * q + j] for j in range(q)] for i in range(q)]

    print(f"Result:\n\nA: {A}\n\nB: {B}\n\nC: {C}\n\n")


def read_data():
    # read data from file
    size = 100_000
    data = ffi.new("double[]", size)
    filename = ffi.new("char[]", b"data.txt")
    retval = lib.read_file(filename, data, size)

    # check if read was successful
    if retval == 0:
        print("Data read successfully:")
        for i in range(size):
            print(data[i])
    else:
        print("Error reading data from file.")
    return data


def write_data(data_list: list):
    size = len(data_list)
    data = ffi.new("double[]", data_list)

    # write data to file
    filename = ffi.new("char[]", b"output.txt")
    retval = lib.write_file(filename, data, size)

    # check if write was successful
    if retval == 0:
        print("Data written successfully.")
    else:
        print("Error writing data to file.")


def main():
    x, y = 2, 3
    result = add(x, y)
    print(f"Add({x}, {y}) = {result}")  # Output: 5

    # build a list of values to sum
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # sum the values in the array and print the results
    print(f"The sum of 1-12 is: {sum(arr)}")

    # Multiply two float values and print the result
    x, y = 2.5, 3.5
    print(f"multiply({x}, {y}) = {mult(x, y)}")

    # Pass a name (string) to a C function and get a greeting
    name = "Gorge"
    print(f"Greeting: {greet(name)}")

    # Create a point and delta values
    p = {"x": 12, "y": 21}
    dx = 10
    dy = 9
    # call move_point()
    result = move_point(p, dx, dy)
    # show result
    print(f"move_point: ({result.x}, {result.y})")

    # Handling boolean values
    x = 27
    print(f"{x} is even. This statement is {is_even(x)}")
    x = 32
    print(f"{x} is even. This statement is {is_even(x)}")

    # Do matrix multiply
    matrix_multiply()

    # Read file
    num_data = read_data()
    print(num_data)

    # Write file
    write_data(list(num_data))


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
