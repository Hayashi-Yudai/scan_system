from django.test import TestCase, Client
from unittest import mock
import json
import os

from core.models import TDSData
from core.forms import SaveDataForm, MoveStepStageForm, StepScanSettingForm


class GPIBAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    @mock.patch("core.views.api_ops.set_lockin_sensitivity")
    def test_change_sensitivity_gpib_failure(self, mock_set_lockin_sensitivity):
        mock_set_lockin_sensitivity.return_value = False
        response = self.client.post(
            "/core/change-sensitivity/", {"unit": 100, "milli-volt": "milli-volt"}
        )
        self.assertEqual(response.status_code, 400)

    @mock.patch("core.views.api_ops.set_lockin_time_const")
    def test_time_const_gpib_failure(self, mock_set_lockin_time_const):
        mock_set_lockin_time_const.return_value = False
        response = self.client.post(
            "/core/change-sensitivity/", {"val": 100, "unit": "milli-sec"}
        )
        self.assertEqual(response.status_code, 400)


class SaveDataFormTest(TestCase):
    def setUp(self):
        self.home_drive = os.getenv("HOMEDRIVE")
        self.home_path = os.getenv("HOMEPATH")

    def test_correct_form(self):

        data = {
            "filename": self.home_drive + self.home_path + "/Desktop/a.csv",
            "measure_type": "STEP",
        }
        form = SaveDataForm(data)

        self.assertTrue(form.is_valid())

    def test_bad_keyname(self):
        data = {
            "badkey": self.home_drive + self.home_path + "/Desktop/a.csv",
            "measure_type": "STEP",
        }
        form = SaveDataForm(data)

        self.assertFalse(form.is_valid())

    def test_bad_measure_type(self):
        data = {
            "filename": self.home_drive + self.home_path + "/Desktop/a.csv",
            "measure_type": "BADKEY",
        }
        form = SaveDataForm(data)

        self.assertFalse(form.is_valid())

    def test_bad_filename(self):
        data = {
            "filename": self.home_drive + self.home_path + "/Desktop/",
            "measure_type": "STEP",
        }
        form = SaveDataForm(data)

        self.assertFalse(form.is_valid())

    def test_non_existing_dir(self):
        data = {
            "filename": "/not/existing/dir/test.csv",
            "measure_type": "STEP",
        }
        form = SaveDataForm(data)

        self.assertFalse(form.is_valid())


class MoveStepStageFormTest(TestCase):
    def test_form_valid(self):
        form = MoveStepStageForm({"position": 100})
        self.assertTrue(form.is_valid())

    def test_non_interger_input_fails(self):
        form = MoveStepStageForm({"position": 0.1})
        self.assertFalse(form.is_valid())

        form = MoveStepStageForm({"position": "abc"})
        self.assertFalse(form.is_valid())

    def test_negative_position_fail(self):
        form = MoveStepStageForm({"position": -100})
        self.assertFalse(form.is_valid())

    def test_zero_position_is_valid(self):
        form = MoveStepStageForm({"position": 0})
        self.assertTrue(form.is_valid())

    def test_valid_keyname_fails(self):
        form = MoveStepStageForm({"positions": 0})
        self.assertFalse(form.is_valid())


class StepScanSettingFormTest(TestCase):
    def test_form_valid(self):
        form = StepScanSettingForm({"start": 0, "end": 10, "step": 5, "lockin": 300})
        self.assertTrue(form.is_valid())

    def test_negative_value_invalid(self):
        form = StepScanSettingForm({"start": -1, "end": 10, "step": 5, "lockin": 300})
        valid = form.is_valid()
        self.assertFalse(valid)

        form = StepScanSettingForm({"start": 0, "end": -10, "step": 5, "lockin": 300})
        self.assertFalse(form.is_valid())

        form = StepScanSettingForm({"start": 0, "end": 10, "step": -5, "lockin": 300})
        self.assertFalse(form.is_valid())

        form = StepScanSettingForm({"start": 0, "end": 10, "step": -5, "lockin": -300})
        self.assertFalse(form.is_valid())

    def test_start_must_smaller_than_end(self):
        form = StepScanSettingForm({"start": 10, "end": 0, "step": 5, "lockin": 300})
        self.assertFalse(form.is_valid())


class DataSavingTest(TestCase):
    def setUp(self):
        self.client = Client()
        TDSData.objects.create(
            measure_type="STEP", position_data="1,2,3", intensity_data="1,2,3"
        )

    @mock.patch("core.views.api_ops.save_data_as_csv")
    def test_save_data(self, mock_save_data_as_csv):
        # Set up
        mock_save_data_as_csv.return_value = None

        # Test
        response = self.client.post(
            "/core/save/", {"filename": "./test.csv", "measure_type": "STEP"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["success"], True)


class CalculationTest(TestCase):
    def setUp(self):
        self.client = Client()
        TDSData.objects.create(position_data="1,2,3", intensity_data="1,2,3")

    def test_calc_fft_bad_param_fail(self):
        response = self.client.post("/core/calc-fft/", {"type": "BAD", "fft": "true"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid parameter")

        response = self.client.post("/core/calc-fft/", {"type": "TDS", "fft": "BAD"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid parameter")


class StepScanTest(TestCase):
    def setUp(self):
        self.client = Client()

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
        self.assertEqual(created_data.measure_type, "STEP")

    def test_tds_boot_lack_parameter_fail(self):
        response = self.client.post(
            "/core/tds-boot/", {"end": 10, "step": 5, "lockin": 300}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid parameter(s)")

    def test_tds_data(self):
        TDSData.objects.create(
            measure_type="STEP",
            position_data="1,2,3",
            intensity_data="1,2,3",
        )
        response = self.client.post("/core/tds-data/")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data["x"], [1, 2, 3])
        self.assertEqual(data["y"], [1, 2, 3])
        self.assertEqual(data["status"], "finished")
