How to demo
============

## Run OPA in server mode

1. Check the [latest OPA release](https://github.com/open-policy-agent/opa/releases) and download it.
2. Put the binary file in the `PATH` of your system
3. Allow its execution with something like
    ```bash
    chmod 755 ~/opa
    ```
3. Run opa in server mode with the sample policies:

    ```bash
    cd examples
    opa run -s data.json app.rego
    ```
    
In this folder (examples) you will find a simple ``app.py`` file that contains endpoints to test how you can see some
data using OPA. For commodity purposes the user id will be passed in the request using the header *Authorization*.

> Run the app.py file with your IDE. It will run in http://localhost:5000


## Try out some http requests

- Check the home page
    curl http://localhost:5000

- Add a new user (steve) data using an admin user: Granted
    ```bash 
    curl -X POST \
      http://localhost:5000/data/steve \
      -H 'Authorization: steve' \
      -H 'Content-Type: application/json' \
      -d '{
        "fullname": "Steve Perez",
        "city": "New York",
        "salary": 3400,
        "biography": "Studied in harvard. Leaves in Miami, Florida"
    }'
    ```
 
 - Get new user's data using another non admin user: Denied
   ```bash
    curl -X GET \
      http://localhost:5000/data/steve \
      -H 'Authorization: paul' \
      -H 'Content-Type: application/json'
    ```
 
 - Get new user's data using an admin user: Granted
   ```bash
    curl -X GET \
      http://localhost:5000/data/steve \
      -H 'Authorization: eliux' \
      -H 'Content-Type: application/json'
    ``` 
    
 - Get new user's data using same user, yet not a admin one: Granted
   ```bash
    curl -X GET \
      http://localhost:5000/data/steve \
      -H 'Authorization: steve' \
      -H 'Content-Type: application/json'
    ```

- Check list of users using a non admin user: Denied
  ```bash
    curl -X GET \
      http://localhost:5000/list \
      -H 'Authorization: paul' \
      -H 'Content-Type: application/json'
    ```
    
- Check list of users using an admin user: Granted
  ```bash
    curl -X GET \
      http://localhost:5000/list \
      -H 'Authorization: eliux' \
      -H 'Content-Type: application/json'
    ```
    
- Try to delete a user using the same user but not an admin one: Denied
    ```bash
    curl -X DELETE \
      http://localhost:5000/data/steve \
      -H 'Authorization: steve' \
      -H 'Content-Type: application/json'
    ```
    
- Try to delete a user using an admin user: Granted
    ```bash
    curl -X DELETE \
      http://localhost:5000/data/steve \
      -H 'Authorization: eliux' \
      -H 'Content-Type: application/json'
    ```