from database import db
import enum

# Defines the progress status for a topic
class ProgressStatus(enum.Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

# Define the model for a topic
class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, unique=True)
    prerequisite_ids = db.Column(db.String(100), default='')

    def __repr__(self):
        return f"<Topic {self.id}: {self.title}>"

# Define the model for learner progress
class LearnerProgress(db.Model):
    __tablename__ = 'learner_progress'
    id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer, nullable=False, index=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False, default=1)
    status = db.Column(db.Enum(ProgressStatus), nullable=False, default=ProgressStatus.NOT_STARTED)
    score = db.Column(db.Integer, default=0)

    topic = db.relationship('Topic')

    def __repr__(self):
        return f"<LearnerProgress {self.id}: Learner {self.learner_id}, Topic {self.topic_id}, Status: {self.status.value}>"