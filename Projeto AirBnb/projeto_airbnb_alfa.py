# -*- coding: utf-8 -*-
"""Projeto AirBnb Alfa.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1G6lff8J-u4f4nWq3x-FFDOwXKNk8_xY3

*Importando Bibliotecas*

---
"""

"""Execute o comando cd /caminho/para/seu/projeto pip install -r requirements.txt 
no terminal para baixar todas as dependências do Projeto"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import folium as fl
import webbrowser as web
import os

"""**Lendo base de *dados***

---





"""

data = pd.read_csv('AB_NYC_2019.csv')
data.head()

"""**Configurando Gráfico**"""

sns.set(style= 'whitegrid')

"""**Calculando a média**"""

media = np.mean(data.loc[:, 'price'])
print(f'A média entre o preço dos alugéis é de ${round(media, 2)}')

"""**Nomes das Regiões**"""

regiao = pd.unique(data['neighbourhood_group'])
print('As Regiões de Nova York são:')
for c in regiao:
  print(c)

"""**Valor máximo de aluguel**"""

max_aluguel = np.max(data['price'])
print('O valor máximo do alugel é de ${}.'.format(round(max_aluguel),2))

"""**Quais são as categorias de imóveis que estão cadastradas dentro da
base de dados da cidade de Nova York?**

"""

categorias_imovel = pd.unique(data['room_type'])
print('As categorias de imoveis disponíveis são: ', end = '')
for e in categorias_imovel:
  print(f'\033[34m{e}\033[m', end= ', ')

"""**Quantos usuários (Hosts) únicos cadastrados existem dentro da base de
dados da cidade de Nova York?**

"""

hosts_unicos = pd.unique(data['host_id'])
print(f'A quantidade de Hosts únicos são {len(hosts_unicos)}')

"""**Como é a variação do preços dos imóveis em NY?**

"""

desvio_padrao = np.std(data['price'])
print(f'Em relação a média dos preços de imóveis, que é de ${round(media, 2)}, os preços variam cerca de ${round(desvio_padrao, 2)}.')

"""**Existem mais imóveis baratos ou caros?**

"""

linhas_filtradas = data.loc[:, 'price'] < 800
sns.histplot(data.loc[linhas_filtradas, 'price'], bins= 8, color= 'blue')
plt.title('Distribuição de imóvem em ralação ao preço de aluguél')
plt.xlabel('Preço aluguél')
plt.ylabel('Qtd. de Imóveis')

"""**Qual a distribuição do número de Reviews? Existem imóveis com muitos
e outro com poucos reviews?**
"""

sns.histplot(data.loc[(data.loc[:,'number_of_reviews'] < 250), 'number_of_reviews'], bins= 5, kde= False, color= 'black')
plt.title('Distribuição de Contagem de reviews por imóvel')
plt.xlabel('Contagem de reviews')
plt.ylabel('Contagem de imóveis')

print('É perceptível que há mais imóveis com menos reviews do que com mais reviews. A média de reviews gira em torno de {} reviews'.format(
    round(np.mean(data['number_of_reviews']),0))
)

"""**. Qual é o valor do aluguel (diária) mais caro de cada região da base de dados da cidade de Nova York?**"""

#se valor na coluna price for o aluguél mensal:
aluguel_diaria = data.loc[:, ['neighbourhood_group', 'price']].groupby('neighbourhood_group').max() / 30
px.bar( aluguel_diaria, x= aluguel_diaria.index, y= 'price')

#se os valores da coluna price já forem as diárias
aluguel_diaria_2 = data.loc[:, ['neighbourhood_group', 'price']].groupby('neighbourhood_group').max().reset_index()
px.bar(data_frame = aluguel_diaria_2, x= 'neighbourhood_group', y= 'price')

"""**2. Conseguimos saber onde estão localizados os imóveis com o valor do aluguel mais caro, na cidade de Nova York?**"""

#Criando um mapa utilizando o plotly.express
dados_loc = data.loc[:, ['neighbourhood_group', 'price', 'latitude', 'longitude']].groupby('neighbourhood_group').max().reset_index()


#Criando um gráfico utilizando o folium

#Configura o tamanho do mapa na tela
fig = fl.Figure(1024, 720, title= 'Imóveis com maior Aluguél de Nova York')

#Cria um mapa base, onde os valores de latitude e longitude são as posições iniciais do mapa.
mapa = fl.Map(
              location = [dados_loc['latitude'].mean(), dados_loc['longitude'].mean()], zoom_start= 10, scale_control= True
)
colors= ('black', 'purple', 'green', 'gray', 'orange')

#cria um laço de repetição onde a cada repetição, é marcado no mapa um ícone de localização, que está na base de dados.
for i,v in enumerate(dados_loc['neighbourhood_group']):
  fl.Marker(
      location= [dados_loc['latitude'][i], dados_loc['longitude'][i]],
      popup= (f'{v} / U${dados_loc["price"][i]}'),
      icon= fl.Icon(color= colors[i])
).add_to(mapa)

#Gera o mapa em um arquivo html
mapa.save('Mapa_imoveis_mais_caros.html')
mapa

caminho_mapa = os.path.abspath('Mapa_imoveis_mais_caros.html')
web.open(f'file://{caminho_mapa}')

"""**Conseguimos saber onde estão localizados os imóveis pelo seu tipo, apenas
para os imóveis disponível para alugar?**
"""

#Criando um mapa
mapa2= fl.Map(location= [dados_loc['latitude'].mean(), dados_loc['longitude'].mean()], title= '50 Imóveis agrupados por tipo.')

#Selecionando os 50 Maiores valores
dados_loc_tipo = data.nlargest(50, 'price')[['price', 'room_type', 'latitude', 'longitude']]

#Criando marcações para cada tipo de imóvel
for i, v in dados_loc_tipo.iterrows():
  if v['room_type'] == 'Entire home/apt':
      fl.Marker(
          location= (
              [v['latitude'], v['longitude']]),
          popup= (f'Entire home/apt; U${v["price"]}'),
          icon= fl.Icon(color= 'blue')
          ).add_to(mapa2)

  elif v['room_type'] == 'Private room':
      fl.Marker(
          location= (
              [v['latitude'], v['longitude']]),
          popup= (f'Private room; U${v["price"]}'),
          icon= fl.Icon(color= 'darkpurple')
          ).add_to(mapa2)


mapa2.save('Mapa_imoveis_por_tipo.html')

caminho_mapa2 = os.path.abspath('Mapa_imoveis_por_tipo.html')
web.open(f'file://{caminho_mapa2}')
#Entire home/apt = blue, Private room= black, Shared room= Yellow



