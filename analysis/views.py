from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import UploadForm
from .models import Upload
import os
from apriopri.settings import FILE_ROOT
# from .apriopri import Apriopri

# Create your views here.

def index(request):
    return render(request,'analysis/index.html', {'form': UploadForm})

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
        print("Form is not valid! : ", form.cleaned_data)

    print('reached')
    context = {
        'form': form
    }
    return render(request, 'analysis/index.html', context)

def analyze(request, test_id):
    upload = get_object_or_404(Upload, pk=test_id)
    # Apriopri(upload.datafile.path)
    try:
        with open(os.path.join(FILE_ROOT, upload.datafile.path), 'r') as csvfile:
            return render(request, 'analysis/analyze.html', {
        'test_id':test_id,
        'data' : csvfile
        })
    except IOError:
        return render(request, 'analysis/analyze.html', {
    'test_id':test_id,
    'error' : 'Unable to read file'
    })

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