from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Quote, Source
from .forms import QuoteForm
from .utils import get_random_quote

def random_quote(request):
    quote = get_random_quote()
    if quote is None:
        return render(request, 'quotes/empty.html')
    quote.views += 1
    quote.save()

    csrf_token = get_token(request)
    context = {
        'quote': quote,
        'total_quotes': Quote.objects.count(),
        'total_sources': Source.objects.count(),
        'csrf_token': csrf_token,
    }
    return render(request, 'quotes/random_quote.html', {'quote': quote})


@require_POST
@csrf_exempt
def rate_quote(request):
    quote_id = request.POST.get('quote_id')
    action = request.POST.get('action')

    if not quote_id or not action:
        return JsonResponse({'status': 'error', 'message': 'Missing parameters'})

    try:
        quote = Quote.objects.get(id=quote_id)

        if action == 'like':
            quote.likes += 1
        elif action == 'dislike':
            quote.dislikes += 1
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'})

        quote.save()

        return JsonResponse({
            'status': 'success',
            'likes': quote.likes,
            'dislikes': quote.dislikes
        })

    except Quote.DoesNotExist:
        return {'status': 'error', 'message': 'Quote not found'}

def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('random_quote')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})

def top_quotes(request):
    source_type = request.GET.get('type', 'all')
    sort_by = request.GET.get('sort', 'likes')

    quotes = Quote.objects.all()

    if source_type != 'all':
        quotes = quotes.filter(source__from_where=source_type)

    if sort_by == 'views':
        quotes = quotes.order_by('-views')
    else:
        quotes = quotes.order_by('-likes')

    quotes = quotes[:10]

    context = {
        'quotes': quotes,
        'current_type': source_type,
        'current_sort': sort_by,
        'source_types': Source.SOURCE_TYPES,
    }

    return render(request, 'quotes/top_quotes.html', context)