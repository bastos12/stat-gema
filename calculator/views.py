# noinspection PyInterpreter
from django.shortcuts import render
from rest_framework.views import APIView
import json
from .models import Statistique
from .helpers import (
    TestStatistiques,
    ProcessStatistique
)

class UploadCSV(APIView):

    def get(self, request):
        return render(request, 'upload_csv.html')
    
    def post(self, request):
        csv_file = request.FILES.get('csv_file')
        process = ProcessStatistique(csv_file)
        random_quali, random_quanti, number_modalite,\
            number_quali, number_quanti = process.get_all_number_value_for_test_decision()
        pvalue, normality, test_type, test_name = process.choice_test(
            choice_quali=random_quali,
            choice_quanti=random_quanti,
            number_modalite=number_modalite,
            number_quali=number_quali,
            number_quanti=number_quanti
        )
        result = Statistique(
            test_name=test_name,
            test_type=test_type,
            data=process.create_dict_from_df(process.cleaning_data),
            p_value=pvalue,
            normality=normality,
            description=process.__str__()
        )
        result.save()
        context = {
            'test_name': test_name,
            'test_type': test_type,
            'p_value' : pvalue,
            'normalité': normality,
            'description': process.__str__()
        }
        return render(request, 'upload_csv.html', {'data': json.dumps(context)})
