class Error():
    def __init__(self, error, about):
        self.error = error
        self.about = about

    def as_string(self, line_number=None):
        error_message = f"{self.error}: {self.about}"
        if line_number is not None:
            error_message += f"\nError occurred on line {line_number}"
        print(error_message)


class SyntaxError(Error):
    def __init__(self, about, line_number=None):
        super().__init__("SyntaxError", about)
        self.as_string(line_number)

class UnknowTypeError(Error):
    def __init__(self, about, line_number=None):
        super().__init__("UnknowTypeError", about)
        self.as_string(line_number)
class UnknowDependenciesError(Error):
    def __init__(self, about, line_number=None):
        super().__init__("UnknowDependenciesError", about)
        self.as_string(line_number)
