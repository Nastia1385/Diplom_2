class TestData:
    # Корректные данные пользователя по умолчанию
    DEFAULT_EMAIL = "testuser@example.com"
    DEFAULT_PASSWORD = "password123"
    DEFAULT_NAME = "Test User"

    # Сообщения об ошибках
    USER_ALREADY_EXISTS_MSG = "User already exists"
    REQUIRED_FIELDS_MSG = "Email, password and name are required fields"
    INCORRECT_CREDENTIALS_MSG = "email or password are incorrect"
    UNAUTHORIZED_MSG = "You should be authorised"
    INGREDIENTS_REQUIRED_MSG = "Ingredient ids must be provided"

    # Хеши ингредиентов (реальные, для успешных тестов)
    VALID_INGREDIENT_HASH_1 = "60d3b41abdacab0026a733c6"
    VALID_INGREDIENT_HASH_2 = "609646e4dc916e00276b2870"
    # Невалидный хеш для негативных тестов
    INVALID_INGREDIENT_HASH = "invalid_ingredient_hash"