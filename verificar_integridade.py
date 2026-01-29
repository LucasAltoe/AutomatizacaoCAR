import pandas as pd
import os
import glob

def verificar_integridade():
    nome_da_subpasta = 'acompanhamento_processos_IntegraCAR' 
    nome_arquivo_final = 'TODOS_DADOS_UNIFICADOS.csv'
    
    caminho_raiz = os.path.dirname(os.path.abspath(__file__))
    caminho_origem = os.path.join(caminho_raiz, nome_da_subpasta)
    caminho_final = os.path.join(caminho_raiz, nome_arquivo_final)
    
    print(f"--- INICIANDO AUDITORIA ---")
    print(f"Origem: {caminho_origem}")
    print(f"Destino: {caminho_final}\n")

    arquivos_origem = glob.glob(os.path.join(caminho_origem, "*.[cC][sS][vV]"))
    total_linhas_origem = 0
    total_arquivos = 0
    
    print("Contando linhas arquivo por arquivo...")
    for arq in arquivos_origem:
        if os.path.basename(arq) == nome_arquivo_final:
            continue
            
        try:
            df = pd.read_csv(arq, sep=',', encoding='utf-8')
            qtd = len(df)
            total_linhas_origem += qtd
            total_arquivos += 1
        except Exception as e:
            print(f"  [ERRO] Não foi possível ler {os.path.basename(arq)}: {e}")

    total_linhas_final = 0
    if os.path.exists(caminho_final):
        try:
            df_final = pd.read_csv(caminho_final, sep=',', encoding='utf-8')
            total_linhas_final = len(df_final)
        except Exception as e:
            print(f"  [ERRO] Não foi possível ler o arquivo final: {e}")
    else:
        print(f"  [ERRO] Arquivo final '{nome_arquivo_final}' não encontrado na raiz!")
        return

    print("\n" + "="*40)
    print("RESUMO DA AUDITORIA")
    print("="*40)
    print(f"Total de arquivos lidos: {total_arquivos}")
    print(f"Soma das linhas (Origem):  {total_linhas_origem}")
    print(f"Linhas no arquivo final:   {total_linhas_final}")
    print("-" * 40)
    
    diferenca = total_linhas_origem - total_linhas_final
    
    if diferenca == 0:
        print("✅ SUCESSO: Os números batem perfeitamente!")
        print("Nenhum dado foi perdido.")
    else:
        print(f"❌ ATENÇÃO: Há uma diferença de {diferenca} linhas.")
        if diferenca > 0:
            print("O arquivo final tem MENOS linhas que a origem. Algum dado não foi copiado.")
        else:
            print("O arquivo final tem MAIS linhas. Pode haver duplicatas.")
    print("="*40)

if __name__ == "__main__":
    verificar_integridade()