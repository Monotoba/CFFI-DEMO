#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>


/**
 * add(x, y) - Simply adds two integers.
 * param: x: int
 * param: y: int
 * return int
 */
int add(int x, int y) {
    return x + y;
}

/**
 * multiply(float x, float y) - Multiplies two float numbers
 * param: x : float - multiplicand float value
 * param: y : float - multiplier float value
 * return product : float
 */
float multiply(float x, float y) {
    return x * y;
}

/**
 * greet(char *name) - Given a name returns a greeting
 * param: name : char* - the name to greet
 * return: greeting : char*
 */
char* greet(char* name) {
    static char message[50];
    sprintf(message, "Hello, %s!", name);
    return message;
}


/**
 * sum(int *array, int length) : Sums all integers in array
 * param: array: int - Array containing integer values to sum.
 * param: length: int - Length of array.
 * return int - sum of all integers in array.
 */
int sum(int *array, int length) {
    int result = 0;
    for (int i = 0; i < length; i++) {
        result += array[i];
    }
    return result;
}


/**
 * callback(int (*f)(int))
 */
void callback(int (*f)(int)) {
    f(42);
}

/**
 * Struct to hold point values
 */
typedef struct {
    int x;
    int y;
} Point;

/**
 * move_point( Point p, int dx, int dy)
 * param: p : Point
 * param: dx : int
 * param: dy : int
 * return: p - modified by (dx, dy)
 */
Point move_point(Point p, int dx, int dy) {
    p.x += dx;
    p.y += dy;
    return p;
}

/**
 * bool is_even(int x) - returns true if x is event.
 * param: x : int - integer value to test
 * return bool - True if x is divisible by two, without
 *               remainder, false otherwise.
 */
bool is_even(int x) {
    return x % 2 == 0;
}

/**
 * Matrix multiplication()
 * param: A : double* - Multiplicand
 * param: B : double* - Multiplier
 * param: C : double* - Result
 * param: m : int - dimension of A
 * param: n : int - dimension of B
 * param: p : int - dimension of C
 */
void matrix_multiply(double* A, double* B, double* C, int m, int n, int p) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < p; j++) {
            double sum = 0;
            for (int k = 0; k < n; k++) {
                sum += A[i * n + k] * B[k * p + j];
            }
            C[i * p + j] = sum;
        }
    }
}


/**
 * read_file(char* filename, double* data, int size)
 * param: filename : char* - pointer to string containing
 * param: data : double* - pointer to data array
 * param: size : int - size of data array
 * return: int : success code, 0 on success, -1 on error
 */
int read_file(char* filename, double* data, int size) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        return -1;
    }

    for (int i = 0; i < size; i++) {
        if (fscanf(file, "%lf", &data[i]) == EOF) {
            break;
        }
    }

    fclose(file);
    return 0;
}

/**
 * write_file(char* filename, double* data, int size)
 * param: filename : char* - pointer to C string
 * param: data : double* - pointer to data array
 * param: size : int - size of data array
 * return: int : success code, 0 on success, -1 otherwise
 */
int write_file(char* filename, double* data, int size) {
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        return -1;
    }

    for (int i = 0; i < size; i++) {
        fprintf(file, "%lf\n", data[i]);
    }

    fclose(file);
    return 0;
}
