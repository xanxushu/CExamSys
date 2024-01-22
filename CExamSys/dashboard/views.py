from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from question_management.models import Question
from paper_generation.models import Paper,PaperQuestion
from user_management.models import CustomUser
import json
from django.db.models import Count, Case, When

@login_required
def dashboard_home(request):
    current_user = request.user
    context = {}

    if current_user.user_type == CustomUser.ADMIN:
        # 管理员视图
        # 最新的五道题和试卷
        latest_questions = Question.objects.all().order_by('-id')[:5]
        latest_papers = Paper.objects.all().order_by('-id')[:5]
        # 全部试卷
        total_papers = Paper.objects.count()
        # 问题类型定义
        question_type_counts = Question.objects.values('question_type').annotate(count=Count('id'))
        # 问题难度定义
        question_difficulty_counts = Question.objects.values('difficulty').annotate(count=Count('id'))
        # 章节定义
        chapter_counts = Question.objects.values('chapter').annotate(count=Count('id'))
        # 问题类型数据模型
        question_type_data = {
            'labels': [item['question_type'] for item in question_type_counts],
            'data': [item['count'] for item in question_type_counts]
        }
        # 问题类型
        question_types = {item['question_type']: item['count'] for item in question_type_counts}
        # 问题类型json
        question_type_json = json.dumps(question_type_data)
        # 每个教师的试卷数
        papers_per_teacher = Paper.objects.values('created_by__username').annotate(count=Count('id'))
        # 章节占比统计
        chapter_distribution = list(Question.objects.values('chapter').annotate(count=Count('id')))
        chapter_distribution_json = json.dumps(chapter_distribution)
        # 难度区间占比统计
        difficulty_distribution = Question.objects.aggregate(
            low=Count(Case(When(difficulty__lte=20, then=1))),
            medium_low=Count(Case(When(difficulty__gt=20, difficulty__lte=40, then=1))),
            medium=Count(Case(When(difficulty__gt=40, difficulty__lte=60, then=1))),
            medium_high=Count(Case(When(difficulty__gt=60, difficulty__lte=80, then=1))),
            high=Count(Case(When(difficulty__gt=80, then=1)))
        )
        difficulty_distribution_json = json.dumps({
            'labels': ['0-20%', '21-40%', '41-60%', '61-80%', '81-100%'],
            'data': [
                difficulty_distribution['low'], 
                difficulty_distribution['medium_low'],
                difficulty_distribution['medium'],
                difficulty_distribution['medium_high'],
                difficulty_distribution['high']
            ]
        })
        # 试卷难度占比数据
        # 获取所有试卷及其难度
        papers = Paper.objects.all()
        paper_difficulty_distribution = {'0-20': 0, '21-40': 0, '41-60': 0, '61-80': 0, '81-100': 0}
        # 计算难度分布
        for paper in papers:
            avg_difficulty = paper.difficulty
            if avg_difficulty <= 20:
                paper_difficulty_distribution['0-20'] += 1
            elif avg_difficulty <= 40:
                paper_difficulty_distribution['21-40'] += 1
            elif avg_difficulty <= 60:
                paper_difficulty_distribution['41-60'] += 1
            elif avg_difficulty <= 80:
                paper_difficulty_distribution['61-80'] += 1
            else:
                paper_difficulty_distribution['81-100'] += 1
        paper_difficulty_distribution_json = json.dumps({
            'labels': ['0-20%', '21-40%', '41-60%', '61-80%', '81-100%'],
            'data': [
                paper_difficulty_distribution['0-20'], 
                paper_difficulty_distribution['21-40'],
                paper_difficulty_distribution['41-60'],
                paper_difficulty_distribution['61-80'],
                paper_difficulty_distribution['81-100']
            ]
        })       
        # 题目使用次数 Top 5 数据
        question_usage = PaperQuestion.objects.values('question__id').annotate(usage_count=Count('question')).order_by('-usage_count')[:5]        
        # print(latest_questions, latest_papers, question_types)  # 调试输出
        print("success")
        context.update({
            'latest_questions': latest_questions,
            'latest_papers': latest_papers,
            'total_papers': total_papers,
            'question_type_counts': json.dumps(list(question_type_counts)),
            'question_difficulty_counts': json.dumps(list(question_difficulty_counts)),
            'chapter_counts': json.dumps(list(chapter_counts)),
            'question_type_json': question_type_json,
            'total_questions': Question.objects.count(),
            'question_types': question_types,
            'papers_per_teacher': papers_per_teacher,
            'chapter_distribution_json': chapter_distribution_json,
            'difficulty_distribution_json': difficulty_distribution_json,
            'paper_difficulty_distribution_json': paper_difficulty_distribution_json,
            'question_usage': json.dumps(list(question_usage)),
        })
    elif current_user.user_type == CustomUser.TEACHER or  current_user.user_type == CustomUser.STUDENT:
        # 教师视图：显示与教师相关的数据
        assigned_questions = Question.objects.filter(assigned_to=current_user).order_by('-id')[:5]
        if current_user.user_type == CustomUser.TEACHER:
            created_papers = Paper.objects.filter(created_by=current_user).order_by('-id')[:5]
            total_papers = Paper.objects.filter(created_by=current_user).count()
            papers_per_teacher = Paper.objects.filter(created_by=current_user).values('created_by__username').annotate(count=Count('id'))
            papers = Paper.objects.filter(created_by=current_user)
        else:
            created_papers = Paper.objects.filter(assigned_to=current_user).order_by('-id')[:5]
            total_papers = Paper.objects.filter(assigned_to=current_user).count()
            papers_per_teacher = Paper.objects.filter(assigned_to=current_user).values('created_by__username').annotate(count=Count('id'))
            papers = Paper.objects.filter(assigned_to=current_user)
        # 统计信息
        question_type_counts = Question.objects.filter(assigned_to=current_user).values('question_type').annotate(count=Count('id'))
        #question_type_json = json.dumps({'labels': [item['question_type'] for item in question_type_counts], 'data': [item['count'] for item in question_type_counts]})
        question_type_data = {
            'labels': [item['question_type'] for item in question_type_counts],
            'data': [item['count'] for item in question_type_counts]
        }
        question_types = {item['question_type']: item['count'] for item in question_type_counts}
        question_type_json = json.dumps(question_type_data)
        # 章节占比统计
        chapter_distribution = list(Question.objects.filter(assigned_to=current_user).values('chapter').annotate(count=Count('id')))
        chapter_distribution_json = json.dumps(chapter_distribution)
        # 难度区间占比统计
        difficulty_distribution = Question.objects.filter(assigned_to=current_user).aggregate(
            low=Count(Case(When(difficulty__lte=20, then=1))),
            medium_low=Count(Case(When(difficulty__gt=20, difficulty__lte=40, then=1))),
            medium=Count(Case(When(difficulty__gt=40, difficulty__lte=60, then=1))),
            medium_high=Count(Case(When(difficulty__gt=60, difficulty__lte=80, then=1))),
            high=Count(Case(When(difficulty__gt=80, then=1)))
        )
        difficulty_distribution_json = json.dumps({
            'labels': ['0-20%', '21-40%', '41-60%', '61-80%', '81-100%'],
            'data': [
                difficulty_distribution['low'], 
                difficulty_distribution['medium_low'],
                difficulty_distribution['medium'],
                difficulty_distribution['medium_high'],
                difficulty_distribution['high']
            ]
        })
        
        paper_difficulty_distribution = {'0-20': 0, '21-40': 0, '41-60': 0, '61-80': 0, '81-100': 0}
        # 计算难度分布
        for paper in papers:
            avg_difficulty = paper.difficulty
            if avg_difficulty <= 20:
                paper_difficulty_distribution['0-20'] += 1
            elif avg_difficulty <= 40:
                paper_difficulty_distribution['21-40'] += 1
            elif avg_difficulty <= 60:
                paper_difficulty_distribution['41-60'] += 1
            elif avg_difficulty <= 80:
                paper_difficulty_distribution['61-80'] += 1
            else:
                paper_difficulty_distribution['81-100'] += 1
        paper_difficulty_distribution_json = json.dumps({
            'labels': ['0-20%', '21-40%', '41-60%', '61-80%', '81-100%'],
            'data': [
                paper_difficulty_distribution['0-20'], 
                paper_difficulty_distribution['21-40'],
                paper_difficulty_distribution['41-60'],
                paper_difficulty_distribution['61-80'],
                paper_difficulty_distribution['81-100']
            ]
        })       
        # 题目使用次数 Top 5 数据
        question_usage = PaperQuestion.objects.values('question__id').annotate(usage_count=Count('question')).order_by('-usage_count')[:5]    
        # print(assigned_questions,created_papers)
        context.update({
            'latest_questions': assigned_questions,
            'latest_papers': created_papers,
            'question_type_counts': json.dumps(list(question_type_counts)),
            'question_type_json': question_type_json,
            'total_questions': Question.objects.filter(assigned_to=current_user).count(),
            'total_papers': total_papers,
            'question_types': question_types,
            'papers_per_teacher': papers_per_teacher,
            'chapter_distribution_json': chapter_distribution_json,
            'difficulty_distribution_json': difficulty_distribution_json,
            'paper_difficulty_distribution_json': paper_difficulty_distribution_json,
            'question_usage': json.dumps(list(question_usage)),
        })

    '''elif current_user.user_type == CustomUser.STUDENT:
        # 学生视图：显示与学生相关的数据
        assigned_questions = Question.objects.filter(assigned_to=current_user).order_by('-id')[:5]
        assigned_papers = Paper.objects.filter(assigned_to=current_user).order_by('-id')[:5]

        # 统计信息
        question_type_counts = assigned_questions.values('question_type').annotate(count=Count('id'))
        question_type_json = json.dumps({'labels': [item['question_type'] for item in question_type_counts], 'data': [item['count'] for item in question_type_counts]})

        context.update({
            'latest_questions': assigned_questions,
            'latest_papers': assigned_papers,
            'question_type_json': question_type_json,
            'total_assigned_questions': assigned_questions.count(),
            'total_assigned_papers': assigned_papers.count(),
        })'''


    return render(request, 'dashboard/home.html', context)

'''@login_required
def my_questions(request):
    current_user = request.user
    if current_user.user_type == CustomUser.ADMIN:
        questions = Question.objects.all()
    elif current_user.user_type == CustomUser.TEACHER:
        questions = Question.objects.filter(assigned_to=current_user)
    else:
        questions = Question.objects.filter(assigned_to=current_user)

    return render(request, 'dashboard/questions.html', {'questions': questions})

@login_required
def my_papers(request):
    current_user = request.user
    if current_user.user_type == CustomUser.ADMIN:
        papers = Paper.objects.all()
    elif current_user.user_type == CustomUser.TEACHER:
        papers = Paper.objects.filter(created_by=current_user)
    else:
        papers = Paper.objects.filter(assigned_to=current_user)

    return render(request, 'dashboard/papers.html', {'papers': papers})
'''