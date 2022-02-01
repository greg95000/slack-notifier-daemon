class ServiceInterface:
    """The service interface to implement all the services, it ensure that the service implement the run method"""

    def __init__(self, *args, **kwargs) -> None:
        pass

    def run(self, status, user=None):
        raise NotImplementedError()
