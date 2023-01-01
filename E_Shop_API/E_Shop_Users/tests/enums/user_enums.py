from enum import Enum


class UserErrorMessages(Enum):
    # birthday enums [test_validators.py]
    DATE_GREATE_1930 = "Date greate than 1930-01-01"
    FUTURE_DATE = "In this test date must be greater than today"
    INCORRECT_DATE_FORMAT = "In this test date must be incorrect"

    # password enums [test_validators.py]
    SHORT_PASSWORD = 'Password must be at least 8 characters long'
    PASSWORD_WITHOUT_NUMBERS = 'Password must contain at least one digit'
    PASSWORD_WITHOUT_CAPITAL_LETTERS = 'Password must contain at least one upper case letter'

    # GET user detail enums [test_views.py]
    GET_USER_DETAIL_FAILED = 'Failed to retrieve user detail for current user'
    GET_USER_DETAIL_INCORRECT = 'User detail data retrieved is not equal to expected data'

    # UPDATE user detail enums [test_views.py]
    UPDATE_USER_DETAIL_FAILED = 'Failed to update user data through UPDATE request'
    UPDATE_USER_INVALID = 'In this test update must be incorrect'
    DELETE_USER_FAILED = 'Failed to delete user. User still exists in the database'
    USER_DETAIL_NOT_UPDATED = 'User detail could not be updated. Please check that the provided data is valid'
    USER_DETAIL_NOT_DELETED = 'The test failed to delete user data from the database'

    # GOOGLE Messages [test_views.py]
    GOOGLE_SITE_NAME_FAILED = "Site name not updated"
    GOOGLE_SITE_DOMAIN_FAILED = "Site domain not updated"
    GOOGLE_UPDATE_FAILED = "Site update failed"
    GOOGLE_ID_FAILED = "Failed to retrieve social app by ID"
    GOOGLE_CREATE_PROVIDER_FAILED = "Failed to create social app with invalid data"

    # SERIALIZERS [test_serializer.py]
    SERIALIZER_RETURNS_ERROR = 'UserDetailSerializer returned unexpected data for user'
    SERIALIZER_EMPTY_PASSWORD = 'The serializer should not be valid when the password field is empty'
    SERIALIZER_FIELD = 'The "password" field should be required'
    SERIALIZER_VALID_DATA = 'Serializer should accept valid data'
    SERIALIZER_PASSWORD = 'Password should be correctly saved to database'
