from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.common.config import settings
from src.common.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle events.

    Handles startup operations including worker initialization and logging
    configuration details. Also manages graceful shutdown procedures.

    Args:
        app: FastAPI application instance

    Yields:
        None: Control to the application during its runtime
    """
    # Startup
    logger.info(f"🚀 Starting {settings.app_name} | RAG Service v{settings.app_version}")
    logger.info(f"Configuration - Debug mode: {settings.debug}, CORS origins: {len(settings.cors_origins)}")


    yield

    # Shutdown
    logger.info(f"🛑 Shutting down {settings.app_name} gracefully...")
    logger.info("✓ Application shutdown complete")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.

    Sets up the application with all necessary middleware, exception handlers,
    and API routers. Configuration is driven by application settings.

    Returns:
        FastAPI: Fully configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        # API documentation is always available at /docs
        # docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    # Configure CORS middleware for cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.debug(f"CORS configured with origins: {settings.cors_origins}")

    # Global exception handler for unhandled errors
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """
        Handle all unhandled exceptions globally.

        Logs the exception details and returns an appropriate error response.
        In debug mode, returns detailed error information; otherwise, returns
        a generic error message.
        """
        logger.error(
            f"Unhandled exception on {request.method} {request.url.path} - "
            f"Type: {type(exc).__name__}, Message: {exc}",
            exc_info=True
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error" if not settings.debug else str(exc)},
        )

    # Register API routers
    from src.rag_service.api import rag_router

    app.include_router(rag_router)

    logger.info("✓ All routers registered successfully")

    return app


app = create_app()


