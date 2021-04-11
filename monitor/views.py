from django.shortcuts import render
from monitor.models import Server

# Create your views here.
def show(request):
    servers = Server.objects.all()
    return render(request, 'view.html', {'servers': servers})


def showById(request, id):
    server = Server.objects.get(id = int(id))
    return render(request, 'viewById.html', {'server': server})
