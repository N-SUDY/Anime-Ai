FROM python



WORKDIR /app



COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

COPY . /app



CMD flask run -h 0.0.0.0 -p 8080 & python3 bot.py
