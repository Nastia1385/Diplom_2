# Базовый URL для API
BASE_URL = "https://stellarburgers.education-services.ru"

# Эндпоинты
class Endpoints:
    CREATE_USER = f"{BASE_URL}/api/auth/register"
    LOGIN_USER = f"{BASE_URL}/api/auth/login"
    USER_INFO = f"{BASE_URL}/api/auth/user"
    CREATE_ORDER = f"{BASE_URL}/api/orders"
    GET_USER_ORDERS = f"{BASE_URL}/api/orders"
    GET_INGREDIENTS = f"{BASE_URL}/api/ingredients"