# FAT16Reader
Esse programa tem por objetivo reproduzir um leitor de FAT 16, desenvolvido em Python.
Ambos arquivos utilizam da biblioteca "struct", mais especificamente a função "unpack", que tem por função ler conjuntos de bytes como little endian ou big endian, pois como o Python realiza tais leituras como big endian e a FAT16 é lida em little endian, tal operação se faz necessária.
Para maior compreensão do funcionamento do código, veja as descrições a seguir.

## fat16reader.py
Das linhas 4 a 17, temos o trecho de código responsável por escolher qual arquivo será lido. Qualquer adição que se faça necessária para ler outro tipo de arquivo, pode ser editada ali.

Das linhas 25 a 33, temos um dicionário responsável por armazenar as informações do boot record, seguindoo padrão da FAT 16.

Das linhas 35 a 41, salvamos o endereço inicial, em bytes, de cada nova área de interesse, sendo elas: FATs, diretório raíz e área de dados.

Das linhas 43 a 51, temos simplesmente o print dessas informações adquiridas.

Na linha 54, salvamos em cont_root_dir uma lista de lista complementares, cada uma contendo os dados de uma das estruturas encontradas no diretório raiz, sejam eles arquivos ou diretórios, através da função checa_pasta().

Das linhas 56 a 61, temos apenas mais funções para printar dados, sendo que na linha 59 chamamos uma função para printar os dados encontrados armazenados em cont_root_dir.

Por fim, na linha 62, temos uma função responsável por apresentar os dados de qual arquivo ou pasta o usuário escolher.

## funcoes.py
Arquivo composto apenas por funções, que farão o trabalho duro na leitura e apresentação dos dados da imagem de FAT16.

A primeira função, checa_pasta, recebe o endereço do conteúdo da imagem e o endereço de um diretório, e tem por função verificar e organizar os arquivos que estão armazenados em tal diretório, seja ele o raíz ou outro subdiretório. Ele será responsável por gerar uma grande lista, "arq_em_dir" (arquivos em diretório), composta de outras listas, que armazenarão nome, extensão, tipo de dado (se é uma pasta ou diretório), cluster inicial, e seu tamanho em bytes.
Tal função ignorará arquivos excluídos e pulará long file names, para então fazer os processamentos dos dados encontrados.

A segunda função, pega_dados, recebe vários dados: o endereço do conteúdo da imagem; a lista com as informações do arquivo ou pasta a ser visualizada, adquirida através da função checa_pasta; o início da FAT; o início da área de dados; a quantidade de bytes por setor; e a quantidade de setores por cluster.
Primeiro, descobriremos a posição do cluster inicial a ser buscado, armazenado na variável pos_ini_fat, e a partir dele, colocamos cada um dos clusteres que o compõem em uma lista.
A seguir, teremos a pos_ini_dados, que define o byte inicial do dado a ser lido dentro da área de dados
