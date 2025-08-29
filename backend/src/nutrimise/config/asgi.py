import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nutrimise.config.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Settings")

if __name__ == "__main__":
    from configurations.asgi import get_asgi_application

    application = get_asgi_application()

    import uvicorn

    from nutrimise.interfaces.frontend_api import app

    uvicorn.run(app.api, host="127.0.0.1", port=8001)
