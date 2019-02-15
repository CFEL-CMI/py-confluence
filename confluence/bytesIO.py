import io


def clean_string(string):
    in_tab = "ÄäÜüÖöß :&"
    out_tab = "AaUuOos___"

    translation = string.maketrans(in_tab, out_tab)
    string = string.translate(translation)
    string = ''.join(e for e in string if e.isalnum() or e == "_" or e == ".")
    return string


class BytesIO(io.BytesIO):

    def __init__(self, bytes_str=None, file_name=None):
        self.name = file_name
        super().__init__(bytes_str)

    def __repr__(self):
        return "\'{}\'".format(self._name)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = clean_string(name)
