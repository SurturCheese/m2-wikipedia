from django.shortcuts import render
from prettytable import PrettyTable
import requests

from django.http import HttpResponse

# Create your views here.


def index(request):
    url ='https://covid-api.com/api/reports/total?date='
    wikiRequest = request.GET.get('request')
    print(wikiRequest)
    table = PrettyTable(["Clé", "Valeur"])
    if wikiRequest == '2020-04-15':
        response = requests.get(url+wikiRequest).json()
        # Ajouter les données à la table
        for key, value in response["data"].items():
            table.add_row([key, value])
        # Imprimer la table
        print(table)
    context = {"table": table}
    return render(request,'searchTemplate/index.html',context)
    