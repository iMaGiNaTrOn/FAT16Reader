import struct
import funcoes

opcao_fat = int(input("Qual arquivo .img você quer ler?"
                      "\nOpção 1: fat16_4sectorpercluster"
                      "\nOpção 2: fat16_1sectorpercluster\n"))

if(opcao_fat == 1):
    file = open("fat16_4sectorpercluster.img", "rb")
elif(opcao_fat == 2):
    file = open("fat16_1sectorpercluster.img", "rb")
else:
    print("Opção inválida. Encerrando aplicação.")
    exit()
    
content = file.read()
file.close()

# B = unsigned char = 1 byte
# H = unsigned short = 2 bytes
# I = unsigned int = 4 bytes
# Q = unsigned long long = 8 bytes

# salvando dados do boot record em um dicionário
boot_record = {
    'bytes_per_sector' : struct.unpack("<H", content[11:13])[0],
    'sector_per_cluster' : content[13],
    'reserved' : struct.unpack("<H", content[14:16])[0],
    'n_FAT' : content[16],
    'sector_per_FAT' : struct.unpack("<H", content[22:24])[0],
    'n_total_sector' : struct.unpack("<H", content[19:21])[0] if (struct.unpack("<H", content[19:21]))[0] > 0 else struct.unpack("<I", content[32:36])[0],
    'root_dir_entries' : struct.unpack("<H", content[17:19])[0]
}

FATs = list()
for i in range(boot_record["n_FAT"]):
    FATs.append((boot_record["reserved"] * boot_record["bytes_per_sector"]) + (i * boot_record["sector_per_FAT"] * boot_record["bytes_per_sector"]))

root_dir = (boot_record["reserved"] + (boot_record["n_FAT"] * boot_record["sector_per_FAT"])) * boot_record["bytes_per_sector"]

data_area = int( ( ((boot_record["root_dir_entries"] * 32)/boot_record["bytes_per_sector"]) + boot_record["reserved"] + (boot_record["n_FAT"] * boot_record["sector_per_FAT"]) ) * boot_record["bytes_per_sector"])

f = funcoes.Funcs(boot_record, FATs, root_dir, data_area)

for key, value in boot_record.items():
    print(key, ": ", value, sep="")

print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")

for i in range(len(FATs)):
    print("Início da FAT ", i, ": ", FATs[i], sep = "")
print("Início do diretorio raiz:", root_dir)
print("Início da área de arquivos:", data_area)
      
# checando conteudo da pasta raiz e armazenando em cont_root_dir
cont_root_dir = f.checa_pasta(content, root_dir)

print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")
print("CONTEÚDO DO DIRETÓRIO RAÍZ")

f.printa_info_dir(cont_root_dir)

opcao_num = int(input("Qual opção você deseja visualizar?\n"))
if opcao_num > len(cont_root_dir) or opcao_num < 0:
    print("Erro, index fora de alcance")
    exit()
else:
    f.pega_dado(content, cont_root_dir[opcao_num])