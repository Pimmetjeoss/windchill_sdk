"""Tests for error handling."""

import pytest

from windchill.errors import (
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ODataError,
    ServerError,
    ValidationError,
    WindchillError,
    raise_for_status,
)


class TestODataError:
    def test_from_standard_response(self):
        body = {
            "error": {
                "code": "WINDCHILL_001",
                "message": "Part not found",
                "details": [{"message": "detail"}],
            }
        }
        err = ODataError.from_response(body)
        assert err.code == "WINDCHILL_001"
        assert err.message == "Part not found"
        assert len(err.details) == 1

    def test_from_flat_response(self):
        body = {"code": "ERR", "message": "Something failed"}
        err = ODataError.from_response(body)
        assert err.code == "ERR"
        assert err.message == "Something failed"

    def test_from_empty_response(self):
        err = ODataError.from_response({})
        assert err.code == ""
        assert err.message == ""


class TestRaiseForStatus:
    def test_success_does_not_raise(self):
        raise_for_status(200)
        raise_for_status(201)
        raise_for_status(204)

    def test_400_raises_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            raise_for_status(400, {"error": {"message": "Bad request"}})
        assert exc_info.value.status_code == 400

    def test_401_raises_authentication_error(self):
        with pytest.raises(AuthenticationError):
            raise_for_status(401, {"error": {"message": "Unauthorized"}})

    def test_403_raises_authorization_error(self):
        with pytest.raises(AuthorizationError):
            raise_for_status(403, {"error": {"message": "Forbidden"}})

    def test_404_raises_not_found_error(self):
        with pytest.raises(NotFoundError):
            raise_for_status(404, {"error": {"message": "Not found"}})

    def test_500_raises_server_error(self):
        with pytest.raises(ServerError):
            raise_for_status(500, {"error": {"message": "Internal error"}})

    def test_unknown_status_raises_base_error(self):
        with pytest.raises(WindchillError):
            raise_for_status(418, {"error": {"message": "I'm a teapot"}})

    def test_error_without_body(self):
        with pytest.raises(WindchillError) as exc_info:
            raise_for_status(500)
        assert "HTTP 500" in str(exc_info.value)

    def test_error_has_odata_error(self):
        with pytest.raises(ValidationError) as exc_info:
            raise_for_status(400, {"error": {"code": "C1", "message": "fail"}})
        assert exc_info.value.odata_error is not None
        assert exc_info.value.odata_error.code == "C1"


class TestExceptionHierarchy:
    def test_all_inherit_from_windchill_error(self):
        assert issubclass(AuthenticationError, WindchillError)
        assert issubclass(AuthorizationError, WindchillError)
        assert issubclass(NotFoundError, WindchillError)
        assert issubclass(ValidationError, WindchillError)
        assert issubclass(ServerError, WindchillError)
