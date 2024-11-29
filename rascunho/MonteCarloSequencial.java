
public class MonteCarloSequencial{
    public static void main(String[] args) {
        calc(4550000);
        // calc(3000);
    }

    public static void calc(int n) {
        long timeBegin = System.currentTimeMillis(); 
        int hit = 0;
        for(int i = 0; i < n; i++){
            double x = Math.random();
            double y = Math.random();

            if(x * x + y * y < 1.0){
                hit++;
            }
        }
        long timeEnd = System.currentTimeMillis(); 
        double pi = 4.0 * hit / n;
        System.out.println("\nPi: "+pi);
        System.out.println("\nCom: " + n + " pontos");
        System.out.println("\nEm: "+(timeEnd-timeBegin)+"ms");
    }
}