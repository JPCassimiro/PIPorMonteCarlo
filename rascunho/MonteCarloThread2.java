public class MonteCarloThread2 {
    static int hit;

    public static void main(String[] args) {
        
        int nNucleos = Runtime.getRuntime().availableProcessors();
        Thread[] threads = new Thread[nNucleos];

        int n = 4550000;
        int parte = n / nNucleos;
        System.out.println("\nparte: " + parte);

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
        double pi = 4.0 * hit / n;
        long tFim = System.currentTimeMillis();
        System.out.println("\nPi: " + pi);
        System.out.println("\nEm: " + (tFim-tInicio)+"ms");
    }

    public static class ThreadMC implements Runnable {
        private int nParte;

        public ThreadMC(int parte){
            this.nParte = parte;
        }
    
        @Override
        public void run(){
            for(int i = 0; i < nParte; i++){
                double x = Math.random();
                double y = Math.random();
                if(x * x + y * y < 1.0){
                    hit++;
                }
            }
        }
    }

}
