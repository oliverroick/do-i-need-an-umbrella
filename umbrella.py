import datapoint
from datetime import datetime, timedelta
from postcodes import PostCoder

conn = datapoint.connection(api_key='f414f0c5-bb8e-49bf-b78a-41c1ce746b57')

site = conn.get_nearest_site(0.00568, 51.50156)
forecast = conn.get_forecast_for_site(site.id, "3hourly")
current_timestep = forecast.now()


def get_forecast(lon, lat):
    site = conn.get_nearest_site(lon, lat)
    return conn.get_forecast_for_site(site.id, "3hourly")


def check_rain(forecast, hours):
    now = datetime.now()
    stop = now + timedelta(hours=hours)

    rain = 0
    for index, day in enumerate(forecast.days):
        for timestep in day.timesteps:
            minutes_to_add = (index * 24 * 60) + timestep.name
            today = datetime(now.year, now.month, now.day)
            timestep_datetime = today + timedelta(minutes=minutes_to_add)

            if timestep_datetime > now and timestep_datetime < stop:
                rain = max(rain, timestep.precipitation.value)

    return rain


def get_location_from_postcode(post_code):
    pc = PostCoder()
    result = pc.get(post_code).get('geo')
    return result.get('lng'), result.get('lat')


def do_i_need_an_umbrella(lon=None, lat=None, post_code=None, hours=24):
    if (lat is None and lon is None) and post_code is not None:
        lon, lat = get_location_from_postcode(post_code)

    forcast = get_forecast(lon, lat)
    return check_rain(forcast, hours)
