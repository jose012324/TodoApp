from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from .models import Todo
from .forms import TodoForm

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back {username} !")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists")
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "Register success")
            return redirect('login') 
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logout")
    return redirect('login')


#crud functions
@login_required
def home(request):
    todo = Todo.objects.filter(user=request.user)
    
    # For edit functionality
    if request.method == 'POST' and 'todo_id' in request.POST:
        todo_id = request.POST.get('todo_id')
        todo_item = get_object_or_404(Todo, user=request.user, id=todo_id)
        form = TodoForm(request.POST, instance=todo_item)
        
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': f"The todo {todo_item.description} is updated"
                })
            messages.success(request, f"The todo {todo_item.description} is updated")
            return redirect('home')
    
    # For adding new todo
    elif request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.user = request.user
            todo_item.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'New todo added'})
            
            messages.success(request, "New todo added")
            return redirect('home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Something error'})
            
            messages.error(request, "Something error")
            return redirect('home')
    else:
        form = TodoForm()

        context = {
            'todo': todo,
            'form': form
        }
    return render(request, 'home.html', context)

#to delete todo
@login_required
def delete(request, todo_id):
    todo = get_object_or_404(Todo, user=request.user, id=todo_id)
    todo.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Deleted success'})
    
    messages.success(request, "Deleted success")
    return redirect('home')


#to mark as done the todo
@login_required
def mark_as_done(request, todo_id):
    todo = get_object_or_404(Todo, user=request.user, id=todo_id)
    todo.status = 'done'
    todo.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success', 
            'message': f"Todo {todo.description} mark as done"
        })
    
    messages.success(request, f"Todo {todo.description} mark as done")
    return redirect('home')