from .models import *


def calculate_summary(restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    reviews = Review.objects.filter(restaurant=restaurant)
    summary = ReviewSummary.objects.get(restaurant=restaurant)
    fc = list(reviews.values_list('food_quality', flat=True))
    sc = list(reviews.values_list('staff_quality', flat=True))
    pr = list(reviews.values_list('price', flat=True))
    summary.food_quality = round(sum(fc) / len(fc), 1)
    summary.staff_quality = round(sum(sc) / len(sc), 1)
    summary.price = round(sum(pr) / len(pr), 1)
    summary.rating = round(sum([summary.food_quality, summary.staff_quality, summary.price]) / 3, 1)
    summary.save()


def calculate_pages(items, items_per_page, current_page):
    max_page = (items - 1) // items_per_page
    min_page = 0 if current_page > 0 else "NaN"
    prev_page = current_page - 1 if current_page > 0 else "NaN"
    next_page = current_page + 1 if current_page < max_page else "NaN"
    max_page = max_page if current_page < max_page else "NaN"
    return min_page, max_page, prev_page, next_page
