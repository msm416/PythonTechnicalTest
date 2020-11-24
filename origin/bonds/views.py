import json
import urllib.request
from urllib.error import HTTPError

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Bond
from .serializers import BondSerializer


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")


class Bonds(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        bonds = Bond.objects.all()
        params = {param.name: self.request.query_params.get(param.name, None) for param in Bond._meta.get_fields() if
                  self.request.query_params.get(param.name, None) != None}

        if bool(dict):
            bonds = bonds.filter(**params)

        serializer = BondSerializer(bonds, many=True)
        return Response(serializer.data)

    def post(self, request):
        legal_name = 'Invalid Name'
        try:
            contents = json.loads(urllib.request.urlopen(
                f"https://leilookup.gleif.org/api/v2/leirecords?lei={request.data['lei']}").read())

            legal_name = contents[0]['Entity']['LegalName']['$']
        except HTTPError as e:
            print(e)
        except:
            print("Couldn't dispatch Legal Name from request.")

        data = request.data.copy()
        data['legal_name'] = legal_name
        serializer = BondSerializer(data=data)
        if serializer.is_valid() and legal_name != 'Invalid Name':
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
