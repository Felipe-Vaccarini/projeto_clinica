from django.conf import settings
from django.db.models.fields.related import ForeignKey, OneToOneField
from django_cpf_cnpj.fields import CPFField
from django.core.validators import RegexValidator
from django.db import models
from medicos.models import Agenda
from django.db.models.fields.related import ForeignKey


class PlanoSaude(models.Model):
    plano = models.CharField(max_length=200, verbose_name="Plano")

    def __str__(self):
        return f'{self.plano}'


class Cliente(models.Model):
    plano = models.ForeignKey(PlanoSaude, on_delete=models.PROTECT, related_name='clientes')
    endlogradouro = models.CharField(max_length=200, verbose_name='Logradouro')
    endbairro = models.CharField(max_length=50, verbose_name='Bairro')
    endcep = models.CharField(max_length=8, verbose_name='CEP')
    endnumero = models.CharField(max_length=4, verbose_name='Número')
    endcomplemento = models.CharField(max_length=100, verbose_name='Complemento', null=True, blank=True)
    endcidade = models.CharField(max_length=100, verbose_name='Cidade')
    enduf = models.CharField(max_length=2, verbose_name='UF')
    nacionalidade = models.CharField(max_length=50, verbose_name='Nacionalidade')




    SEXO = (
        ("MAS", "Maculino"),
        ("FEM", "Feminino")
    )
    
    sexo = models.CharField(max_length=9, choices=SEXO,)
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="O número precisa estar neste formato: \
                        '+99 99 9999-0000'.")

    telefone = models.CharField(verbose_name="Telefone",
                                validators=[phone_regex],
                                max_length=17, null=True, blank=True)
    cpf = CPFField(verbose_name="CPF",
                    max_length=50,
                    unique=True,)
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        verbose_name='Usuário', 
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f'{self.user.name}'
    
class Consulta(models.Model):
    agenda =  OneToOneField(Agenda, on_delete=models.CASCADE, related_name='consulta')
    cliente = ForeignKey(Cliente, on_delete=models.CASCADE, related_name='consulta')
    
    class Meta:
        unique_together = ('agenda', 'cliente')
        
    def __str__(self):
        return f'{self.agenda} - {self.cliente}'
