from django.db import models


class GeoResults(models.Model):
    """
    Georesults to hold the results so that caching can occur.

    :attribute bssid: The bssid passed through from the AP Scan.
    :attribute ssid: Name of the ssid passed through from the AP Scan.
    :attribute vendor: Name of the vendor passed through from the AP Scan.
    :attribute geolocation: Longitude, latitude and accuracy received from geolocation api.
    """
    bssid = models.CharField(max_length=17)
    ssid = models.CharField(max_length=256)
    vendor = models.CharField(max_length=256)
    band = models.CharField(max_length=8, default=None)
    channel = models.CharField(max_length=8)
    frequency = models.IntegerField(default=None)
    rates = models.CharField(max_length=256)
    rssi = models.IntegerField()
    security = models.CharField(max_length=256)
    timestamp = models.FloatField()
    width = models.CharField(max_length=8)
    geolocation = models.JSONField()

    @classmethod
    def get_latest(cls, bssid, ssid):
        """Return the latest object matching the bssid and ssid."""
        try:
            latest_results = cls.objects.get(
                bssid=bssid,
                ssid=ssid
            )
            return latest_results
        except:
            return None
