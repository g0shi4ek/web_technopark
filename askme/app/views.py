from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import Question, Tag, Profile, Answer

def get_best_users():
    return Profile.objects.all()[:10]

def get_best_tags():
    return Tag.objects.all().order_by('name')[:10]



def get_base_context():
    return {
        'best_users': get_best_users(),
        'best_tags': get_best_tags()
    }

def paginate_objects(request, objects, per_page=5, adjacent_pages=2):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page', 1)
    
    try:
        page = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page = paginator.page(1)

    page_num = page.number
    total_pages = paginator.num_pages
    
    start_page = max(page_num - adjacent_pages, 1)
    end_page = min(page_num + adjacent_pages, total_pages)
    
    context = get_base_context()
    context.update({
        'questions': page.object_list,
        'page_obj': page,
        'page_range': range(start_page, end_page + 1),
        'show_first': start_page > 1,
        'show_last': end_page < total_pages,
        'best_users': get_best_users(),
        'best_tags': get_best_tags()
    })
    return context

def base_question_view(request, questions, template_name):
    context = paginate_objects(request, questions)
    return render(request, template_name, context)


def index(request):
    return base_question_view(request, Question.objects.new(), 'index.html')


def hot(request):
    return base_question_view(request, Question.objects.hot(), 'hot.html')


def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = Answer.objects.filter(question=question).order_by('-is_correct', 'created_at')
    context = paginate_objects(request, question.answer_set.all(), per_page=5)
    context['question'] = question
    context['answers'] = answers
    return render(request, 'singleq.html', context)


def questions_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    context = paginate_objects(request, Question.objects.by_tag(tag_name))
    context['tag'] = tag
    return render(request, 'questions_by_tag.html', context)


def simple_view(request, template_name):

    return render(request, template_name, get_base_context())


def registration(request):
    return simple_view(request, 'registration.html')

def login(request):
    return simple_view(request, 'login.html')

def settings(request):
    return simple_view(request, 'settings.html')

def ask(request):
    return simple_view(request, 'ask.html')
