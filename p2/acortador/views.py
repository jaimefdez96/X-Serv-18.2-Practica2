from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Url

FORMULARIO = """
<form action = "" method = "POST">   
Introduzca la URL que desee acortar:<br>
<input type = "text" name = "url" required><br>   
<input type = "submit" value = "Acortar"> 
</form>
"""

# Create your views here.
def principal():
    titulo = '<h1> Acortador de Urls 2.0 </h1>'
    return(titulo + FORMULARIO)

def add_http(url):
    if (url.startswith('http://')) or (url.startswith('https://')):
        return url
    else:
        url = ('http://') + url
        return url

@csrf_exempt
def inicio(request):
    if request.method == 'GET':
        lista = Url.objects.all()
        respuesta = 'Lista de urls acortadas: '
        respuesta += '<ul>'
        for elemento in lista:
            respuesta += '<li><a href=' + str(elemento.id) + '>' + elemento.nombre + '</a>'
        respuesta += '</ul>'
        respuesta = principal() + respuesta
        return HttpResponse(respuesta)
    elif request.method == 'POST':
        url = request.POST['url'] 
        url = add_http(url)
        try: 
            Url.objects.get(nombre=url)
            return HttpResponse('<h1>Url ya acortada</h1>')
        except Url.DoesNotExist:
            url_new = Url(nombre = url)
            url_new.save()
            respuesta = '<ul><li><a href=' + str(url_new.id) + '>' + url_new.nombre + '</a></ul>'
            return HttpResponse(respuesta)
    else:
        return HttpResponse('<h1>405 Method Not Allowed</h1>')


def redirigir(request,numero):
    if request.method == 'GET':
        try:
            url_redirect = Url.objects.get(id=str(numero))
            url_redirect = url_redirect.nombre
            return redirect(url_redirect)
        except Url.DoesNotExist:
            return HttpResponse('<h1>El recurso pedido no se encuentra en la base de datos<h1>')
    else:
        return HttpResponse('<h1>405 Method Not Allowed</h1>')

def error(request):
    return HttpResponse('<h1>404 Not Found</h1>')
