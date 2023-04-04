# mrtn-lov-backend

Backend for the Martian Love music video campaign. This is a FastAPI application that provides an API for the frontend to interact with.

## **Features**

- Collect user prompts via API endpoint
- Store prompts in a PostgreSQL database
- View all prompts or a single prompt by ID via API endpoint
- Update or delete prompts by ID via API endpoint

## **Tech Stack**

- Python 3.9
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (for database migrations)

## **Local Setup**

### **Requirements**

- Python 3.9
- Docker

### **Installation**

1. Clone the repository to your local machine
2. Navigate to the project root directory in your terminal
3. Create a virtual environment by running **`python3 -m venv venv`**
4. Activate the virtual environment by running **`source venv/bin/activate`**
5. Install dependencies by running **`pip install -r requirements.txt`**
6. Start the PostgreSQL database by running **`docker run --name projectname-db -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:13-alpine`**
7. Run the database migrations by running **`alembic upgrade head`**
8. Start the application by running **`uvicorn main:app --host 0.0.0.0 --port 8000`**

### **Usage**

- View API documentation by navigating to **`http://localhost:8000/docs`** in your web browser
- Interact with the API endpoints using an API client like Postman or cURL

### **Running with Docker**

1. Ensure that Docker is installed and running on your local machine
2. Clone the repository to your local machine
3. Navigate to the project root directory in your terminal
4. Build the Docker image by running **`docker build -t projectname .`**
5. Start the Docker container by running **`docker run --name projectname -p 8000:8000 projectname`**

### **Environment Variables**

This application uses environment variables to configure the database connection. The following variables can be set:

- **`DATABASE_URL`**: The URL for the PostgreSQL database connection (default: **`postgresql://postgres:password@localhost:5432/projectname`**)
- **`DATABASE_HOST`**: The hostname for the PostgreSQL database (default: **`localhost`**)
- **`DATABASE_PORT`**: The port number for the PostgreSQL database (default: **`5432`**)
- **`DATABASE_NAME`**: The name of the PostgreSQL database (default: **`projectname`**)
- **`DATABASE_USERNAME`**: The username for the PostgreSQL database (default: **`postgres`**)
- **`DATABASE_PASSWORD`**: The password for the PostgreSQL database (default: **`password`**)

## **Deployment**

To deploy this application to a production environment, you can use Docker Compose to build and run the Docker container. The **`docker-compose.yml`** file in the project root directory contains the configuration for the application and the PostgreSQL database.

1. Ensure that Docker and Docker Compose are installed and running on your server
2. Clone the repository to your server
3. Navigate to the project root directory in your terminal
4. Set the environment variables in the **`docker-compose.yml`** file to configure the database connection
5. Start the application and database by running **`docker-compose up -d`**
6. View the logs for the application and database by running **`docker-compose logs -f`**

## **Credits**

Project Name was created by [Your Name].
