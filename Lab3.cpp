#include <omp.h>
#include <ctime>
#include <math.h>
#include <iostream>

using namespace std;
const double eps = 1e-7;
const double t = 0.1 / 512;
const int n = 512;
const int THREADS = 8;

void fill_matrices(double *m, double *B, double *x) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            m[i * n + j] = i == j ? 2.0 : 1.0;
        }
    }

    for (int i = 0; i < n; i++) {
        B[i] = n + 1;
    }

    for (int i = 0; i < n; i++) {
        x[i] = 0;
    }
}

double normalize(double *v) {
    double result = 0;
    omp_set_num_threads(THREADS);
    for (int i = 0; i < n; i++) {
        result += pow(v[i], 2);
    }
    return sqrt(result);
}

double* mult_matrix_byvec(double *m, double *x) {
    double *result = new double[n];
    int i = 0;
    omp_set_num_threads(THREADS);
#pragma omp parallel for shared(result, m, x) private(i)
    for (i = 0; i < n; i++) {
        result[i] = 0;
        for (int j = 0; j < n; j++) {
            result[i] += m[i * n + j] * x[j];
        }
    }
    return result;
}

void print_x(double *x) {
    cout << "Vector x: ";
    for (int i = 0; i < n - 1; i++) {
        cout << x[i] << ", ";
    }
    cout << x[n - 1] << endl;
}

void solve(double *A, double *b, double *x, double *y) {
    int i = 0;
    while (true) {
        i++;
        y = mult_matrix_byvec(A, x);
        int k;
        omp_set_num_threads(THREADS);
#pragma omp parallel for shared(y) private(k)
        for (k = 0; k < n; k++) {
                y[k] -= b[k];
            }

        double c = normalize(y) / normalize(b);
        if (c < eps) {
            break;
        }


        omp_set_num_threads(THREADS);
#pragma omp parallel for shared(y) private(k)
        for (int k = 0; k < n; k++) {
                y[k] *= t;
        }


        omp_set_num_threads(THREADS);
#pragma omp parallel for shared(x, y) private(k)
        for (int k = 0; k < n; k++) {
                x[k] -= y[k];
        }
    }
}

int main() {
#ifdef _OPENMP
    cout << "OPENMP is working" << endl;
#endif

    double *A = new double[n * n];
    double *b = new double[n];
    double *x = new double[n];
    double *y = new double[n];

    fill_matrices(A, b, x);
    double stime = omp_get_wtime();
    solve(A, b, x, y);
    double etime = omp_get_wtime();
    cout << "Spend time " << etime - stime << " seconds for " << THREADS << " threads" << endl;
    print_x(x);
    delete[] A;
    delete[] b;
    delete[] x;
    delete[] y;
    return 0;
}
