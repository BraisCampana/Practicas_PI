from django.test import TestCase
from django.contrib.auth import models
from urllib3 import HTTPResponse
from home.views import getArtistGraphic, searchItem, getTrackDetails, getArtistDetails, getAlbumDetails, checktweet, searchwiki, twittear, getProfileDetails
from django.conf import settings
from genericpath import exists
import os

# Create your tests here.

class FunctionsTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="test", password="passwordtest", email="test@gmail.com")
    
    def test_created_user(self):
        self.assertIsInstance(self.user, models.User)
        self.assertEqual(self.user.username, "test")
        self.assertFalse(self.user.is_staff)
        self.assertEqual(self.user.password, "passwordtest")
        self.assertEqual(self.user.email, "test@gmail.com")
        pass

    def test_search_item(self):
        search = searchItem('Artistas', None)
        self.assertEquals(search, 'Error: Parámetros no especificados')
        search = searchItem(None, 'Bad')
        self.assertEquals(search, 'Error: Parámetros no especificados')
        search = searchItem('Canciones', 'Nada Fue Un Error')
        self.assertEquals(search['info'][0]['id'], '5QhOF5HXgZ0OFUZSE5kEv1')
        self.assertEquals(search['info'][0]['name'], 'Nada Fue Un Error')
        search = searchItem('Artistas', 'Bad')
        self.assertEquals(search['info'][0]['id'], '4q3ewBCX7sLwd24euuV69X')
        self.assertEquals(search['info'][0]['name'], 'Bad Bunny')
        search = searchItem('Albums', 'verano')
        self.assertEquals(search['info'][0]['id'], '3RQQmkQEvNCY4prGKE6oc5')
        self.assertEquals(search['info'][0]['name'], 'Un Verano Sin Ti')
        search = searchItem('Canciones', 'kadslkfklffkl')
        self.assertEquals(search, {'info': []})
        pass

    def test_track_details(self):
        details = getTrackDetails(None)
        self.assertEquals(details, 'Error: id no especificada')
        details = getTrackDetails('aqnewknlqknflknfk')
        self.assertEquals(details, 'Error: id inválida')
        details = getTrackDetails('5QhOF5HXgZ0OFUZSE5kEv1')
        self.assertEquals(details['name'], 'Nada Fue Un Error')
        self.assertIsNotNone(details['artists'])
        self.assertEquals(details['duration'], '0:03:28')
        self.assertEquals(details['album'], 'Coti')
        self.assertEquals(details['explicit'], False)
        self.assertIsNotNone(details['genres'])
        self.assertEquals(details['urls'], 'https://open.spotify.com/track/5QhOF5HXgZ0OFUZSE5kEv1')
        pass

    def test_artist_details(self):
        details = getArtistDetails(None)
        self.assertEquals(details, 'Error: id no especificada')
        details = getArtistDetails('aqnewknlqknflknfk')
        self.assertEquals(details, 'Error: id inválida')
        details = getArtistDetails('4q3ewBCX7sLwd24euuV69X')
        self.assertEquals(details['name'], 'Bad Bunny')
        self.assertIsNotNone(details['followers'])
        self.assertIsNotNone(details['genres'])
        self.assertIsNotNone(details['popularity'])
        self.assertIsNotNone(details['url_image'])
        self.assertEquals(details['urls'], 'https://open.spotify.com/artist/4q3ewBCX7sLwd24euuV69X')
        pass

    def test_graphic(self):
        if exists('/workspace/spotific/images/myplot.png'):
            os.remove('/workspace/spotific/images/myplot.png')
        result = getArtistGraphic(None)
        self.assertEquals(result, 'Error: id no especificada')
        result = getArtistGraphic('alskdnfkanfk')
        self.assertEquals(result, 'Error: id inválida')
        getArtistGraphic('4q3ewBCX7sLwd24euuV69X')
        self.assertTrue(exists('/workspace/spotific/images/myplot.png'))
        pass

    def test_album_details(self):
        details = getAlbumDetails(None)
        self.assertEquals(details, 'Error: id no especificada')
        details = getAlbumDetails('aqnewknlqknflknfk')
        self.assertEquals(details, 'Error: id inválida')
        details = getAlbumDetails('3RQQmkQEvNCY4prGKE6oc5')
        self.assertEquals(details['name'], 'Un Verano Sin Ti')
        self.assertIsNotNone(details['tracks'])
        self.assertEquals(details['total_tracks'], 23)
        self.assertEquals(details['duration'], '1:21:51')
        self.assertEquals(details['artists'], 'Bad Bunny')
        self.assertEquals(details['release_date'], '2022-05-06')
        self.assertIsNotNone(details['url_image'])
        self.assertEquals(details['urls'], 'https://open.spotify.com/album/3RQQmkQEvNCY4prGKE6oc5')
        pass

    def test_twittear(self):
        tweet = twittear(None, 'https://open.spotify.com/track/71wFwRo8xGc4lrcyKwsvba', 0, self)
        self.assertEquals(tweet, "Error: campos sin especificar")
        tweet = twittear('Callaita', None, 1, self)
        self.assertEquals(tweet, "Error: campos sin especificar")
        tweet = twittear('Callaita', 'https://open.spotify.com/track/71wFwRo8xGc4lrcyKwsvba', None, self)
        self.assertEquals(tweet, "Error: campos sin especificar")
        tweet = twittear('Callaita', 'https://open.spotify.com/track/71wFwRo8xGc4lrcyKwsvba', 0, self)
        self.assertEquals(tweet, "Has twitteado tu actividad correctamente.")
        tweet = twittear('Bad Bunny', 'https://open.spotify.com/artist/4q3ewBCX7sLwd24euuV69X', 1, self)
        self.assertEquals(tweet, "Has twitteado tu actividad correctamente.")
        tweet = twittear('Un Verano Sin Ti', 'https://open.spotify.com/album/3RQQmkQEvNCY4prGKE6oc5', 2, self)
        self.assertEquals(tweet, "Has twitteado tu actividad correctamente.")
        pass

    def test_check_tweet(self):
        tweets = checktweet(None)
        self.assertEquals(tweets, '400 Bad Request\n25 - Query parameters are missing.')
        tweets = checktweet("ksalndfanlankf")
        self.assertEquals(tweets, 'No se ha podido obtener la cuenta de twitter del artista')
        tweets = checktweet("Bad Bunny")
        if 'errors' in tweets.keys():
            # Expired token
            self.assertEquals(tweets['errors'][0]['code'], 89)
        else:
            self.assertIsNotNone(tweets['id'])
            self.assertIsNotNone(tweets['text'])
            self.assertIsNotNone(tweets['name'])
            self.assertIsNotNone(tweets['id_name'])
            self.assertIsNotNone(tweets['date'])
            self.assertIsNotNone(tweets['time'])
        pass

    def test_search_wiki(self):
        info = searchwiki(None)
        self.assertEquals(info, "No se pudo obtener más información del artista")
        info = searchwiki('aklsndakfnlfnask')
        self.assertEquals(info, "No se pudo obtener más información del artista")
        info = searchwiki('Bad Bunny')
        self.assertIsNotNone(info)
        pass
    
    def test_get_profile_details(self):
        result = getProfileDetails()
        self.assertIsNotNone(result['country'])
        self.assertIsNotNone(result['twitter_followers'])
        self.assertIsNotNone(result['twitter_verification'])
        self.assertIsNotNone(result['spotify_followers'])
        self.assertIsNotNone(result['spotify_category'])
        self.assertIsNotNone(result['url_image'])
        pass


