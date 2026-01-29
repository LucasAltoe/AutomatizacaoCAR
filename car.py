import pandas as pd
import os
import glob

def consolidar_planilhas():
    nome_da_subpasta = 'acompanhamento_processos_IntegraCAR' 
    
    caminho_raiz = os.path.dirname(os.path.abspath(__file__))
    
    caminho_leitura = os.path.join(caminho_raiz, nome_da_subpasta)
    
    arquivo_saida = 'TODOS_DADOS_UNIFICADOS.csv'
    
    print(f"Buscando arquivos em: {caminho_leitura}")

    if not os.path.exists(caminho_leitura):
        print(f"ERRO: A pasta '{nome_da_subpasta}' não foi encontrada na raiz.")
        return

    arquivos_csv = glob.glob(os.path.join(caminho_leitura, "*.[cC][sS][vV]"))
    
    lista_dfs = []

    for arquivo in arquivos_csv:
        try:
            df = pd.read_csv(arquivo, sep=',', encoding='utf-8')
            lista_dfs.append(df)
            print(f"Lido: {os.path.basename(arquivo)}")
        except Exception as e:
            print(f"Erro ao ler {os.path.basename(arquivo)}: {e}")

    if lista_dfs:
        df_final = pd.concat(lista_dfs, ignore_index=True)
        caminho_final = os.path.join(caminho_raiz, arquivo_saida)
        df_final.to_csv(caminho_final, index=False, encoding='utf-8-sig')
        
        print("\n" + "="*30)
        print(f"CONCLUÍDO COM SUCESSO!")
        print(f"Arquivo salvo na raiz: {arquivo_saida}")
        print(f"Total de linhas unificadas: {len(df_final)}")
        print("="*30)
    else:
        print("Nenhum arquivo encontrado para processar.")

if __name__ == "__main__":
    consolidar_planilhas()