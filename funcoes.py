import struct

def checa_pasta(conteudo, endereco):
    p_arq = endereco
    arq_em_dir = list()
    while (conteudo[p_arq] != 0):
        aux = list()
        # pos[0] = nome
        # pos[1] = ext
        # pos[2] = tipo
        # pos[3] = cluster
        # pos[4] = tamanho
        
        if conteudo[p_arq] == 229: # checa se o primeiro byte é 'E5', ou seja, se é um arquivo excluido
            p_arq += 32
        else:
            if conteudo[p_arq + 11] == 15: #checa se é 0F, long file name
                p_arq += 32
            else:
                nome = ""
                for i in range(0, 8):
                    if(conteudo[p_arq + i] != 32):
                        nome += chr(conteudo[p_arq + i])
                aux.append(nome)
                extens = ""
                for i in range(8, 11):
                    if(conteudo[p_arq + i] != 32):
                        extens += chr(conteudo[p_arq + i])
                aux.append(extens)
                tipo = conteudo[p_arq + 11]
                aux.append(tipo)
                cluster = struct.unpack("<H", conteudo[p_arq + 26:p_arq + 28])[0]
                aux.append(cluster)
                tamanho = struct.unpack("<I", conteudo[p_arq + 28:p_arq + 32])[0]
                aux.append(tamanho)
                arq_em_dir.append(aux)
                p_arq += 32
    return arq_em_dir

def pega_dado(conteudo, infos, ini_fat, ini_dados, byte_per_sector, sector_per_cluster):
    # checando clusteres em que o arquivo/diretorio deveria estar na FAT
    pos_ini_fat = (infos[3] * 2) + ini_fat
    lista_cluster_fat = list()
    lista_cluster_fat.append(pos_ini_fat)
    while (struct.unpack("<H", conteudo[pos_ini_fat:pos_ini_fat + 2])[0]!= 65535):
        pos_ini_fat += 2
        lista_cluster_fat.append(pos_ini_fat)
    
    byte_per_cluster = sector_per_cluster * byte_per_sector
    
    pos_ini_dados = ((infos[3] - 2) * byte_per_cluster) + ini_dados
    
    if infos[2] == 16:
        print(infos[0])
        arq_dir = checa_pasta(conteudo, pos_ini_dados)
        printa_info_dir(arq_dir)
    else:
        print(infos[0], ".", infos[1], sep="")
        somatorio = 0
        for j in range(len(lista_cluster_fat)):
            i = 0
            if (infos[4] >= ((j + 1) * byte_per_cluster)):
                tamanho = byte_per_cluster
            else:
                tamanho = infos[4] - (j * byte_per_cluster)
            
            while (i < tamanho):
                print(chr(conteudo[pos_ini_dados + (j*byte_per_cluster) + i]), end="")
                i += 1

def printa_info_dir(cont_dir):
    for i in range(len(cont_dir)):
        if (cont_dir[i][2] == 16):
            print("Opção ", i, ": Pasta", sep = "")
            print("Nome: ", cont_dir[i][0], sep = "")
        elif (cont_dir[i][2] == 32):
            print("Opção ", i, ": Arquivo", sep = "")
            print("Nome: ", cont_dir[i][0], ".", cont_dir[i][1], sep = "")
            print("Tamanho: ", round((cont_dir[i][4]/1024), 2), " KB", sep="")
        print()