# Technical-Interview---Savannah-Informatics
This is a guide on how I accomplished the Technical assignment for the Technical Support Engineer.

The Customer Order App is a simple web application designed for managing customer orders. It has been containerized using Docker, deployed on a microk8s scalable cluster.

## Key Features
- User Authentication and Authorization: Integrated with Keycloak for secure user management.
- Data Validation: Sanitize user inputs using bleach.clean() to prevent XSS
- SMS Notifications: Sends SMS notifications to users when an order is added, using Africa's Talking API.
- Database: Uses MySQL for data storage.
- Scalability: Deployed on a microk8s Kubernetes cluster for scalability and reliability.
- Continuous Deployment: Automated updates using Ansible.

## Prerequisites
- Python
- Docker
- Docker Hub account
- microk8s installed on my server
- Ansible installed on my local machine
- MySQL database
- Keycloak server for user authentication and authorization
- Africa's Talking API credentials for SMS notifications

1. ### Testing
Tested my application's routes.
Testing files: 
- ![alt text](test_app.yaml)

![alt text](screenshots/testing.png)


2. ### Dockerize and push the App
Built and pushed the Docker image to Docker Hub.
![alt text](screenshots/Docker_build1.png)

```sh
docker build -t kestack/customer-order-app:latest .
docker push kestack/customer-order-app:latest
```

3. ### Pull Docker Image on Server
SSH into my server and pulled the Docker image from Docker Hub.

```sh
docker pull kestack/customerorder-app:latest
```

4. ### Set Up microk8s
Installed and set up microk8s on my server.

5. ### Deployed the app on microk8s

Configurations files are 
- ![alt text](deployment.yaml) 
- ![alt text](service.yaml)
- ![alt text](hpa.yaml)

Applied the deployment:

![alt text](screenshots/microk8s-deployment.png)

6. ### Set Up Keycloak
Used KeyCloak's documentation to get started. https://www.keycloak.org/getting-started/getting-started-docker

![alt text](screenshots/keycloak-admin-login.png)

Configured KeyCloak to Athenticate and Authorize Users for my app
![alt text](screenshots/customerorder-realm.png)

7. ### Configure MySQL
Set up a MySQL database

Created Customers Table
![alt text](screenshots/customerTable.png)

Created Orders Table
![alt text](screenshots/ordersTable.png)

Overall Database Schema
![alt text](<screenshots/Database Schema.png>)

8. Configure SMS Notifications

Set up Africa's Talking API credentials and configured my application to use these credentials for sending SMS notifications.



## User Journey
Login Page
![alt text](screenshots/Login-page.png)

Redirected to login with KeyCloak
![alt text](screenshots/login-redirect.png)

Simple Homepage
![alt text](screenshots/home.png)

Add Customer Page
![alt text](screenshots/add-customer.png)

Success Adding a Customer
![alt text](screenshots/customeradded-success.png)

Add Order Page
![alt text](screenshots/add-order.png)

Success Adding a Page
![alt text](screenshots/add-order-success.png)

SMS SSent to customer after order creation
![alt text](screenshots/SMS-sending.png)



## Conclusion
My Customer-Order App is set up with Docker, Microk8s, MySQL, Keycloak, and SMS integration. Continuous deployment is managed via Ansible, ensuring my app stays up-to-date with minimal manual intervention.