"""Generate Plex Playlists based on most popular from Tatulli
"""
import configparser
import requests
import os

from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer


def get_popular():
    """Get Home Statistics from Tautulli API
    """
    print("Getting popular media")
    stats = requests.get(config['Tautulli']['url'] + '/api/v2?apikey=' +
                        config['Tautulli']['apikey'] + '&cmd=get_home_stats&time_range=' +
                        config['Tautulli']['timerange'] + "&stats_count=" +
                        config['Tautulli']['count'])

    response = stats.json()
    _popular = {}

    for entry in response['response']['data']:
        if entry['stat_id'] == 'popular_movies':
            _popular['movies'] = entry['rows']
        if entry['stat_id'] == 'popular_tv':
            _popular['tv'] = entry['rows']

    return _popular


def clear_collections(movies_library, tv_library):
    """ Clear media items from collections
    """
    print("Clear Collections")
    movies_collection = movies_library.collection()
    for m_collection in movies_collection:
        if m_collection.title == config['Collections']['movies']:
            for movies in m_collection.children:
                print("    Removing %s from %s" % (movies.title, config['Collections']['movies']))
                movies.removeCollection(config['Collections']['movies'])

    tv_collection = tv_library.collection()
    for t_collection in tv_collection:
        if t_collection.title == config['Collections']['tv']:
            for show in t_collection.children:
                print("    Removing %s from %s" % (show.title, config['Collections']['tv']))
                show.removeCollection(config['Collections']['movies'])


def generate_collections(popular_dict, movies_library, tv_library):
    """ Generate collections based on popular items

    Args:
        popular_dict (dict): Popular Movies and TV Dictionary
    """
    current_int = 0
    limit = int(config['Collections']['limit'])

    print("Creating Movie Collection")
    for movie in popular_dict['movies']:
        if current_int < limit:
            _movie = plex.fetchItem(movie['rating_key'])
            if _movie.librarySectionID == movies_library.key:
                _movie.addCollection(config['Collections']['movies'])
                print("    Added %s to %s" % (_movie.title, config['Collections']['movies']))
                current_int += 1
        else:
            print("Movie Collection limit reached")
            break

    print("Creating TV Collection")
    current_int = 0
    for show in popular_dict['tv']:
        if current_int < limit:
            _show = plex.fetchItem(show['rating_key'])
            if _show.librarySectionID == tv_library.key:
                _show.addCollection(config['Collections']['tv'])
                print("    Added %s to %s" % (_show.title, config['Collections']['tv']))
                current_int += 1
        else:
            print("TV Collection limit reached")
            break


if __name__ == '__main__':
    config = configparser.ConfigParser()

    if (os.path.exists('config.ini')):
        config.read('config.ini')
    else:
        config.read(os.path.dirname(__file__) + os.path.sep + 'config.ini')

    # Login to Plex
    if (config['Plex']['url'] != '' and config['Plex']['token'] != ''):
        print("Logging in using token")
        plex = PlexServer(config['Plex']['url'], config['Plex']['token'])
    elif (config['Plex']['username'] != '' and config['Plex']['password'] != ''):
        print("Logging in using username/password")
        account = MyPlexAccount(config['Plex']['username'], config['Plex']['password'])
        if config['Plex']['server'] != '':
            plex = account.resource(config['Plex']['server']).connect()
        else:
            Exception("[Config file invalid] - Missing [Plex] Server")
    else:
        Exception("[Config file invalid] - Failed to login to Plex")

    movies_library = plex.library.section(config['Libraries']['movies'])
    tv_library = plex.library.section(config['Libraries']['tv'])

    clear_collections(movies_library, tv_library)
    popular = get_popular()
    generate_collections(popular, movies_library, tv_library)
