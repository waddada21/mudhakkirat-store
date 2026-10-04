from django.shortcuts import render, redirect, get_object_or_404
from .models import Mudhakkira, Order

def catalog(request):
    mudhakkirat = Mudhakkira.objects.all()

    # Get the selected filter values from the URL (if any)
    level = request.GET.get('level')
    subject = request.GET.get('subject')

    # Narrow down the results based on what was selected
    if level:
        mudhakkirat = mudhakkirat.filter(level=level)
    if subject:
        mudhakkirat = mudhakkirat.filter(subject__icontains=subject)

    return render(request, 'store/catalog.html', {'mudhakkirat': mudhakkirat})


def order_create(request, mudhakkira_id):
    mudhakkira = get_object_or_404(Mudhakkira, id=mudhakkira_id)

    if request.method == 'POST':
        Order.objects.create(
            mudhakkira=mudhakkira,
            buyer_name=request.POST['buyer_name'],
            buyer_phone=request.POST['buyer_phone'],
            payment_reference=request.POST['payment_reference'],
        )
        return redirect('order_success')

    return render(request, 'store/order_form.html', {'mudhakkira': mudhakkira})


def order_success(request):
    return render(request, 'store/order_success.html')