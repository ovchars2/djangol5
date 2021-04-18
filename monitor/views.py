from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse
from .models import Server, ServerGroup, Notification
from .forms import ServerForm, NotificationForm
from wsgiref.util import FileWrapper
from fpdf import FPDF
from datetime import datetime
import mimetypes, ast, json

# Create your views here.
def show(request):
    servers = Server.objects.all() if request.user.is_authenticated else []
    return render(request, 'view.html', {'servers': servers})


def showById(request, id):
    if not request.user.is_authenticated:
        return redirect('/')
    server = Server.objects.get(id = int(id))
    return render(request, 'viewById.html', {'server': server})

def createNotification(request):
    if not request.user.is_authenticated:
        return redirect('/')
    form = NotificationForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = NotificationForm()

    return render(request, 'createNotification.html', {'form' : form})

def createServer(request):
    if not request.user.is_authenticated:
        return redirect('/')
    form = ServerForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ServerForm()

    return render(request, 'createServer.html', {'form' : form})

def getPDFReport(request):
    if not request.user.is_authenticated:
        return redirect('/')
    serialized_data = serializers.serialize("json", Notification.objects.all())
    data = ast.literal_eval(serialized_data)
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font(family='Arial', size=12)
    current_time = datetime.now().strftime('%a, %b %d %Y, %H:%M:%S')
    pdf.cell(190, 15, current_time, ln=2)
    pdf.set_font(family='Courier', size=10)
    for d in data:
        type = d['fields']['type']
        server = d['fields']['server']
        time_field = datetime.strptime(d['fields']['time'], '%Y-%m-%dT%H:%M:%SZ')
        time_field_str = time_field.strftime('%a, %b %d %Y, %H:%M:%S')
        pdf.cell(190,6, f"Notification {d['pk']}: type: {type}, server: {server}, time: {time_field_str}", ln=2)
    pdf.output('filetodl.pdf', 'F')

    response = HttpResponse(FileWrapper(open('filetodl.pdf', 'rb')), content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename=filetodl.pdf"
    return response

def getJSONDump(request):
    if not request.user.is_authenticated:
        return redirect('/')
    serialized_server = ast.literal_eval(serializers.serialize("json", Server.objects.all()))
    serialized_server_group = ast.literal_eval(serializers.serialize("json", ServerGroup.objects.all()))
    serialized_notif = ast.literal_eval(serializers.serialize("json", Notification.objects.all()))
    dump = {
        'servers': serialized_server,
        'server_groups': serialized_server_group,
        'notifications': serialized_notif
    }
    dump_file = open('dump_file.json', 'w')
    dump_file.write(json.dumps(dump))
    dump_file.close()
    
    file_to_dl = open('dump_file.json', 'r')
    mime_type, _ = mimetypes.guess_type('dump_file.json')
    response = HttpResponse(file_to_dl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % 'dump_file.json'
    return response