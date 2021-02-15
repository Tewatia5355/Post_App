
#!/bin/bash


# Any installation related commands
sudo apt-get update -y
sudo apt upgrade -y
sudo apt-get install -y python3-venv
sudo apt-get install -y python3-pip
pip3 install -r requirements.txt
pip3 install flask-swagger-ui flask-cors




# Any configuration related commands