В Docker compose из предыдущей лабораторной работы был добавлен раздел для последней версии Grafana:

grafana:
    image: grafana/grafana:latest
    user: root
    depends_on:
      - prometheus
    ports:
      - 3000:3000
    volumes:
      - ./grafana:/var/lib/grafana
      - ./grafana/provisioning/:/etc/grafana/provisioning/
    container_name: grafana
    hostname: grafana
    environment:
      TZ: "Europe/Moscow"

Был добавлен Data source Prometheus и сделаны необходимыен дашборды, а также настроен алерт для свободной памяти.
