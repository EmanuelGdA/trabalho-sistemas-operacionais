# Gerenciamento de memória em sistemas operacionais

Trabalho Prático 1 de Sistemas Operacionais, do curso de Engenharia de Software da UniCesumar. Os programas demonstram alocação de memória, fragmentação, coleta de lixo e substituição de páginas.

## Programas

| Questão | Arquivo | O que o programa demonstra |
| --- | --- | --- |
| 1 | [questao1.c](questao1.c) | Compara os valores e os endereços de um vetor local na pilha com os de um vetor alocado no heap com `malloc`. |
| 2 | [questao2.py](questao2.py) | Simula a alocação de processos em partições com First-Fit, mede a fragmentação interna e mostra quando um processo não cabe nas partições livres. |
| 3 | [FifoPaginas.java](FifoPaginas.java) | Simula a substituição de páginas por FIFO e apresenta o número de acertos, faltas e a taxa de faltas. |
| 4 | [questao4.py](questao4.py) | Demonstra contagem de referências, referências cíclicas e coleta de lixo no Python. |
| 5 | [questao5.c](questao5.c) | Mede e compara o tempo de alocação na pilha e no heap. |
| Bônus | [ComparacaoLRU.java](ComparacaoLRU.java) | Compara as taxas de faltas de página de FIFO e LRU usando a mesma sequência de referências. |

## Como executar no Windows

Abra o PowerShell na pasta dos arquivos de código. Use GCC para os programas em C, Python 3 (CPython) para os scripts e um JDK com os comandos `javac` e `java` para os programas em Java. Os programas usam as bibliotecas padrão de cada linguagem.

### Questões 1 e 5 em C

~~~powershell
gcc questao1.c -o questao1.exe
.\questao1.exe

gcc -O0 questao5.c -o questao5.exe
.\questao5.exe
~~~

Os endereços da questão 1 e os tempos da questão 5 podem variar entre execuções.

### Questões 2 e 4 em Python

~~~powershell
python questao2.py
python questao4.py
~~~

As estatísticas de coleta de lixo da questão 4 podem variar conforme a versão do Python.

### Questão 3 e bônus em Java

~~~powershell
javac FifoPaginas.java ComparacaoLRU.java
java FifoPaginas
~~~

Quando o programa pedir a entrada, digite a quantidade de quadros de memória na primeira linha e a sequência de páginas separadas por vírgulas na segunda. Use a entrada abaixo para testar.

~~~text
3
7,0,1,2,0,3,0,4,2,3,0,3,2
~~~

Para comparar FIFO e LRU, execute o comando abaixo e informe a mesma entrada. Nesse exemplo, o FIFO tem 10 faltas de página e o LRU tem 9.

~~~powershell
java ComparacaoLRU
~~~
