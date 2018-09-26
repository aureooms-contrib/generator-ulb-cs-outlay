import os
import sys
import json
import argparse

KM = 0.3573
CURRENCY = 'devises (CAD, USD, \\dots)'

parser = argparse.ArgumentParser('Generate the outlay from a JSON data file.')
parser.add_argument('data', type=argparse.FileType('r'))
parser.add_argument('total', type=argparse.FileType('r'))
args = parser.parse_args()

data = json.load(args.data)
total = json.load(args.total)

data["total"] = total

data.setdefault('advance', 0)

LATEXDIR = 'generator/latex{}'

rules = {
    'string' : lambda string , variables: string ,
    'template-string' : lambda string, variables: string.format(**variables) ,
}


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

def table ( key , details = '' ) :
    items = data.get(key)
    if items is None : lines('string', 'table-missing')
    else:
        lines('string', 'table-begin')
        out('template-string', 'table-header', {'details': details})
        for item in items:
            km = item.get('km')
            if km is not None:
                item.setdefault('currency', '{} km x EUR {}'.format(km, KM))
                item.setdefault('eur', km * KM)
            else:
                item.setdefault('currency', '')
            row(item)
        lines('string', 'table-end')

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
