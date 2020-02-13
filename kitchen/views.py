from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

# 生产管理
from qiantai.models import Food


def distribution(request):
    return render(request, 'kitchen/distribution.html')


# 预加工管理
def prepare(request):
    if request.method == 'GET':
        foods = Food.objects.filter(available=True)
        context = dict()
        context['foods'] = [{'id': food.id, 'name': food.name} for food in foods]
        return render(request, 'kitchen/prepare.html', context)


def finish(request):
    return JsonResponse({'statues': 'success'})
