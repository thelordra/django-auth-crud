from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)  # importa fomulario registro usuarios
from django.contrib.auth.models import User  # modelo registro usuarios
from django.contrib.auth import login, logout, authenticate  # sesion de usuario
from django.db import IntegrityError  # control de errores de integridad
from .forms import TaskForm  # formulario de tareas
from .models import Task  # Modelo de tareas (BD)
from django.utils import timezone  # Metodo de uso horario
# Decorador para proteger las vistas
from django.contrib.auth.decorators import login_required


# Create your views here.
# Vista hola mundo
def home(request):
    return render(request, "home.html")


# Vista registro
def signup(request):
    # Se valida el tipo de consulta a la pagina
    if request.method == "GET":
        # GET se muestra el formulario de acceso
        # form, pertenece al diccionario que se envio desde View (UserCreationForm)
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        # POST se evaluan los valores registrados por el usuario
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # si las contraseñas son iguales Regiser user
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                # Se redirecciona a la vista tareas
                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "El usuario ya existe"},
                )
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "No son las mismas contraseñas"},
        )


# Vita de tareas Pendientes
@login_required
def tasks(request):
    # Consulta a la BD para obtener el listado de tareas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    # Se regresa la vista de tareas con el diccionario de tareas
    return render(request, 'tasks.html', {'tasks': tasks})

# Vita de tareas Completadas


@login_required
def tasks_completed(request):
    # Consulta a la BD para obtener el listado de tareas
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    # Se regresa la vista de tareas con el diccionario de tareas
    return render(request, 'tasks.html', {'tasks': tasks})


# Vita crear tareas
@login_required
def create_tasks(request):
    # Se valida el tipo de consulta a la pagina
    if request.method == "GET":
        # GET se muestra el formulario de registro
        # form, pertenece al diccionario que se envio desde View (UserCreationForm)
        return render(request, "create_tasks.html", {"form": TaskForm})
    else:
        try:
            # POST se evaluan los valores registrados por el usuario
            form = TaskForm(request.POST)
            # se registran los datos del formulario
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            # En caso de error al ejecutar
            return render(request, "create_tasks.html", {"form": TaskForm, 'error': 'Favor de proporcionar datos correctos'})


# Vista de consulta de tarea
@login_required
def task_detail(request, task_id):
    # Se valida el tipo de consulta a la pagina
    if request.method == 'GET':
        # GET se muestra el formulario de registro
        # form, pertenece al diccionario que se envio desde View (UserCreationForm)
        # Se busca en la BD la tarea que corresponda al ID y al usuario activo
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        # Se ingresan los datos de la tarea en la variable formulario
        form = TaskForm(instance=task)
        # Se renderiza vista de detalle con los datos de la tarea en un formulario
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            # POST se evaluan los valores registrados por el usuario
            # Se busca en la BD la tarea que corresponda al ID y al usuario activo#
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            # Se obtiene el contenido del formulario
            form = TaskForm(request.POST, instance=task)
            # Se almacena en BD
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': "Error Actualizando la tarea"})


# Vista para completar una tarea
@login_required
def complete_task(request, task_id):
    # Se busca en la BD la tarea que corresponda al ID y al usuario activo
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        # Se actualiza la fecha de completado
        task.datecompleted = timezone.now()
        # Se guara en la BD
        task.save()
        return redirect('tasks')


# Vista para eliminar una tarea
@login_required
def delete_task(request, task_id):
    # Se busca en la BD la tarea que corresponda al ID y al usuario activo
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        # Se ejecuta el metodo eliminar
        task.delete()
        return redirect('tasks')


# vista de cierre de sesion
@login_required
def signout(request):
    logout(request)
    return redirect("home")


# vista de inicio de sesion
def signin(request):
    # Se valida el tipo de consulta a la pagina
    if request.method == "GET":
        # GET se muestra el formulario de acceso
        # form, pertenece al diccionario que se envio desde View (UserCreationForm)
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        # POST se evaluan los valores registrados por el usuario
        # Realiza la validacion de los datos VS la BD
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            # El usuario no existe
            return render(
                request,
                "signin.html",
                {"form": AuthenticationForm, "error": "Usuario o conraseña erroneos"},
            )
        else:
            # El usuario si existe
            login(request, user)
            return redirect("tasks")
