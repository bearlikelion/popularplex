"""Generate Plex Playlists based on most popular from Tatulli
"""
import configparser
import requests
import plexapi.exceptions

from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer

def get_popular():
    """Get Home Statistics from Tautulli API
    """
    print("Getting popular media")
    stats = requests.get(config['Tautulli']['url'] + '/api/v2?apikey=' +
                        config['Tautulli']['apikey'] + '&cmd=get_home_stats&time_range=' +
                        config['Tautulli']['timerange'])

    response = stats.json()
    _popular = {}

    for entry in response['response']['data']:
        if entry['stat_id'] == 'popular_movies':
            _popular['movies'] = entry['rows']
        if entry['stat_id'] == 'popular_tv':
            _popular['tv'] = entry['rows']

    return _popular


def generate_playlists(popular_dict):
    """Delete and generate popular playlists

    Args:
        popular (dict): Dict of popular Movies and TV from Tautulli API
    """
    try:
        movies_playlist = plex.playlist(config['Playlist']['Movies'])
        if movies_playlist:
            print ("Deleting Movies Playlist")
            movies_playlist.delete()
    except plexapi.exceptions.NotFound:
        pass
    except plexapi.exceptions.BadRequest:
        pass

    try:
        tv_playlist = plex.playlist(config['Playlist']['TV'])
        if tv_playlist:
            print ("Deleting TV Playlist")
            tv_playlist.delete()
    except plexapi.exceptions.NotFound:
        pass
    except plexapi.exceptions.BadRequest:
        pass

    print("Creating Movie Playlist")
    movies = []
    for movie in popular_dict['movies']:
        movies.append(plex.search(movie['title'])[0])
    plex.createPlaylist(config['Playlist']['Movies'], movies)

    print("Creating TV Playlist")
    shows = []
    for show in popular_dict['tv']:
        shows.append(plex.search(show['title'])[0])
    plex.createPlaylist(config['Playlist']['TV'], shows)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

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

    popular = get_popular()
    generate_playlists(popular)
