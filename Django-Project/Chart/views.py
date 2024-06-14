from django.shortcuts import render, redirect
from .models import ServiceOption, CostDiagram
from django.db.models import Sum
from django.db import transaction
from django.contrib.auth.decorators import login_required

@login_required
def cost_diagram(request):
    if request.method == 'POST':
        service_option_id = request.POST.get('service_option')
        cost = request.POST.get('cost')
        date_taken = request.POST.get('date_taken')

        # Validate input data
        if not service_option_id or not cost or not date_taken:
            return render(request, 'cost_diagram.html', {
                'error': 'All fields are required.',
                'service_options': ServiceOption.objects.all(),
                'option_choices': ServiceOption.OPTION_CHOICES
            })

        try:
            cost = float(cost)
        except ValueError:
            return render(request, 'cost_diagram.html', {
                'error': 'Invalid cost value.',
                'service_options': ServiceOption.objects.all(),
                'option_choices': ServiceOption.OPTION_CHOICES
            })

        try:
            service_option = ServiceOption.objects.get(pk=service_option_id)
        except ServiceOption.DoesNotExist:
            return render(request, 'cost_diagram.html', {
                'error': 'Invalid service option selected.',
                'service_options': ServiceOption.objects.all(),
                'option_choices': ServiceOption.OPTION_CHOICES
            })

        with transaction.atomic():
            CostDiagram.objects.create(user=request.user, service_option=service_option, cost=cost, date_taken=date_taken)

        return redirect('cost_diagram')

    else:
        service_options = ServiceOption.objects.all()
        total_cost = CostDiagram.objects.filter(user=request.user).aggregate(total_cost=Sum('cost'))['total_cost'] or 0

        cost_by_percentage = {}
        for option in service_options:
            total_cost_for_option = CostDiagram.objects.filter(user=request.user, service_option=option).aggregate(total_cost=Sum('cost'))['total_cost'] or 0
            cost_percentage = (total_cost_for_option / total_cost * 100) if total_cost > 0 else 0
            cost_by_percentage[option.option_name] = round(cost_percentage, 2)

        context = {
            'service_options': service_options,
            'total_cost': total_cost,
            'cost_by_percentage': cost_by_percentage,
            'option_choices': ServiceOption.OPTION_CHOICES
        }
        return render(request, 'cost_diagram.html', context)
