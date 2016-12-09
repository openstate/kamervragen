#!/usr/bin/env python

import sys
import re
import datetime

from BeautifulSoup import BeautifulSoup
import requests

import logging

logger = logging.getLogger('blaat')
# logger.setLevel(level=logging.INFO)


def fetch_ao_url(url):
    try:
        request = requests.get(url, verify=False)
        status_code = request.status_code
        content = request.content
    except requests.ConnectionError:
        status_code = -1
        content = u''
    except requests.HTTPError:
        status_code = -2
        content = u''
    except requests.URLRequired:
        status_code = -3
        content = u''
    except requests.TooManyRedirects:
        status_code = -4
        content = u''
    except requests.HTTPError:
        status_code = -5
        content = u''
    except requests.RequestException:
        status_code = -6
        content = u''
    return status_code, content


def find_kamerstukken(content, url, what):
    urls = []
    soup = BeautifulSoup(content)

    try:
        lijst = soup.findAll('div', 'lijst')[0]
    except IndexError:
        lijst = None

    if lijst is None:
        return [], []

    kamerstukken = []
    for a in lijst.findAll('a'):
        if what == 'ao':
            match = re.match('\/(kst)-([^\.]*?)\.html', a['href'])
        else:
            match = re.match('\/(kv|ah)-([^\.]*?)\.html', a['href'])
        if match:
            kamerstukken.append(
                'https://zoek.officielebekendmakingen.nl/%s-%s.xml' % (
                    match.group(1), match.group(2), ))

    try:
        paginering = soup.findAll('div', 'paginering beneden')[0]
    except IndexError:
        paginering = None

    if paginering is None:
        return kamerstukken, []

    max_count = paginering.findAll('a')[-2].findAll(text=True)

    if max_count <= 0:
        return kamerstukken, []

    try:
        last_page = int(max_count[0])
    except ValueError:
        last_page = 0

    urls = []
    cur_page = 1
    while (cur_page <= last_page):
        next_page = cur_page + 1
        new_url = re.sub('&_page=(\d+)', '', url)
        new_url += '&_page=%s' % (next_page, )
        cur_page = next_page
        urls.append(new_url)
    # urls = [a['href'] for a in paginering.findAll('a')]

    return kamerstukken, urls


def main(args):
    days_in_month = {
        '01': '31',
        '02': '28',
        '03': '31',
        '04': '30',
        '05': '31',
        '06': '30',
        '07': '31',
        '08': '31',
        '09': '30',
        '10': '31',
        '11': '30',
        '12': '31',
    }

    what_to_par = {
        'ao': 'Kamerstuk',
        'kamervragen': (
            'Aanhangsel+van+de+Handelingen%7cKamervragen+zonder+antwoord')
    }

    what_to_vrt = {
        'ao': 'vrt=Verslag+van+een+algemeen+overleg&zkd=AlleenInDeTitel&',
        'kamervragen': ''
    }
    all_kamerstukken = []

    # year = int(args[0])
    # week = int(args[1])
    # datum_start = isoweek_to_date(year, week)
    # datumstart = datum_start.strftime('%Y%m%d')
    # datum_eind = (datum_start + datetime.timedelta(days=6))
    # datumeind = datum_eind.strftime('%Y%m%d')
    datum_start = datetime.datetime.strptime(args[0], '%Y%m%d')
    datum_eind = datetime.datetime.strptime(args[1], '%Y%m%d')
    days_between = int(args[3])

    datum_curr = datum_start
    while (datum_curr < datum_eind):
        datumstart = datum_curr.strftime('%Y%m%d')
        datum_weekeind = datum_curr + datetime.timedelta(days=days_between)
        datumeind = datum_weekeind.strftime('%Y%m%d')
        par = what_to_par[args[2]]
        zoek = what_to_vrt[args[2]]
        url = (
            'https://zoek.officielebekendmakingen.nl/zoeken/resultaat/'
            '?zkt=Uitgebreid&pst=ParlementaireDocumenten&' + zoek +
            'dpr=AnderePeriode&spd=' + datumstart + '&epd=' + datumeind +
            '&kmr=TweedeKamerderStatenGeneraal&sdt=KenmerkendeDatum&par=' +
            par + '&dst=Opgemaakt%7cOpgemaakt+na+onopgemaakt&isp=true&pnr=1&'
            'rpp=10&_page=1&sorttype=1&sortorder=4')
        status_code, content = fetch_ao_url(url)
        logger.info('%s: %s' % (url, status_code, ))

        if status_code != 200:
            return

        kamerstukken, urls = find_kamerstukken(content, url, args[2])
        all_kamerstukken += kamerstukken

        for url in urls:
            status_code, content = fetch_ao_url(url)
            # print url, status_code

            if status_code != 200:
                continue

            kamerstukken, dummy = find_kamerstukken(content, url, args[2])
            all_kamerstukken += kamerstukken

        datum_curr = datum_curr + datetime.timedelta(days=(days_between + 1))

    all_kamerstukken_clean = list(set(all_kamerstukken))

    for kamerstuk in all_kamerstukken_clean:
        print kamerstuk

if __name__ == '__main__':
    # ./bin/zoek_ob.py 20150101 20150201 kamervragen 1
    main(sys.argv[1:])
