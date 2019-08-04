import hibc
import random
import string
import datetime


def test_check_character():
    for letter in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%':
        assert hibc.get_check_character(letter) == letter
    examples = {
        '+E20831269/$$8020423286539': '+',
        '+E20831339/$$8020223283831': 'T'
    }
    for barcode, check_character in examples.items():
        assert hibc.get_check_character(barcode) == check_character


def test_fuzzy_encode_decode():
    for ref in range(100):
        # noinspection PyUnusedLocal
        data = {
            'check OK': True,
            'lic': random.choice(string.ascii_letters) + ''.join(random.choice(string.ascii_letters + string.digits) for i in range(3)),
            'ref': ''.join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(1, 18))),
            'unit_of_measure': random.choice(string.digits),
            'expiry date': datetime.datetime(random.randint(1969, 2068), random.randint(1, 12), random.randint(1, 28), random.randint(0, 23)),
            'serial number': ''.join(random.choice(string.ascii_letters + string.digits + '-.') for i in range(0, random.randint(0, 30))),
            'lot number': ''.join(random.choice(string.ascii_letters + string.digits + '-.') for i in range(0, random.randint(0, 30))),
            'quantity': random.randint(0, 99999),
            'production date': datetime.date(random.randint(1980, 2100), random.randint(1, 12), random.randint(1, 28))
        }
        if random.random() < 0.5:
            del data['serial number']
        if random.random() < 0.5:
            del data['lot number']
        if random.random() < 0.5:
            del data['quantity']
        if random.random() < 0.5:
            del data['expiry date']
        if random.random() < 0.8:
            del data['production date']
        code = hibc.generate(**data)
        data['barcode'] = code
        result = hibc.parse(code)
        if data.get('lot number', None) == '':
            del data['lot number']
        if data.get('serial number', None) == '':
            del data['serial number']
        data['check character actual'] = result['check character actual']
        data['check character computed'] = result['check character computed']
        assert result == data


def test_primary_codes():
    codes = {
        '+A123BJC5D6E71G': {'check OK': True, 'check character actual': 'G', 'check character computed': 'G', 'lic': 'A123', 'ref': 'BJC5D6E7', 'unit_of_measure': '1'}
    }
    for barcode, reference in codes.items():
        reference['barcode'] = barcode
        assert hibc.parse(barcode) == reference


