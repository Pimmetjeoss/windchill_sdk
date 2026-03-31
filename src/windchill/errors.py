"""Exception hierarchy for Windchill SDK."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ODataError:
    """Parsed OData error response body."""

    code: str = ""
    message: str = ""
    details: list[dict] = field(default_factory=list)
    raw: dict = field(default_factory=dict)

    @classmethod
    def from_response(cls, body: dict) -> ODataError:
        """Parse an OData error response JSON body."""
        error = body.get("error", body)
        return cls(
            code=str(error.get("code", "")),
            message=str(error.get("message", "")),
            details=error.get("details", []),
            raw=body,
        )


class WindchillError(Exception):
    """Base exception for all Windchill SDK errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        odata_error: ODataError | None = None,
    ):
        self.status_code = status_code
        self.odata_error = odata_error
        super().__init__(message)


class AuthenticationError(WindchillError):
    """401 - Invalid credentials or expired session."""


class AuthorizationError(WindchillError):
    """403 - Insufficient permissions."""


class NotFoundError(WindchillError):
    """404 - Entity or endpoint not found."""


class ValidationError(WindchillError):
    """400 - Bad request or business rule violation."""


class ConflictError(WindchillError):
    """409 - Conflict (e.g., already checked out)."""


class ServerError(WindchillError):
    """500 - Internal server error."""


class NotImplementedByServerError(WindchillError):
    """501 - OData feature not implemented by Windchill."""


class BatchError(WindchillError):
    """Error in batch request processing."""


class ChangesetRollbackError(BatchError):
    """Atomic changeset was rolled back due to a failure."""

    def __init__(
        self,
        message: str,
        failed_operation_index: int | None = None,
        **kwargs,
    ):
        self.failed_operation_index = failed_operation_index
        super().__init__(message, **kwargs)


class ContentError(WindchillError):
    """Error during file upload or download."""


STATUS_CODE_TO_EXCEPTION: dict[int, type[WindchillError]] = {
    400: ValidationError,
    401: AuthenticationError,
    403: AuthorizationError,
    404: NotFoundError,
    409: ConflictError,
    500: ServerError,
    501: NotImplementedByServerError,
}


def raise_for_status(status_code: int, body: dict | None = None) -> None:
    """Raise the appropriate WindchillError for an HTTP error status code."""
    if status_code < 400:
        return

    odata_error = ODataError.from_response(body) if body else None
    message = odata_error.message if odata_error else f"HTTP {status_code}"
    exc_class = STATUS_CODE_TO_EXCEPTION.get(status_code, WindchillError)

    raise exc_class(
        message=message,
        status_code=status_code,
        odata_error=odata_error,
    )
