import os
import sys
import re
import json
import argparse
from datetime import datetime

KM = 0.3653
CURRENCY = 'devises (CAD, USD, \\dots)'

parser = argparse.ArgumentParser('Generate the outlay from a JSON data file.')
parser.add_argument('data', type=argparse.FileType('r'))
parser.add_argument('perdiem', type=argparse.FileType('r'))
args = parser.parse_args()

data = json.load(args.data)
PERDIEM = json.load(args.perdiem)


data.setdefault('advance', 0)

LATEXDIR = 'generator/latex{}'

rules = {
    'string' : lambda string , variables: string ,
    'template-string' : lambda string, variables: string.format(**variables) ,
}

def isConvertedDate ( string ) :
    pattern = re.compile("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T00:00:00\\.000Z")
    return pattern.fullmatch(string)

def fixDates ( item ) :
    if isinstance(item, dict):
        for key, value in item.items():
            item[key] = fixDates(value)
        return item
    if isinstance(item, list):
        return list(map(fixDates, item))
    if isinstance(item, str):
        if isConvertedDate(item):
            return item[:10]

    return item


# needs this because yaml2json messes up the dates
data = fixDates(data)

stringdirs = os.listdir(LATEXDIR.format(''))

strings = {}

for entry in stringdirs:
    strings[entry] = {}
    for string in os.listdir(LATEXDIR.format('/' + entry)):
        with open(LATEXDIR.format('/' + entry + '/' + string )) as f:
            strings[entry][string[:-4]] = f.read()

out = lambda kind , key , variables : print(rules[kind](strings[kind][key], variables))
row = lambda variables : out('template-string', 'table-row', variables)
info = data
lines = lambda kind , key : out(kind, key, info)

NEXT_ID = 1

def fill ( item ) :

    global NEXT_ID

    if "id" not in item.keys():
        item["id"] = NEXT_ID
        NEXT_ID += 1

    km = item.get('km')
    if km is not None:
        item.setdefault('currency', '{} km x EUR {}'.format(km, KM))
        item.setdefault('eur', km * KM)
    else:
        item.setdefault('currency', '')

    perdiem = item.get('perdiem')
    if perdiem is not None:
        date = item.get('date')
        begin, end = date.split(' -- ')
        date_format = "%Y-%m-%d"
        a = datetime.strptime(begin, date_format)
        b = datetime.strptime(end, date_format)
        delta = b - a
        days = delta.days
        if days == 0: days = 0.5 # first and last day count half

        if perdiem == 'fria':
            perday = 30
        elif perdiem == 'fnrs':
            perday = 50
        else:
            if days <= 30:
                perday = PERDIEM[perdiem]["short"]
            else:
                perday = PERDIEM[perdiem]["long"]
        total = days * perday
        item.setdefault('eur', total)
        item.setdefault('title', '{} EUR x {} jours {}'.format(perday, days, perdiem.upper()))

CATEGORIES = ['car', 'travel', 'other']

for key in CATEGORIES:
    for item in data.get(key,[]):
        fill(item)

def table ( key , details = '' ) :
    items = data.get(key)
    if items is None : lines('string', 'table-missing')
    else:
        lines('string', 'table-begin')
        out('template-string', 'table-header', {'details': details})
        for item in items:
            row(item)
        lines('string', 'table-end')

amounts = data["total"] = { }

for key in CATEGORIES:
    amounts[key] = sum(map(lambda x: x['eur'], data.get(key,[])))

amounts["all"] = sum(amounts.values()) - data.get('advance', 0)


# Output of LaTeX source starts here

lines('string', 'header')
lines('template-string', 'title')
lines('template-string', 'author')

lines('string', 'document-begin')
lines('template-string', 'intro')

lines('string', 'section-car')
table('car')

lines('string', 'section-travel')
table('travel', CURRENCY)

lines('string', 'section-other')
table('other', CURRENCY)

lines('string', 'section-advance')
lines('template-string', 'content-advance')

lines('string', 'section-refund')
lines('template-string', 'content-refund')

lines('string', 'document-end')