def test_two_linked_codes():
    result = hibc.parse('+E234MEDIX12Y0T')
    assert result == {'check character actual': 'T', 'check character computed': 'T', 'check OK': True, 'lic': 'E234', 'ref': 'MEDIX12Y', 'unit_of_measure': '0', 'barcode': '+E234MEDIX12Y0T'}
    secondary_codes = {
        '+$$+09050001TC': {'check OK': False,
                           'check character actual': 'C',
                           'check character computed': '3',
                           'check link': True,
                           'expiry date': datetime.datetime(2005, 9, 1, 0, 0),
                           'lic': 'E234',
                           'link character primary': 'T',
                           'link character secondary': 'T',
                           'ref': 'MEDIX12Y',
                           'serial number': '0001',
                           'unit_of_measure': '0'},
        '+$$+20928050001TC': {'check OK': False,
                              'check character actual': 'C',
                              'check character computed': 'F',
                              'check link': True,
                              'expiry date': datetime.datetime(2005, 9, 28, 0, 0),
                              'lic': 'E234',
                              'link character primary': 'T',
                              'link character secondary': 'T',
                              'ref': 'MEDIX12Y',
                              'serial number': '0001',
                              'unit_of_measure': '0'},
        '+$$+30509280001TC ': {'check OK': False,
                               'check character actual': ' ',
                               'check character computed': '2',
                               'check link': False,
                               'expiry date': datetime.datetime(2005, 9, 28, 0, 0),
                               'lic': 'E234',
                               'link character primary': 'T',
                               'link character secondary': 'C',
                               'ref': 'MEDIX12Y',
                               'serial number': '0001T',
                               'unit_of_measure': '0'},
        '+$$+4050928200001TC': {'check OK': False,
                                'check character actual': 'C',
                                'check character computed': 'J',
                                'check link': True,
                                'expiry date': datetime.datetime(2005, 9, 28, 20, 0),
                                'lic': 'E234',
                                'link character primary': 'T',
                                'link character secondary': 'T',
                                'ref': 'MEDIX12Y',
                                'serial number': '0001',
                                'unit_of_measure': '0'},
        '+$$+5052710001TC': {'check OK': False,
                             'check character actual': 'C',
                             'check character computed': '9',
                             'check link': True,
                             'expiry date': datetime.datetime(2005, 9, 28, 0, 0),
                             'lic': 'E234',
                             'link character primary': 'T',
                             'link character secondary': 'T',
                             'ref': 'MEDIX12Y',
                             'serial number': '0001',
                             'unit_of_measure': '0'},
        '+$$+605271200001TC': {'check OK': True,
                               'check character actual': 'C',
                               'check character computed': 'C',
                               'check link': True,
                               'expiry date': datetime.datetime(2005, 9, 28, 20, 0),
                               'lic': 'E234',
                               'link character primary': 'T',
                               'link character secondary': 'T',
                               'ref': 'MEDIX12Y',
                               'serial number': '0001',
                               'unit_of_measure': '0'},
        '+$$+70001TC': {'check OK': False,
                        'check character actual': 'C',
                        'check character computed': '$',
                        'check link': True,
                        'lic': 'E234',
                        'link character primary': 'T',
                        'link character secondary': 'T',
                        'ref': 'MEDIX12Y',
                        'serial number': '0001',
                        'unit_of_measure': '0'},
        '+$$09053C001TC': {'check OK': False,
                           'check character actual': 'C',
                           'check character computed': 'K',
                           'check link': True,
                           'expiry date': datetime.datetime(2005, 9, 1, 0, 0),
                           'lic': 'E234',
                           'link character primary': 'T',
                           'link character secondary': 'T',
                           'lot number': '3C001',
                           'ref': 'MEDIX12Y',
                           'unit_of_measure': '0'},
        '+$$20928053C001TC': {'check OK': False,
                              'check character actual': 'C',
                              'check character computed': 'W',
                              'check link': True,
                              'expiry date': datetime.datetime(2005, 9, 28, 0, 0),
                              'lic': 'E234',
                              'link character primary': 'T',
                              'link character secondary': 'T',
                              'lot number': '3C001',
                              'ref': 'MEDIX12Y',
                              'unit_of_measure': '0'},
        '+$$30509283C001TC': {'check OK': False,
                              'check character actual': 'C',
                              'check character computed': 'X',
                              'check link': True,
                              'expiry date': datetime.datetime(2005, 9, 28, 0, 0),
                              'lic': 'E234',
                              'link character primary': 'T',
                              'link character secondary': 'T',
                              'lot number': '3C001',
                              'ref': 'MEDIX12Y',
                              'unit_of_measure': '0'},
        '+$$4050928223C001TC': {'check OK': False,
                                'check character actual': 'C',
                                'check character computed': ' ',
                                'check link': True,
                                'expiry date': datetime.datetime(2005, 9, 28, 22, 0),
                                'lic': 'E234',
                                'link character primary': 'T',
                                'link character secondary': 'T',
                                'lot number': '3C001',
                                'ref': 'MEDIX12Y',
                                'unit_of_measure': '0'},
        '+$$5052713C001TC': {'check OK': False,
                             'check character actual': 'C',
                             'check character computed': 'Q',
                             'check link': True,
                             'expiry date': datetime.datetime(2005, 9, 28, 0, 0),
                             'lic': 'E234',
                             'link character primary': 'T',
                             'link character secondary': 'T',
                             'lot number': '3C001',
                             'ref': 'MEDIX12Y',
                             'unit_of_measure': '0'},
        '+$$605271223C001TC': {'check OK': False,
                               'check character actual': 'C',
                               'check character computed': 'V',
                               'check link': True,
                               'expiry date': datetime.datetime(2005, 9, 28, 22, 0),
                               'lic': 'E234',
                               'link character primary': 'T',
                               'link character secondary': 'T',
                               'lot number': '3C001',
                               'ref': 'MEDIX12Y',
                               'unit_of_measure': '0'},
        '+$$73C001TC': {'check OK': False,
                        'check character actual': 'C',
                        'check character computed': 'D',
                        'check link': True,
                        'lic': 'E234',
                        'link character primary': 'T',
                        'link character secondary': 'T',
                        'lot number': '3C001',
                        'ref': 'MEDIX12Y',
                        'unit_of_measure': '0'},
        '+$$82409053C001TC': {'check OK': False,
                              'check character actual': 'C',
                              'check character computed': 'Y',
                              'check link': True,
                              'expiry date': datetime.datetime(2005, 9, 1, 0, 0),
                              'lic': 'E234',
                              'link character primary': 'T',
                              'link character secondary': 'T',
                              'quantity': 24,
                              'ref': 'MEDIX12Y',
                              'lot number': '3C001',
                              'unit_of_measure': '0'},
        '+$$82420928053C001TC': {'check OK': False,
                                 'check character actual': 'C',
                                 'check character computed': '3',
                                 'check link': True,
                                 'expiry date': datetime.datetime(2005, 9, 28, 0, 0),
                                 'lic': 'E234',
                                 'link character primary': 'T',
                                 'link character secondary': 'T',
                                 'quantity': 24,
                                 'ref': 'MEDIX12Y',
                                 'lot number': '3C001',
                                 'unit_of_measure': '0'},
        '+$$82430509283C001TC': {'check OK': False,
                                 'check character actual': 'C',
                                 'check character computed': '4',
                                 'check link': True,
                                 'expiry date': datetime.datetime(2005, 9, 28, 0, 0),
                                 'lic': 'E234',
                                 'link character primary': 'T',
                                 'link character secondary': 'T',
                                 'quantity': 24,
                                 'ref': 'MEDIX12Y',
                                 'lot number': '3C001',
                                 'unit_of_measure': '0'},
        '+$$8244050928223C001TC': {'check OK': False,
                                   'check character actual': 'C',
                                   'check character computed': '9',
                                   'check link': True,
                                   'expiry date': datetime.datetime(2005, 9, 28, 22, 0),
                                   'lic': 'E234',
                                   'link character primary': 'T',
                                   'link character secondary': 'T',
                                   'quantity': 24,
                                   'ref': 'MEDIX12Y',
                                   'lot number': '3C001',
                                   'unit_of_measure': '0'},
        '+$$8245052713C001TC': {'check OK': False,
                                'check character actual': 'C',
                                'check character computed': '/',
                                'check link': True,
                                'expiry date': datetime.datetime(2005, 9, 28, 0, 0),
                                'lic': 'E234',
                                'link character primary': 'T',
                                'link character secondary': 'T',
                                'quantity': 24,
                                'ref': 'MEDIX12Y',
                                'lot number': '3C001',
                                'unit_of_measure': '0'},
        '+$$824605271223C001TC': {'check OK': False,
                                  'check character actual': 'C',
                                  'check character computed': '2',
                                  'check link': True,
                                  'expiry date': datetime.datetime(2005, 9, 28, 22, 0),
                                  'lic': 'E234',
                                  'link character primary': 'T',
                                  'link character secondary': 'T',
                                  'quantity': 24,
                                  'ref': 'MEDIX12Y',
                                  'lot number': '3C001',
                                  'unit_of_measure': '0'},
        '+$$82473C001TC': {'check OK': False,
                           'check character actual': 'C',
                           'check character computed': 'R',
                           'check link': True,
                           'lic': 'E234',
                           'link character primary': 'T',
                           'link character secondary': 'T',
                           'quantity': 24,
                           'ref': 'MEDIX12Y',
                           'lot number': '3C001',
                           'unit_of_measure': '0'},
        '+$$824TC': {'check OK': False,
                     'check character actual': 'C',
                     'check character computed': '4',
                     'check link': True,
                     'lic': 'E234',
                     'link character primary': 'T',
                     'link character secondary': 'T',
                     'quantity': 24,
                     'ref': 'MEDIX12Y',
                     'unit_of_measure': '0'},
        '+$$90010009053C001TC': {'check OK': False,
                                 'check character actual': 'C',
                                 'check character computed': 'U',
                                 'check link': True,
                                 'expiry date': datetime.datetime(2005, 9, 1, 0, 0),
                                 'lic': 'E234',
                                 'link character primary': 'T',
                                 'link character secondary': 'T',
                                 'quantity': 100,
                                 'ref': 'MEDIX12Y',
                                 'lot number': '3C001',
                                 'unit_of_measure': '0'},
        '+$$90010020928053C001TC': {'check OK': False,
                                    'check character actual': 'C',
                                    'check character computed': '%',
                                    'check link': True,
                                    'expiry date': datetime.datetime(2005, 9, 28, 0, 0),
                                    'lic': 'E234',
                                    'link character primary': 'T',
                                    'link character secondary': 'T',
                                    'quantity': 100,
                                    'ref': 'MEDIX12Y',
                                    'lot number': '3C001',
                                    'unit_of_measure': '0'},
        '+$$90010030509283C001TC': {'check OK': False,
                                    'check character actual': 'C',
                                    'check character computed': '0',
                                    'check link': True,
                                    'expiry date': datetime.datetime(2005, 9, 28, 0, 0),
                                    'lic': 'E234',
                                    'link character primary': 'T',
                                    'link character secondary': 'T',
                                    'quantity': 100,
                                    'ref': 'MEDIX12Y',
                                    'lot number': '3C001',
                                    'unit_of_measure': '0'},
        '+$$9001004050928223C001TC': {'check OK': False,
                                      'check character actual': 'C',
                                      'check character computed': '5',
                                      'check link': True,
                                      'expiry date': datetime.datetime(2005, 9, 28, 22, 0),
                                      'lic': 'E234',
                                      'link character primary': 'T',
                                      'link character secondary': 'T',
                                      'quantity': 100,
                                      'ref': 'MEDIX12Y',
                                      'lot number': '3C001',
                                      'unit_of_measure': '0'},
        '+$$9001005052713C001TC': {'check OK': False,
                                   'check character actual': 'C',
                                   'check character computed': '-',
                                   'check link': True,
                                   'expiry date': datetime.datetime(2005, 9, 28, 0, 0),
                                   'lic': 'E234',
                                   'link character primary': 'T',
                                   'link character secondary': 'T',
                                   'quantity': 100,
                                   'ref': 'MEDIX12Y',
                                   'lot number': '3C001',
                                   'unit_of_measure': '0'},
        '+$$900100605271223C001TC': {'check OK': False,
                                     'check character actual': 'C',
                                     'check character computed': '+',
                                     'check link': True,
                                     'expiry date': datetime.datetime(2005, 9, 28, 22, 0),
                                     'lic': 'E234',
                                     'link character primary': 'T',
                                     'link character secondary': 'T',
                                     'quantity': 100,
                                     'ref': 'MEDIX12Y',
                                     'lot number': '3C001',
                                     'unit_of_measure': '0'},
        '+$$90010073C001TC': {'check OK': False,
                              'check character actual': 'C',
                              'check character computed': 'N',
                              'check link': True,
                              'lic': 'E234',
                              'link character primary': 'T',
                              'link character secondary': 'T',
                              'quantity': 100,
                              'ref': 'MEDIX12Y',
                              'lot number': '3C001',
                              'unit_of_measure': '0'},
        '+$$900100TC': {'check OK': False,
                        'check character actual': 'C',
                        'check character computed': '0',
                        'check link': True,
                        'lic': 'E234',
                        'link character primary': 'T',
                        'link character secondary': 'T',
                        'quantity': 100,
                        'ref': 'MEDIX12Y',
                        'unit_of_measure': '0'},
        '+$+0001TC': {'check OK': False,
                      'check character actual': 'C',
                      'check character computed': '-',
                      'check link': True,
                      'lic': 'E234',
                      'link character primary': 'T',
                      'link character secondary': 'T',
                      'ref': 'MEDIX12Y',
                      'serial number': '0001',
                      'unit_of_measure': '0'},
        '+$3C001TC': {'check OK': False,
                      'check character actual': 'C',
                      'check character computed': 'A',
                      'check link': True,
                      'lic': 'E234',
                      'link character primary': 'T',
                      'link character secondary': 'T',
                      'lot number': 'C001',
                      'ref': 'MEDIX12Y',
                      'unit_of_measure': '0'},
        '+05271LOTBATCHIDTC': {'check OK': False,
                               'check character actual': 'C',
                               'check character computed': 'P',
                               'check link': True,
                               'expiry date': datetime.date(2005, 9, 28),
                               'lic': 'E234',
                               'link character primary': 'T',
                               'link character secondary': 'T',
                               'lot number': 'LOTBATCHID',
                               'ref': 'MEDIX12Y',
                               'unit_of_measure': '0'},
        '+05271TC': {'check OK': False,
                     'check character actual': 'C',
                     'check character computed': 'D',
                     'check link': True,
                     'expiry date': datetime.date(2005, 9, 28),
                     'lic': 'E234',
                     'link character primary': 'T',
                     'link character secondary': 'T',
                     'lot number': '',
                     'ref': 'MEDIX12Y',
                     'unit_of_measure': '0'},
        '+9901510X3TG': {'check OK': True,
                         'check character actual': 'G',
                         'check character computed': 'G',
                         'check link': True,
                         'expiry date': datetime.date(1999, 1, 15),
                         'lic': 'E234',
                         'link character primary': 'T',
                         'link character secondary': 'T',
                         'lot number': '10X3',
                         'ref': 'MEDIX12Y',
                         'unit_of_measure': '0'},
        '+2036510X3/S1234567C': {'check OK': False,
                                 'check character actual': 'C',
                                 'check character computed': 'B',
                                 'check link': False,
                                 'expiry date': datetime.date(2020, 12, 30),
                                 'lic': 'E234',
                                 'link character primary': 'T',
                                 'link character secondary': '7',
                                 'lot number': '10X3',
                                 'ref': 'MEDIX12Y',
                                 'serial number': '123456',
                                 'unit_of_measure': '0'}
    }

    for code, reference in secondary_codes.items():
        reference['barcode'] = code
        reference['primary barcode'] = '+E234MEDIX12Y0T'
        assert hibc.parse(code, result) == reference


