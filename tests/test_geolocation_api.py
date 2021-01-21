from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, APIClient
import responses
import json

from environs import Env

env = Env()
env.read_env()


class TestGeolocationApi(TestCase):
    def setUp(self):
        """Set up test class."""
        self.client = Client()
        self.factory = APIRequestFactory()
        self.geo_url = f"{env.str('GEOLOCATION_URL')}/v1/geolocate?key={env.str('GEOLOCATION_KEY')}"

    @responses.activate
    def test_create_georesults_new(self):
        mock_response = {
          "accuracy": 30,
          "location": {
            "lat": -33.920480999999995,
            "lng": 25.591107599999997
          }
        }
        test_ap_data = {
            "apscan_data": [
                {
                    "band": "2.4",
                    "bssid": "aa:aa:aa:aa:aa:aa",
                    "channel": "5",
                    "frequency": 2432,
                    "rates": "1.0 - 135.0 Mbps",
                    "rssi": -44,
                    "security": "wpa-psk",
                    "ssid": "HUAWEI-B315-C1BE",
                    "timestamp": 1522886948.0,
                    "vendor": "HUAWEI TECHNOLOGIES CO.,LTD",
                    "width": "20"
                }
            ]
        }
        responses.add(responses.POST, self.geo_url, status=200,json=mock_response)
        response = self.client.post('/georesults/', json.dumps(test_ap_data), content_type="application/json")
        self.assertEqual(json.dumps(mock_response).encode(), response.content)

    @responses.activate
    def test_create_georesults_with_existing_data(self):
        mock_response = {
          "accuracy": 30,
          "location": {
            "lat": -33.920480999999995,
            "lng": 25.591107599999997
          }
        }
        test_ap_data = {
            "apscan_data": [
                {
                    "band": "2.4",
                    "bssid": "aa:aa:aa:aa:aa:aa",
                    "channel": "5",
                    "frequency": 2432,
                    "rates": "1.0 - 135.0 Mbps",
                    "rssi": -44,
                    "security": "wpa-psk",
                    "ssid": "HUAWEI-B315-C1BE",
                    "timestamp": 1522886948.0,
                    "vendor": "HUAWEI TECHNOLOGIES CO.,LTD",
                    "width": "20"
                }
            ]
        }
        responses.add(responses.POST, self.geo_url, status=200,json=mock_response)
        self.client.post('/georesults/', json.dumps(test_ap_data), content_type="application/json")
        response = self.client.post('/georesults/', json.dumps(test_ap_data), content_type="application/json")
        self.assertEqual(json.dumps(mock_response).encode(), response.content)

    @responses.activate
    def test_create_georesults_with_missing_data(self):
        mock_response = {
            "accuracy": 30,
            "location": {
                "lat": -33.920480999999995,
                "lng": 25.591107599999997
            }
        }
        test_ap_data = {
            "apscan_data": [
                {
                    "id": 3,
                    "band": "2.4",
                    "bssid": "aa:aa:aa:aa:aa:aa",
                    "channel": "5",
                    "frequency": 2432,
                    "rates": "1.0 - 135.0 Mbps",
                    "rssi": -44,
                    "security": "wpa-psk",
                    "ssid": "HUAWEI-B315-C1BE",
                    "timestamp": 1522886948.0,
                    "vendor": "HUAWEI TECHNOLOGIES CO.,LTD",
                    "width": "20"
                }
            ]
        }
        responses.add(responses.POST, self.geo_url, status=200, json=mock_response)
        self.client.post('/georesults/', json.dumps(test_ap_data), content_type="application/json")
        response = self.client.get('/georesults/')
        expected_result = test_ap_data["apscan_data"]
        expected_result[0]["geolocation"] = mock_response
        self.assertListEqual(expected_result, json.loads(response.content.decode()))
