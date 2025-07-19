from app import app
from database import db
from models import Topic, LearnerProgress, ProgressStatus

def populate_database():
    """
    Populates the database with initial sample data.
    """
    with app.app_context():
        print("Dropping all tables and recreating...")
        db.drop_all()
        db.create_all()
        print("Tables created.")

        # Create topics
        print("Creating topics...")
        topics_data = [
            Topic(id=1, title="Introduction to Python"),
            Topic(id=2, title="Variables and Data Types", prerequisite_ids="1"),
            Topic(id=3, title="Control Flow (If/Else)", prerequisite_ids="2"),
            Topic(id=4, title="Functions", prerequisite_ids="2"),
            Topic(id=5, title="Introduction to APIs", prerequisite_ids="1"),
            Topic(id=6, title="Building a Flask API", prerequisite_ids="4,5")
        ]
        db.session.bulk_save_objects(topics_data)
        print(f"{len(topics_data)} topics created.")

        # Create learner's progress
        print("Creating learner progress data...")
        progress_data = [
            # Learner 1
            LearnerProgress(learner_id=1, topic_id=1, status=ProgressStatus.COMPLETED, score=95),
            LearnerProgress(learner_id=1, topic_id=2, status=ProgressStatus.COMPLETED, score=90),
            LearnerProgress(learner_id=1, topic_id=3, status=ProgressStatus.IN_PROGRESS, score=70),


            # Learner 2
            LearnerProgress(learner_id=2, topic_id=1, status=ProgressStatus.COMPLETED, score=88),

            # Learner 3
            LearnerProgress(learner_id=3)
        ]
        db.session.bulk_save_objects(progress_data)
        print(f"{len(progress_data)} progress records created.")

        db.session.commit()
        print("Database has been successfully populated!")

if __name__ == '__main__':
    populate_database()