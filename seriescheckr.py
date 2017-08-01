#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3

import requests
from bs4 import BeautifulSoup, SoupStrainer
from pushbullet import Pushbullet

import config

CWD = os.getcwd()
PATH = CWD + '/'
PB = Pushbullet(config.API_KEY)


def read_txt():
    """Read lines from txt."""
    if os.path.isfile(PATH + 'urls.txt'):
        try:
            with open(PATH + 'urls.txt', 'r') as urls_txt:
                lines = []
                for line in urls_txt:
                    lines.append(line)

                return lines
        except Error as err:
            print(err)
            exit()
    else:
        print('[ERROR] (urls.txt file doesn\'t exist)')
        exit()


def check(url, series_name, date_time):
    """Checks for updates."""
    head, sep, tail = date_time.partition('T')
    ntail = tail.split('+', 1)[0].replace(' ', '')

    connection = sqlite3.connect(PATH + 'records.db')

    with connection:
        cursor = connection.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS records(sname TEXT, mdate TEXT)')

        cursor.execute('SELECT * FROM records WHERE sname= ?', (series_name,))
        found = cursor.fetchone()
        if found:
            cursor.execute(
                'SELECT mdate FROM records WHERE sname= ?', (series_name,))
            date = cursor.fetchone()[0]
            if date == date_time:
                print(series_name + ': [NO UPDATE]')
            else:
                cursor.execute(
                    'UPDATE records SET mdate = ? WHERE sname = ?', (date_time, series_name))
                print(series_name + ': [UPDATE]',
                      '(updated:', head, 'at', ntail + ')')
                # push a notification.
                push = PB.push_link(
                    'seriescheckr: ' + series_name + ' updated:' + head + ' at: ' + ntail, url)

        else:
            # record does not exist.
            cursor.execute('INSERT INTO records VALUES( ?, ?)',
                           (series_name, date_time,))
            print(series_name + ': [ADDED]')


def init():
    """Init."""
    urls = read_txt()
    for url in urls:
        response = requests.get(url.rstrip(), stream=True)
        strainer = SoupStrainer('meta')
        soup = BeautifulSoup(
            response.content, 'html.parser', parse_only=strainer)
        title = soup.find('meta', property='og:title')['content']
        series_name = (title.rpartition(' |')[0])
        # series_name = (title.rpartition(' |')[0])
        try:
            modified_time = soup.find(
                'meta', property='article:modified_time')['content']
            # check(url, title, modified_time)
        except TypeError:
            print(
                series_name + ': [ERROR] (can\'t find meta tag, possibly webpage not updated)')
            continue
        check(url, series_name, modified_time)


if __name__ == '__main__':
    init()
