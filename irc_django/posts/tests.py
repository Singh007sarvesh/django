from django.test import TestCase
from posts.models import Channel, Message
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class UserAPITest(TestCase):
    def setUp(self):
        users = [
            {
                "username": "anurag",
                "password": "anurag@nitc",
                "email": "anurag@gmail.com"
            },
            {
                "username": "lavkush_tiwari",
                "password": "tiwari@all",
                "email": "lav@gmail.com"
            },
        ]
        for user in users:
            user_obj = User.objects.create_user(username=user['username'], password=user['password'],email=user['email'])
            Token.objects.get_or_create(user=user_obj)
        #User.objects.create_superuser(username="anurag123", password="anurag009", email="anurag123@gmail.com")

    def test_user_invalid(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = client.get("/api/users/")
        self.assertEqual(response.status_code, 404)

    def test_userlist(self):

        client = APIClient()
        response = client.post('/api/login/',{'username': 'anurag', 'password': 'anurag@nitc'})
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.data, {'id': 1, 'username': 'anurag'})
        token = Token.objects.get(user=User.objects.get(username="anurag"))
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/api/users', {'username': 'anurag'}, format='json')
        self.assertEqual(response.status_code, 200)
        response = client.post('/api/users/', {'username': 'anurag'}, format='json')
        self.assertEqual(response.status_code, 404)
        response = client.post('/api/users/', {'username': 'anurag'}, format='json')
        self.assertEqual(response.status_code, 404)

    def test_userdetail(self):
        client = APIClient()
        response = client.post('/api/login/',{'username': 'anurag', 'password': 'anurag@nitc'})
        self.assertEqual(response.status_code, 200)
        token = Token.objects.get(user=User.objects.get(username="anurag"))
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/api/users/1/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/api/users/2/')
        self.assertEqual(response.status_code, 200)
        response = client.get('api/users/20/')
        self.assertEqual(response.status_code,404)
        response = client.patch('/api/users/2/', {'username': 'anurag_a'}, format='json')
        self.assertEqual(response.status_code, 200)
        response = client.patch('/api/users/2/', {'username': 'anurag_a'}, format='json')
        self.assertEqual(response.status_code, 200)
        response = client.delete('/api/users/1/', format='json')
        self.assertEqual(response.status_code, 200)
        response = client.delete('/api/users/2/', format='json')
        self.assertEqual(response.status_code, 200)
        response = client.put('/api/users/1/', {'username': 'anurag_a'}, format='json')
        self.assertEqual(response.status_code, 405)


'''class ChannelAPITest(TestCase):
    def setUp(self):
        
        user = User.objects.create_user(username="lavkush_tiwari", email="lav@gmail.com")
        user.set_password('lav@nitc')
        user.save()
        token = Token.objects.get_or_create(user=user)
        superuser = User.objects.create_superuser(username="anurag", password= "anurag@nitc", email="anurag@gmail.com")
        superuser.set_password('anurag@nitc')
        superuser.save()
        supruser_token = Token.objects.get_or_create(user=superuser)




    # def test_user_invalid(self):
    #     client = APIClient()
    #     client.credentials(HTTP_AUTHORIZATION='Token ' + '')
    #     response = client.get("/api/users/")
    #     self.assertEqual(response.status_code, 404)

    def test_channellist(self):
        client = APIClient()
        response = client.post('/api/login/',{'username': 'lavkush_tiwari', 'password': 'lav@nitc'})
        self.assertEqual(response.status_code, 200)
        token = Token.objects.get(user=User.objects.get(username="lavkush_tiwari"))
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/api/channels/')
        if response==None:
            self.assertEqual(response.status_code, 404)
        response = client.post('/api/channels/', {'name': 'xyz'}, format='json')
        if response==None:
            self.assertEqual(response.status_code, 401)
        response = client.get('/api/channel')
        self.assertEqual(response.status_code, 404)
        response = client.post('/api/channels/', {'name':'abc'}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_channeldetail(self):
        client = APIClient()
        response = client.post('/api/login/',{'username': 'lavkush_tiwari', 'password': 'lav@nitc'})
        self.assertEqual(response.status_code, 200)
        token = Token.objects.get(user=User.objects.get(username="lavkush_tiwari"))
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/api/channels/1/')
        if response==None:
            self.assertEqual(response.status_code, 404)
        response = client.get('/api/channels/a/')
        self.assertEqual(response.status_code, 404)
        response = client.get('/api/channel')
        self.assertEqual(response.status_code,404)
        response = client.delete('/api/channels/1/')
        if response==None:
            self.assertEqual(response.status_code, 404)
        response = client.patch('api/channels/1/', {'name':'pqr'}, format='json')
        self.assertEqual(response.status_code,404)
        response = client.patch('api/channels/200/',{'name':'any'}, format='json')
        self.assertEqual(response.status_code, 404)

    def test_channellist_superuser(self):
        client = APIClient()
        response = client.post('/api/login/',{'username': 'anurag', 'password': 'anurag@nitc'})
        self.assertEqual(response.status_code, 200)
        token = Token.objects.get(user=User.objects.get(username="anurag"))
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/api/channels/')
        self.assertEqual(response.status_code, 200)
        response = client.post('/api/channels/', {'name': 'xyz'}, format='json')
        self.assertEqual(response.status_code, 201)
        response = client.post('/api/channels/', {'name': 'amit'}, format='json')
        self.assertEqual(response.status_code, 201)
        response = client.get('/api/channel')
        self.assertEqual(response.status_code, 404)
        response = client.post('/api/channels/', {'name':'abc'}, format='json')
        self.assertEqual(response.status_code, 201)

    def test_channeldetail_superuser(self):
        client = APIClient()
        response = client.post('/api/login/',{'username': 'anurag', 'password': 'anurag@nitc'})
        self.assertEqual(response.status_code, 200)
        import pdb; pdb.set_trace()
        token = Token.objects.get(user=User.objects.get(username="anurag"))
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/api/channels/{}/'.format(1))
        self.assertEqual(response.status_code, 200)
        response = client.get('/api/channels/a/')
        self.assertEqual(response.status_code, 404)
        response = client.get('/api/channel')
        self.assertEqual(response.status_code,404)
        response = client.patch('api/channels/1/', {'name':'pqr'}, format='json')
        self.assertEqual(response.status_code,200)
        response = client.patch('api/channels/200/',{'name':'any'}, format='json')
        self.assertEqual(response.status_code, 404)
        response = client.delete('/api/channels/1/')
        self.assertEqual(response.status_code, 200)
        '''
       
