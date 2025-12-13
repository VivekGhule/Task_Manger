from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse, HttpResponse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = BASE_DIR / "static" / "index.html"

# Serve index.html at root
def serve_index(request):
    if INDEX_FILE.exists():
        return FileResponse(open(INDEX_FILE, "rb"), content_type="text/html")
    return HttpResponse("<h2>Frontend not found</h2>", content_type="text/html")

urlpatterns = [
    path("", serve_index, name="index"),
    path("api/", include("core.urls")),
]

# static served automatically during development by django when DEBUG=True
# No extra config needed for runserver; in production use collectstatic + webserver
