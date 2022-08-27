# import msvcrt
import tekore
import time

file_path = "file name.txt"
playlist_name = "playlist name"

client_id = "your client id"
client_secret = "your client secret"
redirect_uri = "https://example.com/spotify-redirect"

try:
    conf = tekore.config_from_file('tekore.cfg', return_refresh=True)
    token = tekore.refresh_user_token(*conf[:2], conf[3])
except FileNotFoundError:
    config = (client_id, client_secret, redirect_uri)
    token = tekore.prompt_for_user_token(*config, scope=tekore.scope.every)

spotify = tekore.Spotify(token)

conf = (client_id, client_secret, redirect_uri, token.refresh_token)
tekore.config_to_file('tekore.cfg', conf)

user_id = spotify.current_user().id

start = time.time()
my_playlist = spotify.playlist_create(user_id=user_id, name=playlist_name)

f = open(file_path, "rt")
content_list = f.readlines()
f.close()

my_file = open(f"program result.txt", 'w')
my_file.write("Title searched\tTitle found\tArtist searched\tArtist found\tAlbum searched\tAlbum found\tState\n")
total_song = len(content_list) - 1
song_number = 1
for result in content_list[1:]:
    song_info = result.split("\t")
    search_query = f"{song_info[0]} {song_info[1]} {song_info[3]}"
    print(f"Searching: {song_number}/{total_song}  {search_query}", end="... ")
    search_result = None
    try:
        search_result = spotify.search(search_query)[0]
        song_uri = [search_result.items[0].uri]
        spotify.playlist_add(my_playlist.id, song_uri)
        print("Found", flush=True)
        my_file.write(f"{song_info[0]}\t{search_result.items[0].name}\t{song_info[1]}\t"
                      f"{search_result.items[0].artists[0].name}\t{song_info[3]}\t"
                      f"{search_result.items[0].album.name}\tFound\n")
    except BaseException:
        print("Not found", flush=True)
        my_file.write(f"{song_info[0]}\tn/a\t{song_info[1]}\tn/a\t{song_info[3]}\tN/a\tNot found\n")
    song_number += 1
my_file.close()
print(f"{(time.time()-start):.2f}")

# print("press anything to quit")
# char = msvcrt.getch()
