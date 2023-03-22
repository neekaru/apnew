from bs4 import BeautifulSoup


class Parser:
    def __init__(self, data):
        self.data = data

    def get_bs4(self) -> BeautifulSoup | None:
        try:
            return BeautifulSoup(self.data, "html.parser")
        except Exception:
            return None


class Parser_help:
    def __init__():
        pass

    @staticmethod
    def extract_form_data(form) -> dict[str, str]:
        """Extracts data from a form element.
        Args:
            form: The form element to extract data from.
        Returns:
            A dictionary mapping form input names to their values.
        """
        data = {}
        for input_element in form.find_all("input"):
            name = input_element.get("name")
            value = input_element.get("value")
            data[name] = value
        return data
