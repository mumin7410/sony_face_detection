# for amd64
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV CAMERA_VALUE=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1-mesa-glx \
        curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY . /code/

RUN pip install --no-cache-dir -r requirement.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# for arm64
# FROM python:3.9

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# ENV CAMERA_VALUE=1

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#         libgl1-mesa-glx \
#         curl \
#     && rm -rf /var/lib/apt/lists/* \
#     && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
#     && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
#     && apt-get update && \
#     ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /code

# COPY . /code/

# RUN pip install --no-cache-dir -r requirement.txt

# EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
