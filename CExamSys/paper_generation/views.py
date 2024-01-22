from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Paper, PaperQuestion
from user_management.models import CustomUser
from .forms import PaperForm,AutoGeneratePaperForm
from question_management.models import Question  # 导入Question模型
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from itertools import chain
import random

@login_required
def paper_list(request):
    '''if request.user.user_type != CustomUser.TEACHER:
        return HttpResponseForbidden("只有教师用户可以访问此页面。")'''
    if request.user.is_superuser:
        papers = Paper.objects.all()
    elif request.user.user_type == CustomUser.TEACHER:
        papers = Paper.objects.filter(created_by=request.user)
    else:
        papers = Paper.objects.filter(assigned_to=request.user)
    #papers = Paper.objects.filter(created_by=request.user)
    # 搜索逻辑（根据标题、创建者等搜索）
    search_query = request.GET.get('search', '')
    if search_query:
        papers = papers.filter(title__icontains=search_query)

    return render(request, 'paper_generation/paper_list.html', {
        'papers': papers
    })

@login_required
def paper_add(request):
    if request.method == "POST":
        form = PaperForm(request.POST)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.created_by = request.user
            paper.save()
            form.save_m2m()  # 保存多对多关系
            assigned_students = paper.assigned_to.all()
            for question in paper.questions.all():
                for student in assigned_students:
                    if not question.assigned_to.filter(id=student.id).exists():
                        question.assigned_to.add(student)

            return redirect('paper_generation:paper_list')
    else:
        form = PaperForm()
    return render(request, 'paper_generation/paper_form.html', {
        'form': form
    })

@login_required
def paper_edit(request, pk):
    paper = get_object_or_404(Paper, pk=pk, created_by=request.user)
    if request.method == "POST":
        form = PaperForm(request.POST, instance=paper)
        if form.is_valid():
            form.save()
            # 更新试卷问题
            # 将试卷中的试题分配给学生
            assigned_students = paper.assigned_to.all()
            for question in paper.questions.all():
                for student in assigned_students:
                    if not question.assigned_to.filter(id=student.id).exists():
                        question.assigned_to.add(student)

            #paper.paper_questions.all().delete()
            questions = form.cleaned_data['questions']
            for question in questions:
                PaperQuestion.objects.create(paper=paper, question=question)
            return redirect('paper_generation:paper_list')
    else:
        form = PaperForm(instance=paper)
    # 获取筛选条件
    question_type_query = request.GET.get('question_type', '')
    chapter_query = request.GET.get('chapter', '')
    difficulty_query = request.GET.get('difficulty', '')

    # 获取题目
    questions = Question.objects.all()
    if question_type_query:
        questions = questions.filter(question_type=question_type_query)
    if chapter_query:
        questions = questions.filter(chapter=chapter_query)
    if difficulty_query:
        if difficulty_query == '简单':
            questions = questions.filter(difficulty__lte=20)
        elif difficulty_query == '较易':
            questions = questions.filter(difficulty__gt=20, difficulty__lte=40)
        elif difficulty_query == '中等':
            questions = questions.filter(difficulty__gt=40, difficulty__lte=60)
        elif difficulty_query == '较难':
            questions = questions.filter(difficulty__gt=60, difficulty__lte=80)
        elif difficulty_query == '困难':
            questions = questions.filter(difficulty__gt=80, difficulty__lte=100)

    paginator = Paginator(questions, 10)  # 每页10个题目
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 获取题型、章节和难度的唯一值列表
    question_types = Question.objects.values_list('question_type', flat=True).distinct()
    chapters = Question.objects.values_list('chapter', flat=True).distinct()
    difficulties = Question.objects.values_list('difficulty', flat=True).distinct()

    return render(request, 'paper_generation/paper_form.html', {
        'form': form, 'paper': paper, 'page_obj': page_obj,
        'question_types': question_types, 'chapters': chapters, 'difficulties': difficulties,
        'question_type_query': question_type_query, 'chapter_query': chapter_query, 'difficulty_query': difficulty_query
    })


@login_required
def paper_delete(request, pk):
    paper = get_object_or_404(Paper, pk=pk, created_by=request.user)
    paper.delete()
    return redirect('paper_generation:paper_list')

@login_required
def paper_detail(request, pk):
    paper = get_object_or_404(Paper, pk=pk)

    # 创建题型显示名称的映射
    question_type_display = dict(Question.TYPE_CHOICES)

    # 按题型分组题目
    questions_by_type = {}
    for question in paper.questions.all():
        questions_by_type.setdefault(question.question_type, []).append(question)

    # 按题型的显示顺序排序
    ordered_questions = []
    for question_type, _ in Question.TYPE_CHOICES:
        if question_type in questions_by_type:
            ordered_questions.append((question_type_display[question_type], questions_by_type[question_type]))

    return render(request, 'paper_generation/paper_detail.html', {
        'paper': paper, 'ordered_questions': ordered_questions
    })

