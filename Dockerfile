FROM python:3.11-slim

WORKDIR /app

# Install Odoo dependencies
COPY requirements.txt /app
RUN apt-get update && \
    apt-get install -y libldap2-dev libpq-dev libsasl2-dev \
    build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy Odoo source code
COPY . /app

# Copy entrypoint script, wait-for-psql script and Odoo configuration file
COPY ./docker/entrypoint.sh /app/
COPY ./docker/wait-for-psql.py /usr/local/bin/wait-for-psql.py
COPY ./docker/odoo.conf /etc/odoo/

# Create odoo user and group, set ownership
RUN adduser --system --group --disabled-password \
            --home /var/lib/odoo odoo && \
    mkdir /data && \
    chown odoo:odoo /var/lib/odoo /data

# Set permissions
RUN chown odoo /etc/odoo/odoo.conf && \
    mkdir -p /mnt/extra-addons && \
    chown -R odoo /mnt/extra-addons && \
    chmod +x /app/entrypoint.sh && \
    chmod +x /app/odoo-bin && \
    chmod +x /usr/local/bin/wait-for-psql.py

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
