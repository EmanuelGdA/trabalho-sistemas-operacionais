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
Descritivo: Questão 1 - Alocação estática vs. dinâmica de memória (C).
            Compilar: gcc questao1.c -o questao1
            Executar: ./questao1  (Windows: questao1.exe)
*******************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(void) {
    /* O enunciado chama este array de estático pelo tamanho fixo.
       Em C, ele é uma variável local com duração automática, normalmente na pilha. */
    int estatico[5];
    for (int i = 0; i < 5; i++) {
        estatico[i] = i + 1;                 /* valores de 1 a 5 */
    }

    /* O malloc reserva no heap espaço para 10 inteiros. A checagem de NULL
       vem antes de qualquer acesso ao bloco. */
    int *dinamico = (int *) malloc(10 * sizeof(int));
    if (dinamico == NULL) {
        fprintf(stderr, "Erro: falha na alocacao dinamica.\n");
        return EXIT_FAILURE;
    }

    /* 3. Preenche o array dinamico com valores de 10 a 19 */
    for (int i = 0; i < 10; i++) {
        dinamico[i] = 10 + i;
    }

    /* %p recebe um void*. Os endereços mostram que os elementos de cada
       array ocupam posições consecutivas, com um sizeof(int) entre eles. */
    printf("\nQ1 | Enderecos dos arrays\n");
    printf("%-16s %6s %5s  %s\n", "Origem", "Indice", "Valor", "Endereco");
    printf("--------------------------------------------------\n");
    for (int i = 0; i < 5; i++) {
        printf("%-16s %6d %5d  %p\n", "Pilha (fixo)", i, estatico[i], (void *)&estatico[i]);
    }
    for (int i = 0; i < 10; i++) {
        printf("%-16s %6d %5d  %p\n", "Heap (malloc)", i, dinamico[i], (void *)&dinamico[i]);
    }

    /* A subtração direta de ponteiros de arrays distintos é indefinida em C.
       Aqui comparamos os endereços convertidos para inteiros e subtraímos
       o menor do maior. A distância observada varia entre execuções. */
    uintptr_t end_est = (uintptr_t) estatico;
    uintptr_t end_din = (uintptr_t) dinamico;
    uintptr_t diferenca = (end_est > end_din) ? (end_est - end_din) : (end_din - end_est);

    printf("\nComparacao dos enderecos iniciais\n");
    printf("  Pilha : %p\n", (void *)estatico);
    printf("  Heap  : %p\n", (void *)dinamico);
    printf("  Distancia entre os enderecos: %llu bytes\n", (unsigned long long) diferenca);

    /* O bloco do malloc precisa de free. A duração do array local termina
       quando main retorna. */
    free(dinamico);
    dinamico = NULL;                         /* o bloco já foi devolvido ao alocador */
    return EXIT_SUCCESS;
}
