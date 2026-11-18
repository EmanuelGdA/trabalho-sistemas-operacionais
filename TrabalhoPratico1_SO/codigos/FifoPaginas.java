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
Descritivo: Questão 3 - Simulação do algoritmo de substituição de páginas FIFO (Java).
            Compilar: javac FifoPaginas.java
            Executar: java FifoPaginas
*******************************************************************************/

import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;

public class FifoPaginas {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        try {
            System.out.println("Q3 | Substituicao de paginas por FIFO");
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
            simular(numFrames, refs);
        } catch (NumberFormatException e) {
            System.out.println("Entrada invalida: use apenas numeros inteiros.");
        }
    }

    static void simular(int numFrames, int[] refs) {
        // A cabeça da fila guarda a página que entrou primeiro.
        Queue<Integer> frames = new LinkedList<>();
        int faltas = 0;

        System.out.printf("%n%11s | %-19s | %6s | %s%n",
                "Referencia", "Evento", "Faltas", "Fila (inicio -> fim)");
        System.out.println("------------+---------------------+--------+--------------------");
        for (int pagina : refs) {
            String status;
            if (frames.contains(pagina)) {
                // No FIFO, um acerto mantém a página na mesma posição da fila.
                status = "Acerto";
            } else {
                faltas++;
                // Só há substituição quando todos os quadros estão ocupados.
                if (frames.size() == numFrames) {
                    int removida = frames.poll();
                    status = "Falta (sai " + removida + ")";
                } else {
                    status = "Falta (vaga livre)";
                }
                frames.add(pagina); // a página recém-carregada vai para o fim da fila
            }
            System.out.printf("%11d | %-19s | %6d | %s%n", pagina, status, faltas, frames);
        }

        // O cast para double mantém a parte fracionária da divisão.
        double taxa = (double) faltas / refs.length;
        System.out.printf("%nResumo FIFO | %d referencias | %d acertos | %d faltas (%.2f%%)%n",
                refs.length, refs.length - faltas, faltas, taxa * 100);
    }
}
