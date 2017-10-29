import java.util.*;
import java.util.concurrent.*;


public class MnozenieMacierze {
  public static class Mnozenie implements Callable {
    private Matrix matrix1;
    private Matrix matrix2;
    public Mnozenie(Matrix m1, Matrix m2) {
      this.matrix1 = m1;
      this.matrix2 = m2;
    }
    public Matrix call() {
      return Matrix.multiply(matrix1,matrix2);
    }
  }

  public static void main(String args[]) throws Exception {
  ExecutorService pool = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
    Set<Future<Matrix> > set = new HashSet<Future<Matrix>>();
    //
    // for (String word: args) {
    LinkedList<Matrix> mList = new LinkedList<Matrix>();
    for(int i = 0; i < 100; i++){
        double[][] a1 = { { 1, 2, 3 }, { 4, 5, 6 }, { 9, 1, 3} };
        Matrix a = new Matrix(a1);
        mList.add(a);
    }

    for(int i = 0; i < mList.size(); i+=2){
       Callable< Matrix> ca = new Mnozenie(mList.get(i) , mList.get(i+1));
       Future< Matrix> future = pool.submit(ca);
       set.add(future);
    }

    for (Future<Matrix> future : set) {
       Matrix.print(future.get());
    }

     System.exit(0);
  }
}
