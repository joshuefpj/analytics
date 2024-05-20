# analytics
This system will process a file from a mounted directory. The file will contain a list of debit and `Credit` transactions on an account.

The file will be processed and send a summary information to a user in the form of an email.

The file will contain 3 columns:

    - Id: this will represent the transaction `id`.
    - date: When the transaction was processed, the format will be `MM/DD`.
    - transaction: The amount for the transaction, where a credit transaction is indicated by a plus sign (+) and a debit transaction will be indicated by a minus sign (-). 

The summary email contains information on the total balance in the account, the number of
transactions grouped by month, and the average credit and average debit amounts

## Generate account files.
We can use the function `generate_data()` which will create a new file for a new account.
This function receives 2 parameters:

    - accounts: The number of account files we want to create, set default as 1.
    - rows: Number of transactions we want to create for each account, set default as 10.

## Instructions.
You need to get installed docker-compose on your computer in order to be able to run this project.

You can find a more detailed instructions in https://docs.docker.com/compose/install/

Before we start we need to define some environment variables in order to be able to run this project:

    - postgres_pass
    - postgres_user
    - postgres_db
    - postgres_host (this must match with postgres container's name)
    - sender_email
    - gmail_secret

You can use below command to define these in your current session as environment variables:

    $ export <variable_name>='your desired value here'

Under the `docker/postgres` directory we found our `docker-compose.yml` file, once you there simply run below command:

    docker-compose up -d

Once this command finish, you should have 2 containers up and running:

    - postgres_db_transactions
    - analytics_py-challenge

The first container will contain the Postgres database.
The second one will have the application, this will be set to run every 30 mins, you can modify this behaviour, modify the file `analytic/docker/app/py_cron` and change the values accordingly.

Now we can connect to the containers using below commands:

    - To connect into database, you need to introduce the password defined in `postgres_pass`, We can get the IP as follow:

        $ docker container inspect <container> | grep -i ipaddress
        $ psql -U $postgres_user -h <postgres_container_ip> -p 5432 -d $postgres_db

    - To connect into our linux container so we can monitor the jobs and check logs

        $ docker container exec -it <container> /bin/bash

The email will be send to the login email, if we want to modify this behavior update the receipt_email variable on `main.py` file for the receipt email.

We have defined 4 cron in this container. 3 of them wll take care of the files clean up over below directories:

    - analytic/data_collection
    - analytic/logs
    - analytic/statistic_images

Unfortunately the fourth isn't running at all. so we need to run manually by execution below command:

    $ python3 /usr/app/analytic/main.py > /usr/app/analytic/logs/log_transactions_`date "+%Y%m%d_%H%M%S"`.log 2>&1

## Main app.
Here we store the main logic of our application.

This file will create a new account(we can dissable this behavior by commenting the line).

Function `file_list()` will retrieve all the CSV files from our data directory to be processed.

Once we have the list `generate_details()` function will process each file individually, will extract the details and made some transformations, generate the 'amount transactions' per 'month' for each type(`Debit`|`Credit`) and save as 'PNG' image on image directory.

After processing the details, `send_email()` function will structure and send an email for each account in the list,

## Database.
Tables stored in a Postgres Database.

Only 2 tables are used:

    - account_details
        Will be used to store information about account, including ID (7 character code)

    - transaction_logging
        Will contain a row for each run containing information for the particular account like account ID, credit and debit amoun and date run.

## Versioning
### Vesion 0.1.0
This 0.1.0 version needs a directory where we need to store our credentials for gmail and postgres, all in csv file with 2 columns the first will have the name of the variable second with the actual value for that variable.

Will update this behaviour to take data from environment variables for Docker.

Additionally, this 0.1.0 version isn't attaching correctly the images on email, they appears like attachments instead of be part of the email.

### Version 0.1.1
This 0.1.1 version adds SQLalchemy to communicate with database, adds functions to interact with tables.

Database and table creation added into Dockerfile to be created once container is created.

Adds scheduled cron to get python script run every 30 mins.

### Version 0.1.5
This 0.1.5 fix the image attachment on the email template.

Adds logging messages for tracking purposes for each run. Beside the fact there is already a library for this, decided to create one tiny personal option.

Both containers now are created with docker-compose, cron is added to crontab, is set to run every 30 mins.

Main file is now working as expected, the validation for the file located is now finished and only process those files modified after the previous run.

Accounts are now saved into database into `account_details`, validation to keep account unique.
Transactions are added into `transactions_logging` table.

### Version 1.0.0
Remove hardcoded variable values.

Update cron command. Still facing issues, isn't picked up by cron.
We can get the command from `crontab -l` command in the container and run it manually.

Added missing env variable `postgres_host`.

### Version 1.0.1
Add cron for old files clean up, it will run every 5 mins, cleanining files older than 25 mins, directories to be cleaned up:

    - analytic/logs
    - analytic/data_collection
    - analytic/statistic_images

The directory logs will contain the log files, statistic_images will contain stats images and the data_collection will keep the data files, we can modify behavior either by removing the line or commenting on `py_cron` or increase/decrease the `mmin` value on cron line.

The python script still doesn't run as expected. still we can run manually by getting the command from `py_cron` file
