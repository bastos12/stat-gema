from django.shortcuts import render
import pandas as pd
from rest_framework.views import APIView
import json
from .models import Statistique

class UploadCSV(APIView):
    def get(self, request):
        return render(request, 'upload_csv.html')
    
    def post(self, request, format=None):
        csv_file = request.FILES.get('csv_file')
        # implementer votre logique de test
        df = pd.read_csv(csv_file)
        data = df.to_dict('records')
        # exemple de sauvegarde du model
        result = Statistique(
            test_name='test_name',
            test_type='test_type',
            data={'test': 'exemple'},
            p_value=0.04,
            normality=0.03,
            description='Ceci est une description'
        )
        result.save()
        # permet de renvoyer les données aux fronts
        context = {
            'data': data,
            'informations': "Inserer d'autres infos"
        }
        # ne pas changer le rendu
        return render(request, 'upload_csv.html', {'data': json.dumps(context)})
