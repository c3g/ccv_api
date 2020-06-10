# -*- coding: utf-8 -*-
import json
import xml.etree.ElementTree as ET
from collections import defaultdict


def etree_to_dict(t):
    """
    Converts the xml tree to python dictionary
    :param t: xml root element
    :return: python dictionary
    """
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['text'] = text
        else:
            d[t.tag] = text
    return d


with open('ccv_sample_3.xml', encoding="utf8") as xml_file:
    tree = ET.parse(xml_file)
    d = etree_to_dict(tree.getroot())
    d = d["{http://www.cihr-irsc.gc.ca/generic-cv/1.0.0}generic-cv"]
    json_data = json.dumps(d, indent=4, sort_keys=True)


def get_fields(fields: list):
    """
    :param fields:
    :return:
    """
    all_fields = {}
    for field in fields:
        if 'lov' in field and 'text' in field.get('lov'):
            all_fields[field.get('label')] = field.get('lov').get('text')
        elif 'value' in field and 'text' in field.get('value'):
            all_fields[field.get('label')] = field.get('value').get('text')
        else:
            all_fields[field.get('label')] = ''
    return all_fields


def get_response(sections: list):
    """
    :param sections:
    :return:
    """

    response = {}
    for section in sections:
        response[section.get('label')] = {}
        if 'field' in section:
            if not isinstance(section.get('field'), list):
                section['field'] = [section.get('field')]
            response[section.get('label')] = get_fields(section.get('field'))

        if 'section' in section:
            label_of_section = section['section']['label']
            if not isinstance(section.get('section'), list):
                section['section'] = [section.get('section')]
            response[section.get('label')][label_of_section] = {}
            response[section.get('label')][label_of_section] = get_response(section.get('section'))
    return response


final_data = []


if "section" in d and isinstance(d["section"], list):
    # print("here")
    final_data.extend(get_response(d['section']))

## Final data structure
json_data = json.dumps(final_data, indent=4, sort_keys=True)

with open("data_new.json", "w") as json_file:
    json_file.write(json_data)
    json_file.close()