def test_combined_codes():
    codes = {
        '+E20831269/$$8020423286539+': {'check OK': True,
                                        'check character actual': '+',
                                        'check character computed': '+',
                                        'expiry date': datetime.datetime(2023, 4, 1, 0, 0),
                                        'lic': 'E208',
                                        'quantity': 2,
                                        'ref': '3126',
                                        'lot number': '286539',
                                        'unit_of_measure': '9'},
        '+E20831339/$$8020223283831T': {'check OK': True,
                                        'check character actual': 'T',
                                        'check character computed': 'T',
                                        'expiry date': datetime.datetime(2023, 2, 1, 0, 0),
                                        'lic': 'E208',
                                        'quantity': 2,
                                        'ref': '3133',
                                        'lot number': '283831',
                                        'unit_of_measure': '9'},
        ']C1+H208ACE36E1/19120L914427': {'check OK': True,
                                         'check character actual': '7',
                                         'check character computed': '7',
                                         'expiry date': datetime.date(2019, 4, 30),
                                         'lic': 'H208',
                                         'lot number': 'L91442',
                                         'ref': 'ACE36E',
                                         'unit_of_measure': '1'},
        '+E234MEDIX12Y0/2036510X3/S1234567C': {'check OK': False,
                                               'check character actual': 'C',
                                               'check character computed': '3',
                                               'expiry date': datetime.date(2020, 12, 30),
                                               'lic': 'E234',
                                               'lot number': '10X3',
                                               'ref': 'MEDIX12Y',
                                               'serial number': '1234567',
                                               'unit_of_measure': '0'},
        '+A99912345/$$52001510X3/16D20111212/S77DE1G45-': {'check OK': True,
                                                           'check character actual': '-',
                                                           'check character computed': '-',
                                                           'expiry date': datetime.datetime(2020, 1, 15, 0, 0),
                                                           'lic': 'A999',
                                                           'lot number': '10X3',
                                                           'production date': datetime.date(2011, 12, 12),
                                                           'ref': '1234',
                                                           'serial number': '77DE1G45',
                                                           'unit_of_measure': '5'}
    }
    for barcode, reference in codes.items():
        reference['barcode'] = '+' + barcode.split('+', 1)[-1]
        assert hibc.parse(barcode) == reference