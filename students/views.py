from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404  
from django.contrib.auth import views
from .forms import UserEditForm, AddNote
from .models import CourseAssignment, UserNote


def login(request):
    if request.user.is_authenticated():
        return redirect('profile')
    else:
        return views.login(request, template_name='login_form.html')


def logout(request):
    views.logout(request)
    return redirect('/')


def user_profile(request):
    return render(request, "profile.html", locals())


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile/')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'edit_profile.html', locals())


@login_required
def assignment(request, id):
    assignment = get_object_or_404(CourseAssignment, pk=id)
    is_teacher = request.user.has_perm('student.add_courseassignment')
    
    if assignment.user != request.user or not is_teacher:
        raise Http404()

    if is_teacher:
        notes =  UserNote.objects.filter(assignment=id)
        if request.method == 'POST':
            form = AddNote(request.POST)
            if form.is_valid():
                form.save()
                return redirect('assignment', id=id)
        else:
            form = AddNote()

    return render(request, "assignment.html", locals())
