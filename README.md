# Group 3: DIT826 - Software Engineering for Data-Intensive AI Applications
## CyberSafeAI
### System Description

CyberSafeAI is a web application designed to combat the rising cyber crime linked to social media use by identifying and flagging toxic text. Users can upload messages, tweets, or other text for toxicity analysis, with the system categorizing and assigning percentages to labels such as toxic, severe_toxic, obscene, threat, insult, and identity_hate. By highlighting problematic content, CyberSafeAI provides explainable AI solutions, helping individuals, content creators, and social media managers analyze and refine their text before posting, ultimately fostering a safer and healthier online environment.

### Latest Deployed Version
[User-side application](http://34.88.100.97/)

[Admin-side application](http://34.88.100.97/admin/login/)

Admin login: 

email: admin@example.com, password: p


### Instructions
Clone repository:

```
git clone git@git.chalmers.se:courses/dit826/2024/group3.git

cd backend
```

Running locally (in the backend directory):
```
Install requirements:
pip install -r requirements.txt

Make migrations:
python manage.py makemigrations

Apply migrations:
python manage.py migrate

Collect static files:
python manage.py collectstatic

Run the server:
python manage.py runserver
```
Running through docker (in the root directory):
```
docker build -t cybersafeai:latest .

docker run -p 8000:8000 --name cybersafeai_container cybersafeai:latest
```


### Project Structure 
| Directory  | Content |
|---|---|
| /ai_model  | Directory dedicated for the AI model, including the training, inference, data processing, evaluation, and versioning  |
| /backend  | Contains the backend logic, and configaration files for the django application along with database models  |
| /frontend  | Contains all the files required for the frontend for the user and admin such as HTML file templates, static files, along with frontend logic  |
| .gitignore, .dockerignore  | files to ignore during build or push  |
| deployment.yaml, service.yaml, sqlite-pv-pvc.yaml  | files regarding deployment of the docker container, databases, and AI models  |
| Dockerfile  | Creating a container for the complete application |
| .gitlab-ci.yml  | Gitlab pipeline to build, test, deploy the container |