class MessageAPITest(TestCase):
    def setUp(self):
        

        superuser = User.objects.create_superuser(username="anurag", password= "anurag@nitc", email="anurag@gmail.com")
        superuser.set_password('anurag@nitc')
        superuser.save()
        supruser_token = Token.objects.get_or_create(user=superuser)

        user = User.objects.create_user(username="lavkush_tiwari", email="lav@gmail.com")
        user.set_password('lav@nitc')
        user.save()
        token = Token.objects.get_or_create(user=user)
        
    def test_messagelist(self):
        client = APIClient()
        
        # channel = Channel.objects.all()
        # print(channel)
        response = client.post('/api/login/',{'username': 'anurag', 'password': 'anurag@nitc'})
        self.assertEqual(response.status_code, 200)
        import pdb; pdb.set_trace()
        token = Token.objects.get(user=User.objects.get(username="anurag"))
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = client.post('/api/channels/', {'name': 'xyz'}, format='json')
        self.assertEqual(response.status_code, 201)
        response = client.get('/api/logout')
        self.assertEqual(response.status_code,200)

        client = APIClient()
        response = client.post('/api/login/',{'username': 'lavkush_tiwari', 'password': 'lav@nitc'})
        self.assertEqual(response.status_code, 200)
        token = Token.objects.get(user=User.objects.get(username="lavkush_tiwari"))
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        

        response = client.post('/api/channels/1/messages/',{'message':'helloamit','creator':1,'channel': 1,'created_at':'2012-01-01 00:00:00'})
        self.assertEqual(response.status_code,201)
        channel = Channel.objects.first()
        #import pdb; pdb.set_trace()
        #print(channel.id)
        #response = client.get('/api/channels/{}/messages/'.format(channel.id))
        #self.assertEqual(response.status_code, 404)
        response = client.post('/api/channels/1/messages/',{'message':'helloamit','creator':1,'channel':1,'created_at':'2012-01-01 00:00:00'})
        self.assertEqual(response.status_code, 201)

    def test_messagedetail(self):
        client = APIClient()
        response = client.post('/api/login/',{'username': 'lavkush_tiwari', 'password': 'lav@nitc'})
        self.assertEqual(response.status_code, 200)
        token = Token.objects.get(user=User.objects.get(username="lavkush_tiwari"))
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/api/channels/{}/messages/{}/'.format(1,1))
        self.assertEqual(response.status_code, 200)
        response = client.get('/api/channels/1/messages/2/')
        self.assertEqual(response.status_code, 404)
        response = client.patch('api/channels/2/messages/1/',{'message':'hello','creator':'lavkush_tiwari','channel':'1','created_at':'2012-01-01 00:00:00'})
        self.assertEqual(response.status_code,200)
        response = client.delete('/api/channels/1/messages/1/')
        self.assertEqual(response.status_code,200)


class LogoutAPITest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username="lavkush_tiwari", email="lav@gmail.com")
        user.set_password('lav@nitc')
        user.save()
        token = Token.objects.get_or_create(user=user)

    def test_logout(self):
        client = APIClient()
        response = client.post('/api/login/',{'username': 'lavkush_tiwari', 'password': 'lav@nitc'})
        self.assertEqual(response.status_code, 200)
        token = Token.objects.get(user=User.objects.get(username="lavkush_tiwari"))
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/api/logout')
        self.assertEqual(response.status_code,200)
        response = client.get('/api/logout/')
        self.assertEqual(response.status_code,404)