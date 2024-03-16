FROM ubuntu:22.04

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CAMERA_VALUE=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        libgl1-mesa-glx \
        curl \
        lsb-release \
        sudo \
    && rm -rf /var/lib/apt/lists/* \
    && if ! [[ "22.04" == "$(lsb_release -rs)" ]]; then \
            echo "Ubuntu $(lsb_release -rs) is not currently supported."; \
            exit 1; \
       fi \
    && curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc \
    && curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && ACCEPT_EULA=Y apt-get install -y mssql-tools18 \
    && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc \
    && source ~/.bashrc \
    && apt-get install -y unixodbc-dev

WORKDIR /code

COPY . /code/

RUN pip install --no-cache-dir -r requirement.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
