class ServiceInterface:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def run(self, status, user=None):
        raise NotImplementedError()