'''
@login_required
def auto_generate_paper(request):
    if request.method == 'POST':
        form = AutoGeneratePaperForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            paper = Paper(title=title, created_by=request.user)
            paper.save()

            for question_type, _ in Question.TYPE_CHOICES:
                num_questions = form.cleaned_data.get(f'num_questions_{question_type}', 0)
                if num_questions > 0:
                    # 难度和章节的占比计算
                    difficulty_percentages = [form.cleaned_data.get(f'difficulty_{i}_percent', 0) for i in range(1, 6)]
                    chapter_percentages = {chapter: form.cleaned_data.get(f'chapter_{chapter}_percent', 0) for chapter, _ in form.chapter_choices}

                    # 根据占比选择题目
                    selected_questions = select_questions_by_type_and_percentages(
                        question_type, num_questions, difficulty_percentages, chapter_percentages)
                    for question in selected_questions:
                        PaperQuestion.objects.create(paper=paper, question=question)

            return redirect('paper_generation:paper_detail', pk=paper.pk)
    else:
        form = AutoGeneratePaperForm()

    return render(request, 'paper_generation/auto_generate_paper.html', {'form': form})

def select_questions_by_type_and_percentages(question_type, num_questions, difficulty_percentages, chapter_percentages):
    selected_questions = []
    difficulty_ranges = [(1, 20), (21, 40), (41, 60), (61, 80), (81, 100)]  # 难度区间

    # 新增：验证每个难度和章节组合中可用题目数量
    for level, percent in enumerate(difficulty_percentages, start=1):
        difficulty_range = difficulty_ranges[level - 1]  # 获取对应难度区间
        for chapter, chapter_percent in chapter_percentages.items():
            if percent > 0 and chapter_percent > 0:
                num_chapter_questions = round((percent / 100) * (chapter_percent / 100) * num_questions)
                available_questions = Question.objects.filter(
                    question_type=question_type, 
                    difficulty__range=difficulty_range, 
                    chapter=chapter
                ).count()
                if num_chapter_questions > available_questions:
                    # 如果可用题目不足，则按比例减少各个章节和难度的题目数量，但确保至少有一个题目
                    reduction_factor = available_questions / num_chapter_questions if num_chapter_questions else 0
                    difficulty_percentages[level - 1] *= reduction_factor
                    chapter_percentages[chapter] *= reduction_factor
                    # 确保至少有一个题目被选中
                    if available_questions > 0:
                        difficulty_percentages[level - 1] = max(difficulty_percentages[level - 1], 1)
                        chapter_percentages[chapter] = max(chapter_percentages[chapter], 1)

    # 根据调整后的占比选择题目
    for level, percent in enumerate(difficulty_percentages, start=1):
        if percent > 0:
            difficulty_range = difficulty_ranges[level - 1]  # 获取对应难度区间
            for chapter, chapter_percent in chapter_percentages.items():
                if chapter_percent > 0:
                    num_chapter_questions = round((percent / 100) * (chapter_percent / 100) * num_questions)
                    questions = Question.objects.filter(
                        question_type=question_type, 
                        difficulty__range=difficulty_range, 
                        chapter=chapter
                    )[:num_chapter_questions]
                    selected_questions.extend(questions)

    # 如果选择的题目超过了所需数量，则随机减少以符合数量
    if len(selected_questions) > num_questions:
        selected_questions = random.sample(selected_questions, num_questions)

    return selected_questions
'''

@login_required
def auto_generate_paper(request):
    if request.method == 'POST':
        form = AutoGeneratePaperForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            paper = Paper(title=title, created_by=request.user)
            paper.save()

            total_questions = form.cleaned_data['total_questions']
            selected_questions = select_questions_for_paper(form.cleaned_data, total_questions)

            for question in selected_questions:
                PaperQuestion.objects.create(paper=paper, question=question)

            return redirect('paper_generation:paper_detail', pk=paper.pk)
    else:
        form = AutoGeneratePaperForm()

    return render(request, 'paper_generation/auto_generate_paper.html', {'form': form})

def select_questions_for_paper(cleaned_data, total_questions):
    selected_questions = []
    difficulty_ranges = {1: (0, 30), 2: (31, 70), 3: (71, 100)}

    # 分别根据题型、难度和章节选择题目
    questions_by_type = {}
    questions_by_difficulty = {}
    questions_by_chapter = {}

    for question_type, _ in Question.TYPE_CHOICES:
        num_questions_type = cleaned_data.get(f'num_questions_{question_type}', 0)
        if num_questions_type > 0:
            questions_by_type[question_type] = set(Question.objects.filter(
                question_type=question_type
            )[:num_questions_type])

    for level in range(1, 4):
        num_questions_difficulty = cleaned_data.get(f'num_questions_difficulty_{level}', 0)
        if num_questions_difficulty > 0:
            difficulty_range = difficulty_ranges[level]
            questions_by_difficulty[level] = set(Question.objects.filter(
                difficulty__range=difficulty_range
            )[:num_questions_difficulty])

    for chapter, _ in [(chapter, chapter) for chapter in Question.objects.values_list('chapter', flat=True).distinct()]:
        num_questions_chapter = cleaned_data.get(f'num_questions_chapter_{chapter}', 0)
        if num_questions_chapter > 0:
            questions_by_chapter[chapter] = set(Question.objects.filter(
                chapter=chapter
            )[:num_questions_chapter])

    # 获取所有条件的交集
    all_questions = set.union(*questions_by_type.values(), *questions_by_difficulty.values(), *questions_by_chapter.values())
    
    # 从交集中随机选择指定数量的题目
    all_questions_list = list(all_questions)
    selected_questions = random.sample(all_questions_list, min(total_questions, len(all_questions_list)))

    return selected_questions
