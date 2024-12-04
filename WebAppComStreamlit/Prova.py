import json
import random
from collections import defaultdict

class Prova:
    def __init__(self, arquivo_json, questoes_por_topico):
        """
        Inicializa a prova com o arquivo de questões e a quantidade de questões por tópico.

        :param arquivo_json: Caminho para o arquivo JSON com todas as perguntas.
        :param questoes_por_topico: Dicionário com o número de questões a serem selecionadas por tópico.
        """
        self.questoes_por_topico = questoes_por_topico
        with open(arquivo_json, 'r',encoding='utf-8') as f:
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
            # Ex. de elemento: 'Fundamentals': [{'question': 'What is Java?', 'topic': 'Fundamentals'}],

        # Selecionar aleatoriamente as questões de cada tópico. Itera sobre cada 'topico' X 'quantidade' de vezes
        for topico, quantidade in self.questoes_por_topico.items():
            if topico in perguntas_por_topico:
                self.prova.extend(random.sample(perguntas_por_topico[topico], min(quantidade, len(perguntas_por_topico[topico]))))
                # Se quantidade for maior que nº disponível, seleciona só nº disponível.
                # Se for usado append vai adicionar a lista toda como um elemento. Extend pega cada elemento (questão) da lista e o adiciona

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
            #remover numeração dos distratores:
            distratores_limpos = [distractor.lstrip("1234.- ") for distractor in pergunta['distractors']]
            opcoes = distratores_limpos + [pergunta['answer']]
            # Ex.: opcoes = ["Option A", "Option B", "Option C", "Correct Answer"]

            random.shuffle(opcoes)
            pergunta['options'] = opcoes  # Adiciona as opções embaralhadas

    def enumerar_questoes(self):
        for indice, pergunta in enumerate(self.prova, start=1):
            pergunta['numeração'] = indice

    def gerar_prova(self):
        """
        Gera a prova completa selecionando questões, embaralhando-as e organizando as opções.
        """
        self.selecionar_questoes()
        self.embaralhar_questoes()
        self.embaralhar_respostas()