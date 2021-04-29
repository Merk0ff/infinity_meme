FROM python:3.9 as backend

WORKDIR /requirements
COPY requirements.txt /requirements
RUN pip3 install -r requirements.txt

WORKDIR /ininity_meme
COPY ./ /ininity_meme
RUN ["chmod", "+x", "./scripts/migrate_and_run.sh"]
RUN ["chmod", "+x", "./scripts/run_gunicorn.sh"]
RUN ["chmod", "+x", "./scripts/wait_for_services.sh"]
