# Identificador Placa de Trânsito

Este trabalho foi desenvolvido em trio durante a disciplina de Introdução à Inteligência Artificial, ministrada pela professora Dra. Thaís Gaudencio do Rêgo, com o objetivo de desenvolver as habilidades técnicas necessárias aprendidas.

## Autores

* Alexandre Bezerra de Lima [Alexandreprog](https://github.com/Alexandreprog)
* Ryann Carlos de Arruda Quintino [ryann-arruda](https://github.com/ryann-arruda)
* Samantha Dantas Medeiros [sammid37](https://github.com/sammid37)

## Introdução

Os sinais de trânsito desempenham um papel fundamental e essencial nas rodovias, garantindo a segurança no tráfego de motoristas e pedestres ao fornecer instruções precisas. Entretanto, no presente momento, há uma tendência de constante crescimento das cidades, produzindo uma crescente necessidade de instalação de novos sinais de trânsito com boa visibilidade para os motoristas e demais usuários das rodovias (WEN et al, 2016). 

Segundo o jornal Estadão, até 2030, o mercado de carros autônomos crescerá em uma escala assustadora, de modo que um em cada dez veículos será autônomo. No entanto, de acordo com Wen *et al.* (2016), as configurações das placas de trânsito variam de cidade para cidade em cada país do globo. Dessa forma, faz-se necessário desenvolver um reconhecedor de placas de trânsito com alto desempenho, a fim de auxiliar esses veículos que surgirão.

## Implementação do Modelo

Após observar os fatos supracitados, foi realizada a procura por bases de dados que pudessem auxiliar no desafio de identificar as placas de trânsito. No entanto, não foi possível encontrar nenhum conjunto de dados grande o suficiente, representativo o bastante e com uma qualidade boa para abordar a realidade brasileira que desejávamos explorar neste trabalho.

Dessa forma, buscamos criar nossa própria base de dados através do Google Maps, realizando a captura de telas das placas de trânsito encontradas em rodovias do Nordeste e em algumas cidades do Brasil, como João Pessoa, Caicó, Cuiabá e Joinville. Além disso, escolhemos o formato das placas como critério de classificação: rectangle (retângulo), triangle (triângulo), circle (círculo), rhombus (losângulo), octagon (octágono). Para cada classe foram capturadas 200 imagens, totalizando 1000 imagens no conjunto de dados.

### Classe **Circle**
![c0010](https://github.com/Alexandreprog/Identificador-placa-transito/assets/53544629/36d94523-8b0e-415b-bfbc-c68452298943)

### Classe **Octagon**
![o0013](https://github.com/Alexandreprog/Identificador-placa-transito/assets/53544629/a3c5d16b-8f47-4bc9-b5c2-90ec9c3ea734)

### Classe **Rectangle**
![r0009](https://github.com/Alexandreprog/Identificador-placa-transito/assets/53544629/06a2de2b-78ba-4b53-8fc2-40beecb13e90)

### Classe **Rhombus**
![rh0010](https://github.com/Alexandreprog/Identificador-placa-transito/assets/53544629/da9a2cf0-65d9-4afe-8a89-228a555bf555)

### Classe **Triangle**
![t0005](https://github.com/Alexandreprog/Identificador-placa-transito/assets/53544629/f3a1fba0-4c60-4561-a495-e2b30e572e5e)

Posteriormente, foi necessário escolher um modelo de rede neural que melhor se adequasse ao problema. Para isso, realizamos uma pesquisa para compreender os modelos existentes e sua facilidade de uso, levando em consideração o curto tempo disponível para a implementação do projeto. Assim, optamos pelo modelo YOLO V8 devido à sua superioridade em relação às versões anteriores, conforme pode ser observado no gráfico abaixo.

![yolo-comparison-plots](https://github.com/Alexandreprog/Identificador-placa-transito/assets/53544629/daee0904-a6be-40ad-9a3f-eb4e37a5965d)
###### **Fonte:** https://github.com/ultralytics/ultralytics

Entretanto, a documentação da YOLO não foi tão acessível para um primeiro contato, sendo necessário realizar inúmeras pesquisas e testes a fim de conseguir compreender o que estava descrito e executar o modelo escolhido.

Em seguida, a fim de aumentar o tamanho da base dados foi realizado *Data Augmentation*, no qual as operações de rotação, negativo, *flip*, transformação em escala de cinza foram aplicadas para cada classe. Essas transformações foram implementadas em código *Python*, a rotação foi realizada sob o ângulo de 45º e o *flip* foi na horizontal. Desse modo, nossa base de dados inicial teve seu tamanho aumentado de 1000 imagens para 5000 imagens totais.

Após a aplicação do *Data Augmentation* e a escolha do modelo de rede neural, foi realizado a anotação das imagens seguindo o padrão requisitado pela YOLO para cada classe criada utilizando o *software LabelImg*, o qual pode ser observado abaixo:

![triangle_annotation](https://github.com/Alexandreprog/Identificador-placa-transito/assets/53544629/28d8aee2-44ff-402a-84ac-4b973f57346e)

As dependências utilizadas para o *Data Augmentation* foram:

* PIL
* math
* numpy

Enquanto que a única dependência para o uso da YOLO V8 foi:

* ultralytics

>  Nota: A especificação da máquina utilizada foi:
>  * **Sistema Operacional**: Windows 11
>  * **Processador**: Intel(R) Core(TM) i5-10400 CPU @ 2.90GHz   2.90 GHz
>  * **Memória RAM**: 32GB
>  * **Placa de Vídeo**: Radeon RX550

As anotações foram realizadas por pessoas distintas, de modo que o *software LabelImg* inicia as anotações das classes a partir do 0, o que pode gerar conflitos ao tentar juntá-las. Por exemplo, pode acontecer que o indivíduo A faça a anotação de duas imagens, atribuindo os rótulos 0 e 1, enquanto o indivíduo B, ao anotar outras imagens, também atribua os rótulos 0 e 1. Nesse cenário, surgirá um conflito entre as anotações realizadas pelos indivíduos A e B, tornando necessário resolver esse problema.

O conflito foi solucionado de uma forma extremamente simples: foi criada uma função em *Python* chamada '*changeLabel*', presente no arquivo '[path_preprocessing.py](https://github.com/Alexandreprog/Identificador-placa-transito/blob/main/path_preprocessing.py)', que altera o rótulo de cada classe de modo crescente. Ou seja, a primeira classe fica com o rótulo 0, a segunda com rótulo 1 e assim sucessivamente. Essa abordagem utilizada permite garantir que as classes estejam bem definidas e que o conjunto de dados possa evoluir ao longo do tempo sem efeitos colaterais.

O modelo da YOLO V8 necessita de arquivos de texto (.txt) de treinamento e teste contendo os caminhos para as imagens que deverão ser utilizadas. Entretanto, a fim de garantir que apenas caminhos existentes para as imagens presentes no conjunto de dados estejam contidas nesses arquivos, seguimos o seguinte passo a passo:

1. Produzimos arquivos de texto com o seguinte padrão: *<nome da classe>_annotation*; contendo o caminho para todas as anotações referentes às imagens daquela respectiva classe;

2. Geramos 2 arquivos de texto: um de treino e um de teste. Eles foram produzidos a partir do passo anterior, com a seleção aleatória dos caminhos para as anotações que irão pertencer a cada um dos arquivos. É importante destacar que utilizamos 70% do conjunto de dados para treinamento e 30% para teste. A fim de garantir o balanceamento, essa seleção aleatória foi realizada para cada classe. Ou seja, foram separados 70% dos dados da classe 0 para treinamento e 30% para teste; em seguida, essa ação foi repetida para a classe 1 e assim sucessivamente para todas as classes;

3. Finalmente, foi realizada uma alteração dos caminhos presentes nos arquivos de treino e teste, no qual o trecho “*<nome da classe>_annotation*” foi substituído por “*<nome da classe>//images*” indicando a pasta em que as imagens estão localizadas. Por último, a extensão foi alterada de “*.txt*” para “*.png*” resultando nos caminhos finais para as imagens que são necessários para o modelo da YOLO.

Para cada classe foi necessário criar uma pasta com o nome da classe em minúsculo, devido ao pré-processamento dos caminhos que foi realizado, e dentro dela pastas com os nomes “*images*” e “*labels*”, que receberiam respectivamente as imagens e anotações referentes a cada classe . Sendo essa parte uma dificuldade encontrada no decorrer do projeto, devido a falta de exemplos na documentação da YOLO V8, em repositórios do GitHub e em artigos encontrados.

Por fim, foi necessário realizar a criação de dois arquivos finais, sendo eles:

* **traffic_signs.yaml**: Este arquivo refere-se ao conjunto de dados, aos arquivos com os caminhos para as imagens e as anotações de cada classe. Dessa maneira, ele deverá ser estruturado da seguinte forma: 

```yaml
path: <caminho para a pasta do conjunto de dados>
train: <nome do arquivo de texto com os caminhos para as imagens de treino>
val: <nome do arquivo de texto com os caminhos para as imagens de teste>
test: <deixa vazio ou adiciona o nome do arquivo de texto com os caminhos para as imagens de validação>

names:
    0: circle
    1: octagon
    2: rectangle
    3: rhombus
    4: triangle
```

* **traffic_signs_predict.py**: Este arquivo refere-se a criação e uso do modelo da YOLO V8, no qual ele está sendo treinado e testado com as imagens definidas no arquivo **.yaml**.

## Executando o Modelo

1. Inicialmente, o repositório deverá ser baixado e colocado em uma pasta de sua preferência;
2. Posteriormente, o arquivo *path_preprocessing.py* deverá ser executado da seguinte forma:

``` bash
python path_preprocessing.py
```

3. Em seguida, o caminho para a pasta do *dataset* localizado dentro do repositório baixado deverá ser copiado e inserido no arquivo **.yaml** no local que está identificado com **path**;

4. Finalmente, o arquivo *traffic_signs_predict.py* deverá ser executado da seguinte forma:

```bash
python traffic_signs_predict.py
```

## Resultados e Discussões

Após a execução do modelo, foram utilizadas as seguintes métricas de avaliação:

* Recall: Refere-se a capacidade do modelo de identificar as amostras positivas;
* Precision: Refere-se a capacidade do modelo de classificar corretamente as previsões positivas.

Dessa maneira, foi obtido o seguintes gráficos:

* **Treino**

![PR_curve](https://github.com/Alexandreprog/Identificador-placa-transito/assets/53544629/88cb4c9a-3ff3-4d1b-b128-a772d7194666)

* **Teste**

![PR_curve](https://github.com/Alexandreprog/Identificador-placa-transito/assets/53544629/5aca23bf-c365-47e0-a801-56b97e892ed4)

Observando os gráficos acima podemos constatar a qualidade do modelo, pois as métricas utilizadas variam no intervalo entre 0 e 1, ou seja, entre 0% e 100%. Dessa forma, analisando as figuras verificamos que o nosso modelo obteve valores maiores que 98% para todas as classes, indicando a confiabilidade do modelo em identificar placas de trânsitos brasileiras de diferentes formatos. 

Abaixo podemos observar a classificação para algumas imagens utilizadas na fase de testes.

![val_batch1_pred](https://github.com/Alexandreprog/Identificador-placa-transito/assets/53544629/0e111f26-163a-4ffc-aeb0-8f5a360b1ddb)


## Melhorias Futuras

1. Melhorar o algoritmo da rotação implementado para o *Data Augmentation*, em virtude de que o atual está inserindo ruído nas imagens;

2. Aumentar o tamanho do conjunto de dados capturando imagens de outros estados e cidades brasileiras;

3. Implementar o mesmo problema utilizando aprendizado profundo a fim de fazer uma comparação do resultado.

## Referências

WEN, C. et al. Spatial-Related Traffic Sign Inspection for Inventory Purposes Using Mobile Laser Scanning Data. IEEE Transactions on Intelligent Transportation Systems, [S.I.], v. 17, p. 27-37, abr. 2015. Disponível em: <https://ieeexplore.ieee.org/abstract/document/7089251>. Acesso em: 28 jun. 2023.

De cada dez veículos no mundo, um será carro autônomo até 2030. Estadão, [S.I.], 2020. Disponível em: <https://summitmobilidade.estadao.com.br/carros-autonomos/de-cada-dez-veiculos-no-mundo-um-sera-carro-autonomo-ate-2030/>. Acesso em: 28 jun. 2023