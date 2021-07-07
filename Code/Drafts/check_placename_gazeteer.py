#!/usr/bin/env python3

import urllib.parse
import requests
import json
from datetime import datetime

def log(to_log: str):
    """"Quick and dirty log."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} --- {to_log}")

def build_url(placename: str, search_type: str) -> str:
    """
    Build a url to query the tlcmap/ghap API.

    placename: the place we're trying to locate
    search_type: what search type to use (accepts one of ['contains','fuzzy','exact'])
    """
    safe_placename = urllib.parse.quote(placename.strip().lower())
    if search_type == 'fuzzy':
        url = f"https://tlcmap.org/ghap/search?fuzzyname={safe_placename}&searchausgaz=on&searchpublicdatasets=on&format=json"
    elif search_type == 'exact':
        url = f"https://tlcmap.org/ghap/search?name={safe_placename}&searchausgaz=on&searchpublicdatasets=on&format=json"
    elif search_type == 'contains':
        url = f"https://tlcmap.org/ghap/search?containsname={safe_placename}&searchausgaz=on&searchpublicdatasets=on&format=json"
    else:
        return None
    return url

def query_name(placename: str, search_type: str):
    """
    Use tlcmap/ghap API to check a placename, returning whatever results are found.
    """
    url = build_url(placename, search_type = search_type)
    if url:
        r = requests.get(url)
        log(f"Query returned {r.status_code}")
        if r.ok:
            data = json.loads(r.content)
            return data
    return None

def get_features_from_query_results(query_results):
    """
    docstring
    """
    if query_results:
        return query_results.get('features',[])
    else:
        return None

def query_name_with_fallback(placename: str, search_type_order=['exact','contains','fuzzy']):
    """
    Query API for placename, using search_types in order, and returning first non-null results.
    Note: should mostly return exact, and should almost never need to return fuzzy.
    """
    log(f"Beginning API query for {placename}")
    for search_type in search_type_order:
        log(f"Constructing query for {placename} with {search_type}")
        results = query_name(placename = placename, search_type = search_type)
        if results:
            features = get_features_from_query_results(results)
            log(f"Query returned {len(features)} features")
            break
        else:
            continue
    return results



best_results = query_name_with_fallback('newcastl')
print("done")