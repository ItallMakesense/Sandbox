from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import (TemplateView, ListView,
    DetailView, CreateView)

from .models import Outlet
from .forms import OutletCreateForm


class HomeView(TemplateView):

    template_name = 'home.html'

    def get_context_data(self, *a, **kw):
        context = super().get_context_data(*a, **kw)
        context.update({
            'header': "Gather some stuff in here",
            'overview': "Powered by NoobForce"
            })
        return context

class OutletListView(ListView):

    def get_queryset(self):
        category = self.kwargs.get('category')
        if category:
            queryset = Outlet.objects.filter(category=category)
        else:
            queryset = Outlet.objects.all()
        return queryset

class OutletDetailView(DetailView):

    queryset = Outlet.objects.all()

    # def get_object(self, *a, **kw):
    #     obj = get_object_or_404(Outlet, id=self.kwargs.get('id'))
    #     return obj

class OutletCreateView(CreateView):

    form_class = OutletCreateForm
    template_name = 'outlets/form.html'
    success_url = '/outlets/'

# def outlet_create_view(request):
#     template_name = 'outlets/form.html'
#     form = OutletCreateForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         # obj = Outlet.objects.create(
#         #     name=form.cleaned_data.get('name'),
#         #     address=form.cleaned_data.get('address'),
#         #     category=form.cleaned_data.get('category')
#         #     )
#         form.save()
#         return HttpResponseRedirect('/outlets/')
#     errors = form.errors if form.errors else None
#     context = {'form': form, 'errors': errors}
#     return render(request, template_name, context)

# class SearchOutletListView(OutletListView):
#     def get_queryset(self):
#         return Outlet.objects.filter(category=self.kwargs['category'])

# class RetailOutletListView(OutletListView):
#     queryset = Outlet.objects.filter(category='retail')

# def outlets_list_view(request):
#     template_name = 'outlets/outlets_list.html'
#     queryset = Outlet.objects.all()
#     context = {
#         'object_list': queryset
#     }
#     return render(request, template_name, context)

# class ContactView(View):
#     def get(self, request, *a, **kw):
#         context = {}
#         return render(request, 'contact.html', context)

# def home(request):
#     context = {
#         'header': "This site brings toys lookup in Minsk, Belarus",
#         'overview': "Powered by NoobForce"
#         }
#     return render(request, 'home.html', context)
