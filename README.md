# PYTHON APP INTERACTING WITH RABBITMQ AND CELERY

This is a simple Python application that interacts with RABBITMQ to enable the transfer of messages from the producer to the consumers. It uses Celery, a powerful asynchronous task queue/job queue based on distributed message passing, to handle the background task processing. Flask is used as the web framework to facilitate communication and integration between the different components of the system.

## STEP 1: PYTHON SCRIPTING
Write your Python scripts to create an app that can send an email to the consumer and celery to send tasks using  a queueing system. 
**How will Celery and RABBITMQ meet?**
Asides from the SMTP_PORT, SMTP_SERVER, EMAIL & PASSWORD variable that will be in your .env file, these variables below are expected to be there:
```
CELERY_BROKER_URL=amqp://<rabbitmq-user>:<rabbitmq-password>@<ip-address>:5672//
CELERY_RESULT_BACKEND=rpc://<ip-address>
```


## STEP 2: INSTALL RABBITMCQ
```
sudo apt-get update
sudo apt-get install rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
sudo rabbitmqctl status

```
## STEP 3: CREATE A USER FOR RABBITMCQ
This user and passowrd will be used as a url that Celery will interact with.
You can replace `myuser` and `mypassword` 
```
sudo rabbitmqctl add_user myuser mypassword
sudo rabbitmqctl set_user_tags myuser administrator
sudo rabbitmqctl set_permissions -p / myuser ".*" ".*" ".*"

```
## STEP 4: CONFIGURE RABBITMCQ
To configure RABBITMCQ;
1. Open a file `sudo nano /etc/rabbitmq/rabbitmq.conf`
2. Include the following code in the file
```
listeners.tcp.default = 0.0.0.0:5672
management.listener.port = 15672
management.listener.ip = 0.0.0.0
```

## STEP 5: ALLOW FIREWALL
```
sudo ufw allow 5672
sudo ufw allow 15672
```
## STEP 6: INSTALL NGINX
```
sudo apt-get update
sudo apt-get install nginx   # To install nginx
```
## STEP 7: CREATE AN NGINX CONFIG FILE
1. create the file  `sudo nano /etc/nginx/sites-available/messaging_system.conf`
2. Copy and paste this code in the file
```
server {
    listen 80;
    server_name <server-ip>;  # Use your domain name or IP if necessary

    location / {
        proxy_pass http://127.0.0.1:5000;  # Flask app runs on port 5000
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
3. Create a symlink to the config file that comes with the installation of nginx, test and restart the nginx server.
```
sudo ln -s /etc/nginx/sites-available/messaging_system /etc/nginx/sites-enabled #To create a symlink to enable the sites
sudo nginx -t                # To test the nginx server 
sudo systemctl restart nginx  # To restart the server

```

## STEP 8: INSTALL NGROK
```
 curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok

```

## STEP 9: SIGN UP ON THE NGROK PLATFORM
1. To sign up click here: [NGROK](https://ngrok.com/)
2. Get your authentication token
3. Configure your terminal with the token

## STEP 10: RUN YOUR SERVICES
**First daemonize your Celery**

```

**Deamonise your python app service**
```

```





