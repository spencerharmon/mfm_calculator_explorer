from django.shortcuts import render
from django.http import HttpResponseRedirect

from exec_instances.models import *

from .forms import UploadFileForm
from .parse import Parse, ParseError


def exec_instances(request,**kwargs):
    exec_instances = ExecInstance.objects.all()
    return render(
        request,
        'exec_instances/exec_instances.html',{
            'exec_instances': exec_instances,
            'error_message': kwargs['error_message']}
        )

def instance_detail(request,**kwargs):
    instance = ExecInstance.objects.filter(title=kwargs['instance_name'].strip('/'))
    if instance.exists():
        instance_id = instance[0].id
        aeps_list = AEPS.objects.filter(exec_instance_id=instance_id)
        return render(
            request,
            'exec_instances/instance_detail.html',{
                'aeps_list': aeps_list,
                'instance_name': kwargs['instance_name'],
                'error_message': kwargs['error_message']
            }
        )
    else:
        error_message = (
            'Error: instance \'{0}\' was not found.',
            'kwargs: {1}'.format(
                instance,
                kwargs
            )
        )
        return exec_instances(request,error_message=error_message)

def aeps_detail(request,**kwargs):
    aeps = AEPS.objects.filter(actual_aeps=kwargs['aeps_name'])
    if aeps.exists():
        aeps_id = aeps[0].id
        site_list = Sites.object.filter(aeps_id = aeps_id)
        log_messages = aeps[0].objects.log_messages_set.all()
        return render(
            request,
            'exec_instances/aeps_detail.html',{
                'site_list': site_list,
                'instance_name': kwargs['instance_name'],
                'aeps_name':kwargs['aeps_name'],
                'error_message': kwargs['error_message']
            }
        )
    else:
        error_message = 'Error: aeps \'{0}\' was not found for this instance.'.format(
            aeps
        )
        return instance_detail(request,instance_name=instance_name,error_message=error_message)

def site_detail(request,**kwargs):
    pass

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST['title']
            file_list = request.FILES.getlist('files')
            try:
                parse = Parse(file_list,title)
            except ParseError as e:
                form = UploadFileForm()
                error_message = 'Error: {0}'.format(e)
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
