from django.test import TestCase, Client
import json

from core.models import TDSData


class TestArchive(TestCase):
    def setUp(self):
        self.client = Client()

        TDSData.objects.create(
            start_position=0,
            end_position=10,
            step=5,
            lockin_time=300,
            position_data="1,2,3",
            intensity_data="1,4,9",
            file_name="",
        )

    def test_get_archive_data(self):
        response = self.client.post(
            "/archive/get_archive_data/", {"pk": 1, "fft": "false"}
        )
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual(response_json["x"], [1, 2, 3])
        self.assertEqual(response_json["y"], [1, 4, 9])

        response = self.client.post(
            "/archive/get_archive_data/", {"pk": 1, "fft": "true"}
        )
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual(len(response_json["x"]), 4096)
        self.assertEqual(len(response_json["y"]), 4096)

        for fft_value in response_json["y"]:
            self.assertEqual(fft_value.imag, 0)

        # Resource not found
        response = self.client.post(
            "/archive/get_archive_data/", {"pk": 100, "fft": "true"}
        )
        self.assertEqual(response.status_code, 404)

        # Bad request
        response = self.client.post("/archive/get_archive_data/", {"pk": 1})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid parameter(s)")

        response = self.client.post("/archive/get_archive_data/", {"pk": "bad request"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid parameter(s)")

        response = self.client.post("/archive/get_archive_data/", {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid parameter(s)")

        response = self.client.post("/archive/get_archive_data/", {"bad": "request"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid parameter(s)")

    def test_calc_fft(self):
        response = self.client.post(
            "/archive/calc-fft/",
            content_type="application/json",
            data={"ids": [1], "fft": True},
        )
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json["xs"][0]), 4096)
        self.assertEqual(len(response_json["ys"][0]), 4096)

        for fft_value in response_json["ys"][0]:
            self.assertEqual(fft_value.imag, 0)

        response = self.client.post(
            "/archive/calc-fft/",
            content_type="application/json",
            data={"ids": [1], "fft": False},
        )
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["xs"][0], [1, 2, 3])
        self.assertEqual(response_json["ys"][0], [1, 4, 9])

        # Resoure not found
        response = self.client.post(
            "/archive/calc-fft/",
            content_type="application/json",
            data={"ids": [1, 100], "fft": False},
        )
        self.assertEqual(response.status_code, 404)

        # Bad requests
        response = self.client.post(
            "/archive/calc-fft/",
            content_type="application/json",
            data={"ids": 1, "fft": False},
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            "/archive/calc-fft/",
            content_type="application/json",
            data={"ids": [1]},
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            "/archive/calc-fft/",
            content_type="application/json",
            data={"fft": True},
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            "/archive/calc-fft/",
            content_type="application/json",
            data={},
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            "/archive/calc-fft/",
            content_type="application/json",
            data={"ids": ["1"]},
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            "/archive/calc-fft/",
            content_type="application/json",
            data={"ids": [1], "fft": "bad"},
        )
        self.assertEqual(response.status_code, 400)
