import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Fruta
from .serializers import FrutaSerializer


class DashboardView(View):
    template_name = 'estoque/dashboard.html'

    def get(self, request):
        frutas = Fruta.objects.all()
        context = {
            'frutas': frutas,
            'total_frutas': frutas.count(),
            'total_estoque': sum(fruta.quantidade_estoque for fruta in frutas),
            'vencidas': frutas.filter(status=Fruta.Status.VENCIDA).count(),
        }
        return render(request, self.template_name, context)


class MovimentarEstoqueView(View):
    def post(self, request, fruta_id):
        fruta = get_object_or_404(Fruta, id=fruta_id)
        acao = request.POST.get('acao')
        quantidade = int(request.POST.get('quantidade', 0))

        try:
            if acao == 'entrada':
                fruta.entrada_estoque(quantidade)
            elif acao == 'saida':
                fruta.saida_estoque(quantidade)
            else:
                messages.error(request, 'Ação inválida.')
        except Exception as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, 'Movimentação registrada com sucesso.')

        return redirect('estoque:dashboard')


@method_decorator(csrf_exempt, name='dispatch')
class FrutaApiView(View):
    def get(self, request):
        frutas = [FrutaSerializer.to_dict(fruta) for fruta in Fruta.objects.all()]
        return JsonResponse(frutas, safe=False)

    def post(self, request):
        payload = json.loads(request.body or '{}')
        fruta = Fruta.objects.create(
            nome=payload['nome'],
            tipo=payload['tipo'],
            data_validade=payload['data_validade'],
            quantidade_estoque=payload.get('quantidade_estoque', 0),
        )
        return JsonResponse(FrutaSerializer.to_dict(fruta), status=201)
