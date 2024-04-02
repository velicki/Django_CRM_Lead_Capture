from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from crm.models import Lead
from .serializers import LeadSerializers

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def getData(request):
    leads = Lead.objects.filter(user=request.user)
    serializer = LeadSerializers(leads, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addLead(request):
    serializer = LeadSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def updateLead(request, pk):
    leads = Lead.objects.filter(user=request.user)
    leads = leads.get(id=pk)
    
    if request.method == 'GET':
        serializer = LeadSerializers(leads)
        return Response(serializer.data)


    elif request.method == 'PUT':
        serializer = LeadSerializers(leads, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        leads.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


