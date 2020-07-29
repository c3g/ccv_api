import datetime
from collections import defaultdict


def normalize_string(s: str) -> str:
    """
    :param s:
    :return:
    """
    return s.strip()


def parse_integer(s: str) -> int or None:
    """
    :param s:
    :return:
    """
    int(s) if isinstance(s, str) and len(s) > 0 else None


def etree_to_dict(t) -> dict:
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


def normalize_date(datetime_obj, fmt) -> str:
    """
    :param datetime_obj:
    :param fmt:
    :return: it returns the formatted datetime
    """
    if not datetime_obj:
        return None
    return datetime.datetime.strftime(datetime_obj, fmt)
