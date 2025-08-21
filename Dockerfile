#Using the official Python image from docker hub
FROM python:3.9

#Update package list
RUN apt-get update

#Setting the working directory
WORKDIR /app

#Copy the application files to the working directory
COPY . .

#Copy and install requirements
COPY requirements/requirements.txt ./requirements.txt
RUN pip install --no-cache -r requirements.txt

#Start the application
CMD ["python" , "app.py"]