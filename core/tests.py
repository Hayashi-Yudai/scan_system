from django.test import TestCase, Client
from django.urls import resolve
from unittest import mock
import json

# import time
# import threading

from core.models import TemporalData, TDSData
from core import views


class JsonAPITest(TestCase):
    def setUp(self):
        self.client = Client()

        TemporalData.objects.create(
            data_type="TDS", position_data="1,2,3", intensity_data="1,2,3"
        )
        TemporalData.objects.create(
            data_type="RAPID", position_data="1,2,3", intensity_data="1,2,3"
        )
        TDSData.objects.create(
            start_position=0,
            end_position=10,
            step=1,
            lockin_time=300,
            position_data="1,2,3",
            intensity_data="1,2,3",
        )

    @mock.patch("core.views.api_ops.move_stage")
    def test_move_stage(self, mock_move_stage):
        mock_move_stage.return_value = True
        response = self.client.post("/core/move/", {"position": 100})
        success = json.loads(response.content)["success"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(success, True)

        mock_move_stage.return_value = False
        response = self.client.post("/core/move/", {"position": 100})
        success = json.loads(response.content)["success"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(success, False)

        # Bad parameters
        response = self.client.post("/core/move/", {"position": -100})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"'position' must be positive or zero")

        response = self.client.post("/core/move/", {"position": "bad request"})
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/core/move/", {"positions": 100})
        self.assertEqual(response.status_code, 400)

    @mock.patch("core.views.api_ops.save_data_as_csv")
    def test_save_data(self, mock_save_data_as_csv):
        # Set up
        mock_save_data_as_csv.return_value = None

        # Test
        response = self.client.post(
            "/core/save/", {"path": "./test.csv", "type": "TDS"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["success"], True)

        response = self.client.post(
            "/core/save/", {"path": "./test.csv", "type": "RAPID"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["success"], True)

        # Bad requests
        response = self.client.post(
            "/core/save/", {"paths": "./test.csv", "type": "TDS"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid parameter")

        response = self.client.post("/core/save/", {"path": ".", "type": "TDS"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid path")

        response = self.client.post(
            "/core/save/", {"path": "/not/existing/path", "type": "TDS"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid path")

        response = self.client.post(
            "/core/save/", {"path": "./test.csv", "type": "BadType"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid parameter")

    def test_scan(self):
        pass

    @mock.patch("core.views.api_ops.get_lockin_intensity")
    def test_gpib(self, mock_get_lockin_intensity):
        mock_get_lockin_intensity.return_value = (0.0, True)

        response = self.client.post("/core/gpib/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["intensity"], 0.0)
        self.assertEqual(json.loads(response.content)["connection"], True)

    @mock.patch("core.views.api_ops.calc_fft")
    def test_calc_fft(self, mock_calc_fft):
        # Set up
        mock_calc_fft.return_value = ([], [])

        response = self.client.post("/core/calc-fft/", {"type": "TDS", "fft": "false"})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["x"], [1, 2, 3])
        self.assertEqual(data["y"], [1, 2, 3])

        response = self.client.post("/core/calc-fft/", {"type": "TDS", "fft": "true"})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["x"], [])
        self.assertEqual(data["y"], [])

        # Bad requests
        response = self.client.post("/core/calc-fft/", {"type": "BAD", "fft": "true"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid parameter")

        response = self.client.post("/core/calc-fft/", {"type": "TDS", "fft": "BAD"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid parameter")

    @mock.patch("core.views.api_ops.tds_scan")
    def test_tds_boot(self, mock_tds_scan):
        # Set up
        mock_tds_scan.return_value = True

        # Test
        response = self.client.post(
            "/core/tds-boot/", {"start": 0, "end": 10, "step": 5, "lockin": 300}
        )
        self.assertEqual(response.status_code, 200)

        # Check the data is saved in database correctly
        created_data = TDSData.objects.all().order_by("-measured_date").first()
        self.assertEqual(created_data.start_position, 0)
        self.assertEqual(created_data.end_position, 10)
        self.assertEqual(created_data.step, 5)
        self.assertEqual(created_data.lockin_time, 300)
        self.assertEqual(created_data.position_data, "")
        self.assertEqual(created_data.intensity_data, "")
        self.assertEqual(created_data.file_name, "")

        # Bad request
        response = self.client.post(
            "/core/tds-boot/", {"end": 10, "step": 5, "lockin": 300}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid parameter(s)")

    def test_tds_data(self):
        response = self.client.post("/core/tds-data/")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data["x"], [1, 2, 3])
        self.assertEqual(data["y"], [1, 2, 3])
        self.assertEqual(data["status"], "finished")

    @mock.patch("core.views.api_ops.tds_scan")
    def test_tds_running_value(self, mock_tds_scan):
        # TODO: Resolve django.db.utils.OperationalError: database table is locked
        # This error occurrs even when running one thread
        """
        # Set up
        mock_tds_scan = lambda: time.sleep(3)
        TemporalData.objects.create(
            data_type="TDS", position_data="1,2,3", intensity_data="1,2,3"
        )

        def task():
            return self.client.post(
                "/core/tds-boot/", {"start": 0, "end": 10, "step": 5, "lockin": 300}
            )

        thread = threading.Thread(target=task)
        # Test
        response = self.client.post("/core/tds-data/")

        data = json.loads(response.content)
        self.assertEqual(data["status"], "finished")

        thread.start()
        response = self.client.post("/core/tds-data/")

        data = json.loads(response.content)
        self.assertEqual(data["status"], "running")

        thread.join()
        response = self.client.post("/core/tds-data/")

        data = json.loads(response.content)
        self.assertEqual(data["status"], "finished")
        """
        pass

    @mock.patch("core.views.api_ops.set_lockin_sensitivity")
    def test_change_sensitivity(self, mock_set_lockin_sensitivity):
        mock_set_lockin_sensitivity.return_value = None

        response = self.client.post(
            "/core/change-sensitivity/", {"value": 100, "unit": "milli-volt"}
        )
        self.assertEqual(response.status_code, 200)

        # Bad requests
        response = self.client.post("/core/change-sensitivity/", {"unit": "milli-volt"})
        self.assertEqual(response.status_code, 400)

    @mock.patch("core.views.api_ops.set_lockin_time_const")
    def test_time_const(self, mock_set_lockin_time_const):
        mock_set_lockin_time_const.return_value = None

        response = self.client.post(
            "/core/change-time-const/", {"value": 100, "unit": "milli-sec"}
        )
        self.assertEqual(response.status_code, 200)

        # Bad requests
        response = self.client.post("/core/change-sensitivity/", {"unit": "milli-sec"})
        self.assertEqual(response.status_code, 400)

    @mock.patch("core.views.api_ops.auto_phase_lockin")
    def test_auto_phase(self, mock_auto_phase_lockin):
        mock_auto_phase_lockin.return_value = None

        response = self.client.post("/core/auto-phase/")
        self.assertEqual(response.status_code, 200)


class URLTest(TestCase):
    def test_root(self):
        self.assertEqual(resolve("/core/").func.view_class, views.RapidScan)

    def test_step(self):
        self.assertEqual(resolve("/core/step/").func.view_class, views.StepScan)

    def test_move(self):
        self.assertEqual(resolve("/core/move/").func, views.move)

    def test_save(self):
        self.assertEqual(resolve("/core/save/").func, views.save)

    def test_scan(self):
        self.assertEqual(
            resolve("/core/start_rapid_scan/").func, views.start_rapid_scan
        )

    def test_gpib(self):
        self.assertEqual(resolve("/core/gpib/").func, views.gpib)

    def test_calc_fft(self):
        self.assertEqual(resolve("/core/calc-fft/").func, views.calc_fft)

    def test_tds_data(self):
        self.assertEqual(resolve("/core/tds-data/").func, views.tds_data)

    def test_tds_boot(self):
        self.assertEqual(resolve("/core/tds-boot/").func, views.tds_boot)

    def test_change_sensitivity(self):
        self.assertEqual(
            resolve("/core/change-sensitivity/").func, views.change_sensitivity
        )

    def test_change_time_const(self):
        self.assertEqual(
            resolve("/core/change-time-const/").func, views.change_time_const
        )

    def test_auto_phase(self):
        self.assertEqual(resolve("/core/auto-phase/").func, views.auto_phase)

    def test_rapid_scan_data(self):
        self.assertEqual(resolve("/core/rapid-scan-data/").func, views.rapid_scan_data)

    def test_get_rapid_data(self):
        self.assertEqual(
            resolve("/core/get-rapid-data/").func, views.send_rapid_data_to_front
        )


class TestTDSDataModel(TestCase):
    def test_is_empty(self):
        entry = TDSData.objects.all()
        self.assertEqual(entry.count(), 0)

    def test_create_entry(self):
        TDSData.objects.create(
            start_position=0,
            end_position=10,
            step=5,
            lockin_time=300,
            position_data="1,2,3",
            intensity_data="1,2,3",
            file_name="",
        )
        entry = TDSData.objects.all()
        self.assertEqual(entry.count(), 1)
