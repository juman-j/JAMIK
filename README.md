JAMIK - Choosing food made simple: Personalized AI-powered menu recommendations.
---
This repository contains _the backend part_ of the final project
of the master's program Data Analytics for Business at the Prague University of Economics and Business.

Authors of this part of the project:
- Artem Sorokin
- Jan Doleček  
- Kryštof Dostál (the recommendation engine)
---

The goal of the project was to create a web application to generate a personalized restaurant menu.  
### Basic Functions:
1. **Recommendation engine** based on user history.
2. **Translating** **menus** into a user-selected language (DeepL API).
3. **Filtering dishes** by ingredients, food restrictions, etc.
4. **Allergen warning**.

### Sequence of actions to start the application:
1. Create an **.env** file to store the variables for connecting to your database.  
The variables that need to be added:  
  `DB_HOST`   
  `DB_PORT`  
  `DB_NAME`  
  `DB_USER`  
  `DB_PASS`  
  `SECRET_AUTH` (A constant secret which is used to encode the token)  
  `DEEPL_URL = "https://api-free.deepl.com/v2/translate"`  
  `DEEPL_API_KEY = your key`
3. Create a virtual environment with a python version greater than or equal to **3.10**
4. Install poetry: `pip install poetry`
5. Installing dependencies: `poetry install`
6. Creating all tables in the database: `poetry run alembic upgrade head`
7. Start the application on the local machine: `poetry run uvicorn src.main:app --reload`
8. Documentation of the application will be available at `http://127.0.0.1:8000/docs`
