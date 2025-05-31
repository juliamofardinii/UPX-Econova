import pandas as pd
import json
import numpy as np

# 🔗 Caminho do arquivo CSV
caminho_csv = 'static/dataSheet/CONSUMO MENSAL DE ENERGIA ELÉTRICA POR CLASSE.xlsx - CONSUMO RESIDENCIAL POR UF.csv'

# 📥 Leitura do CSV com cabeçalhos multi-index
df = pd.read_csv(
    caminho_csv,
    sep=',',
    header=[0, 1],
    encoding='utf-8',
    skiprows=4
)

# 🧹 Limpeza: remove a última linha (nota)
df = df.iloc[:-1]

# 🔠 Cria a coluna 'UF' e remove coluna duplicada
df['UF'] = df.iloc[:, 0]
df = df.drop(columns=df.columns[0])
df = df.set_index('UF')

# 🔍 Filtra apenas os anos desejados
anos_interesse = ['2020', '2021', '2022', '2023', '2024']
df = df.loc[:, df.columns.get_level_values(0).isin(anos_interesse)]

# 🔢 Converte os dados de texto para float
df = df.applymap(lambda x: str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x)
df = df.apply(pd.to_numeric, errors='coerce')

# 📊 Gera estatísticas
estatisticas = {}

for estado in df.index:
    dados_estado = df.loc[estado].dropna()

    estatisticas[estado] = {
        'geral': {
            'media': round(dados_estado.mean(), 2),
            'soma': round(dados_estado.sum(), 2),
            'desvio_padrao': round(dados_estado.std(), 2)
        },
        'por_ano': {}
    }

    # 🔥 Análise dos últimos 3 anos (2022, 2023, 2024) separadamente
    for ano in ['2022', '2023', '2024']:
        colunas_ano = [col for col in dados_estado.index if col[0] == ano]
        dados_ano = dados_estado[colunas_ano].dropna()

        if not dados_ano.empty:
            estatisticas[estado]['por_ano'][ano] = {
                'media': round(dados_ano.mean(), 2),
                'soma': round(dados_ano.sum(), 2),
                'desvio_padrao': round(dados_ano.std(), 2)
            }
        else:
            estatisticas[estado]['por_ano'][ano] = {
                'media': None,
                'soma': None,
                'desvio_padrao': None
            }

# 🔧 Função para conversão de tipos NumPy no JSON
def converter(obj):
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    if isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    if isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    return str(obj)

# 💾 Salva no JSON
with open('estatisticas_consumo_residencial.json', 'w', encoding='utf-8') as f:
    json.dump(estatisticas, f, ensure_ascii=False, indent=4, default=converter)

print("✅ Análise estatística salva em 'estatisticas_consumo_residencial.json'")
