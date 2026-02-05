import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from datetime import datetime
import traceback


class LoggingMiddleware(BaseHTTPMiddleware):
    """Custom logging middleware for request/response logging"""

    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        self.logger = logging.getLogger("todo_app")

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Dispatch method for middleware"""

        # Log request start
        start_time = datetime.utcnow()
        request_id = f"req-{start_time.timestamp()}"[:20]

        try:
            # Log request details
            self.logger.info(
                f"Request started: {request_id} {request.method} {request.url.path}",
                extra={"request_id": request_id}
            )

            # Call the next middleware/endpoint
            response = await call_next(request)

            # Calculate processing time
            process_time = (datetime.utcnow() - start_time).total_seconds()

            # Log response details
            self.logger.info(
                f"Request completed: {request_id} {response.status_code} {process_time:.3f}s",
                extra={"request_id": request_id, "status_code": response.status_code, "process_time": process_time}
            )

            return response

        except Exception as e:
            # Log error details
            self.logger.error(
                f"Request error: {request_id} {str(e)}",
                extra={"request_id": request_id, "error": str(e)},
                exc_info=True
            )

            # Re-raise the exception
            raise


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Custom error handling middleware"""

    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        self.logger = logging.getLogger("todo_app")

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Dispatch method for error handling"""

        try:
            return await call_next(request)

        except HTTPException as exc:
            # Handle HTTP exceptions
            return JSONResponse(
                status_code=exc.status_code,
                content={"error": exc.detail},
            )

        except Exception as exc:
            # Handle all other exceptions
            self.logger.error(
                f"Unhandled exception: {str(exc)}",
                exc_info=True
            )

            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error"},
            )


def setup_logging(app: FastAPI) -> None:
    """Setup logging configuration for the application"""

    # Get log level from config
    log_level = logging.INFO
    log_level_name = "INFO"

    try:
        log_level_name = app.state.settings.get_log_level().upper()
        log_level = getattr(logging, log_level_name)
    except Exception:
        pass

    # Configure logging
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(request_id)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),
        ],
    )

    # Add request ID filter
    class RequestIdFilter(logging.Filter):
        def filter(self, record):
            record.request_id = getattr(record, "request_id", "")
            return True

    logging.getLogger().addFilter(RequestIdFilter())


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> Response:
    """Global exception handler"""

    # Log the exception
    logger = logging.getLogger("todo_app")
    logger.error(
        f"Unhandled exception: {str(exc)}",
        exc_info=True
    )

    # Return error response
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )