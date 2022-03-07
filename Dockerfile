FROM python:3.8.4-slim

RUN cp /etc/ssl/openssl.cnf /etc/ssl/openssl.cnf.ORI && \
    sed -i "s/\(CipherString *= *\).*/\1DEFAULT@SECLEVEL=1 /" "/etc/ssl/openssl.cnf" && \
    (diff -u /etc/ssl/openssl.cnf.ORI /etc/ssl/openssl.cnf || exit 0)

WORKDIR /code
COPY "requirements.txt" ./
RUN pip install -r 'requirements.txt' --proxy=$http_proxy

COPY *.py ./

ENTRYPOINT [ "python", "main.py"]
