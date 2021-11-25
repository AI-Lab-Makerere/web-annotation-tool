from django.http import HttpResponse
from django.shortcuts import render
import json
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class AdminPageView(LoginRequiredMixin, CreateView):
    template_name = 'home.html'
    form_class = TeamLeaderModelForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):

        # project name
        project_name = Name.objects.all()
        if project_name.exists():
            project = Name.objects.filter(id=1).get().project_name
        else:
            project = "[ Your Project Name ]"

        # categories
        categories = Category.objects.all()
        categories = categories.values_list('category', flat=True)
        categories = list(categories)

        context = super(AdminPageView, self).get_context_data(**kwargs)

        context.update({
            "name": project,
            "categories": categories,
        })

        return context

    def post(self, request):

        if request.method == 'POST':
            if request.POST.get('action') == 'project_name':
                name = request.POST.get('name')

                project_name = Name.objects.all()
                if project_name.exists():
                    Name.objects.filter(id=1).update(project_name=name)
                else:
                    Name.objects.create(project_name=name)

            elif request.POST.get('action') == 'category_name':
                category = request.POST.get('category')
                Category.objects.create(category=category)

                categories = Category.objects.all()
                categories = categories.values_list('category', flat=True)
                name = list(categories)

            my_context = {
                "upload": name
            }

            return HttpResponse(json.dumps(my_context, indent=4, sort_keys=True, default=str),
                                content_type='application/json')
