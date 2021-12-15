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

    def get_context_data(self, **kwargs):

        # project name
        project = project_name()

        # categories
        categories = Category.objects.all()
        categories = categories.values_list('category', flat=True)
        categories = list(categories)

        # list of team leaders
        leaders = Leader.objects.all()

        logged_in = self.request.user
        if logged_in.is_team_leader:
            category = logged_in.category
            batch_list = leader_table(logged_in)
        elif logged_in.is_annotator:
            category = logged_in.category
            batch_li = annotator_table(logged_in)

        context = super(HomePageView, self).get_context_data(**kwargs)

        if logged_in.is_team_leader:
            context.update({
                "name": project,
                "category": category,
                "unassigned": batch_list[0],
                "assigned": batch_list[1],
                "attributes": batch_list[2],
                "batches": batch_list[3].count(),
                "assigned2": batch_list[4].count(),
                "awaiting": batch_list[5],
                "awaitingXC": batch_list[5].count(),
                "reviewed_count": batch_list[6].count(),
            })

        elif logged_in.is_admin:
            context.update({
                "name": project,
                "categories": categories,
                "leaders": leaders,
            })

        else:
            context.update({
                "name": project,
                "category": category,
                "anno_assigned": batch_li[3].count(),
                "batch_assign": batch_li[0],
                "awaitingX": batch_li[1],
                "awaitingC": batch_li[1].count(),
                "incompleteX": batch_li[2].count(),
                "reviewed_count": batch_li[6].count(),
                "reviewed": batch_li[6]
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
        logged_in = self.request.user
        user.is_admin = False
        user.is_team_leader = False
        user.is_annotator = True
        user.set_password(f"{random.randint(0, 1000000)}")
        user.category = logged_in.category
        user.save()
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


class VGGImageAnnotator(LoginRequiredMixin, TemplateView):
    template_name = 'via.html'

    def get_context_data(self, **kwargs):
        # project name
        project = project_name()

        logged_in = self.request.user
        category = logged_in.category.category

        if logged_in.is_annotator:
            batch = annotator_table(logged_in)
        elif logged_in.is_team_leader:
            batc = leader_table(logged_in)

        context = super(VGGImageAnnotator, self).get_context_data(**kwargs)

        if logged_in.is_team_leader:
            context.update({
                "name": project,
                "category": category,
                "awaiting": batc[5],
                "attributes": batc[2],
            })
        else:
            context.update({
                "name": project,
                "category": category,
                "assigned": batch[4],
                "incomplete": batch[5],
                "reviewed": batch[6]
            })

        return context

    def post(self, request):
        if request.method == 'POST':
            if request.POST.get('action') == 'attributes':
                filename = request.POST.get('filename')
                file = request.FILES.get('file')

                logged_in = self.request.user.leader
                path = default_storage.save('files/' + filename, file)
                query = Attribute.objects.filter(leader=logged_in)
                if query.exists():
                    query.update(attribute_file=path)
                else:
                    Attribute.objects.create(leader=logged_in, attribute_file=path)
                output = "successful"

            elif request.POST.get('action') == 'load_attributes':
                logged_in = self.request.user
                leader = logged_in.annotator.leader
                file = Attribute.objects.get(leader=leader)
                json_file = file.attribute_file.name
                f = open('uploads/' + json_file, 'r')
                output = json.load(f)

            elif request.POST.get('action') == 'load_file':
                pk = request.POST.get('pk')
                file = Batch.objects.get(pk=pk)
                text_file = file.batch_file.name
                f = open('uploads/' + text_file, 'r')
                data = f.read()
                output = data

            elif request.POST.get('action') == 'save_file':
                filename = request.POST.get('filename')
                file = request.FILES.get('file')
                pk = request.POST.get('pk')
                reviewed = request.POST.get('reviewed')

                path = default_storage.save('files/' + filename, file)
                batch = Batch.objects.filter(pk=pk)

                if reviewed == "none":
                    incomplete = IncompleteBatch.objects.filter(batch=batch.first())

                    if incomplete.exists():
                        incomplete.delete()
                        batch.update(is_annotated=True, annotated_file=path, incomplete_file=False)
                    else:
                        batch.update(is_annotated=True, annotated_file=path)

                else:
                    batch.update(annotated_file=path, is_annotated_twice=True, review=None)

                output = "successful"

            elif request.POST.get('action') == 'save_incomplete_file':
                filename = request.POST.get('filename')
                file = request.FILES.get('file')
                pk = request.POST.get('pk')

                path = default_storage.save('files/' + filename, file)
                batch = Batch.objects.get(pk=pk)
                query = IncompleteBatch.objects.filter(batch=batch)
                if query.exists():
                    query.update(incomplete_file=path)
                else:
                    IncompleteBatch.objects.create(batch=batch, incomplete_file=path)
                    Batch.objects.filter(pk=pk).update(incomplete_file=True)
                output = "successful"

            elif request.POST.get('action') == 'load_incomplete_file':
                pk = request.POST.get('pk')
                file = IncompleteBatch.objects.get(pk=pk)
                json_file = file.incomplete_file.name
                f = open('uploads/' + json_file, 'r')
                json_data = json.load(f)
                output = json_data

            elif request.POST.get('action') == 'load_file_for_review':
                pk = request.POST.get('pk')
                file = Batch.objects.get(pk=pk)
                json_file = file.annotated_file.name
                f = open('uploads/' + json_file, 'r')
                json_data = json.load(f)
                output = json_data

            elif request.POST.get('action') == 'save_feedback':
                blob = request.FILES.get('mydata')
                filename = request.POST.get('filename')
                message = request.POST.get('message')
                annotations = request.POST.get('annotations')
                pk = request.POST.get('pk')

                batch = Batch.objects.filter(pk=pk)
                path = default_storage.save('files/' + filename, blob)
                batch.update(annotated_file=path, review=annotations, comment=message)
                output = "successful"

            # elif request.POST.get('action') == 'load_reviewed_file':
            else:
                pk = request.POST.get('pk')
                file = Batch.objects.get(pk=pk)
                json_file = file.annotated_file.name
                f = open('uploads/' + json_file, 'r')
                json_data = json.load(f)
                output = json_data

            my_context = {
                "upload": output
            }

            return HttpResponse(json.dumps(my_context, indent=4, sort_keys=True, default=str), content_type='application/json')


def project_name():
    project_name = Name.objects.all()
    if project_name.exists():
        project = Name.objects.filter(id=1).get().project_name
    else:
        project = "[ Your Project Name ]"

    return project


def leader_table(user):
    batch = Batch.objects.filter(leader=user.leader)
    batches1 = batch.filter(annotator__isnull=True)
    batches3 = batch.filter(annotator__isnull=False)
    batches2 = batches3.filter(is_annotated=False)
    attributes = Attribute.objects.filter(leader=user.leader).count()
    awaiting = batches3.filter(is_annotated=True, review__isnull=True, incomplete_file=False)
    reviewed = batches3.filter(is_annotated=True, review__isnull=False, incomplete_file=False)

    # print(reviewed)

    batches_list = [batches1, batches2, attributes, batch, batches3, awaiting, reviewed]

    return batches_list


def annotator_table(user):
    batch = Batch.objects.filter(annotator=user.annotator)
    assigned = batch.filter(is_annotated=False)
    awaiting = batch.filter(is_annotated=True, incomplete_file=False, review__isnull=True)
    reviewed = batch.filter(is_annotated=True, incomplete_file=False, review__isnull=False)
    # print(reviewed)
    incomplete = batch.filter(incomplete_file=True)
    via_assigned = batch.filter(is_annotated=False, incomplete_file=False)
    via_incomplete = IncompleteBatch.objects.filter(batch__annotator=user.annotator)

    batch_list = [assigned, awaiting, incomplete, batch, via_assigned, via_incomplete, reviewed]

    return batch_list
