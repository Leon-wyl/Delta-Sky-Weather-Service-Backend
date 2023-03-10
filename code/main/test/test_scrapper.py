from scrapper import get_processed_data, create_new_format


def test_create_new_format_key_existence():
    new_format = create_new_format()
    assert 'datasource' in new_format
    assert 'dataset_type' in new_format
    assert 'dataset_id' in new_format
    assert 'time_object' in new_format
    assert 'events' in new_format
    assert 'timestamp' in new_format['time_object']
    assert 'timezone' in new_format['time_object']


def test_create_new_format_value_correctness():
    new_format = create_new_format()
    assert new_format['datasource'] == 'Australian Government Bureau of Meteorology'
    assert new_format['dataset_type'] == 'weather_info'
    assert new_format['dataset_id'] == 'http://reg.bom.gov.au/fwo/IDN60901/IDN60901.94768.json'
    assert new_format['time_object'] is not None
    assert new_format['time_object']['timestamp'] is not None
    assert new_format['time_object']['timezone'] is not None
    assert new_format['events'] == []


def test_get_processed_data_all_null():
    origin_object = {
        "observations": {
            "data": [
                {
                    "sort_order": None,
                    "cloud": "-",
                    "cloud_base_m": None,
                    "cloud_oktas": None,
                    "cloud_type_id": None,
                    "cloud_type": "-",
                    "delta_t": None,
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
                {
                    "sort_order": None,
                    "cloud": "-",
                    "cloud_base_m": "-",
                    "cloud_oktas": None,
                    "cloud_type_id": None,
                    "cloud_type": "-",
                    "delta_t": "-",
                    "gust_kmh": None,
                    "gust_kt": "-",
                    "press_tend": "-",
                    "sea_state": "-",
                    "swell_dir_worded": "-",
                    "swell_height": None,
                    "swell_period": "-",
                    "vis_km": "-",
                    "weather": "-",
                },
                {
                    "sort_order": "-",
                    "cloud": "-",
                    "cloud_base_m": "-",
                    "cloud_oktas": "-",
                    "cloud_type_id": "-",
                    "cloud_type": "-",
                    "delta_t": "-",
                    "gust_kmh": "-",
                    "gust_kt": "-",
                    "press_tend": "-",
                    "sea_state": "-",
                    "swell_dir_worded": "-",
                    "swell_height": "-",
                    "swell_period": "-",
                    "vis_km": "-",
                    "weather": "-",
                },
            ],
        },
    }
    assert get_processed_data(origin_object)['observations']['data'] == [{}, {}, {}]


def test_get_processed_data_some_null():
    origin_object = {
        "observations": {
            "data": [
                {
                    "sort_order": None,
                    "cloud": "asdfaswe2",
                    "cloud_base_m": None,
                    "cloud_oktas": 234,
                    "cloud_type_id": "sdfsdf",
                    "cloud_type": "-",
                    "delta_t": None,
                    "gust_kmh": None,
                    "gust_kt": "None",
                    "press_tend": "sdfgassdfg",
                    "sea_state": "-",
                    "swell_dir_worded": "-",
                    "swell_height": "asd",
                    "swell_period": None,
                    "vis_km": "-",
                    "weather": "-",
                },
                {
                    "sort_order": None,
                    "cloud": "-",
                    "cloud_base_m": "-",
                    "cloud_oktas": None,
                    "cloud_type_id": None,
                    "cloud_type": "-",
                    "delta_t": "-",
                    "gust_kmh": None,
                    "gust_kt": "-",
                    "press_tend": "-",
                    "sea_state": "-",
                    "swell_dir_worded": "-",
                    "swell_height": None,
                    "swell_period": "-",
                    "vis_km": "-",
                    "weather": "-",
                },
                {
                    "sort_order": 4,
                    "cloud": "yes",
                    "cloud_base_m": "abc",
                    "cloud_oktas": "sdfsd",
                    "cloud_type_id": 3,
                    "cloud_type": "sdfs",
                    "delta_t": "sdf",
                    "gust_kmh": "sdf",
                    "gust_kt": "sdf",
                    "press_tend": "sdf",
                    "sea_state": "sdf",
                    "swell_dir_worded": "sdfsadf",
                    "swell_height": "sdfw42",
                    "swell_period": "sdfsqdfa",
                    "vis_km": "werqw2",
                    "weather": "sdfsd",
                },
            ],
        },
    }
    assert get_processed_data(origin_object)['observations']['data'] == [
        {
            "cloud": "asdfaswe2",
            "cloud_oktas": 234,
            "cloud_type_id": "sdfsdf",
            'gust_kt': 'None',
            "press_tend": "sdfgassdfg",
            "swell_height": "asd",
        },
        {},
        {
            "sort_order": 4,
            "cloud": "yes",
            "cloud_base_m": "abc",
            "cloud_oktas": "sdfsd",
            "cloud_type_id": 3,
            "cloud_type": "sdfs",
            "delta_t": "sdf",
            "gust_kmh": "sdf",
            "gust_kt": "sdf",
            "press_tend": "sdf",
            "sea_state": "sdf",
            "swell_dir_worded": "sdfsadf",
            "swell_height": "sdfw42",
            "swell_period": "sdfsqdfa",
            "vis_km": "werqw2",
            "weather": "sdfsd"
        }
    ]


def test_get_processed_data_only_one_not_null():
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
                    "delta_t": None,
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
                },
            ],
        },
    }


