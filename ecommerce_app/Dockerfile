FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/sh"]

# Command to run the CLI app
#ENTRYPOINT ["python", "app.py"]
