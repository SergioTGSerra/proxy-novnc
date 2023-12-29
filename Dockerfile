FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose ports
EXPOSE 5900
EXPOSE 5901
EXPOSE 5902
EXPOSE 6900
EXPOSE 6901
EXPOSE 6902

CMD [ "python", "./app.py" ]