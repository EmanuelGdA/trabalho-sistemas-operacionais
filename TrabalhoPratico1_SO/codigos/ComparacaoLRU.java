/******************************************************************************
Curso: Engenharia de Software
Disciplina: Sistemas Operacionais
Professor: José Carlos Domingues Flores
Turma: ESOFT4
Componentes:
             25001118-2 -  Emanuel Gomes de Almeida
             25033056-2 -  Gabriel Michels Cubas
             25164719-2 -  Rafael Maia
             25291090-2 -  João Lucas Veiga de Carvalho

Data: 18 de Novembro de 2026
Descritivo: Questão Bônus - Comparação entre LRU e FIFO (Java).
            Compilar: javac ComparacaoLRU.java
            Executar: java ComparacaoLRU
*******************************************************************************/

import java.util.*;

public class ComparacaoLRU {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        try {
            System.out.println("Bonus | Comparacao FIFO e LRU");
            System.out.print("Quantidade de quadros: ");
            int numFrames = Integer.parseInt(sc.nextLine().trim());
            if (numFrames <= 0) {
                System.out.println("O numero de frames deve ser maior que zero.");
                return;
            }
            System.out.print("Sequencia de referencias (separadas por virgula): ");
            String[] partes = sc.nextLine().split(",");
            int[] refs = new int[partes.length];
            for (int i = 0; i < partes.length; i++) {
                refs[i] = Integer.parseInt(partes[i].trim());
            }

            // Os dois algoritmos recebem a mesma sequência e a mesma capacidade.
            int faltasFifo = fifo(numFrames, refs);
            int faltasLru = lru(numFrames, refs);

            System.out.printf("%nMesma entrada: %d referencias em %d quadros%n%n", refs.length, numFrames);
            System.out.printf("%-9s | %6s | %14s%n", "Algoritmo", "Faltas", "Taxa de faltas");
            System.out.println("----------+--------+---------------");
            System.out.printf("%-9s | %6d | %13.2f%%%n", "FIFO", faltasFifo, 100.0 * faltasFifo / refs.length);
            System.out.printf("%-9s | %6d | %13.2f%%%n", "LRU", faltasLru, 100.0 * faltasLru / refs.length);
            System.out.print("\nNesta sequencia: ");
            if (faltasLru < faltasFifo) {
                System.out.println("O LRU teve " + (faltasFifo - faltasLru) + " falta(s) a menos.");
            } else if (faltasLru > faltasFifo) {
                System.out.println("O FIFO teve " + (faltasLru - faltasFifo) + " falta(s) a menos.");
            } else {
                System.out.println("Os dois tiveram o mesmo numero de faltas.");
            }
            System.out.println("FIFO segue a ordem de entrada; LRU considera o acesso mais recente.");
        } catch (NumberFormatException e) {
            System.out.println("Entrada invalida: use apenas numeros inteiros.");
        }
    }

    // FIFO guarda a ordem de entrada. Um acerto deixa a fila como está.
    static int fifo(int numFrames, int[] refs) {
        Queue<Integer> frames = new LinkedList<>();
        int faltas = 0;
        for (int p : refs) {
            if (!frames.contains(p)) {
                faltas++;
                if (frames.size() == numFrames) frames.poll();
                frames.add(p);
            }
        }
        return faltas;
    }

    // Cada chave do mapa é uma página carregada. O valor é o índice
    // da última referência àquela página na sequência.
    static int lru(int numFrames, int[] refs) {
        Map<Integer, Integer> ultimoUso = new HashMap<>();
        int faltas = 0;
        for (int t = 0; t < refs.length; t++) {
            int p = refs[t];
            if (!ultimoUso.containsKey(p)) {
                faltas++;
                if (ultimoUso.size() == numFrames) {
                    // Com os quadros cheios, o menor índice indica o uso mais antigo.
                    int vitima = -1, menor = Integer.MAX_VALUE;
                    for (Map.Entry<Integer, Integer> e : ultimoUso.entrySet()) {
                        if (e.getValue() < menor) {
                            menor = e.getValue();
                            vitima = e.getKey();
                        }
                    }
                    ultimoUso.remove(vitima);
                }
            }
            // Um acerto também renova o último uso e pode mudar a próxima vítima.
            ultimoUso.put(p, t);
        }
        return faltas;
    }
}
