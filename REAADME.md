## Creating The Bot in telegram 
    => use BotFather on telegram to create you bot and get your token 
    => save this token in your .env file 

## build the docker container 
    docker build -t my_telegram_bot .
# run the docker container 
    docker run --rm --env-file .env my_telegram_bot
    Note: when using the .env file make sure you remove the quotes around the values
## Hosting docker using railway