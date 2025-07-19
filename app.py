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

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     # This data is needed for every request (GET or POST)
#     learners_query = db.session.query(LearnerProgress.learner_id).distinct().order_by(LearnerProgress.learner_id).all()
#     all_learner_ids = [learner[0] for learner in learners_query]
#     all_topics = Topic.query.all()

#     # --- HANDLE FORM SUBMISSIONS (POST REQUESTS) ---
#     if request.method == 'POST':
#         action = request.form.get('action')

#         # --- Action: Update a course's progress ---
#         if action == 'update':
#             learner_id = request.form.get('learner_id', type=int)
#             topic_id = request.form.get('topic_id', type=int)
#             new_status_str = request.form.get('status')
#             new_score = request.form.get('score', 0, type=int)

#             try:
#                 new_status = ProgressStatus(new_status_str)
#                 progress_record = LearnerProgress.query.filter_by(learner_id=learner_id, topic_id=topic_id).first()

#                 if progress_record:
#                     progress_record.status = new_status
#                     progress_record.score = new_score
#                 else:
#                     new_record = LearnerProgress(learner_id=learner_id, topic_id=topic_id, status=new_status, score=new_score)
#                     db.session.add(new_record)
                
#                 db.session.commit()
#             except Exception as e:
#                 db.session.rollback()
#                 # In a real app, you'd add flash messaging for errors
#                 print(f"Error updating progress: {e}")

#             return redirect(url_for('index', learner_id=learner_id))

#         # --- Action: Add progress for a learner ---
#         elif action == 'add_learner_progress':
#             new_learner_id = request.form.get('new_learner_id', type=int)
#             topic_id = request.form.get('topic_id', type=int)
#             status_str = request.form.get('status')

#             if new_learner_id and topic_id and status_str:
#                 try:
#                     status = ProgressStatus(status_str)
#                     # Check if this record already exists to avoid duplicates
#                     existing = LearnerProgress.query.filter_by(learner_id=new_learner_id, topic_id=topic_id).first()
#                     if not existing:
#                         new_progress = LearnerProgress(learner_id=new_learner_id, topic_id=topic_id, status=status, score=0)
#                         db.session.add(new_progress)
#                         db.session.commit()
#                 except Exception as e:
#                     db.session.rollback()
#                     print(f"Error adding learner progress: {e}")

#             return redirect(url_for('index', learner_id=new_learner_id))

#     # --- DISPLAY PAGE (GET REQUEST) ---
#     selected_learner_id = request.args.get('learner_id', type=int)
#     eligible_courses = []

#     if selected_learner_id:
#         # Fetch all progress for the selected learner
#         learner_progress = LearnerProgress.query.filter_by(learner_id=selected_learner_id).all()
#         progress_map = {p.topic_id: p for p in learner_progress}
#         completed_topics = {p.topic_id for p in learner_progress if p.status == ProgressStatus.COMPLETED}

#         for topic in all_topics:
#             # Check if prerequisites are met
#             prereq_ids = [int(p_id) for p_id in topic.prerequisite_ids.split(',') if p_id]
#             prereqs_met = not prereq_ids or all(p_id in completed_topics for p_id in prereq_ids)

#             current_progress = progress_map.get(topic.id)
#             is_completed = current_progress and current_progress.status == ProgressStatus.COMPLETED

#             # A course is eligible if its prerequisites are met and it's not yet completed
#             if prereqs_met and not is_completed:
#                 status = current_progress.status.value if current_progress else ProgressStatus.NOT_STARTED.value
#                 score = current_progress.score if current_progress else 0
#                 eligible_courses.append({'id': topic.id, 'title': topic.title, 'status': status, 'score': score})

#     return render_template('index.html',
#                            all_learner_ids=all_learner_ids,
#                            selected_learner_id=selected_learner_id,
#                            eligible_courses=eligible_courses,
#                            all_topics=all_topics,
#                            statuses=[s.value for s in ProgressStatus])

if __name__ == '__main__':
    app.run(debug=True)