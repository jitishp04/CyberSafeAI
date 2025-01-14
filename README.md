# Group 3: DIT826 - Software Engineering for Data-Intensive AI Applications
## CyberSafeAI
### System Description

CyberSafeAI is a web application designed to combat the rising cyber crime linked to social media use by identifying and flagging toxic text. Users can upload messages, tweets, or other text for toxicity analysis, with the system categorizing and assigning percentages to labels such as toxic, severe_toxic, obscene, threat, insult, and identity_hate. By highlighting problematic content, CyberSafeAI provides explainable AI solutions, helping individuals, content creators, and social media managers analyze and refine their text before posting, ultimately fostering a safer and healthier online environment.

Further details in the [final report](./FinalReport.pdf).

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

### Contributors and contributions:
#### Team Members:
| **Name**            | **Email**                      |
|----------------------|--------------------------------|
| Jitish Rajankumar Padhya | guspadji@student.gu.se       |
| M.Ali Elhasan        | guselhmu@student.gu.se         |
| Nishchya Arya        | gusaryni@student.gu.se         |
| Raghav Tengse        | gustengra@student.gu.se        |
| Utkarsh Singh        | gussinut@student.gu.se         |

#### Individual Contributions:

| **Name**                    | **Description of Contribution**                                                                                                                                                                                                                                                                                                                                                                                                       |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Jitish Rajankumar Padhya** | - User-side frontend (moderation app): Creating layout, components, fixing logics, code documentation, README.<br>- CI/CD: Creating GitLab pipeline for building, testing, and deployment; working on deployment solutions for GCP using buckets and Kubernetes in a pair programming environment.<br>- Refactoring and bug fixes for moderation app and CSA_AdminApp; architectural decisions for app restructuring.<br>- Removing toyModel and its dependencies for a lighter application.<br>- Experimentation and feature fixes for explainable AI (LIME, BERTtokenizers, highlighting word probabilities for toxicity categories).<br>- Report writing: Sections 1, 2, 3, 7; Architecture diagrams.<br>- Analysis history (user-side): Filtering, fetching, and bug fixes (removed in final iteration).<br>- Main and AI_model directory READMEs. |
| **M.Ali Elhasan**           | - Toy-Model: Created a complete toy model (AI model and GUI).<br>- Project Structure: Organized folder structures for efficient development.<br>- GUI: Set up user frontend and modifiable HTML.<br>- AI Model: Developed NLP-based and other AI models (supervised and unsupervised types).<br>- Train Model: Applied GPU training for faster and more efficient results.<br>- CI/CD: Enhanced deployment processes.<br>- DevOps: Server setup, debugging, and log tracking.<br>- Report checking: Reviewed team reports at key stages.<br>- Backend: Code documentation. |
| **Nishchya Arya**           | - Admin-side frontend (CSA_AdminApp): Created layouts, styled UI, and handled database functionality (upload/download).<br>- Docker: Created and managed Dockerfiles for containerized Django development.<br>- Deployment: Managed Kubernetes YAML files for orchestrating resources and ensured persistent database storage; set up and managed GCP environment.<br>- CI/CD: Minor fixes for successful deployment.<br>- Refactoring and bug fixes for moderation app and CSA_AdminApp.<br>- Backend: Code documentation and README.<br>- Report writing: Sections 1, 4, and 5; Architecture diagrams. |
| **Raghav Tengse**           | - Admin-side frontend: Developed login UI and functionality, authentication services, and logout functionality.<br>- Created Admin User Model.<br>- Testing: Generated unit tests for all system endpoints, including model creation tests.<br>- Report writing: Created user stories for requirements. |
| **Utkarsh Singh**           | - Admin-side frontend: Created and styled layouts; added database filters based on labels.<br>- User-side frontend: Displayed six labels in the dashboard; styled text analysis layout.<br>- Explainable AI: Used LIME and BERTtokenizers for highlighting word probabilities for toxicity categories.<br>- Report writing: Defined project requirements; authored Section 6 (Reflection). |


