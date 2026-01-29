import pandas as pd
import os

def verificar_padronizacao():
    # --- CONFIGURAÇÃO ---
    # Nome do arquivo que você quer checar (pode ser o unificado ou um específico)
    # Se quiser checar o arquivo que acabou de gerar, use 'TODOS_DADOS_UNIFICADOS.csv'
    nome_arquivo = 'TODOS_DADOS_UNIFICADOS_LIMPO.csv'
    
    # Pega o caminho onde o script está
    pasta_raiz = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(pasta_raiz, nome_arquivo)
    
    print(f"Analisando arquivo: {nome_arquivo}...\n")
    
    if not os.path.exists(caminho_arquivo):
        print(f"ERRO: Arquivo não encontrado em {caminho_arquivo}")
        return

    try:
        df = pd.read_csv(caminho_arquivo, sep=',', encoding='utf-8')
    except Exception as e:
        print(f"Erro ao abrir arquivo: {e}")
        return

    problemas_encontrados = False

    # Analisa apenas colunas de texto (object)
    for coluna in df.select_dtypes(include=['object']).columns:
        # Pega os valores únicos da coluna (ignorando vazios)
        valores_unicos = df[coluna].dropna().unique()
        
        # Dicionário para agrupar variações: 
        # Chave = texto minúsculo e sem espaço | Valor = lista de variações originais
        mapa_variacoes = {}
        
        for valor in valores_unicos:
            valor_str = str(valor)
            # Normaliza: tudo minúsculo e remove espaços das pontas
            chave_normalizada = valor_str.lower().strip()
            
            if chave_normalizada not in mapa_variacoes:
                mapa_variacoes[chave_normalizada] = set()
            
            mapa_variacoes[chave_normalizada].add(valor_str)
        
        # Filtra apenas onde existe mais de 1 forma de escrever a mesma coisa
        inconsistencias = {k: v for k, v in mapa_variacoes.items() if len(v) > 1}
        
        if inconsistencias:
            problemas_encontrados = True
            print(f"⚠️  COLUNA: '{coluna}'")
            for base, variacoes in inconsistencias.items():
                lista_var = list(variacoes)
                print(f"   > Variações de '{base}':")
                # Mostra as variações encontradas
                for v in lista_var:
                    print(f"     - \"{v}\"") 
            print("-" * 30)

    if not problemas_encontrados:
        print("✅ Tudo limpo! Não foram encontradas variações de escrita (case sensitive/espaços).")
    else:
        print("\nRESUMO: As linhas acima mostram onde o computador vê diferença, mas nós lemos igual.")

if __name__ == "__main__":
    verificar_padronizacao()