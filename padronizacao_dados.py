import pandas as pd
import os

def corrigir_padroes():
    # --- CONFIGURAÇÕES ---
    arquivo_entrada = 'TODOS_DADOS_UNIFICADOS.csv'
    arquivo_saida = 'TODOS_DADOS_UNIFICADOS_LIMPO.csv' # Salva um novo para garantir
    
    pasta_raiz = os.path.dirname(os.path.abspath(__file__))
    caminho_entrada = os.path.join(pasta_raiz, arquivo_entrada)
    caminho_saida = os.path.join(pasta_raiz, arquivo_saida)
    
    print(f"Lendo: {arquivo_entrada}...")
    
    if not os.path.exists(caminho_entrada):
        print("ERRO: Arquivo de entrada não encontrado.")
        return

    df = pd.read_csv(caminho_entrada, sep=',', encoding='utf-8')
    
    # 1. REMOVER ESPAÇOS EM BRANCO (Trim) DE TODAS AS COLUNAS DE TEXTO
    # Isso resolve "Linhares " vs "Linhares"
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    
    # 2. PADRONIZAÇÃO ESPECÍFICA POR TIPO DE COLUNA
    
    # Lista de colunas para colocar em Title Case (Primeira Maiúscula)
    # Ajuste essa lista com os nomes exatos das suas colunas se necessário
    cols_title = [
        'Campus', 
        'Município', 
        'Nome completo do avaliador do processo CAR',
        'Nome completo do orientador Ifes',
        'Nome completo do ponto focal Idaf',
        'Status',
        'Motivo da reprovação ou cancelamento (se aplicável)',
        'Detalhamento da reprovação ou cancelamento (se aplicável)',
        'Detalhamento da Notificação (Outros - Descrever)'
    ]
    
    # Lista de colunas para colocar TUDO EM MAIÚSCULO (Códigos)
    cols_upper = [
        'Código Edocs',
        'Processo florestal nº', # Geralmente códigos misturam letras e números
        'Código do empreendimento nº'
    ]

    print("Aplicando correções...")

    # Aplica Title Case (Ex: "santa teresa" -> "Santa Teresa")
    for col in cols_title:
        if col in df.columns:
            # .str.title() transforma "da silva" em "Da Silva". 
            # Se preferir que preposições fiquem minúsculas, avise.
            df[col] = df[col].str.title()
            print(f"  > Padronizado (Title Case): {col}")

    # Aplica Upper Case (Ex: "2025-gscxq" -> "2025-GSCXQ")
    for col in cols_upper:
        if col in df.columns:
            df[col] = df[col].str.upper()
            print(f"  > Padronizado (MAIÚSCULO): {col}")

    # 3. CORREÇÃO FINA DE PREPOSIÇÕES (Opcional, mas deixa bonito)
    # O .title() deixa "Da Silva", vamos mudar para "da Silva"
    # Isso é estético. Se não quiser, pode comentar esse bloco.
    preposicoes = ['Da', 'Do', 'De', 'Dos', 'Das', 'E']
    for col in cols_title:
        if col in df.columns:
            for prep in preposicoes:
                # Substitui " Da " por " da " (com espaços para não pegar meio da palavra)
                df[col] = df[col].str.replace(f' {prep} ', f' {prep.lower()} ', regex=False)

    # Salva o arquivo limpo
    df.to_csv(caminho_saida, index=False, encoding='utf-8-sig')
    
    print("\n" + "="*40)
    print("LIMPEZA CONCLUÍDA!")
    print(f"Arquivo salvo como: {arquivo_saida}")
    print("="*40)
    print("DICA: Abra o arquivo novo e confira se 'iBITIRAMA' virou 'Ibitirama'.")

if __name__ == "__main__":
    corrigir_padroes()