import requests


WEATHER_DESCRIPTIONS = {
    0: "açık",
    1: "çoğunlukla açık",
    2: "parçalı bulutlu",
    3: "kapalı",
    45: "sisli",
    48: "kırağılı sisli",
    51: "hafif çiseli",
    53: "çiseli",
    55: "yoğun çiseli",
    61: "hafif yağmurlu",
    63: "yağmurlu",
    65: "şiddetli yağmurlu",
    71: "hafif kar yağışlı",
    73: "kar yağışlı",
    75: "yoğun kar yağışlı",
    80: "hafif sağanak yağışlı",
    81: "sağanak yağışlı",
    82: "şiddetli sağanak yağışlı",
    95: "gök gürültülü fırtınalı",
    96: "dolu ihtimalli fırtınalı",
    99: "şiddetli dolu ihtimalli fırtınalı",
}


def weather_tool(city: str) -> str:
    """Verilen şehrin güncel hava durumunu getirir."""

    city = city.strip()

    if not city:
        return "Lütfen bir il veya şehir adı girin."

    try:
        coordinates = get_city_coordinates(city)

        if coordinates is None:
            return f"'{city}' adında bir şehir bulamadım."

        latitude = coordinates["latitude"]
        longitude = coordinates["longitude"]
        city_name = coordinates["name"]

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "apparent_temperature,"
                "relative_humidity_2m,"
                "weather_code,"
                "wind_speed_10m"
            ),
            "timezone": "auto",
        }

        response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        current = data.get("current")

        if not current:
            return "Hava durumu bilgisi alınamadı."

        temperature = current.get("temperature_2m")
        apparent_temperature = current.get("apparent_temperature")
        humidity = current.get("relative_humidity_2m")
        wind_speed = current.get("wind_speed_10m")
        weather_code = current.get("weather_code")

        description = WEATHER_DESCRIPTIONS.get(
            weather_code,
            "bilinmeyen hava durumu",
        )

        return (
            f"{city_name} için hava {description}.\n"
            f"Sıcaklık: {temperature} °C\n"
            f"Hissedilen sıcaklık: {apparent_temperature} °C\n"
            f"Nem: %{humidity}\n"
            f"Rüzgâr hızı: {wind_speed} km/sa"
        )

    except requests.exceptions.Timeout:
        return "Hava durumu servisi zaman aşımına uğradı."

    except requests.exceptions.ConnectionError:
        return "İnternet bağlantısı kurulamadı."

    except requests.exceptions.RequestException as error:
        return f"Hava durumu servisine erişilirken hata oluştu: {error}"

    except (KeyError, TypeError, ValueError):
        return "Hava durumu verisi işlenirken bir hata oluştu."


def get_city_coordinates(city: str) -> dict | None:
    """Şehir adını enlem ve boylama dönüştürür."""

    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    geocoding_params = {
        "name": city,
        "count": 1,
        "language": "tr",
        "format": "json",
    }

    response = requests.get(
        geocoding_url,
        params=geocoding_params,
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()
    results = data.get("results")

    if not results:
        return None

    location = results[0]

    return {
        "name": location["name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
    }