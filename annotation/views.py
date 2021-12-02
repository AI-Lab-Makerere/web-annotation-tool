from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from .models import *
from .forms import *
from django.db.models import F
import random
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    form_class = TeamLeaderModelForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):

        # project name
        project = project_name()

        # categories
        categories = Category.objects.all()
        categories = categories.values_list('category', flat=True)
        categories = list(categories)

        # list of team leaders
        leaders = Leader.objects.all()
        category = 'none'
        batch_list = []

        logged_in = self.request.user
        if logged_in.is_team_leader:
            category = logged_in.category
            batch_list = leader_table(logged_in)

        context = super(HomePageView, self).get_context_data(**kwargs)

        context.update({
            "name": project,
            "categories": categories,
            "leaders": leaders,
            "category": category,
            "unassigned": batch_list[0],
            "assigned": batch_list[1],
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

            elif request.POST.get('action') == 'batch-upload':
                filename = request.POST.get('filename')
                file = request.FILES.get('file')

                logged_in = self.request.user
                path = default_storage.save('files/' + filename + ".txt", file)
                Batch.objects.create(leader=logged_in.leader, batch_name=filename, batch_file=path)

                Leader.objects.filter(user=logged_in).update(batches=F('batches') + 1)

                name = "successful"

            my_context = {
                "upload": name
            }

            return HttpResponse(json.dumps(my_context, indent=4, sort_keys=True, default=str),
                                content_type='application/json')


class LeaderCreateView(LoginRequiredMixin, CreateView):
    template_name = 'leader_create.html'
    form_class = TeamLeaderModelForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_admin = False
        user.is_team_leader = True
        user.is_annotator = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        Leader.objects.create(user=user)
        # sending an email to the team leader
        send_mail(
            subject="Lacuna Annotation Project",
            message="You were added as a Team Leader here is your username \n" + user.username + "\nAccess this link (your app url) to reset your password",
            # you can change this line below to point to the right mail server
            # you can configure the mail server from the settings file config/settings EMAIL_BACKEND=
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        return super(LeaderCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # project name
        project = project_name()

        context = super(LeaderCreateView, self).get_context_data(**kwargs)

        context.update({
            "name": project,
        })

        return context


class AnnotatorCreateView(LoginRequiredMixin, CreateView):
    template_name = 'annotator_create.html'
    form_class = AnnotatorModelForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_admin = False
        user.is_team_leader = False
        user.is_annotator = True
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        logged_in = self.request.user
        Annotator.objects.create(
            user=user,
            leader=logged_in.leader,
        )
        Leader.objects.filter(user=logged_in).update(annotators=F('annotators') + 1)
        send_mail(
            subject="Lacuna Annotation Project",
            message="You were added as an Annotator here is your username \n" + user.username + "\nAccess this link (your app url) to reset your password",
            # you can change this line below to point to the right mail server
            # you can configure the mail server from the settings file config/settings EMAIL_BACKEND=
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        return super(AnnotatorCreateView, self).form_valid(form)


class AssignAnnotatorView(LoginRequiredMixin, FormView):
    template_name = "annotator_assign.html"
    form_class = AssignAnnotatorForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAnnotatorView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request,
        })
        return kwargs

    def form_valid(self, form):
        annotator = form.cleaned_data["annotator"]
        batch = Batch.objects.get(id=self.kwargs["pk"])
        batch.annotator = annotator
        batch.save()
        return super(AssignAnnotatorView, self).form_valid(form)


def project_name():
    project_name = Name.objects.all()
    if project_name.exists():
        project = Name.objects.filter(id=1).get().project_name
    else:
        project = "[ Your Project Name ]"

    return project


def leader_table(user):
    leader = Leader.objects.filter(user=user).first()
    batches1 = Batch.objects.filter(leader=leader).filter(annotator__isnull=True)
    batches2 = Batch.objects.filter(leader=leader).filter(annotator__isnull=False).filter(is_annotated=False)

    batches_list = [batches1, batches2]

    return batches_list
