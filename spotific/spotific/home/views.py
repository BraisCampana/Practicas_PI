from urllib.request import urlopen
from django.conf import settings
from requests import request
from home.forms import LoginForm, RegisterForm
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from numerize import numerize
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import pandas as pd 
from matplotlib import pyplot as plt
from os.path import exists
import tweepy
import datetime
import wikipedia
from spotipy.oauth2 import SpotifyOAuth
import re
import pytz

### Función Búsqueda canción/artista/álbum
def searchItem(select, title):
    if title and select is not None:
        finalitems={
            'info': []
        }
        items=""
        if select is not None:
            spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
            if select == "Canciones":
                word="track:" + title
                items = spotify.search(word, 10, 0, "track", "ES")['tracks']['items']
            if select == "Artistas":
                word="artist:" + title
                items = spotify.search(word, 10, 0, "artist", "ES")['artists']['items']
            if select == "Albums":
                word="album:" + title
                items = spotify.search(word, 10, 0, "album", "ES")['albums']['items']
            for i in range(len(items)):
                if select == "Canciones" or select == "Albums":
                    artists=[]
                    for j in range(len(items[i]['artists'])):
                        artists.append(items[i]['artists'][j]['name'])
                    values = ', '.join(artists)
                else:
                    values = numerize.numerize(items[i]['followers']["total"])
                finalitems['info'].append({'id': items[i]['id'], 'name': items[i]['name'], 'values': values})
            return finalitems
    else:
        return "Error: Parámetros no especificados"

### Información cancion
def getTrackDetails(id):
    if id is not None:
        track_uri = "spotify:track:"+id
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        try:
            results = spotify.track(track_uri)
        except:
            return "Error: id inválida"
        if results is not None:
            artists=[]
            genres=[]
            for i in range(len(results['artists'])):
                artist_uri = "spotify:artist:"+results['artists'][i]['id']
                artists.append(results['artists'][i]['name'])
                artista = spotify.artist(artist_uri)
                for j in range(len(artista['genres'])):
                    genres.append(artista['genres'][j])
            genres = list(set(genres))
            artist_names = ', '.join(artists)
            genres_names = ', '.join(genres)
            track = {
                'name': results['name'],
                'artists': artist_names,
                'popularity': results['popularity'],
                'duration': str(datetime.timedelta(seconds = round(results['duration_ms']/1000))),
                'album': results['album']['name'],
                'explicit': results['explicit'],
                'genres': genres_names,
                'urls': results['external_urls']['spotify'],
            }
            return track
    else:
        return "Error: id no especificada"

### Información artista
def getArtistDetails(id):
    if id is not None:
        artist_uri = "spotify:artist:"+id
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        try:
            results = spotify.artist(artist_uri)
        except:
            return "Error: id inválida"
        if results is not None:
            artist = {
                'name': results['name'],
                'followers': numerize.numerize(results['followers']['total']),
                'genres': ', '.join(results['genres']),
                'popularity': results['popularity'],
                'url_image': results['images'],
                'urls': results['external_urls']['spotify'],
            }
            return artist
    else:
        return "Error: id no especificada"

### Obtención gráfica artista
def getArtistGraphic(id):
    if id is not None:
        artist_uri = "spotify:artist:"+id
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        try:
            results = spotify.artist_albums(artist_uri, album_type='album')['items']
        except:
            return "Error: id inválida"
        if results:
            albums = []
            years = []
            cache = 0
            for i in range(len(results)):
                albums.append(results[i]['name'])
                checkalbums = list(dict.fromkeys(albums))
                if(((len(checkalbums))+cache) == len(albums)):
                    year = results[i]['release_date'].split('-')[0]
                    years.append(year)
                else:
                    cache+=1
            fig, ax = plt.subplots()
            df = pd.DataFrame({'years': years})
            df['years'].value_counts().sort_index().plot(ax=ax, kind='bar', ylabel='apariciones')
            fig.savefig('/workspace/spotific/images/myplot.png')
        else:
            if exists('/workspace/spotific/images/myplot.png'):
                os.remove('/workspace/spotific/images/myplot.png')
    else:
        return "Error: id no especificada"

