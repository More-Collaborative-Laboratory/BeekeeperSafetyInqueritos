# Created by ${USER} at ${DATE}
# Beekeeper Safety data analysis


import pandas as pd
from pandas import concat
import numpy as np
import re
import functions
from collections import Counter
import matplotlib.pyplot as plt

import pgeocode
portugal = pgeocode.Nominatim('pt')

inqueritos = pd.read_csv("./data/results-survey277348.csv")
print(inqueritos.shape)

#idade média, minima e máxima global
print("Idade média dos inquiridos: " + str(round(inqueritos.Idade.mean(),2))+" anos.")
print("Idade mínima dos inquiridos: " + str(inqueritos.Idade.min())+" anos.")
print("Idade máxima dos inquiridos: " + str(inqueritos.Idade.max())+" anos.")

#corrigir os códigos postais que estão incompletos e completar com xxxx-000
inqueritos['Código Postal'] = inqueritos['Código Postal'].str.split(pat="-")
inqueritos['CodPos'] = [functions.compose_CodPos(x) for x in inqueritos['Código Postal']]
#print(inqueritos['CodPos'].head(35))

#adicionar o distrito ao conjunto de dados
inqueritos['distrito'] = [portugal.query_postal_code(x).state_name for x in inqueritos['CodPos']]

# Distribuição dos inquiridos por distrito
distribuicao_distrito = inqueritos.pivot_table(index=['distrito'], aggfunc='size')
print(distribuicao_distrito)

# Distribuição dos inquiridos por idades
ranges = [0, 25, 35, 45, 55, 65, 75, 100]
a = inqueritos.groupby(pd.cut(inqueritos.Idade, ranges)).count()
print(a)

plt.bar(range(len(ranges)), inqueritos.groupby(pd.cut(inqueritos.Idade, ranges)).count(), align='center')
plt.xticks(range(len(ranges)), list(ranges))

plt.show()

# Análise por concelho
concelhos_totais = pd.Series()
concelhos_totais['concelhos'] = pd.concat([inqueritos["Identificação dos apiários [Apiário n°1][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°2][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°3][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°4][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°5][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°6][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°7][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°8][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°9][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°10][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°11][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°12][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°13][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°14][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°15][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°16][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°17][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°18][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°19][Concelho]"],
                                           inqueritos["Identificação dos apiários [Apiário n°20][Concelho]"]],
                                          ignore_index=True)

concelhos_totais['concelhos'] = concelhos_totais['concelhos'].dropna()

c = Counter(concelhos_totais['concelhos'])

plt.bar(range(len(c)), list(c.values()), align='center')
plt.xticks(range(len(c)), list(c.keys()))

plt.show()
