import pytest
from unittest.mock import patch, Mock
from bot.main import fetch_weather, format_weather_response, select_image

def test_format_weather_response():
    city = "Москва"
    data = {
        "main": {"temp": 15.4, "feels_like": 12.9},
        "weather": [{"description": "пасмурно"}]
    }
    answer, description, temp = format_weather_response(city, data)
    assert "Москва" in answer
    assert "15°C" in answer
    assert "13°C" in answer
    assert description == "Пасмурно"
    assert temp == 15

def test_select_image():
    assert select_image("дождь", 20).endswith("rainy.jpg")
    assert select_image("пасмурно", 20).endswith("cloudy.jpg")
    assert select_image("облачно", 20).endswith("cloudy.jpg")
    assert select_image("ясно", 5).endswith("cold.png")
    assert select_image("ясно", 15).endswith("sunny.jpg")

@patch('bot.main.requests.get')
def test_fetch_weather_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"some": "data"}
    mock_get.return_value = mock_response

    result = fetch_weather("Москва")
    assert result == {"some": "data"}
    mock_get.assert_called_once()

@patch('bot.main.requests.get')
def test_fetch_weather_failure(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = fetch_weather("НеверныйГород")
    assert result is None
