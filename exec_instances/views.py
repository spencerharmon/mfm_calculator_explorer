from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from exec_instances.models import *

from .forms import UploadFileForm
from .parse import Parse, ParseError
from .breadcrumb import *

def exec_instances(request,**kwargs):
    exec_instances = ExecInstance.objects.all()
    breadcrumb = [reverse('exec_instances:exec_instances')]
    return render(
        request,
        'exec_instances/exec_instances.html',{
            'exec_instances': exec_instances,
            'error_message': kwargs['error_message']
            }
        )

def instance_detail(request,**kwargs):
    instance = ExecInstance.objects.filter(title=kwargs['instance_name'].strip('/'))
    if instance.exists():
        instance_id = instance[0].id
        aeps_list = AEPS.objects.filter(exec_instance_id=instance_id)
        url_dict = {
            'Instances': reverse('exec_instances:exec_instances'),
            kwargs['instance_name']: reverse('exec_instances:instance_detail',kwargs={'instance_name':kwargs['instance_name']})
        }
        breadcrumb = Breadcrumb(url_dict=url_dict).gen()
        return render(
            request,
            'exec_instances/instance_detail.html',{
                'aeps_list': aeps_list,
                'instance_name': kwargs['instance_name'],
                'breadcrumb': breadcrumb,
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
    aeps_name = kwargs['aeps_name']
    instance_name = kwargs['instance_name']
    try:
        aeps = AEPS.objects.filter(
            aeps=aeps_name,
            exec_instance=ExecInstance.objects.get(title=instance_name)
        )
        if aeps.exists():
            aeps_id = aeps[0].id
            site_list = Site.objects.filter(aeps_id = aeps_id)
            log_messages = LogMessage.objects.filter(aeps_id = aeps_id)
            url_dict = {
                'Instances': reverse('exec_instances:exec_instances'),
                kwargs['instance_name']: reverse('exec_instances:instance_detail',kwargs={'instance_name':kwargs['instance_name']}),
                kwargs['aeps_name']: reverse('exec_instances:aeps_detail',kwargs={
                    'instance_name':kwargs['instance_name'],
                    'aeps_name': kwargs['aeps_name']
                    }
                )
            }
            breadcrumb = Breadcrumb(url_dict=url_dict).gen()
            return render(
                request,
                'exec_instances/aeps_detail.html',{
                    'site_list': site_list,
                    'instance_name': kwargs['instance_name'],
                    'aeps_name':kwargs['aeps_name'],
                    'log_messages': log_messages,
                    'breadcrumb': breadcrumb,
                    'error_message': kwargs['error_message']
                }
            )
        else:
            error_message = 'Error: aeps \'{0}\' was not found for this instance.'.format(
                kwargs['aeps_name']
            )
            return instance_detail(request,instance_name=instance_name,error_message=error_message)
    except ValueError:
        error_message = 'Error: aeps \'{0}\' was not found for this instance.'.format(
            kwargs['aeps_name']
        )
        return instance_detail(request,instance_name=instance_name,error_message=error_message)

def site_detail(request,**kwargs):
    site = Site.objects.filter(id = kwargs['site_id'])
    if site.exists():
        site = Site.objects.get(id = kwargs['site_id'])
        url_dict = {
            'Instances': reverse('exec_instances:exec_instances'),
            kwargs['instance_name']: reverse('exec_instances:instance_detail',kwargs={'instance_name':kwargs['instance_name']}),
            kwargs['aeps_name']: reverse('exec_instances:aeps_detail',kwargs={
                'instance_name':kwargs['instance_name'],
                'aeps_name': kwargs['aeps_name']
                }
            ),
            (site.x,site.y): reverse('exec_instances:site_detail',kwargs={
                    'instance_name': kwargs['instance_name'],
                    'aeps_name': kwargs['aeps_name'],
                    'site_id': kwargs['site_id']
                }
            )
        }
        breadcrumb = Breadcrumb(url_dict=url_dict).gen()
        return render(
            request,
            'exec_instances/site_detail.html',{
                'instance_name': kwargs['instance_name'],
                'aeps_name': kwargs['aeps_name'],
                'site': site,
                'breadcrumb': breadcrumb,
                'error_message': kwargs['error_message']
            }
        )
    else:
        error_message = 'Error: Site ID \'{0}\' not found.'.format(kwargs['site_id'])
        return aeps_detail(request,aeps_name=kwargs['aeps_name'],instnace_name=kwargs['instance_name'],error_messag=error_message)

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
