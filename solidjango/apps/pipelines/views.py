from django.http import HttpResponse
from django.template import loader, RequestContext

from django.conf import settings

from utils.adjustment import ConfigurationFromYamlFile, YamlFileEditor
from utils.launcher import Launcher

import os

conf = ConfigurationFromYamlFile(settings.SOLIDA_CONFIG_FILE)
s_conf = conf.get_pipelines_section()


def index(request):
    template = loader.get_template('pipelines/index.html')
    context = dict(pipelines_list=s_conf)
    return HttpResponse(template.render(context, request))


def details(request, pipeline_id):
    template = loader.get_template('pipelines/details.html')
    context = dict(pipeline=s_conf.get(pipeline_id))
    return HttpResponse(template.render(context, request))


def setup(request, pipeline_id):
    template = loader.get_template('pipelines/setup.html')
    req_dict = request.POST.dict()
    del req_dict['csrfmiddlewaretoken']
    launcher = Launcher()
    launcher.create_profile(pipeline=pipeline_id, profile=settings.SOLIDA_PROFILE_NAME)
    editor = YamlFileEditor(os.path.join(settings.SOLIDA_PROFILE_ROOT,
                                         pipeline_id,
                                         settings.SOLIDA_PROFILE_NAME) + '.yaml')
    editor.edit_vars(req_dict)
    profile_conf = editor.get()

    context = dict(pipeline=s_conf.get(pipeline_id), profile=profile_conf, remote=conf.get_remote_section())
    return HttpResponse(template.render(context, request))


def deploy(request, pipeline_id):
    template = loader.get_template('pipelines/deploy.html')
    req_dict = request.POST.dict()
    del req_dict['csrfmiddlewaretoken']
    editor = YamlFileEditor(os.path.join(settings.SOLIDA_PROFILE_ROOT,
                                         pipeline_id,
                                         settings.SOLIDA_PROFILE_NAME) + '.yaml')
    editor.edit_vars(req_dict)
    launcher = Launcher()
    launcher.deploy_project(pipeline=pipeline_id,
                            profile=settings.SOLIDA_PROFILE_NAME,
                            user=req_dict.get('remote_user'),
                            host=req_dict.get('host'),
                            connection=req_dict.get('connection')
                            )
    context = dict(pipeline=s_conf.get(pipeline_id))
    return HttpResponse(template.render(context, request))



