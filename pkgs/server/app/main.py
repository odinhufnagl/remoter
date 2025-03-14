from fastapi.concurrency import asynccontextmanager
import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from app.shared.core.middleware import exception_middleware
from app.users.routes.users_routes import router as users_router
from app.auth.routes.auth_routes import router as auth_router
from app.runner.routes import router as runner_router
from fastapi import APIRouter
from app.config import settings

api_router = APIRouter()


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)
app.add_middleware(exception_middleware.ExceptionMiddleware)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Length", "Content-Type"],
    )


# health check
@api_router.get("/health-check", tags=["health"])
async def health():
    return {"status": "ok"}


api_router.include_router(users_router, prefix="/users")
api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(runner_router, prefix="/runner")
app.include_router(api_router, prefix=settings.API_V1_STR)
