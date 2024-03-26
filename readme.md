# LM-IMAGES
lm-images backend

## INSTALL
### WINDOWS
1) python (3.10.12, include PATH)
2) install pip (https://pip.pypa.io/en/stable/installation/)
3) install virtual env (https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
### LINUX
 - already have
## CLONE

git clone https://github.com/borisbasic/lm_images

cd lm_images

## Install virtual enviroment (venv)
 - python -m venv venv (win)
 - python3 -m venv venv (linux)
start virtual env 
 - windows, venv\Scripts\activate
 - linux, source venv/bin/activate

pip install -r requirements.txt

## START SERVER

uvicorn main:app --reload

## DOCUMENTATION

http://localhost:8000/docs#/




## DOCKER

