# Use an official Python image
FROM python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for GDAL
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
ENV GEOS_LIBRARY_PATH=/usr/lib/libgeos_c.so

# Set the working directory in the container
WORKDIR /app

# Copy project files
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files (optional)

# RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the Django application
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["/bin/bash"]
