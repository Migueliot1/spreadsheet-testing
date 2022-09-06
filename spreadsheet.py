import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

from utils import get_range, get_body_insert


class SpreadsheetAPI:
    def __init__(self, spreadsheet_id, sheet_title, sheet_id, credentials, apis):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials,
                                                                            apis)  # данные сервисного аккаунта
        self.http_auth = self.credentials.authorize(httplib2.Http())  # авторизация
        self.service = apiclient.discovery.build('sheets', 'v4', http=self.http_auth)  # сервисный аккаунт
        self.spreadsheet_id = spreadsheet_id  # токен таблицы
        self.sheet_title = sheet_title  # заголовок листа
        self.sheet_id = sheet_id  # id листа

    def get_sheet(self):
        """
        Получение всех данных листа
        :return:
        """
        response = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=self.sheet_title
        ).execute()
        return response

    def get(self, range_: str):
        """
        Получение данных из таблицы по диапазону
        :param range_: диапазон значений (Примеры: "А1", "А1:В4")
        :return:
        """
        response = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range_
        ).execute()
        return response

    def insert(self, values, start_column=None, end_column=None, sheet_name=None) -> bool:
        """
        Вставка в определенный интервал
        :param values: значения для вставки
        :param start_column: Start column of the cleaning range
        :param end_column: End column of the cleaning range
        :param sheet_name: Title of sheet
        :return: True if values inserted, False if not
        """

        if not sheet_name:
            sheet_name = self.sheet_title

        _range = get_range(start_column, end_column, sheet_name)
        body = get_body_insert(_range, values)

        try:
            self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                                             body=body).execute()
            return True
        except Exception as err:
            print(err)
            return False

    # очищает данные в таблице по range
    def clear(self, range_):
        """
        Очищает заданный промежуток в таблице
        :param range_: диапазон значений (Примеры: "А1", "А1:В4")
        :return:
        """
        self.service.spreadsheets().values().clear(spreadsheetId=self.spreadsheet_id, range=range_).execute()

    def get_sheet_url(self) -> str:
        """
        Генерация ссылки на таблицу
        :return: ссылка на таблицу
        """
        return 'https://docs.google.com/spreadsheets/d/' + self.spreadsheet_id + '/edit#gid=' + str(self.sheet_id)


    def sessionClose(self):
        """
        Отключение от сети. 
        Необходим для корректной работы тестов.
        """
        self.http_auth.close()
