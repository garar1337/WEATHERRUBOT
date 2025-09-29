import pytest
from unittest.mock import patch, Mock
from bot.main import collect_data, send_weather, select_image

def test_send_weather():
    city = "Москва"
    data = {
        "main": {"temp": 15.4, "feels_like": 12.9},
        "weather": [{"description": "пасмурно"}]
    }
    answer, description, temp = send_weather(city, data)
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
def test_collect_data_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"main": {"temp": 20}, "weather": [{"description": "ясно"}]}
    mock_get.return_value = mock_response

    result = collect_data("Москва")
    assert result == {"main": {"temp": 20}, "weather": [{"description": "ясно"}]}
    mock_get.assert_called_once()

@patch('bot.main.requests.get')
def test_collect_data_failure(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = collect_data("Неверный Город")
    assert result is None