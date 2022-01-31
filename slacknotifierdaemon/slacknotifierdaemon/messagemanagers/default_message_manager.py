from slacknotifierdaemon.slacknotifierdaemon.messagemanagers.message_manager_interface import (
    MessageManagerInterface,
)
import re


class DefaultMessageManager(MessageManagerInterface):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.status = kwargs.get("status", {})

    def parse_message(self, message: str):
        for status in self.status:
            regexes = self.status[status]["regexes"]
            for regex in regexes:
                if re.search(message, regex):
                    return status
        return None
