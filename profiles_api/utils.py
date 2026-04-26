from django.core.paginator import Paginator

def get_age_group(age):
    if age is None:
        return None

    if age <= 12:
        return "child"
    elif age <= 19:
        return "teenager"
    elif age <= 59:
        return "adult"
    return "senior"


def get_top_country(nation_data):
    countries = nation_data.get("country", [])
    if not countries:
        return None

    return max(countries, key=lambda x: x["probability"])


def format_profile(profile):
    return {
        "id": str(profile.id),
        "name": profile.name,
        "gender": profile.gender,
        "gender_probability": profile.gender_probability,
        "age": profile.age,
        "age_group": profile.age_group,
        "country_id": profile.country_id,
        "country_name": profile.country_name,
        "country_probability": profile.country_probability,
        "created_at": profile.created_at.isoformat()
    }


def format_profile_list(profile):
    return {
        "id": str(profile.id),
        "name": profile.name,
        "gender": profile.gender,
        "age": profile.age,
        "age_group": profile.age_group,
        "country_id": profile.country_id
    } 

def apply_sort_and_paginate(request, queryset):
    sort_by = request.GET.get("sort_by", "created_at")
    order = request.GET.get("order", "asc")

    allowed_sort_fields = [
        "age",
        "created_at",
        "gender_probability"
    ]

    if sort_by in allowed_sort_fields:
        if order == "desc":
            sort_by = f"-{sort_by}"
        queryset = queryset.order_by(sort_by)

    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1
    limit = min(int(request.GET.get("limit", 10)), 50)

    paginator = Paginator(queryset, limit)
    page_obj = paginator.get_page(page)

    return {
        "page": page,
        "limit": limit,
        "total": paginator.count,
        "objects": page_obj
    }