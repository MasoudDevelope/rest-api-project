FROM python:3.11
#EXPOSE 5000  -- commented when wanted to use gunicorn
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r  requirements.txt
COPY . .
#CMD ["flask", "run", "--host", "0.0.0.0"] this line changed to the below one 
#when wanted to use gunicorn
CMD ["gunicorn" , "--bind", "0.0.0.0:80", "app:create_app()"]
