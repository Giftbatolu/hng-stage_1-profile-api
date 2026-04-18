from .models import Profile


def get_filtered_profiles(filters):
    queryset = Profile.objects.all()

    gender = filters.get("gender")
    country_id = filters.get("country_id")
    age_group = filters.get("age_group")

    if gender:
        queryset = queryset.filter(gender__iexact=gender.strip())

    if country_id:
        queryset = queryset.filter(country_id__iexact=country_id.strip())

    if age_group:
        queryset = queryset.filter(age_group__iexact=age_group.strip())

    return queryset