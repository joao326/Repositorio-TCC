import json, random, re, unicodedata
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
        self.normalizar_perguntas() # Normaliza corrigindo caracteres ao carregar
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
        Adiciona numeração às questões da prova.
        """
        for indice, pergunta in enumerate(self.prova, start=1):
            pergunta['numeração'] = indice

    def normalizar_perguntas(self):
        """
        Normaliza os dados das perguntas carregadas, corrigindo a codificação Unicode e limpando espaços extras.
        """
        for pergunta in self.perguntas:
            pergunta['question'] = unicodedata.normalize('NFKC', pergunta['question']).strip()
            pergunta['answer'] = unicodedata.normalize('NFKC', pergunta['answer']).strip()
            pergunta['topic'] = unicodedata.normalize('NFKC', pergunta['topic']).strip()
            if 'distractors' in pergunta:
                pergunta['distractors'] = [
                    unicodedata.normalize('NFKC', distractor).strip() for distractor in pergunta['distractors']
                ]
            if 'options' in pergunta:
                pergunta['options'] = [
                    unicodedata.normalize('NFKC', option).strip() for option in pergunta['options']
                ]       

    def gerar_prova(self, arquivo_saida=None):
        """
        Gera a prova completa selecionando questões, embaralhando-as e organizando as opções.
        """
        self.selecionar_questoes()
        self.embaralhar_questoes()
        self.embaralhar_respostas()
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
