import json
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

def query_dict_to_json(query):
    json_data = {}
    for dat in query:
        json_data[dat] = json.loads(query[dat])
    return json_data

class GetNote(generics.RetrieveAPIView):
    serializer_class = NoteSerializer
    def get_object(self,*args,**kwargs):
        note = Note.objects.filter(uid=self.kwargs['uid'], is_viewed=False)
        if note.exists():
            note_obj = note[0]
            if not note_obj.is_forever:
                note_obj.is_viewed = True
                note_obj.save()
            return note_obj
        else:
            return None

class Save(APIView):
    def post(self,request):
        note = Note.objects.create(
            uid=request.data['uid'],
            text=request.data['text']
        )
        if request.FILES.getlist('files'):
            for file in request.FILES.getlist('files'):
                Image.objects.create(note=note,file=file)
        return Response(status=200)


class Upadate(APIView):
    def post(self,request):
        note = Note.objects.get(uid=request.data['uid'])
        note.wallet = request.data['wallet']
        note.twitter = request.data['twitter']
        note.save()
        return Response(status=200)


class DaoRequestView(APIView):
    def post(self, request):
        data = request.data
        print(request.FILES.getlist('file'))
        result = {'status':True}

        try:
            code = DaoCode.objects.get(code=data['code'],is_used=False)
            # code.is_used = True
            # code.save()
            obj = DaoRequest.objects.create(code=code,twitter=data['twitter'],dao_twitter=data['dao_twitter'])
            if request.FILES.getlist('file'):
                obj.file = request.FILES['file']
                obj.save()
        except:
            result = {'status': False}


        return Response(result, status=200)

class Fill(APIView):

    def get(self,request):
        from openpyxl import load_workbook
        wb = load_workbook(filename='gen3.xlsx')
        sheet_obj = wb.active
        max_row = sheet_obj.max_row
        x=0
        for i in range(2, max_row+1):
            uid = sheet_obj.cell(row=i, column=1).value
            text = sheet_obj.cell(row=i, column=2).value
            #only_twitter = sheet_obj.cell(row=i, column=3).value
            if uid:
                Note.objects.create(uid=uid,text=text,only_twitter=True,is_wl=True)
                x+=1
        print(x)
        return Response(status=200)