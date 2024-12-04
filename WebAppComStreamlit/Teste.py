import json, re, random
from collections import defaultdict

class Prova:
    def __init__(self, arquivo_json, questoes_por_topico):
        """
        Inicializa a prova com o arquivo de questões e a quantidade de questões por tópico.

        :param arquivo_json: Caminho para o arquivo JSON com todas as perguntas.
        :param questoes_por_topico: Dicionário com o número de questões a serem selecionadas por tópico.
        """
        self.questoes_por_topico = questoes_por_topico
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            self.perguntas = json.load(f)
        self.prova = []

    def selecionar_questoes(self):
        """
        Seleciona aleatoriamente uma quantidade específica de questões para cada tópico com base em questoes_por_topico.
        """
        perguntas_por_topico = defaultdict(list)

        # Organizar perguntas por tópico
        for pergunta in self.perguntas:
            perguntas_por_topico[pergunta['topic']].append(pergunta)

        # Selecionar aleatoriamente as questões de cada tópico
        for topico, quantidade in self.questoes_por_topico.items():
            if topico in perguntas_por_topico:
                self.prova.extend(random.sample(perguntas_por_topico[topico], min(quantidade, len(perguntas_por_topico[topico]))))

    def embaralhar_questoes(self):
        """
        Embaralha a ordem das questões selecionadas, misturando tópicos.
        """
        random.shuffle(self.prova)

    def embaralhar_respostas(self):
        """
        Embaralha a ordem das respostas e distratores para cada questão na prova.
        """
        for pergunta in self.prova:
            # Remover apenas a numeração padrão no início (ex.: "1. ", "2. ", etc.)
            distratores_limpos = [
                re.sub(r"^\s*\d+\.\s*", "", distractor.strip()) for distractor in pergunta['distractors']
            ]
            # Adicionar a resposta correta
            opcoes = distratores_limpos + [pergunta['answer'].strip()]

            # Embaralhar as opções
            random.shuffle(opcoes)
            pergunta['options'] = opcoes  # Atualizar as opções da pergunta

    def enumerar_questoes(self):
        """
        Adiciona numeração às questões selecionadas.
        """
        for indice, pergunta in enumerate(self.prova, start=1):
            pergunta['numeração'] = indice

    def gerar_prova(self, arquivo_saida=None):
        """
        Gera a prova completa selecionando questões, embaralhando-as e organizando as opções.
        Se um arquivo de saída for fornecido, salva a prova processada no arquivo.

        :param arquivo_saida: Caminho para o arquivo onde a prova processada será salva (opcional).
        """
        # Etapas de processamento
        self.selecionar_questoes()
        self.embaralhar_questoes()
        self.embaralhar_respostas()
        self.enumerar_questoes()

        # Exibe ou salva as perguntas processadas
        if arquivo_saida:
            with open(arquivo_saida, 'w', encoding='utf-16') as f:
                json.dump(self.prova, f, indent=4, ensure_ascii=False)
            print(f"Prova processada salva em '{arquivo_saida}'")
        else:
            print("=== Perguntas Processadas ===")
            for pergunta in self.prova:
                print(f"Pergunta: {pergunta['question']}")
                print(f"Opções: {pergunta['options']}")
                print(f"Resposta Correta: {pergunta['answer']}")
                print(f"Tópico: {pergunta.get('topic', 'Não especificado')}")
                print(f"Numeração: {pergunta.get('numeração', 'Sem numeração')}")
                print("-" * 40)

questoes_por_topico = {
    "Basic Syntax": 11,
    "DataTypes, Variables": 11,
    "Conditionals": 9,
    "Functions": 11,
    "Loops": 8,
    "Exception Handling": 12,
    "DataStructures": 6,
    "OOP, Interfaces, Classes": 10,
    "Packages": 12,
    "Working With Files and APIs": 11
}
prova = Prova("perguntasT.json", questoes_por_topico)
prova.gerar_prova("prova_processada.json")
