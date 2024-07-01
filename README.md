# Bot de Envio Automático de Imagens para Produtos (NuvemShop)

Este é um bot desenvolvido em Python para automatizar o processo de envio de imagens para produtos na plataforma Tiendanube. Ele faz uso da API da Tiendanube para buscar produtos sem imagens e enviar imagens correspondentes a partir de uma pasta local.


# Funcionalidades

Busca de Produtos Sem Fotos: O bot faz uma consulta à API da Tiendanube para identificar produtos que não possuem imagens cadastradas.

Processamento de Imagens: O bot lê uma planilha Excel e uma pasta local de imagens para associar cada imagem corretamente ao produto correspondente na Tiendanube.

Envio de Imagens: Após associar as imagens aos produtos corretos, o bot envia as imagens para a plataforma usando a API da Tiendanube.

Monitoramento e Logging: Utiliza o módulo logging para registrar eventos durante a execução do bot, facilitando a monitoração e solução de problemas.

# Pré-requisitos

Python 3.x instalado
pip install requests openpyxl selenium


# Configuração

Credenciais da API: Obtenha seu store_id e access_token da Tiendanube. Substitua esses valores no código:
store_id = 123456
access_token = 'seu_access_token_aqui'

# Uso

python botApiNuvemGuga.py
