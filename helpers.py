import numpy as np

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


def get_release_info(release, verbose=False):
    """ Get all release informations from a link 
    """

    release_id = release['id']
    master_id = release['master_id'] if 'master_id' in release else np.nan

    artists_info = release["artists"]
    artists = [artists_info[idx]['name'] for idx in range(len(artists_info))]
    title = release['title']
    format_ = release['formats'][0]['name']
    # format_ = release['formats'][0]['descriptions']
    
    # labels_info = release["labels"]
    # labels = [labels_info[idx]['name'] for idx in range(len(labels_info))]
    # labels = [labels_info[idx]['name'] for idx in range(len(labels_info))]
    labels = release["labels"][0]['name']
    genres = release['genres']
    styles = release['styles']
    country = release['country']
    year = release['year']
    
    rating = release['community']['rating']
    have_want = (release['community']['have'], release['community']['want'])
    num_for_sale = release['num_for_sale']

    tracklist = get_tracklist_info(release["tracklist"])
    nb_track = len(tracklist)


    url = release['uri']
    
    if verbose:
        print('RELEASE_ID: %s\n' % release_id)
        print('MASTER_ID: %s\n' % master_id)
        
        print('Artists: %s' % artists)
        print('Title:   %s' % title)
        print('Format:  %s\n' % support)
        #print('Format:  %s\n' % format_)

        print('Labels:    %s' % labels)
        print('Genres:   %s' % genres)
        print('Styles:   %s' % styles)
        print('Country:  %s' % country)
        print('year: %s\n' % year)

        print('Rating:      %s' % rating)
        print('Have/Want:   %s/%s' % (have_want[0], have_want[1]))
        print('Nb for sale: %s\n' % num_for_sale)

        print('Tracklist (%d tracks):' % nb_tracks) 
        for track in tracklist:
            print('- %s %s (%s)' % (track[0], track[1], track[2]) )
            
        print('URL: %s' % release['uri'])
            
    return release_id, master_id, artists, title, format_, \
           labels, genres, styles, country, year, \
           rating, have_want, num_for_sale, nb_tracks, tracklist, url