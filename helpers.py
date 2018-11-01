import numpy as np
import requests
import time
from bs4 import BeautifulSoup


def get_tracklist_info(tracklist):
    """ Only keep informations needed from the tracklist
    """

    tracklist_info = []
    
    for track in tracklist:
        artists = [ artists['name'] for artists in track['artists']] if 'artists' in track else ''
        title = track['title']
        duration = track['duration']
        tracklist_info.append( (artists, title, duration) )    
        
    return(tracklist_info)


def get_release_prices(release_url):

    html = requests.get(release_url)

    if html.status_code == 429:
        print('Rate Limiting ! Wait 60 secondes...', end=' ')
        time.sleep(60)
        print('Done!')
        html = requests.get(release_url)

    soup = BeautifulSoup(html.content, 'html.parser')

    # Find a best way, work only with CA$
    currency = 'CHF'
    lowest_price = soup.find(class_='last').find_all('li')[1].text.strip().split(currency)[-1]
    median_price = soup.find(class_='last').find_all('li')[2].text.strip().split(currency)[-1]
    highest_price = soup.find(class_='last').find_all('li')[3].text.strip().split(currency)[-1]

    return float(lowest_price), float(median_price), float(highest_price)



def get_release_info(release, verbose=False):
    """ Get all release informations from a link 
    """

    release_id = release['id']
    master_id = release['master_id'] if 'master_id' in release else np.nan

    artists_info = release["artists"]
    artists = [artists_info[idx]['name'] for idx in range(len(artists_info))]
    title = release['title']

    labels = release["labels"][0]['name']
    genres = release['genres']
    styles = release['styles']
    country = release['country']
    year = release['year']

    medium = release['formats'][0]['name']
    description = release['formats'][0]['descriptions']
    
    rating = release['community']['rating']
    have_want = (release['community']['have'], release['community']['want'])
    num_for_sale = release['num_for_sale']

    tracklist = get_tracklist_info(release["tracklist"])
    nb_track = len(tracklist)

    url = release['uri']

    if len(release['formats']) > 1:
        print('\n\n', url, '\n\n')


    lowest_price, median_price, highest_price = get_release_prices(url)

    
    if verbose:
        print('RELEASE_ID: %s\n' % release_id)
        print('MASTER_ID: %s\n' % master_id)
        
        print('Artists: %s' % artists)
        print('Title:   %s' % title)

        print('Labels:    %s' % labels)
        print('Genres:   %s' % genres)
        print('Styles:   %s' % styles)
        print('Country:  %s' % country)
        print('Year: %s\n' % year)

        print('medium: %s' % medium)
        print('description: %s' % description)

        print('Rating:      %s' % rating)
        print('Have/Want:   %s/%s' % (have_want[0], have_want[1]))
        print('Nb for sale: %s\n' % num_for_sale)
        print('Lowest price:  %f' % lowest_price)
        print('Median price:  %f' % median_price)
        print('Highest price: %f' % highest_price) 

        print('Tracklist (%d tracks):' % nb_track) 
        for track in tracklist:
            print('- %s %s (%s)' % (track[0], track[1], track[2]) )
            
        print('URL: %s' % release['uri'])
            
    return release_id, master_id, artists, title, \
           labels, genres, styles, country, year, \
           medium, description, rating, have_want, \
           num_for_sale, lowest_price,  median_price, \
           highest_price, nb_track, tracklist, url