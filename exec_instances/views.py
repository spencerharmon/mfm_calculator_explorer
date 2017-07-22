from django.shortcuts import render
from django.http import HttpResponseRedirect

from exec_instances.models import ExecInstance

from .forms import UploadFileForm
from .parse import Parse, ParseError

def exec_instances(request):
    pass

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST['title']
            file_list = request.FILES.getlist('files')
            try:
                parse = Parse(file_list,title)
                raise ParseError
            except ParseError as e:
                form = UploadFileForm()
                error_message = e
#                error_message = e
                return render(request, 'exec_instances/upload.html', {'form': form, 'error_message': error_message})
            else:
                redirect_url = parse.redirect_url
                return HttpResponseRedirect(redirect_url)
        else:
            form = UploadFileForm()
            error_message = form.errors
            return render(request, 'exec_instances/upload.html', {'form': form, 'error_message': error_message})
    else:
        form = UploadFileForm()
        return render(request, 'exec_instances/upload.html', {'form': form})
