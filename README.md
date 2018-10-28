# anathasevaashrama


# Instalation Guide :
  * Create virtual environment
    * virtualenv env 
    * pip install -r requirments.txt
    
  * DataBase Creation    
    
    *  Install Postgress sql from https://www.postgresql.org/download/
    *  psql -U postgress
    *  CREATE USER college_admin WITH PASSWORD roo@1234
    *  CREATE DATABASE college_data
    *  GRANT CONNECT ON DATABASE college_data TO college_admin;
    *  GRANT USAGE ON SCHEMA public TO college_admin;
    *  GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO college_admin;
    *  GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO college_admin;
    
# Setup and Run
  * python manage.py makemigrations
  * python manage.py migrate
  * python manage.py runserver
  
  
