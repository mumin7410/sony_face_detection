FROM ubuntu:20.04

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CAMERA_VALUE=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        libgl1-mesa-glx \
        curl \
        sudo \
    && rm -rf /var/lib/apt/lists/* \
    && echo "Checking Ubuntu version..." \
    && ubuntu_version=$(cat /etc/os-release | grep VERSION_ID | cut -d '"' -f 2) \
    && if [ "$ubuntu_version" != "20.04" ]; then \
            echo "Ubuntu $ubuntu_version is not currently supported."; \
            exit 1; \
       fi \
    && echo "Adding Microsoft package repository..." \
    && curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc \
    && curl https://packages.microsoft.com/config/ubuntu/$ubuntu_version/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && \
    echo "Installing MS SQL Server tools..." \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> /root/.bashrc \
    && echo "Installing additional dependencies..." \
    # && apt-get install -y libodbc-dev \
    && echo "Setup completed successfully."


WORKDIR /code

COPY . /code/

RUN pip install --no-cache-dir -r requirement.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
