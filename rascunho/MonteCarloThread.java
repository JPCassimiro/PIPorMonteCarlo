public class MonteCarloThread {
    public static void main(String[] args) {
        int nNucleos = Runtime.getRuntime().availableProcessors();
        Thread[] threads = new Thread[nNucleos];
        long tInicio = System.currentTimeMillis();
        int n = 4550000;
        for (int i = 0; i < nNucleos; i++) {
            int parte = ((i + 1) * n)/nNucleos;
            threads[i] = new Thread(new ThreadMC(parte,0));
            threads[i].start();
        }
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        long tFim = System.currentTimeMillis();
        System.out.println(tFim-tInicio);
    }

}
