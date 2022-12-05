from datetime import date
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db.models.fields.related import ForeignKey
from django_cpf_cnpj.fields import CPFField


class Especialidade(models.Model):
    nome = models.CharField(verbose_name="Nome", max_length=200)
    
    def __str__(self):
        return f'{self.nome}'

    
class Medico(models.Model):
    nome = models.CharField(verbose_name="Nome", max_length=200)
    crm = models.CharField(verbose_name="CRM", max_length=200)
    especialidade = ForeignKey(Especialidade,
                               on_delete=models.CASCADE,
                               related_name='medicos')
    cpf = CPFField(verbose_name="CPF",
                   max_length=50,
                   unique=True, )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="O número precisa estar neste formato: \
                       '+99 99 9999-0000'.")

    telefone = models.CharField(verbose_name="Telefone",
                                validators=[phone_regex],
                                max_length=17, null=True, blank=True)
    SEXO = (
        ("MAS", "Maculino"),
        ("FEM", "Feminino")
    )

    sexo = models.CharField(max_length=9, choices=SEXO, )
    email = models.EmailField(verbose_name="Email")
    endlogradouro = models.CharField(max_length=200, verbose_name='Logradouro')
    endbairro = models.CharField(max_length=50, verbose_name='Bairro')
    endcep = models.CharField(max_length=8, verbose_name='CEP')
    endnumero = models.CharField(max_length=4, verbose_name='Número')
    endcomplemento = models.CharField(max_length=100, verbose_name='Complemento', null=True, blank=True)
    endcidade = models.CharField(max_length=100, verbose_name='Cidade')
    enduf = models.CharField(max_length=2, verbose_name='UF')
    nacionalidade = models.CharField(max_length=50, verbose_name='Nacionalidade')
    foto = models.ImageField(upload_to='foto/')
    
    def __str__(self):
        return f'{self.nome}'



def validar_dia(value):
    today = date.today()
    weekday = date.fromisoformat(f'{value}').weekday()

    if value < today:
        raise ValidationError('Não é possivel escolher um data atrasada.')
    if (weekday == 5) or (weekday == 6):
        raise ValidationError('Escolha um dia útil da semana.')

class Agenda(models.Model):
    medico = ForeignKey(Medico, on_delete=models.CASCADE, related_name='agenda')
    dia = models.DateField(help_text="Insira uma data para agenda", validators=[validar_dia])
    
    HORARIOS = (
        ("1", "07:00 ás 08:00"),
        ("2", "08:00 ás 09:00"),
        ("3", "09:00 ás 10:00"),
        ("4", "10:00 ás 11:00"),
        ("5", "11:00 ás 12:00"),
    )
    horario = models.CharField(max_length=10, choices=HORARIOS)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name='Usuário', 
        on_delete=models.CASCADE
    )
    class Meta:
        unique_together = ('horario', 'dia')
        
    def __str__(self):
        return f'{self.dia.strftime("%b %d %Y")} - {self.get_horario_display()} - {self.medico}'
