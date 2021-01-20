from rest_framework import serializers

from .models import GeoResults


class GeoResultsSerializer(serializers.ModelSerializer):
    """Standard ModelSerializer for the GeoResult model."""

    class Meta:
        model = GeoResults
        fields = ('id', 'bssid', 'ssid', 'vendor', 'geolocation', 'band', 'channel',
                  'frequency', 'rates', 'rssi', 'security', 'timestamp', 'width')
