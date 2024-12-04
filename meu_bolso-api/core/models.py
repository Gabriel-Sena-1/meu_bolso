from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tipo_usuario = models.IntegerField(default=1)
    qtd_grupos = models.IntegerField(default=3)
    ativo = models.BooleanField(default=True)

    # Resolve os conflitos de related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    class Meta:
        db_table = 'usuarios'

class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    usuarios = models.ManyToManyField(
        Usuario,
        through='UsuarioGrupo',
        related_name='grupos'
    )

    class Meta:
        db_table = 'grupos'

    def __str__(self):
        return self.nome

class UsuarioGrupo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'usuario_grupo'
        unique_together = ('usuario', 'grupo')

class Gasto(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.FloatField()
    data = models.DateTimeField(default=timezone.now)
    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.PROTECT,  # Mudamos de RESTRICT para PROTECT
        related_name='gastos'
    )

    class Meta:
        db_table = 'gastos'

class Log(models.Model):
    registro = models.TextField()
    data = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'log'