import java.util.ArrayList;
import java.util.List;

public class MonteCarloThread {
    static int hit;
    static final List<Integer> resultList = new ArrayList<>();
    
    public static void main(String[] args) {
        
        int nNucleos = Runtime.getRuntime().availableProcessors();
        Thread[] threads = new Thread[nNucleos];

        // int n = 4550000;
        int n = 8000;
        // int n = 150000;
        // int n = 500000;
        // int n = 1000000;
        int parte = n / nNucleos;

        long tInicio = System.currentTimeMillis();

        for (int i = 0; i < nNucleos; i++) {
            threads[i] = new Thread(new ThreadMC(parte));
            threads[i].start();
        }
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        for(int i = 0; i < resultList.size(); i++){
            hit += resultList.get(i);
        }
        double pi = 4.0 * hit / n;
        long tFim = System.currentTimeMillis();
        System.out.println("\nPi: " + pi);
        System.out.println("\nEm: " + (tFim-tInicio)+"ms");
        System.out.println("\nCom: " + n);
    }

    public static class ThreadMC implements Runnable {
        private final int nParte;

        public ThreadMC(int parte){
            this.nParte = parte;
        }
    
        @Override
        public void run(){
            int localHit = 0;
            long tInicio = System.currentTimeMillis();
            for(int i = 0; i < nParte; i++){
                double x = Math.random();
                double y = Math.random();
                if(x * x + y * y < 1.0){
                    localHit++;
                }
            }
            synchronized (resultList) {
                resultList.add(localHit);
            }
            long tFim = System.currentTimeMillis();
            System.out.println("\nA thread '"+ Thread.currentThread().getName() + "' terminou sua parte de " + nParte + " em: " + (tFim-tInicio)+"ms");
        }
    }

}
