import builtins


class FileNotFoundError(builtins.FileNotFoundError):
    def __init__(self, filename: str):
        super().__init__(f"File `{filename}` does not exist")


class FileExistsError(builtins.FileExistsError):
    def __init__(self, filename: str):
        super().__init__(f"File `{filename}` already exists")
