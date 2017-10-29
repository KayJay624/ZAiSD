/******************************************************************************
 *  Compilation:  javac Matrix.java
 *  Execution:    java Matrix
 *
 *  A bare-bones collection of static methods for manipulating
 *  matrices.
 *
 ******************************************************************************/
 import java.util.Random;

public class Matrix {

  public double[][] m;

  Matrix( double[][] m){
    this.m = m;
  }
    // return a random m-by-n matrix with values between 0 and 1
    public static double[][] random(int m, int n) {
        double[][] a = new double[m][n];
        Random rand = new Random();

        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                a[i][j] = rand.nextDouble();
        return a;
    }

    // return n-by-n identity matrix I
    public static double[][] identity(int n) {
        double[][] a = new double[n][n];
        for (int i = 0; i < n; i++)
            a[i][i] = 1;
        return a;
    }

    // return x^T y
    public static double dot(double[] x, double[] y) {
        if (x.length != y.length) throw new RuntimeException("Illegal vector dimensions.");
        double sum = 0.0;
        for (int i = 0; i < x.length; i++)
            sum += x[i] * y[i];
        return sum;
    }

    // return B = A^T
    public static double[][] transpose(double[][] a) {
        int m = a.length;
        int n = a[0].length;
        double[][] b = new double[n][m];
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                b[j][i] = a[i][j];
        return b;
    }

    // return c = a + b
    public static double[][] add(double[][] a, double[][] b) {
        int m = a.length;
        int n = a[0].length;
        double[][] c = new double[m][n];
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                c[i][j] = a[i][j] + b[i][j];
        return c;
    }

    // return c = a - b
    public static double[][] subtract(double[][] a, double[][] b) {
        int m = a.length;
        int n = a[0].length;
        double[][] c = new double[m][n];
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                c[i][j] = a[i][j] - b[i][j];
        return c;
    }

    // return c = a * b
    public static Matrix multiply(Matrix a, Matrix b) {
        int m1 = a.m.length;
        int n1 = a.m[0].length;
        int m2 = b.m.length;
        int n2 = b.m[0].length;
        if (n1 != m2) throw new RuntimeException("Illegal matrix dimensions.");
        double[][] c1 = new double[m1][n2];
        Matrix c = new Matrix(c1);
        for (int i = 0; i < m1; i++)
            for (int j = 0; j < n2; j++)
                for (int k = 0; k < n1; k++)
                    c.m[i][j] += a.m[i][k] * b.m[k][j];
        return c;
    }

    // matrix-vector multiplication (y = A * x)
    public static double[] multiply(double[][] a, double[] x) {
        int m = a.length;
        int n = a[0].length;
        if (x.length != n) throw new RuntimeException("Illegal matrix dimensions.");
        double[] y = new double[m];
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                y[i] += a[i][j] * x[j];
        return y;
    }


    // vector-matrix multiplication (y = x^T A)
    public static double[] multiply(double[] x, double[][] a) {
        int m = a.length;
        int n = a[0].length;
        if (x.length != m) throw new RuntimeException("Illegal matrix dimensions.");
        double[] y = new double[n];
        for (int j = 0; j < n; j++)
            for (int i = 0; i < m; i++)
                y[j] += a[i][j] * x[i];
        return y;
    }
    public static void print(Matrix a){
      int m = a.m.length;
      int n = a.m[0].length;
      for (int j = 0; j < n; j++){
          for (int i = 0; i < m; i++)
              System.out.print(a.m[j][i] + " ");
          System.out.println();
      }
    }

    // test client
    // public static void main(String[] args) {
    //     System.out.println("D");
    //     System.out.println("--------------------");
    //     double[][] d = { { 1, 2, 3 }, { 4, 5, 6 }, { 9, 1, 3} };
    //     Matrix.print(d);
    //     System.out.println();
    //
    //     System.out.println("I");
    //     System.out.println("--------------------");
    //     double[][] c = Matrix.identity(5);
    //     Matrix.print(c);
    //     System.out.println();
    //
    //     System.out.println("A");
    //     System.out.println("--------------------");
    //     double[][] a = Matrix.random(5, 5);
    //     Matrix.print(a);
    //     System.out.println();
    //
    //     System.out.println("A^T");
    //     System.out.println("--------------------");
    //     double[][] b = Matrix.transpose(a);
    //     Matrix.print(b);
    //     System.out.println();
    //
    //     System.out.println("A + A^T");
    //     System.out.println("--------------------");
    //     double[][] e = Matrix.add(a, b);
    //     Matrix.print(e);
    //     System.out.println();
    //
    //     System.out.println("A * A^T");
    //     System.out.println("--------------------");
    //     double[][] f = Matrix.multiply(a, b);
    //     Matrix.print(f);
    //     System.out.println();
    // }
}
