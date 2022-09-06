from spreadsheet import SpreadsheetAPI
from utils import get_range

import unittest

# IMPORTANT
# To properly run all of this I had to change DEFAULT_TLS VERSION 
# in __init__.py of httplib2
# Should be: DEFAULT_TLS_VERSION = getattr(ssl, "PROTOCOL_TLS_CLIENT")

SAMPLE_SPREADSHEET_ID = '1X0487zRLFx6ZYg3eD2XV6iGLYbnxRR0WuhJnuvK3oOk'

class TestSpreadsheetAPI(unittest.TestCase):

    res = 'https://docs.google.com/spreadsheets/d/1X0487zRLFx6ZYg3eD2XV6iGLYbnxRR0WuhJnuvK3oOk/edit#gid=165149585'

    def setUp(self):
        '''
        Set up a connection before every test.
        '''
        # Connect to Google Sheets API project
        self.api = SpreadsheetAPI(
            spreadsheet_id=SAMPLE_SPREADSHEET_ID, 
            sheet_title='Top Search Keywords',
            sheet_id='165149585',
            credentials='service_credentials.json', 
            apis='https://www.googleapis.com/auth/spreadsheets'
        )
        super().setUp()


    def tearDown(self):
        '''
        Close a connection after each test.
        '''
        self.api.sessionClose()


    def test_get_sheet_url(self):
        '''
        Test of get_sheet_url()
        '''
        url = self.api.get_sheet_url()
        self.assertEqual(url, self.res)


    def test_get_sheet(self):
        '''
        Test of get_sheet()
        '''
        sheet = self.api.get_sheet()
        result = {'range': "'Top Search Keywords'!A1:Z1000", 'majorDimension': 'ROWS', 'values': [['', 'Jan', 'Feb'], ['1', 'heat', 'cats'], ['2', 'aurora', 'snow'], ['3', 'summer', 'hiking']]}
        self.assertEqual(sheet, result)


    def test_get(self):
        '''
        Test of get()
        '''
        response_cell = self.api.get('B1')
        response_column = self.api.get('B1:B4')

        value_cell = response_cell['values']
        values_column = response_column['values']

        result_cell = [['Jan']]
        result_column = [['Jan'], ['heat'], ['aurora'], ['summer']]

        self.assertEqual(value_cell, result_cell)
        self.assertEqual(values_column, result_column)


    def test_insert(self):
        '''
        Test of insert()
        '''
        response_cell = self.api.insert(values=[['Header']], start_column='A1', sheet_name='Insert test')
        response_row = self.api.insert(values=[['testing'], ['testing'], ['testing'], ['testing']], start_column='A2', end_column='A5', sheet_name='Insert test')
        self.assertTrue(response_cell)
        self.assertTrue(response_row)

    
    def test_clear(self):
        '''
        Test of clear()
        '''
        self.api.clear(get_range(start='A2', end='A4', sheet_name='Top Search Keywords'))
        
        range_cell = 'A2'
        range_column = 'A3:A4'

        response_cell = self.api.get(range_cell)
        response_column = self.api.get(range_column)

        result_cell = {'range': "'Top Search Keywords'!{}".format(range_cell), 'majorDimension': 'ROWS'}
        result_column = {'range': "'Top Search Keywords'!{}".format(range_column), 'majorDimension': 'ROWS'}

        self.api.insert(values=[['1'],['2'],['3']], start_column='A2', end_column='A4', sheet_name='Top Search Keywords')

        # Place values back so they'll be available for the next test
        self.assertEqual(response_cell, result_cell)
        self.assertEqual(response_column, result_column)




if __name__ == '__main__':

    # Run all the tests inside of TestSpreadsheetAPI class
    unittest.main()
