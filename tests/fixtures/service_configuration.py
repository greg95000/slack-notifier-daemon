import pytest


@pytest.fixture
def service_config_empty_data():
    return {}


@pytest.fixture
def devices_config_data():
    return {
        "arduino": {
            "service": {
                "name": "ArduinoService",
                "port": "COM1",
                "baudrate": 192500,
            }
        },
        "philips-hue": {
            "service": {
                "name": "PhilipsHueService",
                "ip_address": "192.168.0.0",
                "lamps": [1, 2],
                "status": {
                    "ALERT": {"color": 984427},
                    "WARNING": {"color": 16770102},
                    "OK": {"color": 2258959},
                },
            }
        },
    }


@pytest.fixture
def device_config_data():
    return {
        "arduino": {
            "service": {
                "name": "ArduinoService",
                "port": "COM2",
                "baudrate": 192500,
            }
        }
    }


@pytest.fixture
def channels_config_data():
    return {
        "channels": {
            "test_name1": {
                "message-manager": {
                    "status": {
                        "ALERT": {"regexes": ["test"]},
                        "WARNING": {"regexes": ["blop", "blop3"]},
                        "OK": {"regexes": ["blop2"]},
                    }
                },
                "devices": {
                    "arduino": {
                        "service": {
                            "name": "ArduinoService",
                            "port": "COM1",
                            "baudrate": 192500,
                        }
                    },
                    "philips-hue": {
                        "service": {
                            "name": "PhilipsHueService",
                            "ip_address": "192.168.0.0",
                            "lamps": ["test", "test"],
                            "status": {
                                "ALERT": {"color": 984427},
                                "WARNING": {"color": 16770102},
                                "OK": {"color": 2258959},
                            },
                        }
                    },
                },
            },
            "test_name2": {},
        }
    }


@pytest.fixture
def channels_from_slack_data():
    return {
        "channels": [
            {
                "id": "test_id1",
                "is_channel": True,
                "name": "test_name1",
                "purpose": {"value": "test_description"},
            },
        ]
    }
