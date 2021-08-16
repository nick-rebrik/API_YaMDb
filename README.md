# API Yamdb
 ***REST API for the service - databases of reviews about movies, books and music.***
### Description
The YaMDb project collects user reviews of works. The works are divided into categories: "Books", "Movies", "Music". The list of categories (Category) can be expanded (for example, you can add a category "Fine Arts" or "Jewelry"). The works themselves are not stored in YaMDb, you can't watch a movie or listen to music here. Each category has works: books, movies or music. For example, in the category "Books" there may be works "Winnie the Pooh and all-all-all" and "Martian Chronicles", and in the category "Music" - the song "Davecha" by the group "Insects" and Bach's second suite. The work can be assigned a genre from the list of presets (for example, "Fairy Tale", "Rock" or "Arthouse"). Only an administrator can create new genres. Grateful or indignant readers leave a review of the works and give the work a rating (rating in the range from one to ten). From the set of scores, the average score is automatically calculated.

### Technologies

- Python 3.7
- Django 3.0.5
- Django REST Framework
- Simple JWT
- ReDoc

### Quick start

1. Install and activate the virtual environment
2. Install all packages from [requirements.txt](https://github.com/nick-rebrik/Yatube/blob/master/requirements.txt)<br>
  ```pip install -r requirements.txt```
3. Run in command line:<br>
  ```python manage.py collectstatic```<br>
  ```python manage.py makemigrations```<br>
  ```python manage.py migrate```<br>
  ```python manage.py runserver```

### User registration algorithm

- The user sends a POST request with the email parameter to ```http://127.0.0.1:8000/api/v1/auth/email/```.
- YaMDB sends an email with a confirmation_code to the email address.
- The user sends a POST request with the parameters email and confirmation_code to ```http://127.0.0.1:8000/api/v1/auth/token/```, in response to the request he receives a token (JWT token). These operations are performed once, when the user registers. As a result, the user receives a token and can work with the API, sending this token with each request. After registration and receipt of the token, the user can send a PATCH request to ```http://127.0.0.1:8000/api/v1/users/me/``` and fill in the fields in his profile (description of the fields - in the documentation).

### Custom roles

- Anonymous - can view descriptions of works, read reviews and comments.
- Authenticated user (user) - can read everything, like Anonymous, can additionally publish reviews and rate works (movies / books / songs), can comment on other people's reviews and rate them; can edit and delete your reviews and comments.
- Moderator - the same rights as the Authenticated User plus the right to delete and edit any reviews and comments.
- Administrator - full rights to manage the project and all its contents. Can create and delete works, categories and genres. Can assign roles to users.
- The Django Administrator has the same rights as the Administrator role.

#### To view all API commands, go to the [ReDoc](http://127.0.0.1:8000/api/v1/redoc/) page:
```python
http://127.0.0.1:8000/api/v1/redoc/
```

### Authors

- [Nick Rebrik](https://github.com/nick-rebrik) - Team Leader. Review, comments and rating system
- [Yana Karausheva](https://github.com/anay2103) - Authorization and user part
- [Anatoliy Zubarev](https://github.com/anatoliy-zubarev) - Categories, genres and titles part
