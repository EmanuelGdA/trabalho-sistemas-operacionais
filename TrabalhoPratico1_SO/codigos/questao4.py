"""
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
Descritivo: Questão 4 - Demonstração do Garbage Collector em Python.
            Executar: python questao4.py
"""

import gc
import sys


class Objeto:
    def __init__(self, nome):
        self.nome = nome
        self.dados = [0] * 100_000      # a lista ocupa memória com 100 mil posições
        self.ref = None                 # este atributo permite ligar um objeto a outro
        print(f"    + {self.nome} criado")

    def __del__(self):
        # A mensagem permite ver em que momento o CPython finaliza o objeto.
        print(f"    - {self.nome} finalizado")


class No:
    """Classe leve, usada so para gerar muitos ciclos no cenario 4."""
    def __init__(self):
        self.outro = None


print("Q4 | Coleta de lixo no CPython")
print("\n01 | Contagem de referencias")
a = Objeto("A")
# Passar a como argumento de getrefcount cria uma referência temporária.
# Por isso o valor exibido inclui essa referência extra.
print("    A sozinho       ->", sys.getrefcount(a), "referencias")
b = a                               # os dois nomes apontam para o mesmo objeto
print("    Depois de b = a ->", sys.getrefcount(a), "referencias")
del b                               # a ainda mantém o objeto acessível
print("    Depois de del b ->", sys.getrefcount(a), "referencias")
print("    del a -> ultima referencia removida")
del a                               # no CPython, a contagem chega a zero e o objeto é destruído
print("\n02 | Ciclo entre X e Y (X -> Y -> X)")
# Pausa a coleta automática de ciclos. A contagem de referências continua ativa.
gc.disable()
x = Objeto("X")
y = Objeto("Y")
x.ref = y
y.ref = x
# Os nomes somem, mas X e Y ainda guardam referências um ao outro.
del x, y
print("    del x, y -> as referencias internas do ciclo continuam ativas")
print("    gc.collect() -> busca manual por ciclos")
# A coleta manual funciona mesmo com a coleta automática desativada.
# A contagem retornada pode incluir as listas de dados ligadas a X e Y.
coletados = gc.collect()
print(f"    Retorno da coleta: {coletados} objetos inalcancaveis")

print("\n03 | Autorreferencia (Z -> Z)")
z = Objeto("Z")
z.ref = z
print("    Z com autorreferencia ->", sys.getrefcount(z), "referencias")
del z                               # a referência que Z guarda para si mesmo ainda existe
print("    del z -> o ciclo permanece; chamando gc.collect()")
coletados = gc.collect()
print(f"    Retorno da coleta: {coletados} objetos inalcancaveis")

print("\n04 | Coleta automatica durante a criacao de ciclos")
gc.enable()                         # retoma a coleta automática
gc.collect()                        # faz uma coleta antes de registrar o ponto de partida
print("    Limiares do gc:", gc.get_threshold())
antes = [g["collections"] for g in gc.get_stats()]
# A cada nova dupla, n1 e n2 passam a apontar para os novos nós.
# A dupla anterior fica inacessível por fora do ciclo e pode ser coletada.
for _ in range(20_000):
    n1, n2 = No(), No()
    n1.outro, n2.outro = n2, n1
# As estatísticas são acumuladas. Subtraímos os valores anteriores
# para contar as coletas disparadas durante o laço.
depois = [g["collections"] for g in gc.get_stats()]
for i in range(3):
    print(f"    Geracao {i} -> {depois[i] - antes[i]:>3} coletas durante o laco")
print("    Objetos que sobrevivem podem passar para geracoes mais antigas.")

print("\nEstatisticas acumuladas (gc.get_stats)")
print(f"{'Geracao':>7} | {'Coletas':>7} | {'Coletados':>9} | {'Incoletaveis':>12}")
print("--------+---------+-----------+-------------")
for i, g in enumerate(gc.get_stats()):
    print(f"{i:>7} | {g['collections']:>7} | {g['collected']:>9} | {g['uncollectable']:>12}")
