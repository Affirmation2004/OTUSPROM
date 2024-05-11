Лабораторная работа сделана с использованием предыдущих наработок в docker compose.
В качестве каналов для получения алертов были использованы почта и telegram бот.
Для эмуляции smtp сервера был использован MailHog как простейший вариант. Для возможности отправки алертов в telegram был создан бот и канал для получения алертов https://t.me/otus_alerting_group (данные в файле txt).

В качестве примеров алертов critical и warning были использованы следующие настройки правил в prometheus:

groups: 
- name: test
  rules:
  - alert: PrometheusTargetMissing
    expr: up == 0
    for: 0m
    labels:
      severity: critical
    annotations:
      summary: "Prometheus target missing (instance {{ $labels.instance }})"
      description: "A Prometheus target has disappeared. An exporter might be crashed. VALUE = {{ $value }}  LABELS: {{ $labels }}"

  - alert: HostOutOfMemory
    expr: (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100 < 99) * on(instance) group_left (nodename) node_uname_info{nodename=~".+"}
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: Host out of memory (instance {{ $labels.instance }})
      description: "Node memory is filling up (< 10% left)\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

Конфиг alertmanager следующий:

global:
  resolve_timeout: 5m
  http_config:
    follow_redirects: true
    enable_http2: true
  smtp_from: alertmanager@otus.org
  smtp_hello: localhost
  smtp_smarthost: 172.23.32.1:1025
  smtp_require_tls: false
  pagerduty_url: https://events.pagerduty.com/v2/enqueue
  opsgenie_api_url: https://api.opsgenie.com/
  wechat_api_url: https://qyapi.weixin.qq.com/cgi-bin/
  victorops_api_url: https://alert.victorops.com/integrations/generic/20131114/alert/
  telegram_api_url: https://api.telegram.org
  webex_api_url: https://webexapis.com/v1/messages
route:
  receiver: default-reciever
  continue: false
  routes:
  - receiver: telegram-test
    matchers:
    - severity="warning"
    continue: false
  - receiver: email
    matchers:
    - severity="critical"
    continue: false
receivers:
- name: telegram-test
  telegram_configs:
  - send_resolved: true
    http_config:
      follow_redirects: true
      enable_http2: true
    api_url: https://api.telegram.org
    bot_token: <secret>
    chat_id: -1002088104183
    message: '{{ template "telegram.default.message" . }}'
    parse_mode: HTML
- name: email
  email_configs:
  - send_resolved: true
    to: test@local.com
    from: alertmanager@otus.org
    hello: localhost
    smarthost: 172.23.32.1:1025
    headers:
      From: alertmanager@otus.org
      Subject: '{{ template "email.default.subject" . }}'
      To: test@local.com
    html: '{{ template "email.default.html" . }}'
    require_tls: false
- name: default-reciever
templates: []

