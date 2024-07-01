import base64
import requests
import json
import os
import openpyxl
import time
import shutil
import re
import logging
from selenium.common.exceptions import *

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("BEM-VINDO, GUSTAVO! :)")
logging.info("BOT INICIADO")
logging.info("BUSCANDO FOTOS...")

# Função para verificar se o arquivo é uma imagem com base na extensão
def is_image(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in (".jpg", ".jpeg", ".png", ".gif", ".bmp")

# Função para carregar a planilha
def carregar_planilha(caminho_planilha):
    return openpyxl.load_workbook(caminho_planilha)['Sheet1']

# Função para obter valores de uma coluna específica da planilha
def obter_valores_coluna(aba, coluna, min_row=7):
    return [row[coluna-1] for row in aba.iter_rows(min_row=min_row, max_col=coluna, values_only=True)]

# Função para processar arquivos de imagem
def processar_arquivos(pasta):
    arquivos_da_pasta = os.listdir(pasta)
    return [filename for filename in arquivos_da_pasta if is_image(filename)]

# Função para limpar nome da foto
def limpar_nome_foto(nome_foto):
    nome_sem_extensao, _ = os.path.splitext(nome_foto)
    nome_sem_extensao = nome_sem_extensao.lstrip('0123456789_ ')
    return re.sub(r'\.\w+.*$', '', nome_sem_extensao)

# Função para buscar produtos sem fotos
def buscar_produtos_sem_fotos(store_id, access_token):
    all_products = []
    page = 1
    per_page = 30
    while True:
        url = f'https://api.tiendanube.com/v1/{store_id}/products?page={page}&per_page={per_page}'
        response = requests.get(url, headers={'Authentication': f'bearer {access_token}'})
        if response.status_code == 200:
            products = response.json()
            if not products:
                break
            all_products.extend(products)
            page += 1
        else:
            logging.error(f'Erro ao obter produtos: {response.status_code}, {response.text}')
            break
    return [product for product in all_products if not product['images']], all_products

# Função para enviar imagens para o site
def enviar_imagens(produtos_sem_fotos, objetos_produtos, store_id, access_token):
    for objeto_produto in objetos_produtos:
        titulo_objeto = objeto_produto["titulo"]
        base64_image = objeto_produto["base64"]
        for produto in produtos_sem_fotos:
            titulo_produto = produto['name']['pt']
            if titulo_objeto == titulo_produto:
                logging.info(f"Equivalência encontrada: {titulo_objeto} : {titulo_produto}")
                product_id = produto['id']
                filename = f'{titulo_objeto}.jpg'
                headers = {'Authentication': f'bearer {access_token}', 'Content-Type': 'application/json'}
                payload = {'filename': filename, 'position': 1, 'attachment': base64_image}
                response = requests.post(f'https://api.tiendanube.com/v1/{store_id}/products/{product_id}/images', headers=headers, data=json.dumps(payload))
                if response.status_code == 201:
                    logging.info(f'Imagem enviada com sucesso para o produto {titulo_objeto} (correspondente a {produto["name"]["pt"]})')
                    source_path = f'C:/Users/geral/Desktop/fotosProdutos/{objeto_produto["nome do arquivo"]}'
                    destination_path = 'C:/Users/geral/Desktop/feitos/'
                    try:
                        shutil.move(source_path, destination_path)
                        logging.info(f'Arquivo movido para a pasta "feitos" com sucesso')
                        time.sleep(2)
                    except Exception as e:
                        logging.error(f'Erro ao mover o arquivo para a pasta "feitos": {str(e)}')
                else:
                    logging.error(f'Erro ao enviar imagem para o produto: {titulo_objeto} (correspondente a {produto["name"]["pt"]}): {response.status_code}, {response.text}')

def main():
    planilha_path = 'C:/Users/geral/Desktop/ListaProdutos_Subirsite.xlsx'
    pasta_de_fotos = "C:/Users/geral/Desktop/fotosProdutos"
    store_id = 123456
    access_token = ''

    aba = carregar_planilha(planilha_path)
    arquivos_fotos = processar_arquivos(pasta_de_fotos)

    if not arquivos_fotos:
        logging.warning("PASTA DE FOTOS VAZIA! COLOQUE MAIS FOTOS PARA CONTINUAR...")
        return

    valores_coluna_c = obter_valores_coluna(aba, 3)
    valores_coluna_d = obter_valores_coluna(aba, 4)

    objetos_produtos = []

    for arquivo_de_foto in arquivos_fotos:
        nome_da_foto_sem_extensao = limpar_nome_foto(arquivo_de_foto)
        found_match = False
        valor_coluna_d_correspondente = None

        for idx, valor_coluna_c in enumerate(valores_coluna_c):
            if nome_da_foto_sem_extensao.lower() in valor_coluna_c.lower():
                valor_coluna_d_correspondente = valores_coluna_d[idx]
                found_match = True
                break

        if valor_coluna_d_correspondente is not None:
            with open(os.path.join(pasta_de_fotos, arquivo_de_foto), "rb") as image_file:
                base64_data = base64.b64encode(image_file.read()).decode("utf-8")
            objetos_produtos.append({"nome do arquivo": arquivo_de_foto, "titulo": valor_coluna_d_correspondente, "base64": base64_data})

    produtos_sem_fotos, all_products = buscar_produtos_sem_fotos(store_id, access_token)
    enviar_imagens(produtos_sem_fotos, objetos_produtos, store_id, access_token)

    logging.info(f'TOTAL DE PRODUTOS RETORNADOS DO SITE: {len(all_products)}')
    logging.info(f'TOTAL DE PRODUTOS SEM FOTO: {len(produtos_sem_fotos)}')

if __name__ == "__main__":
    main()
