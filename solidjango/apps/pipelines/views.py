from django.http import HttpResponse
from django.template import loader, RequestContext

from django.views.generic.base import TemplateView

from django.conf import settings

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from utils.adjustment import ConfigurationFromYamlFile, YamlFileEditor
from utils.launcher import Launcher

import os

conf = ConfigurationFromYamlFile(settings.SOLIDA_CONFIG_FILE)
s_conf = conf.get_pipelines_section()


class IndexView(TemplateView):
    template_name = 'pipelines/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        pipelines = [v for k, v in s_conf.items()]
        paginator = Paginator(pipelines, 5)
        page = self.request.GET.get("page")
        try:
            show_pipelines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_pipelines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_pipelines = paginator.page(paginator.num_pages)
        context["pipelines_list"] = show_pipelines
        return context


class DetailsView(TemplateView):
    template_name = 'pipelines/details.html'

    def get_context_data(self, pipeline_id, **kwargs):
        context = super(DetailsView, self).get_context_data(**kwargs)
        context['pipeline'] = s_conf.get(pipeline_id)
        return context


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



