FROM python

COPY main.py /
COPY requirements.txt /

RUN apt update && \
    apt install -y iputils-ping &&\
    pip install --root-user-action=ignore --upgrade pip && \
    pip install --root-user-action=ignore -r requirements.txt

ENTRYPOINT [ "python", "./main.py" ]
