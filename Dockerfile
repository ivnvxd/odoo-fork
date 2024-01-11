FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libfreetype6-dev libxml2-dev libzip-dev libsasl2-dev \
    libjpeg-dev zlib1g-dev libpq-dev libxslt1-dev \
    libldap2-dev libtiff5-dev libopenjp2-7-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy Odoo source code
COPY . /app

# Copy entrypoint script, wait-for-psql script and Odoo configuration file
COPY ./docker/entrypoint.sh /app/
COPY ./docker/wait-for-psql.py /usr/local/bin/wait-for-psql.py
COPY ./docker/odoo.conf /etc/odoo/

# Create odoo user and group, set ownership and permissions
RUN adduser --system --group --disabled-password --home /var/lib/odoo odoo && \
    mkdir /data /mnt/extra-addons && \
    chown odoo:odoo /var/lib/odoo /data /mnt/extra-addons /etc/odoo/odoo.conf && \
    chmod +x /app/entrypoint.sh /app/odoo-bin /usr/local/bin/wait-for-psql.py

# Install wkhtmltopdf and npm packages
RUN apt-get update && apt-get install -y \
    xfonts-75dpi wkhtmltopdf \
    node-less npm && \
    npm install -g less less-plugin-clean-css rtlcss && \
    rm -rf /var/lib/apt/lists/*

# Mount /var/lib/odoo to allow restoring filestore and /mnt/extra-addons for users addons
VOLUME ["/var/lib/odoo", "/mnt/extra-addons"]

# Expose Odoo services
EXPOSE 8069

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

# Set default user when running the container
USER odoo

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["odoo"]
