from lxml import etree as ET
import os
import re
import csv
import json
from functools import partial
import sys

languages = ['en', 'fr']

xml_lang = '{http://www.w3.org/XML/1998/namespace}lang'
nsmap = {'xml': 'http://www.w3.org/XML/1998/namespace'}

OUTPUTDIR = os.path.join('out', 'clv3')


def normalize_whitespace(x):
    if x is None:
        return x
    x = x.strip()
    x = re.sub(r'\s+', ' ', x)
    return x


def codelist_item_todict(codelist_item, default_lang='', lang='en'):
    out = {}
    for child in codelist_item:
        el_name = child.tag
        if child.prefix is not None:
            el_name = '{}:{}'.format(
                child.prefix, child.tag.split('}')[1])
        if child.find('narrative') is not None:
            if lang == default_lang:
                narrative = child.xpath(
                    'narrative[not(@xml:lang)]',
                    namespaces=nsmap)
                if len(narrative) == 0:
                    continue
                out[el_name] = normalize_whitespace(narrative[0].text)
            else:
                narrative = child.find(
                    'narrative[@xml:lang="{}"]'.format(lang),
                    namespaces=nsmap)
                if narrative is None:
                    continue
                out[el_name] = normalize_whitespace(narrative.text)
        else:
            out[el_name] = normalize_whitespace(child.text)

    if 'public-database' in codelist_item.attrib:
        if codelist_item.attrib['public-database'] in ['1', 'true']:
            out['public-database'] = True
        else:
            out['public-database'] = False
    return out


def utf8_encode_dict(d):
    def enc(a):
        if type(a) == str:
            return a.encode('utf8')
        else:
            return None
    return dict((enc(k), enc(v)) for k, v in d.items())


for language in languages:
    codelists = ET.Element('codelists')
    codelists_list = []

    try:
        os.makedirs(os.path.join(OUTPUTDIR, 'json', language))
        os.makedirs(os.path.join(OUTPUTDIR, 'csv', language))
    except OSError:
        pass

    for fname in os.listdir('combined-xml'):
        codelist = ET.parse(os.path.join('combined-xml', fname))
        attrib = codelist.getroot().attrib
        assert attrib['name'] == fname.replace('.xml', '')

        default_lang = codelist.getroot().attrib.get(xml_lang)
        codelist_dicts = list(map(partial(codelist_item_todict, default_lang=default_lang, lang=language), codelist.getroot().find('codelist-items').findall('codelist-item')))

        fieldnames = [
            'code',
            'name',
            'description',
            'category',
            'url'
        ]

        if fname == 'OrganisationRegistrationAgency.xml':
            fieldnames.append('public-database')

        dw = csv.DictWriter(open(os.path.join(OUTPUTDIR, 'csv', language, attrib['name'] + '.csv'), 'w'), fieldnames)
        dw.writeheader()
        for row in codelist_dicts:
            if sys.version_info.major == 2:
                row = utf8_encode_dict(row)
            dw.writerow(row)

        name_elements = codelist.getroot().xpath('/codelist/metadata/name[{}@xml:lang="{}"]'.format('not(@xml:lang) or ' if language == default_lang else '', language))
        description_elements = codelist.getroot().xpath('/codelist/metadata/description[{}@xml:lang="{}"]'.format('not(@xml:lang) or ' if language == default_lang else '', language))
        url_elements = codelist.getroot().xpath('/codelist/metadata/url')

        # JSON
        json.dump(
            {
                'attributes': {
                    'name': attrib['name'],
                    'complete': attrib.get('complete'),
                    'category-codelist': attrib.get('category-codelist'),
                },
                'metadata': {
                    'name': name_elements[0].text if name_elements else '',
                    'description': description_elements[0].text if description_elements else '',
                    'url': url_elements[0].text if url_elements else ''
                },
                'data': codelist_dicts
            },
            open(os.path.join(OUTPUTDIR, 'json', language, attrib['name'] + '.json'), 'w')
        )
        codelists_list.append(attrib['name'])

        ET.SubElement(codelists, 'codelist').attrib['ref'] = attrib['name']

tree = ET.ElementTree(codelists)
tree.write(os.path.join(OUTPUTDIR, 'codelists.xml'), pretty_print=True)

json.dump(codelists_list, open(os.path.join(OUTPUTDIR, 'codelists.json'), 'w'))
