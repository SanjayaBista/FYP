from time import timezone
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Coupon
from .forms import CouponForm
from django.shortcuts import redirect

@login_required(login_url='account:login')
def useCoupon(request):
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, startFrom__lte=now, endOn__gte=now, active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')