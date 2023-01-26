import django.forms.utils
from django.forms import ModelForm


def calculate_pages(items, items_per_page, current_page):  # delete, not used
    max_page = (items - 1) // items_per_page
    min_page = 0 if current_page > 0 else "NaN"
    prev_page = current_page - 1 if current_page > 0 else "NaN"
    next_page = current_page + 1 if current_page < max_page else "NaN"
    max_page = max_page if current_page < max_page else "NaN"
    return min_page, max_page, prev_page, next_page


def collect_forms_errors(forms: list[ModelForm]):
    errors_str = ''
    for form in forms:
        errors = form.errors.as_data()
        for name, error_list in errors.items():
            errors_str += f"{name}: "
            for error in error_list:
                errors_str += "".join(error.messages)
    return errors_str
