import PIL
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from PIL import Image as PILImage

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
    imagem_redimensionada = imagem.resize((largura, altura), resample=PIL.Image.LANCZOS)
    imagem_redimensionada.save(imagem_path)

def gerar_certificados(dados):
    for pessoa in dados:
        largura, altura = 2339, 1655
        pdf_certificado = f"Certificado_{pessoa['nome']}.pdf"

        redimensionar_imagem('fundocertificado.png', largura, altura)

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

        elementos = []

        elementos.append(Spacer(1, 1))

        nome_certificado = f"Certificado para {pessoa['nome']}"
        cpf_certificado = f"CPF: {pessoa['cpf']}"

        estilo_titulo = ParagraphStyle(
            'CustomTitle',
            fontName='Helvetica',
            fontSize=60,
            spaceAfter=12,
            textColor='black'
        )

        elementos.append(Paragraph(nome_certificado, estilo_titulo))
        elementos.append(Paragraph(cpf_certificado, estilo_titulo))

        pdf.build(elementos)
        
        print(f"Certificado gerado para {pessoa['nome']}.")

def main():
    nome_arquivo_excel = 'seuarquivo.xlsx'
    dados = ler_dados_excel(nome_arquivo_excel)
    gerar_certificados(dados)

if __name__ == "__main__":
    main()
