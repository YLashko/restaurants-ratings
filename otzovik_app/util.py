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
