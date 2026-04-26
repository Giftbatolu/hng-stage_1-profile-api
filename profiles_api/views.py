from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pycountry

from .models import Profile
from .services import fetch_external_data
from .utils import get_age_group, get_top_country, format_profile, format_profile_list, apply_sort_and_paginate
from .filters import ProfileFilter

def error(message, code):
    return Response({"status": "error", "message": message}, status=code)

class HomeView(APIView):
    def get(self, request):
         return Response({
        "status": "success",
        "message": "Profile API is live",
        "endpoints": {
            "create_profile": "/api/profiles",
            "get_all_profiles": "/api/profiles",
            "get_single_profile": "/api/profiles/{id}",
            "delete_profile": "/api/profiles/{id}"
        }
    })

class ProfileListCreateView(APIView):
    def post(self, request):
        name = request.data.get("name")

        if name is None or name.strip() == "":
            return error("Missing or empty name", 400)
        
        if not isinstance(name, str):
            return error("Invalid type", 422)

        name = name.strip().lower()
        
        existing = Profile.objects.filter(name__iexact=name).first()
        if existing:
            return Response({
                "status": "success",
                "message": "Profile already exists",
                "data": format_profile(existing)
            }, status=200)

        data, err = fetch_external_data(name)
        if err:
            return error(err, 502)
        
        age_value = data["age"]["age"]
        age_group = get_age_group(age_value)

        top_country = get_top_country(data["nation"])
        if not top_country:
            return error("Nationalize returned an invalid response", 502)
        
        country_id = top_country["country_id"]
        country = pycountry.countries.get(alpha_2=country_id)
        country_name = country.name if country else country_id

        profile = Profile.objects.create(
            name=name,
            gender=data["gender"]["gender"],
            gender_probability=data["gender"]["probability"],
            age=age_value,
            age_group=age_group,
            country_id=country_id,
            country_name=country_name,
            country_probability=top_country["probability"]
        )
        
        return Response({
            "status": "success",
            "data": format_profile(profile)
        }, status=201)

    def get(self, request):
        queryset = ProfileFilter(request.GET, queryset=Profile.objects.all()).qs

        result = apply_sort_and_paginate(request, queryset)
        data = [format_profile_list(p) for p in result["objects"]]

        return Response({
            "status": "success",
            "page": result["page"],
            "limit": result["limit"],
            "total": result["total"],
            "data": data
        }, status=200)

class ProfileDetailView(APIView):

    def get_object(self, id):
        try:
            return Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return None

    def get(self, request, id):
        profile = self.get_object(id)
        if not profile:
            return error("Profile not found", 404)

        return Response({
            "status": "success",
            "data": format_profile(profile)
        }, status=200)

    def delete(self, request, id):
        profile = self.get_object(id)
        if not profile:
            return error("Profile not found", 404)

        profile.delete()
        return Response(status=204)