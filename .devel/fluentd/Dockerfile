FROM fluent/fluentd
RUN ["gem", "install", "httpclient"]
RUN ["gem", "install", "fluent-plugin-secure-forward", "--no-rdoc", "--no-ri"]
RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-rdoc", "--no-ri", "--version", "2.12.5"]
