from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from .forms import QuestionForm ,QuestionSearchForm
from django.contrib.auth.decorators import login_required

'''
@login_required
def question_list(request):
    if request.user.is_superuser:
        questions = Question.objects.all()
    else:
        questions = request.user.assigned_questions.all()
    return render(request, 'question_management/question_list.html', {'questions': questions})
'''

@login_required
def question_list(request):
    form = QuestionSearchForm(request.GET or None)
    if request.user.is_superuser:
        questions = Question.objects.all()
    else:
        questions = request.user.assigned_questions.all()
    #print(request.user.user_type)
    if form.is_valid():
        if form.cleaned_data['qid']:
            questions = questions.filter(id=form.cleaned_data['qid'])
        if form.cleaned_data['keyword']:
            questions = questions.filter(question_text__icontains=form.cleaned_data['keyword'])
        if form.cleaned_data['question_type']:
            questions = questions.filter(question_type=form.cleaned_data['question_type'])
        if form.cleaned_data['chapter']:
            questions = questions.filter(chapter__icontains=form.cleaned_data['chapter'])
        if form.cleaned_data['difficulty_from'] is not None:
            questions = questions.filter(difficulty__gte=form.cleaned_data['difficulty_from'])
        if form.cleaned_data['difficulty_to'] is not None:
            questions = questions.filter(difficulty__lte=form.cleaned_data['difficulty_to'])

    return render(request, 'question_management/question_list.html', {
        'questions': questions,
        'form': form
    })

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

@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'question_management/question_detail.html', {'question': question})
