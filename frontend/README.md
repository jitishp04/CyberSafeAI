## Frontend Folder

This folder contains all the files related to the **frontend** of the application to render the user interface. It includes the HTML templates, static files (CSS/ images).

### Folder structure:
#### 1. Static files:
- **/static/css**: 
  - **/dashboard.css**: Styles for the admin dashboard. 
  - **/login.css**:  Styles for the admin login page.
- **/static/images/CSA_AdminApp**:
  - **/logo.png**: App logo.
  
#### 2. HTML templates:
- **/templates/CSA_AdminApp**: Admin-side app
  - **/admin_dashboard.html**: Admin dashboard page for managing data and training models.
  - **/admin_login.html**: Admin login page.
- **/templates/moderation**: Client-side app
  - **/components**:
    - **error.html**: Displays dynamic error messages.
    - **form.html**: Contains the form for submitting user input for text analysis.
    - **header.html**: Provides a header component.
    - **results.html**: Displays the results of the text analysis.
  - **base.html**: Base template that other templates extend.
  - **home.html**: Main moderation page.
