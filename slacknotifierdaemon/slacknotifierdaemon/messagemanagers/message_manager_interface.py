class MessageManagerInterface:
    def __init__(self, status: dict = {}) -> None:
        self.status = status

    def parse_message(self, message: str):
        raise NotImplementedError()
