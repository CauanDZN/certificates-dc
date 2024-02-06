from datetime import datetime, timedelta

feriados_str = [
    '12/02/2024', '13/02/2024', '14/02/2024',
    '19/03/2024', '25/03/2024', '29/03/2024', '21/04/2024',
    '01/05/2024', '30/05/2024', '15/08/2024', '07/09/2024',
    '12/10/2024', '02/11/2024', '15/11/2024', '25/12/2024'
]
feriados = [datetime.strptime(date, '%d/%m/%Y').date() for date in feriados_str]

def str_para_data(data_str):
    return datetime.strptime(data_str, '%d/%m/%Y').date()

def data_para_str(data):
    return data.strftime("%d/%m/%Y")

def calcular_data_futura(data_inicio, semanas):
    data_inicio = str_para_data(data_inicio)
    dias = semanas * 7

    while dias > 0:
        data_inicio += timedelta(days=1)
        if data_inicio.weekday() < 5 and data_inicio not in feriados:
            dias -= 1

    return data_para_str(data_inicio)

termino_planejamento = calcular_data_futura('02/03/2024', 12)
print("Última aula de Planejamento e Estratégia é:", termino_planejamento)

termino_copy = calcular_data_futura(termino_planejamento, 10)
print("Última aula de Copywriting é:", termino_copy)

termino_design = calcular_data_futura(termino_copy, 13)
print("Última aula de Design e Video é:", termino_design)

termino_trafego = calcular_data_futura(termino_design, 13)
print("Última aula de Tráfego e Performance é:", termino_trafego)