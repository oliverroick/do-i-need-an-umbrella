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
                if timestep.precipitation.value > 50:
                    rain = 2
                elif timestep.precipitation.value > 20 and rain == 0:
                    rain = 1

    return rain


def get_location_from_postcode(post_code):
    pc = PostCoder()
    result = pc.get(post_code).get('geo')
    return result.get('lng'), result.get('lat')


def do_i_need_an_umbrella(lon=None, lat=None, post_code=None, hours=24):
    if (lat is None and lon is None) and post_code is not None:
        lon, lat = get_location_from_postcode(post_code)

    forcast = get_forecast(lon, lat)
    is_it_going_to_rain = check_rain(forcast, hours)

    if is_it_going_to_rain == 2:
        return 'Hell yes'
    elif is_it_going_to_rain == 1:
        return 'Not really'
    else:
        return 'Nope'


# print do_i_need_an_umbrella(lon=0.00568, lat=51.50156)
# print do_i_need_an_umbrella(post_code='NW5 2HG', hours=2)
