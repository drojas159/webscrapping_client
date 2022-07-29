from django.shortcuts import render
from django.http import HttpResponse
from .logic.analyze import preprocessing as pp
from .logic.analyze import analyze 

# Create your views here.
def analyze(request):
    return render(request, 'analyze/analyze.html',{})
    #return HttpResponse("Insertado")

def split_words(request):
    try:        
        dataset=pp.main()        
        return render(request, 'analyze/analyze.html',{
            "dataset" : dataset
        })    
    except (Exception) as err:
        print(f"Unexpected {err=}, {type(err)=}")       

def predict_users(request):
    return render(request, 'analyze/predict_users.html',{})    
    """ try:        
        #analyze.predict()        
        
    except (Exception) as err:
        print(f"Unexpected {err=}, {type(err)=}")  """

    