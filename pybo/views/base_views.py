from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Question



def index(request):
    """
    pybo 목록 출력
    """
    #입력 인자
    page = request.GET.get('page', '1')     #페이지
    kw = request.GET.get('kw', '')  # 검색어

    #조회
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    #페이징 처리
    paginator = Paginator(question_list, 10)     #페이지 당 10개씩 보여주기
    page_obj = paginator.get_page(page)


    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'pybo/question_list.html', context)


    


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    page = request.GET.get('page', '1')
    question = get_object_or_404(Question, pk = question_id)

    answers = question.answer_set.all()
    paginator = Paginator(answers, 5)      #페이지 당 5개씩 표시
    page_obj = paginator.get_page(page)

    context = {
        'question' : question,
        'answers' : page_obj,
        'page' : page, 
    }
    return render(request, 'pybo/question_detail.html', context)

