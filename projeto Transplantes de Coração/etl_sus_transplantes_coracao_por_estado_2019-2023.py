# Origem dos dados: http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sih/cnv/qiuf.def

# Importando biblioteca
#%%
import pandas as pd

# Extraindo os dados
#%%
dados = pd.read_csv("base_raw_sus_transplantes_coracao_por_estado_2019-2023.csv",sep=";")
dados.head()

# Conhecendo o conjunto de dados
#%%
dados.columns
#%%
dados.info()

# Seleção das variáveis de interesse
#%%
dados.drop("Total", axis=1, inplace=True)
# %%
dados.head()

# Transformação dos dados

## Padronização do campo Unidade de Federação
#%%
dados["Unidade da Federação"] = dados["Unidade da Federação"].str[3:]
dados.head()

## Restruturação da tabela para um formato que permita operações de agregação de forma mais intuitiva
#%%
dados = dados.melt(id_vars=["Unidade da Federação"])
dados.head()
# %%
dados.columns = ['Estado', 'Ano', 'Transplantes']
dados.head()

## Convertendo o campo transplantes de string para float e lidando com valores numéricos vazios, representados pelo símbolo -
#%%
dados["Transplantes"] = dados["Transplantes"].str.replace(",",".")
dados["Transplantes"] = dados["Transplantes"].str.replace("-","0")
dados.head()
#%%
dados["Transplantes"] = dados["Transplantes"].astype(float).apply(lambda x: round(x, 2))
dados.head()
#%%
dados.info()
#%%

## Observendo os valores únicos das variáveis
#%%

for var in dados.columns:
    print(f"{var}: \n",dados[var].unique(),"\n")

## Tratando o valor al da variável estado
#%%
dados[dados["Estado"]=="al"]
dados["Estado"] = dados["Estado"].replace("al","Alagoas")

dados["Estado"].unique()
#%%
dados
#%%
dados.to_parquet("sus_transplantes_coracao_por_estado_2019-2023.parquet")
#%%
