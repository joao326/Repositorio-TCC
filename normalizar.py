import json
import unicodedata

def normalizar_dados(arquivo_json, arquivo_saida):
    """
    Carrega um arquivo JSON, normaliza os caracteres e salva o JSON corrigido.
    
    :param arquivo_json: Caminho para o arquivo JSON original.
    :param arquivo_saida: Caminho para salvar o JSON corrigido.
    """
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    for pergunta in dados:
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

    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    print(f"Arquivo normalizado salvo em: {arquivo_saida}")

# Uso:
normalizar_dados('perguntas_processadas.json', 'perguntasT_normalizado.json')