def test_get_processed_data_only_one_null():
    origin_object = {
        "observations": {
            "data": [
                {
                    "sort_order": 2,
                    "cloud": "saf",
                    "cloud_base_m": 'None',
                    "cloud_oktas": 'None',
                    "cloud_type_id": 'None',
                    "cloud_type": 'asdfasd',
                    "delta_t": 'None',
                    "gust_kmh": 'None',
                    "gust_kt": 'None',
                    "press_tend": 'asdfasd',
                    "sea_state": 'asdfasd',
                    "swell_dir_worded": 'asdfasd',
                    "swell_height": 'None',
                    "swell_period": 'None',
                    "vis_km": 'asdfasd',
                    "weather": 'asdfasd',
                },
                {
                    "sort_order": 2,
                    "cloud": "saf",
                    "cloud_base_m": None,
                    "cloud_oktas": 'None',
                    "cloud_type_id": 'None',
                    "cloud_type": 'asdfasd',
                    "delta_t": 'None',
                    "gust_kmh": 'None',
                    "gust_kt": 'None',
                    "press_tend": 'asdfasd',
                    "sea_state": 'asdfasd',
                    "swell_dir_worded": 'asdfasd',
                    "swell_height": 'None',
                    "swell_period": 'None',
                    "vis_km": 'asdfasd',
                    "weather": 'asdfasd',
                },
            ],
        },
    }
    assert get_processed_data(origin_object) == {
        "observations": {
            "data": [
                {
                    "sort_order": 2,
                    "cloud": "saf",
                    "cloud_base_m": 'None',
                    "cloud_oktas": 'None',
                    "cloud_type_id": 'None',
                    "cloud_type": 'asdfasd',
                    "delta_t": 'None',
                    "gust_kmh": 'None',
                    "gust_kt": 'None',
                    "press_tend": 'asdfasd',
                    "sea_state": 'asdfasd',
                    "swell_dir_worded": 'asdfasd',
                    "swell_height": 'None',
                    "swell_period": 'None',
                    "vis_km": 'asdfasd',
                    "weather": 'asdfasd',
                },
                {
                    "sort_order": 2,
                    "cloud": "saf",
                    "cloud_oktas": 'None',
                    "cloud_type_id": 'None',
                    "cloud_type": 'asdfasd',
                    "delta_t": 'None',
                    "gust_kmh": 'None',
                    "gust_kt": 'None',
                    "press_tend": 'asdfasd',
                    "sea_state": 'asdfasd',
                    "swell_dir_worded": 'asdfasd',
                    "swell_height": 'None',
                    "swell_period": 'None',
                    "vis_km": 'asdfasd',
                    "weather": 'asdfasd',
                },
            ],
        },
    }


