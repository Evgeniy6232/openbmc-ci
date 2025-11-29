FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    qemu-system-arm \
    wget \
    unzip \
    net-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /qemu

# Копируем вашу прошивку и скрипт
COPY romulus/obmc-phosphor-image-romulus-20250909100209.static.mtd /qemu/romulus/
COPY openbmc.sh /qemu/openbmc.sh
RUN chmod +x /qemu/openbmc.sh

EXPOSE 2222 2443 2623

CMD ["/qemu/openbmc.sh"]
