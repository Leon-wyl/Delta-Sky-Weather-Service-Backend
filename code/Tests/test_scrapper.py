from code.main.scrapper import get_processed_data
import pytest


@pytest.fixture
def test_get_processed_data():
    origin_object = {
        "observations": {
            "data": [
                {
                    "sort_order": 0,
                    "cloud": "-",
                    "cloud_base_m": None,
                    "cloud_oktas": None,
                    "cloud_type_id": None,
                    "cloud_type": "-",
                    "delta_t": 5.3,
                    "gust_kmh": None,
                    "gust_kt": None,
                    "press_tend": "-",
                    "sea_state": "-",
                    "swell_dir_worded": "-",
                    "swell_height": None,
                    "swell_period": None,
                    "vis_km": "-",
                    "weather": "-",
                },
            ],
        },
    }
    assert get_processed_data(origin_object) == {
        "observations": {
            "data": [
                {
                    "sort_order": 0,
                    "delta_t": 5.3,
                },
            ],
        },
    }
