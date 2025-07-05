from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from . import _graph

# Create your views here.
def hello(request):
    return HttpResponse("Hello World!")

def numero(request, num):
    resp = "<html><body><h1>{}</h1></body></html>".format(num)
    return HttpResponse(resp)

def numberot(request, num):
    tparams = {
        'num_arg': num,
    }

    return render(request, 'numerot.html', tparams)

def info(request):
    values = request.META.items()
    html = []
    for k, v in values:
        html.append("<tr><td>{}</td><td>{}</td></tr>".format(k, v))
    return HttpResponse("<table>{}</table>".format("\n".join(html)))

def sendinfo(request):
    """Renders sendinfo page."""

    assert isinstance(request, HttpRequest)
    if 'nome' in request.POST and 'idade' in request.POST:
        nome = request.POST['nome']
        idade = request.POST['idade']
        if nome and idade:
            return render(
                request,
                'send_results.html',
                {
                    'nome': nome,
                    'idade': idade,
                }
            )
        else:
            return render(
                request,
                'send_info.html',
                {
                    'error': True,
                }
            )
        
    else:
        return render(
            request,
            'send_info.html',
            {
                'error': False,
            }
        )

def imc(request):

    assert isinstance(request, HttpRequest)
    if "peso" in request.POST and "altura" in request.POST:
        peso = request.POST["peso"]
        altura = request.POST["altura"]
        if peso and altura:
            peso = float(peso)
            altura = float(altura)
            imc = peso / (altura ** 2)
            message = ""
            
            if imc < 18.5:
                message = "Abaixo do peso ideal"
            elif 18.5 <= imc < 25:
                message = "Peso normal"
            elif 25 <= imc < 30:
                message = "Excesso de peso"
            elif 30 <= imc < 35:
                message = "Obesidade (grau I)"
            elif 35 <= imc < 40:
                message = "Obesidade (grau II)"
            else:
                message = "Obesidade (grau III)"

            return render(
                request,
                'imc_results.html',
                {
                    'imc': imc,
                    'peso': peso,
                    'altura': altura,
                    'message': message,
                }
            )
        else:
            return render(
                request,
                'imc.html',
                {
                    'error': True,
                }
            )
    else:
        return render(
            request,
            'imc.html',
            {
                'error': False,
            }
        )
    
def search_all_movies(request):
    lista = _graph.query([('?film', 'directed_by', '?director'),
                          ('?film', 'name', '?name')
                          ])
    tparams = {
        'movies': lista,
    }
    return render(request, 'search_all_movies.html', tparams)

