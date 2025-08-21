# **Jail Management System**
This repository features a demo api for a Jail Management application. Featuring crud operations for the inmates of the database, as well as registering, changing cells and convicting inmates with crimes. The project uses [PostgreSQL](https://www.postgresql.org/) as a databse.
[Docker](https://www.docker.com/) is needed for the application to be ran.

# Requirements
For running the api, you will need either a linux or a windows based machine with [Docker](https://www.docker.com/) installed. Having [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/) can also be used to test the ednpoints or you can use a browser.

# Setup
For getting the database set up on your machine, running this command at root level is enough:
```
docker compose up
```
Afterwards the app is gonna be available on:
```
localhost:5000
```
