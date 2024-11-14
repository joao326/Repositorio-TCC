import json
from collections import Counter

def contar_questoes(arquivo_json):
    # Carregar as perguntas do arquivo JSON
    with open(arquivo_json, 'r') as f:
        perguntas = json.load(f)

    # Contar a quantidade total de questões
    total_questoes = len(perguntas)

    # Contar a quantidade de questões por tópico
    contagem_por_topico = Counter(pergunta['topic'] for pergunta in perguntas)

    # Contar a quantidade de questões por nível de dificuldade
    contagem_por_dificuldade = Counter(pergunta['difficulty'] for pergunta in perguntas)

    # Exibir os resultados
    print(f"Quantidade total de questões: {total_questoes}\n")

    print("Quantidade de questões por tópico:")
    for topico, contagem in contagem_por_topico.items():
        print(f"  - {topico}: {contagem}")

    print("\nQuantidade de questões por nível de dificuldade:")
    for dificuldade, contagem in contagem_por_dificuldade.items():
        print(f"  - {dificuldade.capitalize()}: {contagem}")

# Exemplo de uso
arquivo_json = 'perguntas.json'
contar_questoes(arquivo_json)
