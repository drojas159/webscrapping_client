from django.shortcuts import render
from django.http import HttpResponse
from .logic.analyze import preprocessing as pp

# Create your views here.
def analyze(request):
    return render(request, 'analyze/analyze.html',{})
    #return HttpResponse("Insertado")

def split_words(request):
    try:        
        pp.main()
    except (Exception) as err:
        print(f"Unexpected {err=}, {type(err)=}")       

    return render(request, 'analyze/analyze.html',{})