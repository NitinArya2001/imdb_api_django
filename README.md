# imdb_api_django

1. Setup the code in local and create a virtual environment
     python -m venv env
2. After Creating virtual environment activate it
     cd env/scripts/activate
3. After that Install the requirements
     pip install -r requirements.txt
4. To upload the movies data use this api endpoint - http://127.0.0.1:8000/upload/
   
5. To view the list of all the movies with filter and ordering with pagination, use this api endpoint - http://127.0.0.1:8000/movies/?year=1995&language=en&sort=release_date_dsc
