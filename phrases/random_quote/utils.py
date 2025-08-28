import random
from .models import Quote


def get_random_quote():
    quotes = list(Quote.objects.all())
    if not quotes: return None
    weights = [quote.weight for quote in quotes]
    return random.choices(quotes, weights=weights, k=1)[0]