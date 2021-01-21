"""Views model for geolocation api"""
import logging
from rest_framework import viewsets
from .serializers import GeoResultsSerializer
from .models import GeoResults
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
import requests
from django.forms.models import model_to_dict

from environs import Env

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

env = Env()
env.read_env()


class GeoResultsView(viewsets.ModelViewSet):
    queryset = GeoResults.objects.all()
    serializer_class = GeoResultsSerializer

    def create(self, request: Request, *args, **kwargs):
        """
        Extend http post method from the ModelViewSet.

        Checks if data already exist and transforms incoming request data and then calls a create.
        """
        apscan_data = request.data['apscan_data']
        existing_data = None
        collected_data = {
          "considerIp": 'false',
          "wifiAccessPoints": []
        }
        geolocation = None
        for ap in apscan_data:
            self.validate_dict_contains_required_fields(ap, ["bssid", "ssid"])
            existing_data = GeoResults.get_latest(ap["bssid"], ap["ssid"])
            if existing_data:
                logger.info("Found existing results.")
                geolocation = model_to_dict(existing_data)['geolocation']
            elif geolocation:
                logger.info("Found existing results but some GeoResults have not yet been created")
                logger.info("Creating the GeoResults.")
                result = ap
                result["geolocation"] = geolocation
                a = GeoResults(
                    **result
                )
                a.save()
            else:
                collected_data["wifiAccessPoints"].append({
                    "macAddress": ap["bssid"],
                    "signalStrength": ap["rssi"],
                    "signalToNoiseRatio": 0
                })
        if not existing_data:
            url = f"{env.str('GEOLOCATION_URL')}/v1/geolocate?key={env.str('GEOLOCATION_KEY')}"
            logger.info(f"Couln't find any previous results. Fetching data now from {url}")
            geolocation_request = requests.post(url, json=collected_data)
            geolocation = geolocation_request.json()
            for ap in apscan_data:
                result = ap
                result["geolocation"] = geolocation
                a = GeoResults(
                    **result
                )
                a.save()
        return JsonResponse(geolocation)

    @staticmethod
    def validate_dict_contains_required_fields(
            raw_dict: dict,
            required_fields: list,
    ) -> None:
        """
        Validate all fields in the given list are in the dictionary.

        Intended use is on the paramater dictionary where all field values would be of a
        known type.
        :param raw_dict: raw dictionary to validate.
        :param required_fields: fields required to be present in the raw_dict
        :raise: ValidationError
        """
        missing_fields = []
        for item in required_fields:
            if item not in raw_dict:
                missing_fields.append(item)
        if missing_fields:
            raise ValidationError(f"Missing fields {missing_fields}.")
