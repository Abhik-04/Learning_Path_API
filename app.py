from flask import Flask, jsonify, render_template, request, redirect, url_for
from database import db
from models import Topic, LearnerProgress, ProgressStatus

# app configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learning_path.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize DB with app
db.init_app(app)


# API Endpoints
@app.route('/api/learning-path/<int:learner_id>', methods=['GET'])
def get_learning_path(learner_id):
    try:
        # Fetch all topics and progress records once
        all_topics = Topic.query.all()
        learner_progress = LearnerProgress.query.filter_by(learner_id=learner_id).all()
        
        # Create maps for efficient lookups
        progress_map = {p.topic_id: p for p in learner_progress}
        completed_topics = {p.topic_id for p in learner_progress if p.status == ProgressStatus.COMPLETED}

        eligible_topics_with_status = []
        for topic in all_topics:
            # Check if the topic's prerequisites are met
            prereq_ids = [int(p_id) for p_id in topic.prerequisite_ids.split(',') if p_id]
            prerequisites_met = not prereq_ids or all(p_id in completed_topics for p_id in prereq_ids)

            # A topic is eligible if its prerequisites are met and it's not yet completed
            current_progress = progress_map.get(topic.id)
            is_completed = current_progress and current_progress.status == ProgressStatus.COMPLETED

            if prerequisites_met and not is_completed:
                # Get the current status and score, defaulting to "Not Started"
                status = current_progress.status.value if current_progress else ProgressStatus.NOT_STARTED.value
                score = current_progress.score if current_progress else 0
                
                eligible_topics_with_status.append({
                    'id': topic.id,
                    'title': topic.title,
                    'status': status,
                    'score': score
                })
        
        # This endpoint now only returns JSON, as it's just for the main page's script
        return jsonify({
            "learner_id": learner_id,
            "eligible_topics": eligible_topics_with_status
        })

    except Exception as e:
        return jsonify({"error": "Failed to fetch learning path.", "details": str(e)}), 500

# The main page route
@app.route('/')
def index():
    learners = db.session.query(LearnerProgress.learner_id).distinct().all()
    learner_ids = sorted([learner[0] for learner in learners])
    return render_template('index.html', learner_ids=learner_ids)

if __name__ == '__main__':
    app.run(debug=True)
