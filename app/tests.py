from lyricsgenius import Genius

def search(query):
    genius = Genius("XXX")
    songs = genius.search_songs(query)
    songs = [song['result'] for song in songs['hits']]
    # select only 'artist_names', 'header_image_thumbnail_url', 'title', 'path'
    songs = [{key: song[key] for key in ['artist_names', 'header_image_thumbnail_url', 'title', 'path', 'id', 'url']} for song in songs]    
    return songs

def get_lyrics(song_url):
    genius = Genius("XXX")
    return genius.lyrics(song_url=song_url)


if __name__ == "__main__":
    song_url = search("Nekfeu Rêve d'avoir des rêves")[0]['url']
    print(get_lyrics(song_url))