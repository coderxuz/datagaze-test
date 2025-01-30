
from app.services import get_temp_color, get_wind_color, get_cloud_color

def test_get_temp_color():
    result = get_temp_color(temp_c=-15)
    assert result == '#B3DFFD'
    
    result = get_temp_color(temp_c=-10)
    assert result == '#B3DFFD'
    
    result = get_temp_color(temp_c=-7)
    assert result == '#E6F7FF'

def test_get_wind_color():
    result = get_wind_color(wind_kph=5)
    assert result == '#E0F7FA'

    result = get_wind_color(wind_kph=15)
    assert result == '#B2EBF2'

    result = get_wind_color(wind_kph=50)
    assert result == '#0288D1'
    
def test_get_cloud_color():
    result = get_cloud_color(cloud_percentage=5)
    assert result == '#FFF9C4'

    result = get_cloud_color(cloud_percentage=25)
    assert result == '#FFF176'

    result = get_cloud_color(cloud_percentage=80)
    assert result == '#9E9E9E'
