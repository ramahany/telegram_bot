## Creating The Bot in telegram 
    => use BotFather on telegram to create you bot and get your token 
    => save this token in your .env file 



## build the docker container 
    docker build -t my_telegram_bot .
### run the docker container 
    docker run --rm --env-file .env my_telegram_bot
    Note: when using the .env file make sure you remove the quotes around the values

## For div with docker 
    because i use COPY it copies all the files to the image once its builtk, so to avoid that i will be using the following instruction while div.
    CMD:
        docker run --rm --env-file .env -v .:/app my_telegram_bot

### using docker composer 
    Yes, build: . tells docker-compose to look for a Dockerfile in the current directory and build it automatically when you run docker-compose up.
    If you want to force a rebuild after changes to your Dockerfile or requirements:
    docker-compose up --build
    Otherwise docker-compose up reuses the previously built image.
    
## Hosting docker using railway