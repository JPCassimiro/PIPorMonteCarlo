public class MonteCarloSequencial {
    public static void main(String[] args) {
        // valor total de pontos
        estimatePi(4550000); // valor padrão

        // valores alternativos para teste
        // estimatePi(8000);
        // estimatePi(150000);
        // estimatePi(1000000);
    }

    public static void estimatePi(int totalPoints) {
        long timeStart = System.currentTimeMillis();

        int hit = 0;// numero de pontos dentro do circulo

        for (int i = 0; i < totalPoints; i++) {// loop que tenta colocar os pontos dentro do circulo
            double x = Math.random();// coordenada x do ponto
            double y = Math.random();// coordenada y do ponto
            if (x * x + y * y < 1.0) {// checa se o ponto está no quadrante correto do circulo
                hit++;// incrementa o contador
            }
        }

        long timeEnd = System.currentTimeMillis();

        double pi = 4.0 * hit / totalPoints;// propaga o resutaldo para os outros quadrantes do circulo

        System.out.println("\nPi estimado: " + pi);
        System.out.println("\nCom: " + totalPoints + " pontos totais");
        System.out.println("\nEm: " + (timeEnd - timeStart) + "ms");
    }
}