### Información álbum
def getAlbumDetails(id):
    if id is not None:
        album_uri = "spotify:album:"+id
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        try:
            results = spotify.album(album_uri)
        except:
            return "Error: id inválida"
        if results is not None:
            popularities = []
            tracks = []
            duration_ms = 0
            artists=[]
            for i in range(len(results['artists'])):
                artists.append(results['artists'][i]['name'])
                artist_names = ', '.join(artists)
            for track in results['tracks']['items']:
                duration_ms += track['duration_ms']
                artists=[]
                for i in range(len(track['artists'])):
                    artists.append(track['artists'][i]['name'])
                values = ', '.join(artists)
                tracks.append({'id': track['id'], 'name': track['name'], 'artists': values})
                popularities.append(spotify.track(track['uri'])['popularity'])
            df = pd.DataFrame({'popularities': popularities})
            album = {
                'name': results['name'],
                'tracks': tracks,
                'total_tracks': results['total_tracks'],
                'duration': str(datetime.timedelta(seconds = round(duration_ms/1000))),
                'popularity': round(df['popularities'].mean(),2),
                'artists': artist_names,
                'release_date': results['release_date'],
                'url_image': results['images'],
                'urls': results['external_urls']['spotify'],
            }
            return album
    else:
        return "Error: id no especificada"

### Función Twittear mi actividad (0 -> canciones, 1 -> artistas, 2 -> albums)
def twittear(name, link, tipo, request):
    if name and link and tipo is not None:
        auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_KEY_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        user = request.user.username
        try:
            now = datetime.datetime.now(pytz.timezone("Europe/Madrid"))
            current_time_hour = now.strftime("%H:%M:%S")
            current_time_day = now.strftime("%d/%m/%Y")
            if(tipo == 0):
                api.update_status("A las "+current_time_hour+" del día "+current_time_day+", el usuario "+user+" vió información de la canción '"+name+"'. Para escucharla puedes acceder a: "+link)
            elif(tipo == 1):
                api.update_status("A las "+current_time_hour+" del día "+current_time_day+", el usuario "+user+" se informó sobre el artista "+name+". Para ver su página de Spotify puedes acceder a: "+link)
            elif(tipo == 2):
                api.update_status("A las "+current_time_hour+" del día "+current_time_day+", el usuario "+user+" vió información del álbum "+name+". Para ver y escuchar sus canciones puedes acceder a "+link)
        except tweepy.TweepyException as e:
            return str(format(e))
        return "Has twitteado tu actividad correctamente."
    else:
        return "Error: campos sin especificar"

### Función Ver último tweet artista
def checktweet(name):
    auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_KEY_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    try:
        search = api.search_users(name, count = 20)
        if search:
            artist = None
            ### Obtenemos el artista según su verificación o, si no está verificado en Twitter, según su número de seguidores
            for i in range(len(search)):
                if i == 0:
                    artist = search[0]
                # print(str(i)+" - Name = "+search[i].name+" | Followers = "+str(search[i].followers_count))
                if search[i].verified == True:
                    artist = search[i]
                    break
                if search[i].followers_count >= artist.followers_count:
                    artist = search[i]
            # print("Choosen - Name = "+artist.name+" | Followers = "+str(artist.followers_count))
            ### Obtiene el ultimo tweet del artista o, en casos más pequeños, el más destacado sobre el artista
            last_tweet = api.user_timeline(user_id = artist.id, count = 10)[0]
            tweet_stats = {
                'id': last_tweet.id,
                'text': last_tweet.text,
                'name': last_tweet.user.name,
                'id_name': last_tweet.user.screen_name,
                'date': str(last_tweet.created_at.date()),
                'time': str(last_tweet.created_at.time()),
            }
            return tweet_stats
        else:
            return "No se ha podido obtener la cuenta de twitter del artista"
    except tweepy.TweepyException as err:
        # print("Tweepy Error: {}".format(e))
        return str(format(err))

