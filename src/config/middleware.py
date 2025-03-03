MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "src.utils.svcs.middleware.ContainerMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
