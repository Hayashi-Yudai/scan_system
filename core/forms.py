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
