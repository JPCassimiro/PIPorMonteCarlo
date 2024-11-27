

public class ThreadMC implements Runnable {
    private int n;
    private int hit;
    public ThreadMC(int pInicial, int hit){
        this.n = pInicial;
        this.hit = hit;
    }

    @Override
    public void run(){
        for(int i = 0; i < n; i++){
            double x = Math.random();
            double y = Math.random();
            if(x * x + y * y < 1.0){
                hit++;
            }
        }
        double pi = 4.0 * hit / n;
        System.out.println("\npi: "+pi);
    }
}
