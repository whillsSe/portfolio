# Nginxの公式イメージをベースにする
FROM nginx:alpine

# Nginxの設定ファイルをコンテナにコピー
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 任意でSSL証明書やキーをコンテナにコピー
COPY server.crt /etc/nginx/ssl/
COPY server.key /etc/nginx/ssl/
