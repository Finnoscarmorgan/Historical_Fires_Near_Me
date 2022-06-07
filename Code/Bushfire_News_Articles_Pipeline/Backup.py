import urllib.parse
import requests
import json
from datetime import datetime
import statistics
import pandas as pd
import os
import time
import math
from fuzzywuzzy import fuzz

def log(to_log: str):
    """"Quick and dirty log."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} --- {to_log}")


def build_url(placename: str, search_type: str, search_public_data: bool = True) -> str:
    """
    Build a url to query the tlcmap/ghap API.
    placename: the place we're trying to locate
    search_type: what search type to use (accepts one of ['contains','fuzzy','exact'])
    """
    safe_placename = urllib.parse.quote(placename.strip().lower())

    if search_type == 'fuzzy':
            url = f"https://tlcmap.org/ghap/search?fuzzyname={safe_placename}&searchausgaz=on&format=json"
        elif search_type == 'exact':
            url = f"https://tlcmap.org/ghap/search?name={safe_placename}&searchausgaz=on&format=json"
        elif search_type == 'contains':
            url = f"https://tlcmap.org/ghap/search?containsname={safe_placename}&searchausgaz=on&format=json"
        else:
            return None
        return url


def query_name(placename: str, search_type: str):
    """
    Use tlcmap/ghap API to check a placename, implemented fuzzy search but will not handle non returns.
    """
    url = build_url(placename, search_type, search_public_data = False)
    if url:
        r = requests.get(url)
        if r.url == 'https://tlcmap.org/ghap/maxpaging':
            return None
        log(f"Query returned {r.status_code}")
        if r.ok:
            """
            NOTE: we could catch json.decoder.JSONDecodeError, but since json=<3.4 doesn't raise this,
                  a generic ValueError is more portable
            See: https://stackoverflow.com/questions/44714046/python3-unable-to-import-jsondecodeerror-from-json-decoder
            """
            try:
                data = json.loads(r.content)
            except ValueError: #Error handling for 0 matches 
                return None
            return data
    return None


def get_features_from_query_results(query_results):
    """
    docstring
    """
    if query_results:
        return query_results.get('features', [])
    else:
        return None


def query_name_with_fallback(placename: str,
                             search_type_order=['exact', 'fuzzy']):  # remove 'contains' from search sequence
    """
    Query API for placename, using search_types in order, and returning first non-null results.
    Note: should mostly return exact, and should almost never need to return fuzzy.
    """
    # eliminate placenames with four or less characters
    if type(placename) == float:
        return None
    if len(placename) <= 4:
        search_type_order = ['exact']

    log(f"Beginning API query for {placename}")
    for search_type in search_type_order:
        log(f"Constructing query for {placename} with {search_type}")
        results = query_name(placename=placename, search_type=search_type)
        if results:
            features = get_features_from_query_results(results)
            log(f"Query returned {len(features)} features")

            results['searchType'] = search_type

            # implement check for fuzzy search, return first result and evaluate Levenstein distance,
            # return result if match ratio is greater than 75%?
            if search_type == 'fuzzy':
                goodMatch = []
                for f in features:
                    ratio = fuzz.ratio(placename.lower(), f['properties']['name'].lower())
                    if ratio >= 90:  # have changed to 90
                        goodMatch.append(f)

                if len(goodMatch) == 0:
                    results = None
                else:
                    results['features'] = goodMatch
            break
        else:
            continue
    return results


def find_state_certainty(best_results: dict, threshold: float):
    """
    Determine the percentage of placenames present in each state
    """
    state_count = []
    
    for f in best_results['features']:
        if 'state' in f['properties']:
            state_count += [f['properties']['state']]

    best_results['n_results'] = len(state_count)

    # Filter out "None" state
    # n_unique = len(set({state: count for state, count in test.items() if state}))

    state_count_uniques = list(set(state_count))
    n_unique = len(state_count_uniques)
    winner = None
    states = {}

    for this_state in state_count_uniques:
        mentions = [i for i, x in enumerate(state_count) if x == this_state]
        percent_total_mentions = len(mentions) / len(state_count) * 100
        states[this_state] = {'raw': len(mentions), 'percentage': percent_total_mentions}

        if percent_total_mentions >= 1 / n_unique * 100 and winner == None:
            candidates = [this_state]
            winner = this_state
            winnerPct = percent_total_mentions
        elif percent_total_mentions >= 1 / n_unique * 100:
            candidates.append(this_state)
            winner = 'Ambiguous'
            winnerPct = float('NaN')

    if winner == None:
        winner = 'No best estimate'

    best_results['states'] = states
    best_results['most_likely_state'] = winner
    best_results['winnerPct'] = winnerPct

    """
    Find the median coordinates of the place name. If there is a clear winner amongst the states, only select entries
    from that state. Otherwise just take the median (for cases where 'multiple sites' are potential winners, these
    coordinates might be very dubious)
    """

    tmpLat = []
    tmpLong = []

    for f in best_results['features']:
        if 'state' in f['properties']:
            if f['properties']['state'] in candidates and type(f['geometry']['coordinates'][0]) is float:
                tmpLat.append(f['geometry']['coordinates'][0])
                tmpLong.append(f['geometry']['coordinates'][1])

    if len(tmpLat) > 0:
        best_results['best_coords'] = [statistics.median(tmpLat), statistics.median(tmpLong)]
        medLatDist = [x - best_results['best_coords'][0] for x in tmpLat]
        medLongDist = [x - best_results['best_coords'][1] for x in tmpLong]
        medDists = []
        for i in range(len(medLatDist)):
            medDists.append(math.sqrt(medLatDist[i] ** 2 + medLongDist[i] ** 2))

        best_results['mean_median_dist'] = statistics.mean(medDists)
        best_results['median_median_dist'] = statistics.median(medDists)
    else:
        best_results['best_coords'] = [float('NaN'), float('NaN')]
        best_results['mean_median_dist'] = float('NaN')
        best_results['median_median_dist'] = float('NaN')

    return best_results

# Establish input and output file
inputfile = '/Users/fiannualamorgan/Documents/GitHub/third_test_input.csv'
outfile = outFile = inputfile.split("/")[-1].split(".")[0] + "output.csv"

data_to_add = pd.read_csv(inputfile)

lats = []
longs = []
finalStates = []
mean_median_distances = []
median_median_distances = []
n_results = []
winnerPct = []
searchType = []
start = time.time()

for i in data_to_add.index:
    df = data_to_add.loc[i, :]

    best_results = query_name_with_fallback(df.iloc[0])

    """
    Adjust the sensitivity of the state certainty by scaling the second input. At 1, it means that to be considered
    the 'winner', a state needs to have more than or equal to the number of places that would be expected by chance.
    So if only VIC and NSW are found, One would need 50% or more of the place names to be considered the actual state
    containing the locality of interest. If four states are found, then one needs more than 25% of the total place names
    to be the winner. Scaling this number to 1.5 would mean those numbers are scaled to 75% and 37.5%, respectively.
    """
    if best_results != None:
        best_results = find_state_certainty(best_results, 1)  # threshold(was 1.5)

        lats.append(best_results['best_coords'][0])
        longs.append(best_results['best_coords'][1])
        finalStates.append(best_results['most_likely_state'])
        mean_median_distances.append(best_results['mean_median_dist'])
        median_median_distances.append(best_results['median_median_dist'])
        n_results.append(best_results['n_results'])
        winnerPct.append(best_results['winnerPct'])
        searchType.append(best_results['searchType'])
    else:
        lats.append(float('NaN'))
        longs.append(float('NaN'))
        finalStates.append('None')
        mean_median_distances.append(float('NaN'))
        median_median_distances.append(float('NaN'))
        n_results.append(0)
        winnerPct.append(float('NaN'))
        searchType.append('None')

data_to_add['Latitude'] = lats
data_to_add['Longitude'] = longs
data_to_add['State'] = finalStates
data_to_add['mean_median_dist'] = mean_median_distances
data_to_add['median_median_dist'] = median_median_distances
data_to_add['n_results'] = n_results
data_to_add['winnerPct'] = winnerPct
data_to_add['searchType'] = searchType

"""
Write to csv
"""
data_to_add.to_csv(outFile, header=True)

end = time.time()
print("Time elapsed | ", round(end - start, 2), "seconds")
print("CSV written")
print('done')