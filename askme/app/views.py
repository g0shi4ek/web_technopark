from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

TAGS = [
    {
        'all_tags' : ['tag 0', 'tag 1', 'tag 2', 'tag 3']
    }
]

QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is a text for question {i}',
        'img_path': "img/smyleface.jpg",  
        'tags': [f'tag {i%4}', f'tag {(i+1)%4}'],
        'answers': 3
    }for i in range(30)
]

def paginate(objects_list, request, per_page=10, adjacent_pages=2):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # Если номер страницы не целое число - показываем первую страницу
        page = paginator.page(1)
    except EmptyPage:
        # Если страница пустая - показываем последнюю страницу
        page = paginator.page(paginator.num_pages)

     # Рассчитываем диапазон соседних страниц
    page_num = page.number
    total_pages = paginator.num_pages
    
    start_page = max(page_num - adjacent_pages, 1)
    end_page = min(page_num + adjacent_pages, total_pages)
    
    page_range = range(start_page, end_page + 1)
    
    return {
        'page': page,
        'page_range': page_range,
        'show_first': start_page > 1,
        'show_last': end_page < total_pages
    }

def get_all_tags():
    all_tags = set()
    for question in QUESTIONS:
        all_tags.update(question['tags'])
    return sorted(all_tags)


# Create your views here.
def index(request):
    pagination_data = paginate(QUESTIONS, request, per_page=5)
    return render(request, 'index.html', {
        'questions': pagination_data['page'].object_list,
        'page_obj': pagination_data['page'],
        'page_range': pagination_data['page_range'],
        'show_first': pagination_data['show_first'],
        'show_last': pagination_data['show_last'],
        'all_tags': get_all_tags() 
    })

def hot(request):
    pagination_data = paginate(QUESTIONS, request, per_page=5)
    return render(request, 'index.html', {
        'questions': pagination_data['page'].object_list,
        'page_obj': pagination_data['page'],
        'page_range': pagination_data['page_range'],
        'show_first': pagination_data['show_first'],
        'show_last': pagination_data['show_last'],
        'all_tags': get_all_tags() 
    })

def question(request, question_id):
    return render(request, 'singleq.html', context={'question': QUESTIONS[question_id]})


def questions_by_tag(request, tag_name):
    filtered_questions = [q for q in QUESTIONS if tag_name in q['tags']]
    pagination_data = paginate(filtered_questions, request, per_page=5)
    
    return render(request, 'questions_by_tag.html', {
        'tag': tag_name,
        'questions': pagination_data['page'].object_list,
        'page_obj': pagination_data['page'],
        'page_range': pagination_data['page_range'],
        'show_first': pagination_data['show_first'],
        'show_last': pagination_data['show_last'],
        'all_tags': get_all_tags() 
    })

def registration(request):
    return render(request, 'registration.html', context={'all_tags': get_all_tags()})

def login(request):
    return render(request, 'login.html', context={'all_tags': get_all_tags()})

def settings(request):
    return render(request, 'settings.html', context={'all_tags': get_all_tags()})

def ask(request):
    return render(request, 'ask.html', context={'all_tags': get_all_tags()})
