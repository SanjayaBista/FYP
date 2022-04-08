from django.shortcuts import get_object_or_404
from Home.models import ExchangeRate,CurrencyState

def template_processor(request):
	exchange_rate = ExchangeRate.objects.all()
	currency = request.GET.get('currency', None)
	if currency:
		CurrencyState.objects.all().delete()
		CurrencyState.objects.get_or_create(state = currency)
	if CurrencyState.objects.all().exists():
		state = CurrencyState.objects.last().state
	else:
		state = None
	return {'currency':state,'exchange_rate':exchange_rate}

