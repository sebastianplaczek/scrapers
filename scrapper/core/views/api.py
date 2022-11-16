from django.shortcuts import render, HttpResponse

from core.models import LinksToScrap,UsersLinks
from core.serializers import LinksSerializer,UserLinkSerializer,LinkNestedSerializer,UserSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status,viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User

from django.core import serializers as s


services_list = ['www.reserved.com']



class LinksToScrapList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    # def get(self,request):
    #     user = User.objects.get(id=request.data['user_id'])
    #     #user_links = UsersLinks.objects.filter(user=user)
    #     user_links = UsersLinks.objects.filter(user=user).select_related('linktoscrap')\
    #         .values_list('linktoscrap__link','linktoscrap__item_name','create_date')
    #     user_links = s.serialize('json',user_links)
    #     #serializer = LinksSerializer(linkstoscrap,many=True)
    #     return HttpResponse(user_links,content_type='application/json')
    #     #return Response(user_links)
    #     #return Response(serializer.data)

    def get(self,request):
        user = User.objects.get(id=request.data['user_id'])
        user_links = UsersLinks.objects.filter(user=user,active=1)
        serialized = LinkNestedSerializer(user_links,many=True)
        return Response(serialized.data)



    def post(self,request):
        service = None
        for _ in services_list:
            if _ in request.data['link']:
                service = _

        if service == None:
            return Response('Unknown service',status=status.HTTP_400_BAD_REQUEST)


        db_link = LinksToScrap.objects.filter(link=request.data['link'],active=1)
        if db_link.exists():
            link_id = db_link[0].id
        else:

            link_serializer = LinksSerializer(data={
                'link' : request.data['link'],
                'service' : service,
                'active' : 1
            })

            if link_serializer.is_valid():
                saved_link = link_serializer.save()
                link_id = saved_link.id

        link = LinksToScrap.objects.get(id=link_id)
        user = User.objects.get(id=request.data['user_id'])
        db_user_link = UsersLinks.objects.filter(user=user,active=1,linktoscrap=link)

        if db_user_link.exists():
            return Response('User have this link already', status=status.HTTP_400_BAD_REQUEST)
        else:

            user_link_serializer = UserLinkSerializer(data={
                'user': request.data['user_id'],
                'linktoscrap': saved_link.id,
                'active': 1
            })
            if user_link_serializer.is_valid():
                user_link_serializer.save()
                return Response(link_serializer.data,status=status.HTTP_201_CREATED)
        return Response(link_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset= User.objects.all()
    serializer_class = UserSerializer()



