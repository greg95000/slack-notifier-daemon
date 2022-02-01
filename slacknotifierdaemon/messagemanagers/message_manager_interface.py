class MessageManagerInterface:
    """The MessageManager is the manager of slack message, it will consume the date to return the status and the user.
    This class is the interface for all the MessageManager which must implement parse_message
    """

    def __init__(self, status: dict = {}) -> None:
        """Init the MessageManager

        Args:
            status (dict, optional): [description]. Defaults to {}.
        """
        self.status = status

    def parse_message(self, message: str):
        """Parse the message to produce value required for the services of the devices

        Args:
            message (str): The message to consume

        Raises:
            NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError()
