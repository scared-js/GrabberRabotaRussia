import requests

API_HREF = 'https://opendata.trudvsem.ru/api/v1/vacancies/company/inn/'


class Grabber:
    def __init__(self, inn):
        self.vacancies = []
        self.inn = inn

    def loadDataFromApi(self, offset=0):
        base_url = API_HREF + str(self.inn)
        post = {'offset': offset, 'limit': 100}

        query = requests.get(url=base_url, params=post)
        data = query.json()

        if 'vacancies' in data['results']:
            vacancies = data['results']['vacancies']

            self.vacancies += vacancies

            if len(vacancies) >= 100:
                self.loadDataFromApi(offset + 1)

    def appendDataFrame(self, data):
        for vacancy in self.vacancies:
            vacancy = vacancy['vacancy']

            row = {
                'inn': self.inn,
                'company_name': vacancy['company']['name'],
                'vacancy_name': vacancy['job-name'],
                'creation-date': vacancy['creation-date'],
                'education': vacancy['requirement']['education'],
                'qualification': '',
                'experience': vacancy['requirement']['experience'],
                'work_places': vacancy['work_places'],
                'duty': vacancy['duty'] if 'duty' in vacancy else '',
                'addresses': vacancy['addresses']['address'][0]['location'],
                'specialisation': vacancy['category']['specialisation'],
            }

            data = data._append(row, ignore_index=True)

        return data
