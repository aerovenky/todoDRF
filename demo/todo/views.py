from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import generics
import simplejson as json
from .models import Label, Note
from .serializers import NoteSerializer, LabelSerializer
# Create your views here.

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getLabels(request):
    '''
    GET -- gives the list of labels for that user
    POST -- Creates a label
    POST DATA
    name : <lable name>
    '''
    if request.method == 'GET':
        mylables = Label.objects.filter(user=request.user).values('id','name')
        return Response(mylables)
    else:
        reqjson = json.loads(request.body)
        name = reqjson.get('name')
        if name:
            this_label = Label.objects.create(user=request.user,name=name)
            return Response({'id':this_label.id, 'name':this_label.name},status=201)
        else:
            return Response({'name': 'not found'},status=400)

@api_view(['GET','POST','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def LabelDetail(request,pk):
    '''
    GET -- to get label details
    POST -- Updates the label
    POST DATA
    name : <lable name>
    DELETE -- TO delete the label
    '''
    label = Label.objects.filter(id=pk).filter(user=request.user).first()
    if label:
        if request.method == 'GET':
            return Response({'id':label.id, 'name':label.name})
        elif request.method == 'POST':
            reqjson = json.loads(request.body)
            name = reqjson.get('name')
            if name:
                label.name = name
                label.save()
                return Response({'id':label.id, 'name':label.name}, status=202)
            else:
                return Response({'name': 'not found'},status=400)
        else:
            label.delete()
            return Response({'message': 'label deleted'})

        return Response({'message':'your post'})
    else:
        return Response({'error':'label not found'},status=404)

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getNotes(request):
    '''
    GET -- gives the list of notes for that user
    POST -- Creates a NOTE
    POSTDATA
    name : <name of note>
    body : <body of note>
    '''
    if request.method == 'GET':
        myNotes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(myNotes, many=True)
        return Response(serializer.data)
    else:
        reqjson = json.loads(request.body)
        name = reqjson.get('name')
        body = reqjson.get('body')
        if name and body:
            this_note = Note.objects.create(name=name,body=body,user=request.user)
            return Response(NoteSerializer(this_note).data, status=201)
        else:
            return Response({'error': 'name or body missing'},status=400)

@api_view(['GET','POST','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def NoteDetail(request,pk):
    '''
    GET -- to get label details
    POST -- Updates the label
    POST DATA

    name : <note name>

    body : <note body>

    DELETE -- TO delete the label
    '''
    note = Note.objects.filter(id=pk).filter(user=request.user).first()
    if note:
        if request.method == 'GET':
            return Response(NoteSerializer(note).data)
        elif request.method == 'POST':
            reqjson = json.loads(request.body)
            name = reqjson.get('name')
            body = reqjson.get('body')
            if name and body:
                note.name = name
                note.body = body
                note.save()
                return Response(NoteSerializer(note).data, status=202)
            else:
                return Response({'error': 'name or body not found'},status=400)
        else:
            note.delete()
            return Response({'message': 'note deleted'})
    else:
        return Response({'error':'note not found'},status=404)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def NoteLabel(request,pk):
    '''
    Note label management
    POST DATA
    add : labelid1,labelid2,labelid3 # adds these labels to this note
    remove : labelid4,labelid5   # removes these labels from this note
    '''
    note = Note.objects.filter(id=pk).filter(user=request.user).first()
    if note:
        reqjson = json.loads(request.body)
        add = reqjson.get('add')
        remove = reqjson.get('remove')
        if add or remove:
            if add:
                print add
                label_ids = add.split(',')
                labels = Label.objects.filter(user=request.user).filter(id__in=label_ids)
                for label in labels:
                    note.labels.add(label)

            if remove:
                label_ids = remove.split(',')
                labels = note.labels.filter(user=request.user).filter(id__in=label_ids)
                for label in labels:
                    note.labels.remove(label)
            return Response(NoteSerializer(note).data, status=202)

        return Response({'error':'add / remove missing'}, status=202)
    else:
        return Response({'error':'note not found'},status=404)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def NoteByLabel(request,label_id):
    '''
    gives list of labels for a label
    '''
    notes = Note.objects.filter(user=request.user).filter(labels__id=label_id)
    return Response(NoteSerializer(notes,many=True).data)
