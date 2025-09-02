from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from . import forms, models, ping_address


@login_required
def ping_ip_address(request, pk):
    ip_address = models.PC.objects.get(id=pk).ip_address
    result = ping_address.ping(ip_address)
    return render(request, "main/ping_address.html", {"result": result, 'ip_address': ip_address})


def get_ping_data(request):
    ip_address = request.GET.get('ip_address')
    result = ping_address.ping(ip_address)
    data = {
        'result': result,
        'ip_address': ip_address
    }
    return JsonResponse(data)


def get_pc_details(request, pk):
    try:
        pc = models.PC.objects.get(pk=pk)
        data = {
            'id': pc.id,
            'name': pc.name,
            'ip_address': pc.ip_address,
            'status': pc.status,
            'system_condition': pc.system_condition
        }
    except models.PC.DoesNotExist:
        data = {
            'error': 'PC not found'
        }
    return JsonResponse(data)


def verify_pc_name(request):
    name = request.GET.get('name')
    result = models.PC.objects.filter(name=name).exists()
    data = {
        'result': result,
        'name': name
    }
    return JsonResponse(data)


def verify_pc_ip_address(request):
    ip_address = request.GET.get('ip_address')
    result = models.PC.objects.filter(ip_address=ip_address).exists()
    data = {
        'result': result,
        'ip_address': ip_address
    }
    return JsonResponse(data)


@login_required
def add_pc(request):
    if request.method == 'POST':
        form = forms.CreatePCForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('main_app:pc-list'))
    else:
        form = forms.CreatePCForm()

    return render(request,'main/add_pc.html',{'form':form})


@login_required
def add_pc_from_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        ip_address = request.POST.get('ip_address')

        name_exists = models.PC.objects.filter(name=name).exists()
        ip_address_exists = models.PC.objects.filter(ip_address=ip_address).exists()

        if name_exists or ip_address_exists:
            if name_exists:
                messages.error(request, "PC with this name already exists.")
            if ip_address_exists:
                messages.error(request, "PC with this IP address already exists.")
            
            context = {
                "name": name,
                "ip_address": ip_address,
                "pc_list": models.PC.objects.all(),
            }
            return render(request, "main/pc_list.html", context)

        # If no errors, create PC
        models.PC.objects.create(
            name=name,
            ip_address=ip_address,
            status='connected',
            system_condition='active',
        )
        messages.success(request, "PC added successfully.")
        return HttpResponseRedirect(reverse_lazy('main_app:pc-list'))

    # fallback for GET
    context = {
        "pc_list": models.PC.objects.all()
    }
    return render(request, "main/pc_list.html", context)


@login_required
def delete_pc(request, pk):
    models.PC.objects.filter(pk=pk).delete()
    messages.success(request, "PC deleted successfully.")
    return HttpResponseRedirect(reverse_lazy('main_app:pc-list'))


class PCListView(LoginRequiredMixin, FormMixin, ListView):
    model = models.PC
    template_name = "main/pc_list.html"
    context_object_name = "pc_list"
    form_class = forms.CreatePCForm
    success_url = reverse_lazy("main_app:pc-list")
    
    def get_queryset(self):
        qs = super().get_queryset()
        filter_type = self.request.GET.get("filter")

        if filter_type == "repair":
            qs = qs.filter(system_condition='repair')
        return qs.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form" not in context:
            context = {
                "form": self.get_form(),
            }
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        pc_id = request.POST.get("pc_id")
        if pc_id:  # update
            pc = get_object_or_404(models.PC, id=pc_id)
            form = forms.CreatePCForm(request.POST, instance=pc)
        else:  # create
            form = forms.CreatePCForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))
        

class PCDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'main/pc_detail.html'
    
    def get_context_data(self, **kwargs):
        pc = models.PC.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context.update({
            'pc': pc,
        })
        return context
    

class PCUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = forms.UpdatePCForm
    success_message = 'successfully updated!'
    template_name = 'main/update_pc.html'

    def get_success_url(self):
        return reverse_lazy('main_app:pc-detail', kwargs={'pk' : self.object.pk})

    def get_queryset(self, **kwargs):
        return models.PC.objects.filter(pk=self.kwargs['pk'])
