from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from .forms import QuestionForm
from django.contrib.auth.decorators import login_required

@login_required
def question_list(request):
    if request.user.is_superuser:
        questions = Question.objects.all()
    else:
        questions = request.user.assigned_questions.all()
    return render(request, 'question_management/question_list.html', {'questions': questions})

@login_required
def question_add(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            return redirect('question_management:question_list')
    else:
        form = QuestionForm()
    return render(request, 'question_management/question_form.html', {'form': form})

@login_required
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('question_management:question_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'question_management/question_form.html', {'form': form})

@login_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    return redirect('question_management:question_list')
