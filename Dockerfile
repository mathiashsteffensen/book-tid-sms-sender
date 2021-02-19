FROM python:3
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV PY_ENV=production
COPY . .
EXPOSE 8080
CMD waitress-serve --call 'server:run'