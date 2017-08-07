import math
import os
import re
import requests
from pyquery import PyQuery as pq


def _collect_from_bing(q, start=0, stop=28, save_dir='./'):
    """
    Search and collects images from Bing.
    Parameters
    ==========
    q : str
        search keyword
    start : int
        first index of images want to collect
    stop : int
        last index of images want to collect
    save_dir : str
        directory of images want to save
    """
    # check the directory exists.
    if not os.path.exists('{0}/{1}'.format(save_dir, q)):
        os.makedirs('{0}/{1}'.format(save_dir, q))

    a = int(math.log10(stop)) + 1

    url = 'https://www.bing.com/images/search'
    params = {
        'q':q,
        'form':'A',
        'qft':'+filterui:face-face'
    }

    # crawl images
    for n in range(start, stop, 28):
        params['first'] = n
        params['count'] = 28

        response = requests.get(url=url, params=params, timeout=10)
        html = pq(response.text)

        # parse links of images
        links = []
        for item in html('#main .row .item .thumb').items():
            links.append(item.attr('href'))

        if len(links) > 0:
            # save images
            for (i, link) in enumerate(links):
                img = requests.get(url=link).content
                file_name = str(n + i).zfill(a)
                with open('{0}/{1}/bing_{2}.jpg'.format(save_dir, q, file_name), 'wb') as f:
                    f.write(img)
            print('Number of images saved is : {}'.format(n + len(links)))
        else:
            break

    print('Complete!')


def _collect_from_google(q, start=0, stop=20, save_dir='./'):
    """
    Search and collects images from Google.
    Parameters
    ==========
    q : str
        search keyword
    start : int
        first index of images want to collect
    stop : int
        last index of images want to collect
    save_dir : str
        directory of images want to save
    """
    # check the directory exists.
    if not os.path.exists('{0}/{1}'.format(save_dir, q)):
        os.makedirs('{0}/{1}'.format(save_dir, q))

    a = int(math.log10(stop)) + 1

    url = 'https://www.google.com/search'
    params = {
        'q':q,
        'tbm':'isch',
        'tbs':'itp:face'
    }

    # crawl images
    for n in range(start, stop, 20):
        params['start'] = n

        response = requests.get(url=url, params=params, timeout=10)
        html = pq(response.text)

        # parse links of images
        links = []
        for item in html('#ires tr a img').items():
            links.append(item.attr('src'))

        if len(links) > 0:
            # save images
            for (i, link) in enumerate(links):
                img = requests.get(url=link).content
                file_name = str(n + i).zfill(a)
                with open('{0}/{1}/google_{2}.jpg'.format(save_dir, q, file_name), 'wb') as f:
                    f.write(img)
            print('Number of images saved is : {}'.format(n + len(links)))
        else:
            break

    print('Complete!')


def collect(from_, q, start=0, stop=20, save_dir='./'):
    """
    Search and collects images.
    Parameters
    ==========
    from_ : str
        from which sites to collect
    q : str
        search keyword
    start : int
        first index of images want to collect
    stop : int
        last index of images want to collect
    save_dir : str
        directory of images want to save
    """
    if from_ == 'all':
        _collect_from_bing(q, start, stop, save_dir)
        _collect_from_google(q, start, stop, save_dir)
    elif from_ == 'bing':
        _collect_from_bing(q, start, stop, save_dir)
    elif from_ == 'google':
        _collect_from_google(q, start, stop, save_dir)
    else:
        raise ValueError("argument 'from_' must be one of 'all', 'bing', and 'google'.")
