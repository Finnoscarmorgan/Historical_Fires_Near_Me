import urllib.parse
from pandas.core.reshape.reshape import stack_multiple
import requests
import json
from datetime import datetime
import statistics
import pandas as pd
import os


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
    if len(placename) <= 4:
       search_type_order=['exact']
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

def find_state_certainty(best_results: dict,threshold: float):
    """
    Determine the percentage of placenames present in each state
    """
    state_count=[]
    for f in best_results['features']:
        state_count += [f['properties']['state']]

    state_count_uniques = list(set(state_count))
    n_unique = len(state_count_uniques)
    winner = None
    states={}

    for this_state in state_count_uniques:
        mentions=[i for i, x in enumerate(state_count) if x == this_state]
        percent_total_mentions=len(mentions)/len(state_count)*100
        states[this_state]={'raw':len(mentions),'percentage':percent_total_mentions}

        if percent_total_mentions >= 1 / n_unique * 100 * threshold and winner == None:
            winner=this_state
        elif percent_total_mentions >= 1 / n_unique * 100 * threshold:
            winner='Ambiguous'

    if winner==None:
        winner='Multiple sites'

    best_results['states']=states
    best_results['most_likely_state']=winner

    """
    Find the median coordinates of the place name. If there is a clear winner amongst the states, only select entries 
    from that state. Otherwise just take the median (for cases where 'multiple sites' are potential winners, these
    coordinates might be very dubious)
    """

    tmpLat=[]
    tmpLong=[]
    if winner != None and winner != 'Multiple sites':
        for f in best_results['features']:
            if f['properties']['state'] == winner and type(f['geometry']['coordinates'][0]) is float:
                tmpLat.append(f['geometry']['coordinates'][0])
                tmpLong.append(f['geometry']['coordinates'][1])
        
        if len(tmpLat) > 0:
            best_results['best_coords']=[statistics.median(tmpLat),statistics.median(tmpLong)]
        else:
            best_results['best_coords']=[0,0]

    elif winner =='Multiple sites' and type(f['geometry']['coordinates'][0]) is float:
        for f in best_results['features']: 
            tmpLat.append(f['geometry']['coordinates'][0])
            tmpLong.append(f['geometry']['coordinates'][1])
        
        if len(tmpLat) > 0:
            best_results['best_coords']=[statistics.median(tmpLat),statistics.median(tmpLong)]
        else:
            best_results['best_coords']=[0,0]

    return best_results

"""
Establish input and output file
"""

inputfile = '/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/Sections/Bushfire_News_Articles_19th_Century/Transformed_Data/Geocoded_LOCATION_Mappify_API/Output/2543_failed.csv'
outfile = outFile = inputfile.split("/")[-1].split(".")[0] + "_output.csv"

data_to_add = pd.read_csv(inputfile)

lats=[]
longs=[]
finalStates=[]

for i in data_to_add.index:
    df = data_to_add.loc[i,:]

    best_results = query_name_with_fallback(df.iloc[0])

    # Adjust the sensitivity of the state certainty by scaling the second input. At 1, it means that to be considered 
    # the 'winner', a state needs to have more than or equal to the number of places that would be expected by chance.
    # So if only VIC and NSW are found, One would need 50% or more of the place names to be considered the actual state 
    # containing the locality of interest. If four states are found, then one needs more than 25% of the total place names
    # to be the winner. Scaling this number to 1.5 would mean those numbers are scaled to 75% and 37.5%, respectively.
    if best_results != None:
        best_results = find_state_certainty(best_results,1.5)
        lats.append(best_results['best_coords'][0])
        longs.append(best_results['best_coords'][1])
        finalStates.append(best_results['most_likely_state'])
    else:
        lats.append(0)
        longs.append(0)
        finalStates.append('None')

data_to_add['Latitude']=lats
data_to_add['Longitude']=longs
data_to_add['State']=finalStates

"""
Write to csv
"""
data_to_add.to_csv(outFile,header = True)

print('done')
