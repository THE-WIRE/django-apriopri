import pandas as pd
import numpy as np
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import UploadForm
from .models import Upload
import os
from apriopri.settings import FILE_ROOT, BASE_DIR
import json

def index(request):
    return render(request,'analysis/index.html')

def login(request):
    return render(request,'analysis/login.html')

def upload(request):
    return render(request,'analysis/upload.html', {'form': UploadForm})

def upload_file(request):
    upload = "Nothing"
    form = UploadForm(request.POST or None, request.FILES or None)
    print(request)
    if form.is_valid():
        print("Form validated", form.cleaned_data)
        upload = form.save(commit=False)
        upload.datafile = request.FILES['datafile']
        if handle_uploaded_file(upload.datafile):
            upload.save()
            return HttpResponseRedirect('/analysis/tests')
    else:
        print("Form is not valid! : ", form)

    print('reached')
    context = {
        'form': form
    }
    return render(request, 'analysis/upload.html', context)

## COMMENTED FOR NEW TEST
# def analyze(request, test_id):
#     upload = get_object_or_404(Upload, pk=test_id)
#     # Apriopri(upload.datafile.path)
#     print(os.path.join(FILE_ROOT, upload.datafile.path))
#     print(upload.datafile.path)
#     try:
#         with open(os.path.join(FILE_ROOT, upload.datafile.path), 'r') as csvfile:
#             return render(request, 'analysis/analyze.html', {
#         'test_id':test_id,
#         'data' : csvfile
#         })
#     except IOError:
#         return render(request, 'analysis/analyze.html', {
#     'test_id':test_id,
#     'error' : 'Unable to read file'
#     })


## HERE IS NEW TEST
def view(request, test_id):
    upload = get_object_or_404(Upload, pk=test_id)

    try:
        datafile = read_file(os.path.join(FILE_ROOT, upload.datafile.path))
        y = np.array(datafile)
        rows = len(y)
        return render(request, 'analysis/view.html', { 'test_id':test_id, 'data' : y[:20], 't_headers': datafile.columns, 'act_rows': rows})
    except IOError:
        return render(request, 'analysis/view.html', {
    'test_id':test_id,
    'error' : 'Unable to read file'
    })

def read_file(file):
    x = pd.read_csv(file)
    return x

def handle_uploaded_file(f):
    print('Uploading file...', f.name)
    try:
        with open(os.path.join(FILE_ROOT, f.name), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    except:
        print("Error occured...!")
        return False
    
    print('File uploaded')
    return True

def list_tests(request):
    uploads = Upload.objects.all()
    return render(request, 'analysis/tests.html', {'tests' : uploads})

def getdata(request, test_id):
    upload = get_object_or_404(Upload, pk=test_id)
    with open(os.path.join(FILE_ROOT, upload.datafile.path) + '.processed_out.json', 'r') as file:
            data = json.loads(file.read())
            return JsonResponse(data, safe=False)
def plot(request, test_id):
    return render(request, 'analysis/plot.html', {'test_id' : test_id})

def plot2(request, test_id):
    return render(request, 'analysis/plot2.html', {'test_id' : test_id})

def plot3(request, test_id):
    return render(request, 'analysis/plot3.html', {'test_id' : test_id})

def analyze(request, test_id, sup=0.01, conf=0.01):
    support = sup
    confidence = conf
    upload = get_object_or_404(Upload, pk=test_id)

    try:
        ## Run apriori algorithm of raw data
        if(os.name == 'nt'):
            command = 'python'
        elif(os.name == 'posix'):
            command = 'python3'
        print(command + ' ' + os.path.join(BASE_DIR, 'aprioris.py') + ' -f json -d , -c '+ confidence +' -s '+ support +' < ' + os.path.join(FILE_ROOT, upload.datafile.path) + ' > ' + upload.datafile.name + '.out.json')
        os.system(command + ' ' + os.path.join(BASE_DIR, 'aprioris.py') + ' -f json -d , -c '+ confidence +' -s '+ support +' < ' + os.path.join(FILE_ROOT, upload.datafile.path) + ' > ' + upload.datafile.name + '.out.json')

        ## Preprocessing of data
        data = []

        with open(os.path.join(FILE_ROOT, upload.datafile.path) + '.out.json', 'r+') as file:
            for line in file:
                x = json.loads(line)
                data.append(x)
        o_data = []

        for d in data:
            for i in d['items']:
                for stats in d['ordered_statistics']:
                    item = {}
                    item['name'] = i
                    item['support'] = d['support']
                    item['before'] = stats['items_base']
                    item['after'] = stats['items_add']
                    item['conf'] = stats['confidence']
                    item['lift'] = stats['lift']
                    o_data.append(item)
                    
        with open(os.path.join(FILE_ROOT, upload.datafile.path) + '.processed_out.json', 'w') as file:
            file.write(json.dumps(o_data))

        ## Display data in tabular format

        data = []
        with open(os.path.join(BASE_DIR, upload.datafile.name + '.out.json')) as f:
            for line in f:
                data.append(json.loads(line.strip('\n')))
        
        return render(request, 'analysis/analyze.html', { 'test_id':test_id, 'data' : data})
    except IOError:
        return render(request, 'analysis/analyze.html', {
    'test_id':test_id,
    'error' : 'Unable to read file'
    })