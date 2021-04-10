from django.views.generic import ListView, DeleteView, CreateView
from todo.models import Todo
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
from django.forms import model_to_dict
from django.views.generic.edit import BaseDeleteView, BaseCreateView
# Create your views here.

@method_decorator(ensure_csrf_cookie, name='dispatch') # ensure_csrf_cookie을 쓰면 csrf토큰을 만들어 리스트로 뿌립니다 즉 이걸 Vue가 받아서 axios를 다시 날려줍니다.
class ApiTodoLV(ListView) :
    
    model = Todo
    
    #def get(self, request, *args, **kwargs) :
    #   tmpList = [ 
    #        {'id': 1, 'name': 'd정승화', 'todo': 'Django와 Vue를 사용한 Todo 프로그램 제작'},
    #        {'id': 2, 'name': 'd장동건', 'todo': '굉장히 부담스럽네요'},
    #        {'id': 3, 'name': 'd원빈', 'todo': '해커톤은 처음이라서요 잘 부탁드려요'}
    #    ]
    #    return JsonResponse(data=tmpList, safe=False)

    def render_to_response(self, context, **response_kwargs) :
        todoList = list(context['object_list'].values()) # Values는 딕셔너리 형태로 변경시켜주는 역할 디장고 모델 공식문서에서 확인가능
        return JsonResponse(todoList, safe=False) # 딕셔너리가 아니면 Fasle... 이것도 장고 공식문서에서 확인이 가능한데 대체 이런걸 어떻게 알고 다 쓰는거냐고 ㅅㅂ

class ApiTodoDelV(DeleteView):
    model = Todo
    
    def delete(self, request, *args, **kwargs): 
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse(data={}, status=204)

@method_decorator(csrf_exempt, name='dispatch')
class ApiTodoCV(CreateView) :
    model = Todo
    fields = '__all__'
    
    def get_form_kwargs(self) :
        kwargs = super().get_form_kwargs()
        kwargs['data'] = json.loads(self.request.body)
        return kwargs

    def form_valid(self, form) :
        self.object = form.save()
        newTodo = model_to_dict(self.object)
        return JsonResponse(data=newTodo, status=201)

    def form_invalid(self, form):
        self.request.body.decode('utf8')
        return JsonResponse(data=form.errors, status=400)
