from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from .forms import CadastroRestauranteForm, ColaboradorForm, LoginForm, User, CadastroHotelForm, Hotel, CadastroObraForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Profile, Restaurante,Colaborador, Obra
from django.contrib.auth.models import Group,User
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.decorators import user_passes_test
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
import logging
from django.apps import apps
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from Sistema.utils.mongo.mongo_model import ControleRefeicoes
from bson import ObjectId
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required

pedido_model = ControleRefeicoes()


@api_view(['GET'])
def minha_api(request):
    if request.user.groups.filter(name='Encarregado').exists():
        raise PermissionDenied("Encarregados não podem acessar esta API.")
    return Response({"data": "Dados sensíveis"})

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@api_view(['POST'])
@user_passes_test(is_admin)
def criar_usuario(request):
    # (apenas Admin pode acessar)
    return Response({"message": "Usuário criado com sucesso!"})


def login(request):
    if request.user.id is not None:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect('home')
        context = {'acesso negado': True}
        return render (request, 'login.html', {'form': form})
    return render(request, 'login.html', {'form': LoginForm()})

@csrf_protect
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return render(request, 'logout.html')  # ou redirect('login')
    return redirect('home')  # se acessar via GET, redireciona



@login_required
def home(request):
    return render (request, 'home.html')

@login_required
def lista_colaboradores(request):
    colaboradores = Colaborador.objects.all()  # Ou sua queryset personalizada
    return render(request, 'listar-colaboradores.html', {'colaboradores': colaboradores}) 

@login_required
def editar_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, pk=id)
    
    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador atualizado com sucesso!')
            return redirect('listar-colaboradores')
    else:
        form = ColaboradorForm(instance=colaborador)
    
    obras = Obra.objects.all()  # <- Adicione isso aqui

    return render(request, 'editar-colaborador.html', {
        'form': form,
        'colaborador': colaborador,
        'obras': obras
    })

@login_required
def excluir_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, pk=id)
    
    if request.method == 'POST':
        colaborador.delete()
        return redirect('listar-colaboradores') 
    
    return render(request, 'excluir-colaborador.html', {'colaborador': colaborador})

@login_required
def cadastro_colaborador(request):
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            colaborador = form.save()  
            messages.success(request, 'Colaborador cadastrado com sucesso!')
            return redirect('listar-colaboradores') 
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = ColaboradorForm()
    
    
    obras = Obra.objects.all()
    
    return render(request, 'cadastro.html', {
        'form': form,
        'obras': obras
    })
@login_required
def cadastrar_restaurante(request):
    if request.method == 'POST':
        form = CadastroRestauranteForm(request.POST)
        if form.is_valid():
            restaurante = form.save(commit=False)
            restaurante.endereco = form.endereco_formatado  # usa o endereço formatado do clean
            restaurante.save()

            messages.success(request, 'Restaurante cadastrado com sucesso!')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = CadastroRestauranteForm()

    return render(request, 'cadastrar-restaurante.html', {'form': form})

@login_required
def editar_restaurante(request, id):
    restaurante = get_object_or_404(Restaurante, id=id)

    if request.method == 'POST':
        form = CadastroRestauranteForm(request.POST, instance=restaurante)
        if form.is_valid():
            restaurante = form.save(commit=False)
            restaurante.endereco = form.endereco_formatado 
            restaurante.save()

            messages.success(request, 'Restaurante atualizado com sucesso!')
            return redirect('listar-restaurantes')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = CadastroRestauranteForm(instance=restaurante)

    return render(request, 'editar-restaurante.html', {'form': form, 'restaurante': restaurante})

@login_required
def excluir_restaurante(request, id):
    restaurante = get_object_or_404(Restaurante, id=id)

    if request.method == 'POST':
        restaurante.delete()
        return redirect('listar-restaurantes') 

    return redirect('listar-restaurantes')
              
logger = logging.getLogger(__name__)


@login_required
def cadastro_hotel(request):
    if request.method == 'POST':
        form = CadastroHotelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hotel cadastrado com sucesso!')
            return redirect('listar-hoteis')  
    else:
        form = CadastroHotelForm()

    return render(request, 'cadastrar-hotel.html', { 'form': form})


@login_required
def listar_hoteis(request):
    hotel = Hotel.objects.all()
    context = {'hotel': hotel}
    return render (request, 'lista-hoteis.html', context)


