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
Descritivo: Questão 5 - Comparação de desempenho: pilha x heap (C).
            Compilar: gcc -O0 questao5.c -o questao5
            Executar: ./questao5  (Windows: questao5.exe)
*******************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 1000000          /* operacoes por teste */
#define REPETICOES 5       /* cada teste roda varias vezes para tirar a media */

typedef struct {
    int a;
    int b;
    double c;
} Dado;

/* As duas funções somam no mesmo acumulador. O acesso a sink é observável
   por ser volatile. O -O0 reduz otimizações que podem mudar o teste. */
volatile long long sink = 0;

/* A variável local é criada a cada chamada e o espaço na pilha pode ser
   reutilizado assim que a função retorna. */
void usa_pilha(int i) {
    Dado d;
    d.a = i;
    d.b = i * 2;
    d.c = i * 0.5;
    sink += d.a;
}

/* O objeto tem o mesmo tipo usado na pilha. Aqui malloc reserva o bloco
   e free o devolve ao alocador ao fim de cada chamada. */
void usa_heap(int i) {
    Dado *d = (Dado *) malloc(sizeof(Dado));
    if (d == NULL) {
        fprintf(stderr, "Erro: falha no malloc.\n");
        exit(EXIT_FAILURE);
    }
    d->a = i;
    d->b = i * 2;
    d->c = i * 0.5;
    sink += d->a;
    free(d);
}

/* Cada medição cobre o laço inteiro, incluindo as chamadas e a inicialização
   dos campos. CLOCKS_PER_SEC ajuda a converter os ticks em milissegundos. */
double medir_pilha(void) {
    clock_t ini = clock();
    for (int i = 0; i < N; i++) usa_pilha(i);
    return (double)(clock() - ini) * 1000.0 / CLOCKS_PER_SEC;   /* ms */
}

double medir_heap(void) {
    clock_t ini = clock();
    for (int i = 0; i < N; i++) usa_heap(i);
    return (double)(clock() - ini) * 1000.0 / CLOCKS_PER_SEC;   /* ms */
}

int main(void) {
    double soma_pilha = 0, soma_heap = 0;

    printf("Q5 | Tempo de alocacao: pilha e heap\n");
    printf("%d operacoes por teste, %d rodadas. Tempos em milissegundos.\n\n", N, REPETICOES);
    printf("%-8s | %11s | %11s\n", "Rodada", "Pilha (ms)", "Heap (ms)");
    printf("---------+-------------+------------\n");
    for (int r = 1; r <= REPETICOES; r++) {
        double tp = medir_pilha();
        double th = medir_heap();
        soma_pilha += tp;
        soma_heap += th;
        printf("%8d | %11.2f | %11.2f\n", r, tp, th);
    }

    double media_pilha = soma_pilha / REPETICOES;
    double media_heap = soma_heap / REPETICOES;

    printf("---------+-------------+------------\n");
    printf("%-8s | %11.2f | %11.2f\n", "Media", media_pilha, media_heap);

    /* Usamos a média da pilha como base para o percentual. O teste de zero
       evita dividir por zero quando o relógio não distingue o intervalo. */
    if (media_pilha > 0) {
        printf("\nVariacao do tempo do heap em relacao a pilha: %+.1f%%\n",
               (media_heap - media_pilha) / media_pilha * 100.0);
        printf("Razao entre os tempos (heap / pilha): %.2fx\n", media_heap / media_pilha);
    } else {
        printf("Tempo da pilha abaixo da resolucao do relogio; aumente N.\n");
    }

    /*
     * A pilha costuma ter um custo menor porque basta reservar espaço no
     * quadro da função. No heap, malloc e free gerenciam os blocos livres.
     *
     * Como toda rodada usa blocos do mesmo tamanho e os libera logo após
     * o uso, o alocador pode reaproveitar esses blocos. A média ajuda a
     * reduzir o efeito das oscilações entre as rodadas. Os tempos também
     * dependem da máquina, da carga do sistema e do compilador.
     */
    return EXIT_SUCCESS;
}
