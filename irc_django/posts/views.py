from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from posts.serializers import UserSerializer
from rest_framework.parsers import JSONParser
from .models import Channel, Message
from django.utils import timezone
from rest_framework import permissions
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from posts.serializers import ChannelSerializer, MessageSerializer
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'posts/signup.html', {'form': form})
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if not form.is_valid():
            return HttpResponse("Plz enter valid data in your form")
        form.save()
        return redirect('/login_users')
    else:
        return HttpResponse("unsupported method")


def admin(request):
    if not request.user.is_authenticated:
        return redirect('/login_users')
    elif request.method == "GET":
        return render(request, 'posts/admin.html')
    elif request.method == 'POST':
        channel_name = request.POST['channel']
        name = Channel(name=channel_name)
        name.save()
        return HttpResponse("Channel is created")
    else:
        return HttpResponse("Plz...")


def message(request, channel_id):
    now = timezone.now()
    userid = request.user.id
    user_id = User.objects.filter(pk=userid).get(pk=userid).id
    print(user_id)
    if request.method == 'GET':
        return render(request, 'posts/channel.html')
    if request.method == 'POST':
        messages_ = request.POST['post_message']
        data = Message(message=messages_,creator=User.objects.get(pk=user_id),channel=Channel.objects.get(pk=channel_id),created_at=now)
        data.save()
        return redirect('/messages/{}'.format(channel_id))


def display_message(request, channel_id):
    if not request.user.is_authenticated:
        return redirect('/login_users')
    elif request.user.is_authenticated:
        channels = Channel.objects.all()
        print(channel_id)
        messages = Message.objects.filter(channel=channel_id)
        return render(request, 'posts/channel.html', {'channels': channels,'messages':messages,'channels_id':channel_id,'creator':request.user})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/messages')
        #return HttpResponse("already login")
    elif request.method == 'GET':
        return render(request, 'posts/login.html')
    elif request.method == 'POST':
        username = request.POST['user_name']
        password = request.POST['user_password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if(username == "anurag" and password == "anurag@nitc"):
                    return redirect('/moderator')
                return redirect('/messages/12')
            else:
                return HttpResponse("Your  account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return redirect('/login_users')


def logout_user(request):
    logout(request)
    return redirect("/login_users")


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 2
#     page_size_query_param = 'page_size'
#     max_page_size = 4


class ChannelList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
   # pagination_class = LimitOffsetPagination

    def get(self, request, format=None):
        if request.user.is_superuser:
            channels = Channel.objects.all()
            paginator = Paginator(channels, 2)
            page = request.GET.get('page')
            try:
                channels = paginator.page(page)
            except PageNotAnInteger:
                channels = paginator.page(1)
            except EmptyPage:
                channels = paginator.page(paginator.num_pages)
            serializer = ChannelSerializer(channels, many=True)
            return Response(serializer.data)
        else:
            return Response("Forbidden Access")

    def post(self, request, format=None):
        if request.user.is_superuser:
            print(request.user)
            serializer = ChannelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Only super user can create channel")


class ChannelDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Channel.objects.get(pk=pk)
        except Channel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if request.user.is_superuser:
            channel = self.get_object(pk)
            serializer = ChannelSerializer(channel)
            return Response(serializer.data)
        else:
            return Response("Forbidden Access")

    def patch(self, request, pk, format=None):
        if request.user.is_superuser:
            channel = self.get_object(pk)
            serializer = ChannelSerializer(channel, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Only super user can patch..")

    def delete(self, request, pk, format=None):
        if request.user.is_superuser:
            channel = self.get_object(pk)
            channel.delete()
            return Response("deleted", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Only super user can delete..")


class MessageList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        if request.user.is_superuser:
            channel = Channel.objects.get(pk=pk)
            messages = Message.objects.filter(channel=channel).order_by(id)
            paginator = Paginator(messages, 3)
            page = request.GET.get('page')
            try:
                messages = paginator.page(page)
            except PageNotAnInteger:
                messages = paginator.page(1)
            except EmptyPage:
                messages = paginator.page(paginator.num_pages)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        else:
            channel = Channel.objects.get(pk=pk)
            messages = Message.objects.filter(channel=channel,creator=request.user.id).order_by(id)
            paginator = Paginator(messages, 3)
            page = request.GET.get('page')
            try:
                messages = paginator.page(page)
            except PageNotAnInteger:
                messages = paginator.page(1)
            except EmptyPage:
                messages = paginator.page(paginator.num_pages)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, msg_id):
        try:
            return Message.objects.get(pk=msg_id)
        except Message.DoesNotExist:
            raise Http404

    def get(self, request, pk, msg_id, format=None):
        message = self.get_object(msg_id)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def patch(self, request, pk, msg_id, format=None):
        message = self.get_object(msg_id)
        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, msg_id, format=None):
        message = self.get_object(msg_id)
        message.delete()
        return JsonResponse(
            "Deleted", safe=False, json_dumps_params={'indent': 4})


class UserList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = User.objects.all().order_by('id')
        paginator = Paginator(user, 2)
        page = request.GET.get('page')
        try:
            user = paginator.page(page)
        except PageNotAnInteger:
            user = paginator.page(1)
        except EmptyPage:
            user = paginator.page(paginator.num_pages)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Created Successfully")
        return Response(serializer.errors)


class UserDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        if request.user.is_superuser:
            user.delete()
            return JsonResponse("Deleted", safe=False,json_dumps_params={'indent': 4})
        else:
            return JsonResponse(
                "Enter valid user", safe=False,
                           json_dumps_params={'indent': 4})

    def patch(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data)
        return Response(
            serializer.errors)


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response("Logged out ", status=status.HTTP_200_OK)
