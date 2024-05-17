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

## Main app.
Here we store the main logic of our application.

This file will create a new account(we can dissable this behavior by commenting the line).

Function `file_list()` will retrieve all the CSV files from our data directory to be processed.

Once we have the list `generate_details()` function will process each file individually, will extract the details and made some transformations, generate the 'amount transactions' per 'month' for each type(`Debit`|`Credit`) and save as 'PNG' image on image directory.

After processing the details, `send_email()` function will structure and send an email for each account in the list,

## Database.

## Versioning
### Vesion 0.1.0
This 0.1.0 version needs a directory where we need to store our credentials for gmail and postgres, all in csv file with 2 columns the first will have the name of the variable second with the actual value for that variable.

Will update this behaviour to take data from environment variables for Docker.

Additionally, this 0.1.0 version isn't attaching correctly the images on email, they appears like attachments instead of be part of the email.