def test_get_processed_data_all_not_null():
    origin_object = {
        "observations": {
            "data": [
                {
                    "sort_order": 0,
                    "wmo": 94769,
                    "name": "Fort Denison",
                    "history_product": "IDN60901",
                    "local_date_time": "10/03:00am",
                    "local_date_time_full": "20230310030000",
                    "aifstime_utc": "20230309160000",
                    "lat": -33.9,
                    "lon": 151.2,
                    "apparent_t": "yes",
                    "cloud": "yes",
                    "cloud_base_m": "yes",
                    "cloud_oktas": "yes",
                    "cloud_type_id": "yes",
                    "cloud_type": "yes",
                    "delta_t": "yes",
                    "gust_kmh": 17,
                    "gust_kt": 9,
                    "air_temp": "yes",
                    "dewpt": "yes",
                    "press": "yes",
                    "press_qnh": "yes",
                    "press_msl": "yes",
                    "press_tend": "yes",
                    "rain_trace": "yes",
                    "rel_hum": "yes",
                    "sea_state": "yes",
                    "swell_dir_worded": "yes",
                    "swell_height": "yes",
                    "swell_period": "yes",
                    "vis_km": "yes",
                    "weather": "yes",
                    "wind_dir": "WNW",
                    "wind_spd_kmh": 15,
                    "wind_spd_kt": 8
                },
                {
                    "sort_order": 1,
                    "wmo": 94769,
                    "name": "Fort Denison",
                    "history_product": "IDN60901",
                    "local_date_time": "10/02:30am",
                    "local_date_time_full": "20230310023000",
                    "aifstime_utc": "20230309153000",
                    "lat": -33.9,
                    "lon": 151.2,
                    "apparent_t": "yes",
                    "cloud": "yes",
                    "cloud_base_m": "yes",
                    "cloud_oktas": "yes",
                    "cloud_type_id": "yes",
                    "cloud_type": "yes",
                    "delta_t": "yes",
                    "gust_kmh": 17,
                    "gust_kt": 9,
                    "air_temp": "yes",
                    "dewpt": "yes",
                    "press": "yes",
                    "press_qnh": "yes",
                    "press_msl": "yes",
                    "press_tend": "yes",
                    "rain_trace": "yes",
                    "rel_hum": "yes",
                    "sea_state": "yes",
                    "swell_dir_worded": "yes",
                    "swell_height": "yes",
                    "swell_period": "yes",
                    "vis_km": "yes",
                    "weather": "yes",
                    "wind_dir": "W",
                    "wind_spd_kmh": 15,
                    "wind_spd_kt": 8
                },
                {
                    "sort_order": 2,
                    "wmo": 94769,
                    "name": "Fort Denison",
                    "history_product": "IDN60901",
                    "local_date_time": "10/02:00am",
                    "local_date_time_full": "20230310020000",
                    "aifstime_utc": "20230309150000",
                    "lat": -33.9,
                    "lon": 151.2,
                    "apparent_t": "yes",
                    "cloud": "yes",
                    "cloud_base_m": "yes",
                    "cloud_oktas": "yes",
                    "cloud_type_id": "yes",
                    "cloud_type": "yes",
                    "delta_t": "yes",
                    "gust_kmh": 15,
                    "gust_kt": 8,
                    "air_temp": "yes",
                    "dewpt": "yes",
                    "press": "yes",
                    "press_qnh": "yes",
                    "press_msl": "yes",
                    "press_tend": "yes",
                    "rain_trace": "yes",
                    "rel_hum": "yes",
                    "sea_state": "yes",
                    "swell_dir_worded": "yes",
                    "swell_height": "yes",
                    "swell_period": "yes",
                    "vis_km": "yes",
                    "weather": "yes",
                    "wind_dir": "WNW",
                    "wind_spd_kmh": 13,
                    "wind_spd_kt": 7
                }
            ]
        }
    }
    assert get_processed_data(origin_object) == {
        "observations": {
            "data": [
                {
                    "sort_order": 0,
                    "wmo": 94769,
                    "name": "Fort Denison",
                    "history_product": "IDN60901",
                    "local_date_time": "10/03:00am",
                    "local_date_time_full": "20230310030000",
                    "aifstime_utc": "20230309160000",
                    "lat": -33.9,
                    "lon": 151.2,
                    "apparent_t": "yes",
                    "cloud": "yes",
                    "cloud_base_m": "yes",
                    "cloud_oktas": "yes",
                    "cloud_type_id": "yes",
                    "cloud_type": "yes",
                    "delta_t": "yes",
                    "gust_kmh": 17,
                    "gust_kt": 9,
                    "air_temp": "yes",
                    "dewpt": "yes",
                    "press": "yes",
                    "press_qnh": "yes",
                    "press_msl": "yes",
                    "press_tend": "yes",
                    "rain_trace": "yes",
                    "rel_hum": "yes",
                    "sea_state": "yes",
                    "swell_dir_worded": "yes",
                    "swell_height": "yes",
                    "swell_period": "yes",
                    "vis_km": "yes",
                    "weather": "yes",
                    "wind_dir": "WNW",
                    "wind_spd_kmh": 15,
                    "wind_spd_kt": 8
                },
                {
                    "sort_order": 1,
                    "wmo": 94769,
                    "name": "Fort Denison",
                    "history_product": "IDN60901",
                    "local_date_time": "10/02:30am",
                    "local_date_time_full": "20230310023000",
                    "aifstime_utc": "20230309153000",
                    "lat": -33.9,
                    "lon": 151.2,
                    "apparent_t": "yes",
                    "cloud": "yes",
                    "cloud_base_m": "yes",
                    "cloud_oktas": "yes",
                    "cloud_type_id": "yes",
                    "cloud_type": "yes",
                    "delta_t": "yes",
                    "gust_kmh": 17,
                    "gust_kt": 9,
                    "air_temp": "yes",
                    "dewpt": "yes",
                    "press": "yes",
                    "press_qnh": "yes",
                    "press_msl": "yes",
                    "press_tend": "yes",
                    "rain_trace": "yes",
                    "rel_hum": "yes",
                    "sea_state": "yes",
                    "swell_dir_worded": "yes",
                    "swell_height": "yes",
                    "swell_period": "yes",
                    "vis_km": "yes",
                    "weather": "yes",
                    "wind_dir": "W",
                    "wind_spd_kmh": 15,
                    "wind_spd_kt": 8
                },
                {
                    "sort_order": 2,
                    "wmo": 94769,
                    "name": "Fort Denison",
                    "history_product": "IDN60901",
                    "local_date_time": "10/02:00am",
                    "local_date_time_full": "20230310020000",
                    "aifstime_utc": "20230309150000",
                    "lat": -33.9,
                    "lon": 151.2,
                    "apparent_t": "yes",
                    "cloud": "yes",
                    "cloud_base_m": "yes",
                    "cloud_oktas": "yes",
                    "cloud_type_id": "yes",
                    "cloud_type": "yes",
                    "delta_t": "yes",
                    "gust_kmh": 15,
                    "gust_kt": 8,
                    "air_temp": "yes",
                    "dewpt": "yes",
                    "press": "yes",
                    "press_qnh": "yes",
                    "press_msl": "yes",
                    "press_tend": "yes",
                    "rain_trace": "yes",
                    "rel_hum": "yes",
                    "sea_state": "yes",
                    "swell_dir_worded": "yes",
                    "swell_height": "yes",
                    "swell_period": "yes",
                    "vis_km": "yes",
                    "weather": "yes",
                    "wind_dir": "WNW",
                    "wind_spd_kmh": 13,
                    "wind_spd_kt": 7
                }
            ]
        }
    }