@login_required
def editar_hotel(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    
    if request.method == 'POST':
        form = CadastroHotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('listar-hoteis')
    else:
        form = CadastroHotelForm(instance=hotel)
    return render(request, 'editar-hotel.html', {'form': form, 'hotel': hotel})  


@login_required
def redirecionar_edicao_hotel(request):
    if request.method == 'POST':
        hotel_id = request.POST.get('hotel_id')
        if hotel_id:
            return redirect ('editar-hotel', id=hotel_id)
        else:
            return HttpResponseBadRequest("Nenhum hotel selecionado.")
    return HttpResponseBadRequest("Requisição inválida.")



# View para deletar qualquer modelo autorizado
#Modelos permitidos 
ALLOWED_MODELS = ['Hotel', 'Restaurante', 'Colaborador', 'Obra'] 

@login_required
def deletar_generico(request):
    if request.method == 'POST':
        model_name = request.POST.get('model')
        ids = request.POST.getlist('ids')
        redirect_to = request.POST.get('redirect_to', 'home')

        if model_name not in ALLOWED_MODELS:
            return HttpResponseForbidden("Modelo não permitido.")

        try:
            Model = apps.get_model('Sistema', model_name)  
            Model.objects.filter(id__in=ids).delete()
        except Exception as e:
            print(f"Erro ao deletar: {e}")  

        return redirect(reverse(redirect_to))
    return redirect('home')



@login_required
def cadastrar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        tipo = request.POST.get('tipo')
        admin_password = request.POST.get('admin_password', '')

        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem!')
            return redirect('cadastrar_usuario')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já está em uso!')
            return redirect('cadastrar_usuario')

        try:
            grupo_admin, _ = Group.objects.get_or_create(name='Administradores')
            grupo_encarregado, _ = Group.objects.get_or_create(name='Encarregados')

            user = User.objects.create_user(username=username, email=email, password=password)

            if tipo == 'admin':
                user.groups.add(grupo_admin)
                user.is_staff = True
                user.save()
            else:
                user.groups.add(grupo_encarregado)

            # ✅ Cria o Profile com o tipo correto
            Profile.objects.create(user=user, tipo=tipo)

            messages.success(request, 'Usuário e perfil criados com sucesso!')
            return redirect('cadastrar_usuario')

        except Exception as e:
            messages.error(request, f'Erro no sistema: {str(e)}')

    return render(request, 'cadastrar_usuario.html')


@login_required
def listar_colaboradores(request):
    return render (request, 'lista-colaborador.html')



@login_required
def listar_restaurantes(request, ):
    restaurantes = Restaurante.objects.all()
    context = {'restaurantes': restaurantes}
    return render (request, 'lista-restaurantes.html', context)


@login_required
def cadastro_obras(request):
    if request.method == 'POST':
        form = CadastroObraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar-obras')
    else: 
        form = CadastroObraForm()
        
    return render(request, 'cadastrar-obra.html', {'form': form})

@login_required
def listar_obras(request):
    user = request.user

    if user.groups.filter(name='Encarregados').exists():
        obras = Obra.objects.filter(encarregado_responsavel=user)
    else:
        obras = Obra.objects.all()

    context = {
        'obras': obras,
        'pode_ver_colaboradores': user.groups.filter(name='Administradores').exists() or user.is_superuser,
        'pode_ver_restaurantes': user.has_perm('Sistema.view_restaurante') or user.is_superuser,
        'pode_ver_obras': user.has_perm('Sistema.view_obra') or user.is_superuser,
        'pode_adicionar_obra': user.has_perm('Sistema.add_obra') or user.is_superuser,
        'pode_editar_obra': user.has_perm('Sistema.change_obra') or user.is_superuser,
        'pode_deletar_obra': user.has_perm('Sistema.delete_obra') or user.is_superuser,
        'pode_ver_usuarios': user.groups.filter(name='Administradores').exists() or user.is_superuser,
        'pode_ver_dashboard': user.groups.filter(name='Administradores').exists() or user.is_superuser,
    }

    return render(request, 'lista-obras.html', context)

@login_required
def editar_obra(request, id):
    obra = get_object_or_404(Obra, id=id)

    if request.method == 'POST':
        form = CadastroObraForm(request.POST, instance=obra)  
        if form.is_valid():
            form.save()
            return redirect('listar-obras')  
    else:
        form = CadastroObraForm(instance=obra)  

    return render(request, 'editar-obra.html', {'form': form})


@login_required
def detalhes_obra(request, id):
    obra = get_object_or_404(Obra, id=id)
    return render(request, 'detalhes-obra.html', {'obra': obra})


@login_required
@permission_required('Sistema.view_refeicao', raise_exception=True)
def listar_pedidos(request):
    colaboradores = Colaborador.objects.all()
    return render(request, 'listar-pedidos.html', {'colaboradores': colaboradores})


# Manda Mongo
@login_required
@permission_required('Sistema.add_refeicao', raise_exception=True)
def cadastrar_pedido(request):
    if request.method == "POST":
        data = request.POST.get("data")
        refeicoes_ids = request.POST.getlist("refeicoes")
        pedido_model.registrar_refeicoes(data, refeicoes_ids, request.user)
        return redirect("listar_pedidos")
    return redirect("listar_pedidos")


# Lista todas as refeicoes cadastradas Mongo 
@login_required
def listar_registros(request):
    user = request.user
    is_encarregado = user.groups.filter(name='Encarregados').exists()
    is_administrador = user.groups.filter(name='Administradores').exists()
    is_superuser = user.is_superuser

    registros = pedido_model.listar_registros()
    paginator = Paginator(registros, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'registros': page_obj,
        'page_obj': page_obj,
        'is_encarregado': is_encarregado,
        'is_administrador': is_administrador,
        'is_superuser': is_superuser,
    }

    return render(request, 'listar-registros.html', context)

    
@login_required
def editar_registro(request, registro_id):
    registro = pedido_model.buscar_registro(registro_id)
    if request.method == "POST":
        nova_data = request.POST.get("data_refeicao")
        pedido_model.atualizar_data_refeicao(registro_id, nova_data)
        return redirect('listar_registros')
    return render(request, 'editar-registro.html', {'registro': registro})

@login_required
def excluir_registro(request, registro_id):
    pedido_model.excluir_registro(registro_id)
    return redirect('listar_registros')

@login_required
def relatorio(request):
    filtros = {
        "data_inicio": request.GET.get("data_inicio"),
        "data_fim": request.GET.get("data_fim"),
        "obra_id": request.GET.get("obra_id"),
        "colaborador_id": request.GET.get("colaborador_id")
    }

    filtros_aplicados = any([filtros["data_inicio"], filtros["data_fim"], filtros["obra_id"], filtros["colaborador_id"]])

    if filtros_aplicados:
        # Validação de intervalo
        try:
            data_inicio = datetime.strptime(filtros["data_inicio"], "%Y-%m-%d")
            data_fim = datetime.strptime(filtros["data_fim"], "%Y-%m-%d")

            if (data_fim - data_inicio).days > 31:
                messages.error(request, "O intervalo de datas não pode ultrapassar 31 dias.")
                return render(request, "dashboard.html", {
                    "obras": pedido_model.listar_obras_unicas(),
                    "colaboradores": pedido_model.listar_colaboradores_unicos(),
                    "total_refeicoes": 0,
                    "total_colaboradores": 0,
                    "refeicoes_por_dia": [],
                    "soma_valor_refeicoes": 0,
                })
        except (ValueError, TypeError):
            messages.error(request, "Datas inválidas.")
            # mesmo retorno acima em caso de erro
            return render(request, "dashboard.html", {
                "obras": pedido_model.listar_obras_unicas(),
                "colaboradores": pedido_model.listar_colaboradores_unicos(),
                "total_refeicoes": 0,
                "total_colaboradores": 0,
                "refeicoes_por_dia": [],
                "soma_valor_refeicoes": 0,
            })

        # Se intervalo válido:
        dados = {
            "total_refeicoes": pedido_model.total_refeicoes(filtros),
            "total_colaboradores": pedido_model.total_colaboradores_unicos(filtros),
            "refeicoes_por_dia": pedido_model.refeicoes_por_dia(filtros),
            "soma_valor_refeicoes": pedido_model.somar_valor_refeicoes(filtros),
        }
    else:
        dados = {
            "total_refeicoes": 0,
            "total_colaboradores": 0,
            "refeicoes_por_dia": [],
            "soma_valor_refeicoes": 0,
        }

    dados["obras"] = pedido_model.listar_obras_unicas()
    dados["colaboradores"] = pedido_model.listar_colaboradores_unicos()

    return render(request, "dashboard.html", dados)

@login_required
def home(request):
    user = request.user

    context = {
        'pode_ver_refeicoes': user.has_perm('Sistema.view_refeicao') or user.is_superuser,
        'pode_ver_obras': user.has_perm('Sistema.view_obra') or user.is_superuser,
        'pode_ver_dashboard': user.groups.filter(name='Administradores').exists() or user.is_superuser,
        'pode_ver_usuarios': user.groups.filter(name='Administradores').exists() or user.is_superuser,
        'pode_ver_colaboradores': user.groups.filter(name='Administradores').exists() or user.is_superuser,
        'pode_ver_restaurantes': user.has_perm('Sistema.view_restaurante') or user.is_superuser,
        'pode_ver_hoteis': user.groups.filter(name='Administradores').exists() or user.is_superuser,
        'grupo_nome': user.groups.first().name.upper() if user.groups.exists() else 'SUPERUSER',
        'username_maiusculo': user.username.upper()
    }

    return render(request, 'home.html', context)
