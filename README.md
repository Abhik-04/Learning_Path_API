# Learning_Path_API
A Flask web application that generates a personalized learning path for users based on their progress and topic prerequisites.

## Directory Structure

<pre>
├── app.py
├── database.py
├── models.py
├── populate_db.py
├── requirements.txt
├── static
│   └── style.css
└── templates
    └── index.html
</pre>

## File Descriptions

`app.py`: Main Flask application with all routes and logic.

`database.py`: Initializes the SQLAlchemy database connection

`models.py`: Defines the Topic and LearnerProgress database models.

`populate_db.py`: A script to create and seed the database with sample data.

`requirements.txt`: Lists the required Python packages for the project.

`static/style.css`: Contains all CSS for styling the web interface.

`templates/index.html`: The HTML template for the user-facing dashboard.

## How to Download and Run

Execute the following commands in your terminal to get the project running locally.

1. Clone the Repository
   
   `git clone https://github.com/Abhik-04/Learning_Path_API.git`
   
   `cd Learning_Path_API`

3. Set Up Virtual Environment & Install Dependencies

   `python3 -m venv venv`
   
   `source venv/bin/activate`

   `pip install -r requirements.txt`

4. Initialize the Database

   `python3 populate_db.py`

5. Run the Application

   `flask run`

The HTML page will be available at `http://127.0.0.1:5000/`. The JSON of various endpoints for a specific learner will be available at `http://127.0.0.1:5000/api/learning-path/<int:learner_id>` where different learner id needs to be added in place of `<learner_id>` to access the specific endpoint. 