### Función para obtener detalles de Wikipedia del Artista
def searchwiki(name):
    try:
        wikipedia.set_lang('es')
        artist = wikipedia.search(name, results=1)
        info = wikipedia.summary(artist, sentences=2, auto_suggest=False)
        if info is not None:
            info = re.sub(r'==.*?==+', '', info)
            info = re.sub(r'\[.*?\]+', '', info)
            info = info.replace('\n', ' ')
        return info
    except:
        return "No se pudo obtener más información del artista"

### Información html canciones
def canciones(request, id_cancion):
    track_info = getTrackDetails(id_cancion)
    message = ""
    if request.method == 'POST':
        if request.POST["twittear"] == "Twittear mi actividad":
            message = twittear(track_info['name'], track_info['urls'], 0, request)
    return render(request, 'home/canciones.html', {'track': track_info, 'message': message})

### Información html artistas
def artistas(request, id_artista):
    artist = getArtistDetails(id_artista)
    message=""
    tweet=""
    wiki=""

    ### Obtener gráfica Pubs / Años
    getArtistGraphic(id_artista)

    ### Obtener imagen de spotify del artista
    image = artist['url_image']
    if image != []:
        artist['url_image'] = artist['url_image'][0]['url']

    ### Posibles métodos POST recibidos
    if request.method == 'POST':
        if request.POST["twittear"] == "Twittear mi actividad":
            message = twittear(artist['name'], artist['urls'], 1, request)
        elif request.POST["twittear"] == "Ver actividad":
            tweet = checktweet(artist['name'])
        elif request.POST["twittear"] == "Más información":
            wiki = searchwiki(artist['name'])

    ### Recibir información adicional de artista
    return render(request, 'home/artistas.html', {'artist': artist, 'message': message, 'tweet': tweet, 'wiki': wiki})

### Información html albums
def albums(request, id_album):
    album = getAlbumDetails(id_album)
    message=""
    image = album['url_image']
    if image != []:
        album['url_image'] = album['url_image'][0]['url']
    if request.method == 'POST':
        if request.POST["twittear"] == "Twittear mi actividad":
            message = twittear(album['name'], album['urls'], 2, request)
    return render(request, 'home/albums.html', {'album': album, 'message': message})

### Registro
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password, email=email)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            registerError = "Hubo algún problema en el formulario."
        return render(request, 'home/register_error.html', {'form': form, 'registerError': registerError})

### Logout
def logout_view(request):
    logout(request)
    return redirect(request.GET['next'])

### Registro html
def registerPage(request):
    signupForm=RegisterForm()
    return render(request, 'home/register.html', {'signup_form': signupForm})

def getProfileDetails():
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-read-private'))
    results = spotify.current_user()

    auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_KEY_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    profile = {
        'country': results['country'],
        'twitter_followers': len(api.get_followers()),
        'twitter_verification': api.verify_credentials().verified,
        'spotify_followers': results['followers']['total'],
        'spotify_category': results['product'],
        'url_image': results['images'][0]['url'],
    }
    return profile

### Profile
def profile(request):
    ## AL CERRAR LA VENTANA DE REDIRECCIÓN SIN LOGUEARTE, QUEDA EL PUERTO OCUPADO??
    profile = getProfileDetails()
    if request.method == 'POST':
        if request.POST["logout"] == "Cerrar sesión":
            logout(request)
            return redirect('/')
    return render(request, 'home/profile.html', {'profile': profile})

### Main

def index(request):
    loginError=""
    if 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            loginError="Usuario o contraseña inválidos."
    loginForm=LoginForm()

    # Búsqueda
    if request.method == "POST":
        selection = request.POST.get('selItem')
        finaltracks = searchItem(selection, request.POST.get('song-formpost'))
    else:
        selection = None
        finaltracks = None

    if request.user.is_authenticated:
        context={
            'user':request.user,'login_form':loginForm,'loginError':loginError, 
            'selection': selection, 'finaltracks': finaltracks,
        }
    else:
        context={'login_form':loginForm,'loginError':loginError}

    return render(request, 'home/index.html', context)


