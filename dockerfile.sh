
#!/bin/bash


# git clone the repo
git clone https://gitlab.crio.do/COHORT_ME_BUILDOUT_XMEME_ENROLL_1612436694845/yashbsr3-me_buildout_xmeme.git

# cd to the cloned repo directory
cd ./yashbsr3-me_buildout_xmeme


# Create the container image, this will use the Dockerfile

docker build -t xmeme_app .

# Run the app container on port 8081

docker run -d --net="host" xmeme_app

# Run sleep.sh

chmod +x sleep.sh

./sleep.sh


# Execute the POST /memes endpoint using curl

curl --location --request POST 'http://localhost:8081/memes' --header 'Content-Type: application/json' --data-raw '{"name": "xyz","url": "https://i.ytimg.com/vi/LfHxDuBbBtk/sddefault.jpg#404_is_fine","caption": "This is a meme"}'


# Execute the GET /memes endpoint using curl

curl --location --request GET 'http://localhost:8081/memes'