# XMEME Project

It is Stage 2-B project for CRIO Winter of Doing 2021. We needed to make a fullstack website to upload, update and share meme with our Crio Family!

## Directory Contents

It Contains items as follows:

1. Frontend Folder (All the files for Frontend)
2. Dockerfile
3. requirements.txt
4. Readme file
5. Mandatory files (install.sh, sleep.sh,server_run.sh)

## Tech-Stack

- Frontend : BootStrap,JavaScript,CSS,Html
- Backend : Flask,sqlite3
- Deployment : (Earlier) AWS EC2 (t2-micro,ubuntu 20.04 ARM x64), Nginx Server, Gunicorn,
  (Latest) Frontend on Netlify and Backend on Heroku.
- Added Dockerfile for ease of usage

## For usage

You can upload new Images as Memes and update the Caption/Url of same also

- Frontend : [Frontend Page](https://xmemeshare.netlify.app/test.html)
- Backend API : [Backend Api for Get and Post memes](https://xmemeshare.herokuapp.com/memes)
- Backend API : [Backend Api for Get and Patch a particular meme (copy the link and update the id param)](https://xmemeshare.herokuapp.com/memes/{id})

## Made By

- Yash Kumar
- [Contact me on Email](mailto:yashbsr3@gmail.com?subject=[GitHub]%20Source%20XMEME%20APP)
