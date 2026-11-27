import quakewatch as qw


def test_mindanao_nearest_city_uses_latitude_longitude_order(loaded):
    clean = qw.integrate()
    event = clean[clean["time"].dt.strftime("%Y-%m-%d %H:%M") == "2023-12-02 14:37"]

    assert event["city_id"].iloc[0] == "C10"
