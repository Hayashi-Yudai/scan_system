from django import forms
import os
import logging

logger = logging.getLogger("root")


class SaveDataForm(forms.Form):
    filename = forms.CharField(label="file name")
    measure_type = forms.CharField(label="measure type")

    def __init__(self, *args, **kwargs):
        super(SaveDataForm, self).__init__(*args, **kwargs)
        self.fields["filename"].widget.attrs.update(
            {
                "class": "form-input input-lg",
                "id": "save-area",
            }
        )

    def clean_filename(self):
        filename = self.cleaned_data["filename"]
        if filename is None:
            logger.error("Core.SaveDataForm: path is None")

            self.add_error("filename", "path is None")
            raise forms.ValidationError("path is None")
        elif len(filename) == 0:
            logger.error("Core.SaveDataForm: path is empty")

            self.add_error("filename", "path is empty")
            raise forms.ValidationError("path is empty")
        elif filename.count("/") < 1 or filename.endswith("/"):
            logger.error("Core.SaveDataForm: path is invalid")

            self.add_error("filename", "path is invalid")
            raise forms.ValidationError("path is invalid")

        if filename.startswith("~"):
            filename = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + filename[1:]

        directory = filename.rsplit("/", 1)[0]
        if not os.path.exists(directory):
            logger.error(f"Core.SaveDataForm: {directory} does not exist")

            self.add_error("filename", f"{directory} folder does not exist")
            raise forms.ValidationError("Non-existing directory")

        return filename

    def clean_measure_type(self):
        measure_type = self.cleaned_data["measure_type"]

        if measure_type not in ["STEP", "RAPID"]:
            raise forms.ValidationError("Invalid measure type")

        return measure_type


class MoveStepStageForm(forms.Form):
    position = forms.IntegerField(initial=0)

    def __init__(self, *args, **kwargs):
        super(MoveStepStageForm, self).__init__(*args, **kwargs)

        self.fields["position"].widget.attrs.update(
            {
                "class": "form-input input-lg",
                "id": "stage-position",
            }
        )

    def clean_position(self):
        position = self.cleaned_data["position"]

        if position < 0:
            logger.warning(f"Core.MoveStepStageForm: invalid position={position}")
            raise forms.ValidationError("Invalid position")

        return position


class StepScanSettingForm(forms.Form):
    start = forms.IntegerField()
    end = forms.IntegerField()
    step = forms.IntegerField()
    lockin = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super(StepScanSettingForm, self).__init__(*args, **kwargs)

        self.fields["start"].widget.attrs.update(
            {
                "class": "form-input input-lg",
                "id": "start-position",
                "placeholder": "Start",
            }
        )
        self.fields["end"].widget.attrs.update(
            {"class": "form-input input-lg", "id": "end-position", "placeholder": "End"}
        )
        self.fields["step"].widget.attrs.update(
            {"class": "form-input input-lg", "id": "moving-step", "placeholder": "Step"}
        )
        self.fields["lockin"].widget.attrs.update(
            {"class": "form-input input-lg", "id": "lockin-time"}
        )

    def clean_start(self):
        start = self.cleaned_data["start"]

        if start < 0:
            raise forms.ValidationError(
                "Start position must be greater than or equal to 0"
            )

        return start

    def clean_end(self):
        end = self.cleaned_data["end"]

        if end < 0:
            raise forms.ValidationError(
                "End position must be greater than or equal to 0"
            )

        return end

    def clean_step(self):
        step = self.cleaned_data["step"]

        if step <= 0:
            raise forms.ValidationError("End position must be greater than 0")

        return step

    def clean_lockin_time(self):
        lockin = self.cleaned_data["lockin"]

        if lockin <= 0:
            raise forms.ValidationError("Lockin time must be greater than 0")

        return lockin

    def clean(self):
        try:
            start = self.data["start"]
            end = self.data["end"]
        except KeyError:
            raise forms.ValidationError("required key(s) is lack")

        if end <= start:
            raise forms.ValidationError("End position must be greater than start")

        return self.cleaned_data


class RapidScanSettingForm(forms.Form):
    duration = forms.IntegerField()
    sampling_rate = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(RapidScanSettingForm, self).__init__(*args, **kwargs)

        self.fields["duration"].widget.attrs.update(
            {
                "class": "form-input input-lg",
                "id": "measurement-time-area",
                "name": "measurement-time",
                "placeholder": "Measurement time",
            }
        )
        self.fields["sampling_rate"].widget.attrs.update(
            {
                "class": "form-input input-lg",
                "id": "sampling-rate-area",
                "name": "sampling-rate",
                "placeholder": "Sampling rate",
            }
        )

    def clean_duration(self):
        duration = self.cleaned_data["duration"]
        if duration <= 0:
            raise forms.ValidationError("duration must be positive")

        return duration

    def clean_sampling_rate(self):
        sampling_rate = self.cleaned_data["sampling_rate"]
        if sampling_rate <= 0 or sampling_rate > 100:
            raise forms.ValidationError("invalid sampling rate")

        return sampling_rate
