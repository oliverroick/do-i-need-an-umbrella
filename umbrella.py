import datapoint
from postcodes import PostCoder

conn = datapoint.connection(api_key='f414f0c5-bb8e-49bf-b78a-41c1ce746b57')

site = conn.get_nearest_site(0.00568, 51.50156)
forecast = conn.get_forecast_for_site(site.id, "3hourly")
current_timestep = forecast.now()


def get_forecast(lon, lat):
    site = conn.get_nearest_site(lon, lat)
    return conn.get_forecast_for_site(site.id, "3hourly")


def check_rain(forecast):
    rain = 0
    for day in forecast.days:
        for timestep in day.timesteps:
            print timestep.name
            if timestep.precipitation.value > 50:
                rain = 2
            elif timestep.precipitation.value > 20 and rain == 0:
                rain = 1

    return rain


def get_location_from_postcode(post_code):
    pc = PostCoder()
    result = pc.get(post_code).get('geo')
    return result.get('lng'), result.get('lat')


def do_i_need_an_umbrella(lon=None, lat=None, post_code=None):
    if (lat is None and lon is None) and post_code is not None:
        lon, lat = get_location_from_postcode(post_code)

    forcast = get_forecast(lon, lat)
    is_it_going_to_rain = check_rain(forcast)

    if is_it_going_to_rain == 2:
        return 'Hell yes'
    elif is_it_going_to_rain == 1:
        return 'Not really'
    else:
        return 'Nope'


# print do_i_need_an_umbrella(lon=0.00568, lat=51.50156)
# print do_i_need_an_umbrella(post_code='NW5 2HG')
