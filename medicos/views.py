from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Medico, Agenda, Especialidade
from django_weasyprint import WeasyTemplateView
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML

class RelatorioMedicosView(WeasyTemplateView):
    def get(self, request, *args, **kwargs):
        medicos = Medico.objects.order_by('nome').all()
        html_string = render_to_string('medicos/relatorio_medicos.html', {'medicos': medicos})
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/relatorio-medicos.pdf')
        fs = FileSystemStorage('/tmp')

        with fs.open('relatorio-medicos.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="relatorio-medicos.pdf'
        return response



class TestMixinIsAdmin(UserPassesTestMixin):
    def test_func(self):
        is_admin_or_is_staff = self.request.user.is_superuser or \
            self.request.user.is_staff
        return bool(is_admin_or_is_staff)

    def handle_no_permission(self):
        messages.error(
            self.request, "Você não tem permissões!"
        )
        return redirect("accounts:index")

class MedicoCreateView(LoginRequiredMixin, TestMixinIsAdmin, CreateView):

    model = Medico
    login_url = 'accounts:login'
    template_name = 'medicos/cadastro.html'
    fields = ['nome', 'crm', 'especialidade', 'cpf', 'telefone', 'sexo', 'email', 'endlogradouro', 'endbairro',
              'endcep', 'endnumero', 'endcomplemento', 'endcidade', 'enduf', 'nacionalidade', 'foto']
    success_url = reverse_lazy('medicos:medicos_lista')
    
class MedicoListView(ListView):
    
    login_url = 'accounts:login'
    template_name = 'medicos/medicos_list.html'

    def get_queryset(self):
        return Medico.objects.all().order_by('-pk')
    
class EspecialidadeCreateView(LoginRequiredMixin, TestMixinIsAdmin, CreateView):

    model = Especialidade
    login_url = 'accounts:login'
    template_name = 'medicos/cadastro.html'
    fields = ['nome']
    success_url = reverse_lazy('medicos:especialidade_lista')


class EspecialidadeUpdateView(LoginRequiredMixin, TestMixinIsAdmin, UpdateView):
    model = Especialidade
    login_url = 'accounts:login'
    template_name = 'medicos/especialidade_cadastro.html'
    fields = ['nome']
    success_url = reverse_lazy('medicos:especialidade_lista')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EspecialidadeDeleteView(LoginRequiredMixin, TestMixinIsAdmin, DeleteView):
    model = Especialidade
    success_url = reverse_lazy('medicos:especialidade_lista')
    template_name = 'form_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Especialidade excluída com sucesso!")
        return reverse_lazy('medicos:especialidade_lista')


    
class EspecialidadeListView(LoginRequiredMixin, TestMixinIsAdmin, ListView):
    
    login_url = 'accounts:login'
    template_name = 'medicos/especialidade_list.html'

    def get_queryset(self):
        return Especialidade.objects.all().order_by('-pk')


class AgendaCreateView(LoginRequiredMixin, TestMixinIsAdmin, CreateView):

    model = Agenda
    login_url = 'accounts:login'
    template_name = 'medicos/agenda_cadastro.html'
    fields = ['medico', 'dia', 'horario']
    success_url = reverse_lazy('medicos:agenda_lista')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class AgendaUpdateView(LoginRequiredMixin, TestMixinIsAdmin, UpdateView):

    model = Agenda
    login_url = 'accounts:login'
    template_name = 'medicos/agenda_cadastro.html'
    fields = ['medico', 'dia', 'horario']
    success_url = reverse_lazy('medicos:agenda_lista')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class AgendaDeleteView(LoginRequiredMixin, TestMixinIsAdmin, DeleteView):
    model = Agenda
    success_url = reverse_lazy('medicos:agenda_lista')
    template_name = 'form_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Consulta excluída com sucesso!")
        return reverse_lazy('medicos:agenda_lista')


class AgendaListView(LoginRequiredMixin, TestMixinIsAdmin, ListView):
    
    login_url = 'accounts:login'
    template_name = 'medicos/agenda_list.html'

    def get_queryset(self):
        return Agenda.objects.filter().order_by('-pk')

    
medico_cadastro = MedicoCreateView.as_view()
medico_lista = MedicoListView.as_view()
especialidade_cadastro = EspecialidadeCreateView.as_view()
especialidade_atualizar = EspecialidadeUpdateView.as_view()
especialidade_lista = EspecialidadeListView.as_view()
especialidade_deletar = EspecialidadeDeleteView.as_view()
agenda_cadastro = AgendaCreateView.as_view()
agenda_atualizar = AgendaUpdateView.as_view()
agenda_lista = AgendaListView.as_view()
agenda_deletar = AgendaDeleteView.as_view()
relatorio_medicos = RelatorioMedicosView.as_view()
