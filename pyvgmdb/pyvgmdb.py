# -*- coding: utf-8 -*-
import requests

from pyvgmdb.VGMdbObject import *

NAME = 'pyvgmdb'
VERSION = '0.0.2'
BASE_URL = 'http://vgmdb.info'

logging.basicConfig(level=logging.DEBUG)


class Category(object):
    ALBUM = 'albums'
    ARTIST = 'artists'
    ORG = 'orgs'
    PRODUCT = 'products'


def request(url, query):
    full_url = "{}/{}/{}".format(BASE_URL, url, query)
    try:
        r = requests.get(full_url,
                         headers={'User-agent': NAME + '/' + VERSION},
                         params={'format': 'json'})
        r.raise_for_status()
        if r.ok:
            return r.json()
        else:
            return {'error': r.status_code}
    except Exception as e:
        return {'error': e}


def search(query):
    """Submit a search request to the VGMdb API, and return the "results" section of
    the response after parsing it into VGMdbObject objects.

    For reference, the response from a search query of $query to VGMdb looks like
    this:
    {
        "link": "search/$query",
        "meta": {},
        "query": "$query",
        "results": {
            "albums": [],
            "artists": [],
            "orgs": [],
            "products": []
        },
        "sections": [
            "albums",
            "artists",
            "orgs",
            "products"
        ],
        "vgmdb_link": "http://vgmdb.net/search?q=$query"
    }
    :param query: the search string
    :return: a dictionary of VGMdbObject objects organised under the keys "albums",
             "artists", "orgs" and "products".
    """
    data = request('search', query)["results"]
    objs = dict()
    objs[Category.ALBUM] = [VGMdbProductSummary(e) for e in data[Category.ALBUM]]
    objs[Category.ARTIST] = [VGMdbArtistSummary(e) for e in data[Category.ARTIST]]
    objs[Category.ORG] = [VGMdbOrgSummary(e) for e in data[Category.ORG]]
    objs[Category.PRODUCT] = [VGMdbProductSummary(e) for e in data[Category.PRODUCT]]
    return objs


def search_albums(query):
    """Equivalent to `search(query)[Category.ALBUM]`
    :param query: the search string
    :return: the "albums" section of the VGBdb API response, parsed into VGMdbAlbumResult
             objects.
    """
    return search(query)[Category.ALBUM]


def search_artists(query):
    """Equivalent to `search(query)[Category.ARTIST]`
    :param query: the search string
    :return: the "artists" section of the VGBdb API response, parsed into VGMdbArtistResult
             objects.
    """
    return search(query)[Category.ARTIST]


def search_orgs(query):
    """Equivalent to `search(query)[Category.ORG]`
    :param query: the search string
    :return: the "orgs" section of the VGBdb API response, parsed into VGMdbOrgResult
             objects.
    """
    return search(query)[Category.ORG]


def search_products(query):
    """Equivalent to `search(query)[Category.PRODUCT]`
    :param query: the search string
    :return: the "products" section of the VGBdb API response, parsed into
             VGMdbProductResult objects.
    """
    return search(query)[Category.PRODUCT]


def get_album(album_id):
    return VGMdbAlbum(request('album', album_id))


def get_artist(artist_id):
    return VGMdbArtist(request('artist', artist_id))


def get_org(org_id):
    return VGMdbOrg(request('org', org_id))


def get_product(product_id):
    return VGMdbProduct(request('product', product_id))
