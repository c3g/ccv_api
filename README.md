# Canadian Common CV API
CCV API is a Django-based backed system to query the available CCVs. 


## **Technologies Used**

### **Server-side**
* [Python 3.7+](http://www.python.org): The language of choice.
* [Django 3.0+](https://www.djangoproject.com/): Framework used in this project.

### **Database**
* [PostgreSQL](https://www.postgresql.org/): Relational Database of choice.


## Installation 
1. Clone the repository
    ```bash
     git clone https://github.com/c3g/fms.git
    ```
  
2. Create a virtual environment with Python 3 or later, and activate it 
     ```bash
     virtualenv venv -p python3 
     source venv/bin/activate
     ```

3. Install the dependencies required for this project 
    ```bash 
    pip3 install -r requirements.txt
    ``` 
4. Create a new configuration file depending on the environment(development or production).
    ```bash
    cp ccv_api/development.cfg.dist ccv_api/development.cfg 
    ```
5. Create a new postgres database and configure credentials in the config file.
    ```editorconfig
    [database]  
    NAME: db_name
    USER: db_user
    PASSWORD: password_for_user
    HOST: localhost
    PORT: 5432
    ```
6. Run migrations to migrate existing schema to the database
    ```bash
   python3 manage.py migrate
    ```
## Running server
After following all installation steps, Run the Django server
```
python3 manage.py runserver
```

## Running Tests

