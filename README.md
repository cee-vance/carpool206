# 🚌 Carpool206

## Overview
Carpool206 is a **full‑stack carpooling application** built with Django and Docker. It enables users to create profiles, schedule rides, chat with other commuters, and manage carpools in the Seattle area. The project demonstrates containerized deployment, backend design, and integration of real‑time features.

The application is **deployed on AWS** and publicly accessible at [carpool206.org](https://carpool206.org). I am actively adding new features and refining the platform.

## Features
- **User authentication** with profile management  
- **Ride scheduling**: create, join, and manage carpools  
- **Chat system** for communication between riders and drivers  
- **Dockerized deployment** for reproducibility and portability  
- **Unit tests** for backend validation  
- **Cloud deployment** on AWS with a live production site  

## Tech Stack
- **Backend:** Django, Python  
- **Database:** PostgreSQL  
- **Frontend:** Django templates + Bootstrap  
- **Deployment:** Docker, Docker Compose, AWS EC2  

## Getting Started
```bash
# Clone the repo
git clone https://github.com/cee-vance/carpool206.git
cd carpool206

# Build and run with Docker
docker-compose up --build
