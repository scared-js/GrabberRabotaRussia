import pandas as pd
from grabber import Grabber

# Название файла с инн предприятий
# Первый столбец должен иметь заголовок inn
INPUT_XLSX = 'inn_data.xlsx'

# Название выходного файла
RESULT_XLSX = 'result_data.xlsx'

data = pd.read_excel(INPUT_XLSX)
response_data = pd.DataFrame()

for key, row in data.iterrows():
    print('Собираю данные по ' + str(row.inn) + '\n')
    grabber = Grabber(row.inn)
    grabber.loadDataFromApi()

    count_after = len(response_data.index)
    response_data = grabber.appendDataFrame(response_data)
    count_vacancies = len(response_data.index) - count_after

    print('Найдено вакансий ' + str(count_vacancies) + '\n')

# В теории при большом кол-ве данных можно переписать на дописывание файла Excel, а не создания сразу всего
response_data.to_excel(RESULT_XLSX, sheet_name='Лист 1', index=False)
print('OK' + '\n')
