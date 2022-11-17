# Use an official Python runtime as a parent image
FROM sanicframework/sanic:3.8-latest

# Set the working directory to /app
WORKDIR /dcoya_blog_app

# Copy the current directory contents into the container at /app
COPY . /dcoya_blog_app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8000

#Run app.py when the container launches
# CMD ["python", "server.py"]

## new img - docker build -t dcoya-image .
## docker run --name mysanic -p 8000:8000 -d dcoya-image
