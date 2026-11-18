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
Descritivo: Questão 2 - Simulação de partições fixas com First-Fit (Python).
            Executar: python questao2.py
"""

# O tamanho de cada partição é fixo. "uso" guarda quanto o processo pediu
# e "processo" vale None quando a partição está livre.
TAMANHOS = [100, 150, 200, 250, 300]          # soma = 1000 unidades
particoes = [
    {"id": i + 1, "tamanho": t, "processo": None, "uso": 0}
    for i, t in enumerate(TAMANHOS)
]


def fragmentacao_total():
    """Soma a sobra dentro das partições ocupadas. As livres ficam fora da conta."""
    return sum(p["tamanho"] - p["uso"] for p in particoes if p["processo"] is not None)


def alocar_processo(nome, tamanho):
    """First-Fit: percorre as partições na ordem da lista e para na primeira que serve."""
    if tamanho <= 0:
        print(f"Erro: tamanho invalido para {nome}.")
        return False
    # A liberação é feita pelo nome, então cada nome identifica um só processo.
    if any(p["processo"] == nome for p in particoes):
        print(f"Erro: o processo {nome} ja esta alocado.")
        return False

    for p in particoes:
        if p["processo"] is None and p["tamanho"] >= tamanho:
            p["processo"] = nome
            p["uso"] = tamanho
            # A sobra fica reservada junto com o processo até ele ser liberado.
            frag = p["tamanho"] - tamanho
            print(f"[ENTRADA] {nome}: {tamanho} de {p['tamanho']} unidades na particao {p['id']}"
                  f" | Sobra: {frag} | Total interno: {fragmentacao_total()}")
            return True

    # Cada processo precisa caber inteiro em uma partição livre.
    print(f"[RECUSADO] {nome}: nenhuma particao livre comporta {tamanho} unidades"
          f" | Total interno: {fragmentacao_total()}")
    return False


def liberar_processo(nome):
    """Libera a particao ocupada pelo processo."""
    for p in particoes:
        if p["processo"] == nome:
            # A partição volta a ficar disponível com sua capacidade original.
            p["processo"] = None
            p["uso"] = 0
            print(f"[SAIDA] {nome}: particao {p['id']} liberada"
                  f" | Total interno: {fragmentacao_total()}")
            return True
    print(f"Erro: processo {nome} nao encontrado.\n")
    return False


def exibir_memoria():
    """Mostra o estado atual das particoes."""
    print(f"{'Particao':>8} | {'Capacidade':>10} | {'Processo':<8} | {'Uso':>4} | {'Sobra interna':>13}")
    print("---------+------------+----------+------+--------------")
    for p in particoes:
        processo = p["processo"] if p["processo"] is not None else "livre"
        sobra = p["tamanho"] - p["uso"] if p["processo"] is not None else "-"
        print(f"{p['id']:>8} | {p['tamanho']:>10} | {processo:<8} | {p['uso']:>4} | {sobra:>13}")
    print()


if __name__ == "__main__":
    print("Q2 | Particoes fixas com First-Fit (1000 unidades)\n")
    alocar_processo("P1", 90)
    alocar_processo("P2", 140)
    alocar_processo("P3", 180)
    print("\nMemoria apos as tres primeiras alocacoes")
    exibir_memoria()
    liberar_processo("P2")
    alocar_processo("P4", 100)                 # reutiliza a partição de P2 e deixa 50 de sobra
    alocar_processo("P5", 350)                 # 350 supera a capacidade da maior partição
    print("\nMemoria ao fim do teste")
    exibir_memoria()
    # Sobras das partições ocupadas por P1, P4 e P3: 10 + 50 + 20 = 80.
    print(f"Fragmentacao interna final: {fragmentacao_total()} unidades")
