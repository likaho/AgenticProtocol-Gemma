# Use the official Python image from the Docker Hub
FROM python:3.10-slim
# Install CA certificates
RUN apt-get update && apt-get install -y ca-certificates && apt-get install -y curl && apt-get clean

# Disable SSL verification
# ENV REQUESTS_CA_BUNDLE=""
USER root

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade certifi
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade pyopenssl
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Install the dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port Streamlit will run on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]