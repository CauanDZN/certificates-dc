import PIL
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

def importar_fonte(fonte_path, fonte_nome):
    pdfmetrics.registerFont(TTFont(fonte_nome, fonte_path))

def ler_dados_excel(nome_arquivo):
    workbook = openpyxl.load_workbook(nome_arquivo)
    sheet = workbook.active

    dados = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        nome, cpf = row
        dados.append({'nome': nome, 'cpf': cpf})

    return dados

def redimensionar_imagem(imagem_path, largura, altura):
    imagem = PILImage.open(imagem_path)

    proporcao = min(largura / float(imagem.width), altura / float(imagem.height))

    nova_largura = int(imagem.width * proporcao)
    nova_altura = int(imagem.height * proporcao)

    imagem_redimensionada = imagem.resize((nova_largura, nova_altura), resample=PIL.Image.LANCZOS)
    imagem_redimensionada.save(imagem_path)

def gerar_pagina_certificado(pdf, frente_path, verso_path, largura, altura, pessoa):
    elementos = []

    elementos.append(Spacer(1, 1))

    nome_certificado = f"Certificado para {pessoa['nome']}"
    cpf_certificado = f"CPF: {pessoa['cpf']}"

    estilo_titulo = ParagraphStyle(
        'CustomTitle',
        fontName='Montserrat-Regular',
        fontSize=60,
        spaceAfter=12,
        textColor='black'
    )

    # Verifica se a imagem da frente é mais larga que a página
    imagem_frente = PILImage.open(frente_path)
    if imagem_frente.width > largura:
        largura_frente = imagem_frente.width
    else:
        largura_frente = largura

    # Adiciona a imagem da frente na página
    elementos.append(Image(frente_path, width=largura_frente, height=altura))
    elementos.append(Paragraph(nome_certificado, estilo_titulo))
    elementos.append(Paragraph(cpf_certificado, estilo_titulo))

    # Adiciona a imagem do verso na página seguinte
    pdf.build(elementos)
    pdf.add_page()
    pdf.build([Image(verso_path, width=largura, height=altura)])

def gerar_certificados(dados):
    fonte_path = './fonts/Montserrat-Regular.ttf'
    fonte_nome = 'Montserrat-Regular'
    importar_fonte(fonte_path, fonte_nome)

    for pessoa in dados:
        largura, altura = 2000, 1414
        pdf_certificado = f"Certificado_{pessoa['nome']}.pdf"
        frente_path = 'frente.png'
        verso_path = 'verso.png'

        # Redimensiona as imagens
        redimensionar_imagem(frente_path, largura, altura)
        redimensionar_imagem(verso_path, largura, altura)

        margem_esquerda = 0
        margem_direita = 0
        margem_superior = 0
        margem_inferior = 0

        pdf = SimpleDocTemplate(
            pdf_certificado,
            pagesize=(largura + margem_esquerda + margem_direita, altura + margem_superior + margem_inferior),
            leftMargin=margem_esquerda,
            rightMargin=margem_direita,
            topMargin=margem_superior,
            bottomMargin=margem_inferior
        )

        gerar_pagina_certificado(pdf, frente_path, verso_path, largura, altura, pessoa)
        
        print(f"Certificado gerado para {pessoa['nome']}.")

def main():
    nome_arquivo_excel = 'seuarquivo.xlsx'
    dados = ler_dados_excel(nome_arquivo_excel)
    gerar_certificados(dados)

if __name__ == "__main__":
    main()
