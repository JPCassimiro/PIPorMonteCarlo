import java.util.ArrayList;
import java.util.List;

public class MonteCarloThread {
    static int hit;// valor total de pontos dentro do circuilo
    static final List<Integer> resultList = new ArrayList<>();// lista global de resultados parciais

    public static void main(String[] args) {

        int nThreads = 4;
        Thread[] threads = new Thread[nThreads];

        int totalPoints = 4550000; // valor padrão

        // int n = 8000;
        // int n = 150000;
        // int n = 500000;
        // int n = 1000000;

        int slice = totalPoints / nThreads;// parte do total de pontos que será trabalhado em cada thread

        long timeStart = System.currentTimeMillis();

        for (int i = 0; i < nThreads; i++) {// loop que cria as threads e da start
            threads[i] = new Thread(new ThreadMC(slice));// criação da thread
            threads[i].start();// inicia da thread
        }

        for (Thread thread : threads) {// join nas threads
            try {
                thread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        for (int i = 0; i < resultList.size(); i++) {// loop que pega a lista global de resutaldos parciais
            hit += resultList.get(i);// total de resultados parciais
        }

        double pi = 4.0 * hit / totalPoints;// propaga o resutaldo para os outros quadrantes do circulo

        long timeEnd = System.currentTimeMillis();

        System.out.println("\nPi estimado: " + pi);
        System.out.println("\nEm: " + (timeEnd - timeStart) + "ms");
        System.out.println("\nCom: " + totalPoints + " pontos totais");
    }

    public static class ThreadMC implements Runnable {// declaração da thread

        private final int sliceThread;

        public ThreadMC(int slice) {// atribuição da slice
            this.sliceThread = slice;
        }

        @Override
        public void run() {// operação que será feita pela thread
            int localHit = 0;// variavel local de acertos

            long timeStart = System.currentTimeMillis();

            for (int i = 0; i < sliceThread; i++) {// loop que tenta colocar os pontos dentro do circulo
                double x = Math.random();// coordenada x do ponto
                double y = Math.random();// coordenada y do ponto
                if (x * x + y * y < 1.0) {// checa se o ponto está no quadrante correto do circulo
                    localHit++;// incrementa o contador local
                }
            }

            synchronized (resultList) {// região critica para não causar condição de corrida, somente uma thread por vez pode manipular essa variavel
                resultList.add(localHit);// atribuição do valor de acertos parcial ao vetor de valores total
            }

            long timeEnd = System.currentTimeMillis();

            System.out.println("\nA thread '" + Thread.currentThread().getName() + "' terminou sua parte de " + sliceThread + " em: " + (timeEnd - timeStart) + "ms");
        }
    }

}
