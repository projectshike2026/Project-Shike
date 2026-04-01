"""
Database models for Section Tracker application.
All tables defined with SQLAlchemy ORM.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model - stores student information and credentials."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), unique=True, nullable=False)  # e.g., CSE22-001
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(255), default='default.png')
    bio = db.Column(db.Text, default='')
    skills = db.Column(db.Text, default='[]')  # JSON array of skills
    work = db.Column(db.String(255), default='')  # Current work/position
    experience = db.Column(db.Text, default='')  # Work experience
    education = db.Column(db.String(255), default='')  # Education info
    total_score = db.Column(db.Integer, default=0)
    rank = db.Column(db.Integer, default=0)
    role = db.Column(db.String(20), default='student')  # student/moderator/admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    projects = db.relationship('Project', backref='author', lazy='dynamic')
    notes = db.relationship('Note', backref='uploader', lazy='dynamic')
    activities = db.relationship('Activity', backref='user', lazy='dynamic')
    scoreboard = db.relationship('Scoreboard', backref='user', uselist=False)
    players = db.relationship('Player', backref='user', lazy='dynamic')
    achievements = db.relationship('UserAchievement', backref='user', lazy='dynamic')
    events_created = db.relationship('Event', backref='creator', lazy='dynamic')
    post_likes = db.relationship('PostLike', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set the password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'




class Project(db.Model):
    """Project model - stores student projects."""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Web Dev, Mobile, AI/ML, IoT, DBMS
    github_link = db.Column(db.String(255), default='')
    demo_link = db.Column(db.String(255), default='')
    thumbnail = db.Column(db.String(255), default='default_project.png')
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    collaborators = db.Column(db.Text, default='[]')  # JSON array of user_ids
    
    # Relationships
    ratings = db.relationship('ProjectRating', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def average_rating(self):
        """Calculate average rating."""
        if self.rating_count == 0:
            return 0
        return round(self.total_rating / self.rating_count, 1)
    
    def __repr__(self):
        return f'<Project {self.title}>'


class ProjectRating(db.Model):
    """Project ratings and reviews."""
    __tablename__ = 'project_ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    rated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating_value = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to user who rated
    rater = db.relationship('User', backref='ratings_given')
    
    def __repr__(self):
        return f'<Rating {self.rating_value} for Project {self.project_id}>'


class Sport(db.Model):
    """Sports categories."""
    __tablename__ = 'sports'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(50), default='fa-trophy')
    
    # Relationships
    players = db.relationship('Player', backref='sport', lazy='dynamic')
    
    def __repr__(self):
        return f'<Sport {self.name}>'


class Player(db.Model):
    """Player profiles for sports."""
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sport_id = db.Column(db.Integer, db.ForeignKey('sports.id'), nullable=False)
    jersey_number = db.Column(db.Integer, default=0)
    position = db.Column(db.String(50), default='')
    is_captain = db.Column(db.Boolean, default=False)
    
    # Relationships
    performances = db.relationship('MatchPerformance', backref='player', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Player {self.user.username} - {self.sport.name}>'


class MatchPerformance(db.Model):
    """Match performance records."""
    __tablename__ = 'match_performances'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    opponent_team = db.Column(db.String(100), nullable=False)
    match_date = db.Column(db.Date, nullable=False)
    
    # Cricket stats
    runs = db.Column(db.Integer, default=0)
    wickets = db.Column(db.Integer, default=0)
    catches = db.Column(db.Integer, default=0)
    balls_faced = db.Column(db.Integer, default=0)
    overs_bowled = db.Column(db.Float, default=0.0)
    
    # Football stats
    goals = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    
    # Badminton/other stats
    points_scored = db.Column(db.Integer, default=0)
    
    # Verification
    verified = db.Column(db.Boolean, default=False)
    
    @property
    def strike_rate(self):
        """Calculate batting strike rate."""
        if self.balls_faced == 0:
            return 0
        return round((self.runs / self.balls_faced) * 100, 2)
    
    def __repr__(self):
        return f'<Match vs {self.opponent_team} on {self.match_date}>'


class Note(db.Model):
    """Notes and study materials."""
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20), default='pdf')  # pdf, doc, video_link
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    download_count = db.Column(db.Integer, default=0)
    helpful_count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Note {self.title}>'


class Activity(db.Model):
    """Activity log for scoring and feed."""
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, default='')
    points_earned = db.Column(db.Integer, default=0)
    related_id = db.Column(db.Integer, default=0)  # Reference to project_id, note_id, etc.
    activity_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Activity {self.activity_type} by User {self.user_id}>'


class Scoreboard(db.Model):
    """User scoreboards for rankings."""
    __tablename__ = 'scoreboards'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    weekly_score = db.Column(db.Integer, default=0)
    monthly_score = db.Column(db.Integer, default=0)
    yearly_score = db.Column(db.Integer, default=0)
    lifetime_score = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Scoreboard User {self.user_id}: {self.lifetime_score} pts>'


class Achievement(db.Model):
    """Achievement badges definitions."""
    __tablename__ = 'achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='fa-medal')
    criteria = db.Column(db.Text, default='{}')  # JSON describing unlock conditions
    points = db.Column(db.Integer, default=0)
    
    # Relationships
    users = db.relationship('UserAchievement', backref='achievement', lazy='dynamic')
    
    def __repr__(self):
        return f'<Achievement {self.name}>'


class UserAchievement(db.Model):
    """User earned achievements."""
    __tablename__ = 'user_achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=False)
    earned_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserAchievement User {self.user_id} earned {self.achievement_id}>'


class Event(db.Model):
    """Events and activities calendar."""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    event_type = db.Column(db.String(50), nullable=False)  # competition, workshop, study_session
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), default='')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Event {self.title}>'


class PostLike(db.Model):
    """Likes on activities/posts."""
    __tablename__ = 'post_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Like by User {self.user_id}>'


class Comment(db.Model):
    """Comments on activities/posts."""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Comment by User {self.user_id}>'


class Status(db.Model):
    """User status updates (100 char max)."""
    __tablename__ = 'statuses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    author = db.relationship('User', backref='statuses')
    
    def __repr__(self):
        return f'<Status by User {self.user_id}>'


class Poll(db.Model):
    """User polls with voting."""
    __tablename__ = 'polls'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    author = db.relationship('User', backref='polls')
    options = db.relationship('PollOption', backref='poll', lazy='dynamic', cascade='all, delete-orphan')
    votes = db.relationship('PollVote', backref='poll', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def is_expired(self):
        """Check if poll has expired."""
        return datetime.utcnow() > self.expires_at
    
    @property
    def total_votes(self):
        """Get total vote count."""
        return self.votes.count()
    
    def __repr__(self):
        return f'<Poll {self.question}>'


class PollOption(db.Model):
    """Poll answer options."""
    __tablename__ = 'poll_options'
    
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)
    option_text = db.Column(db.String(100), nullable=False)
    vote_count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<PollOption {self.option_text}>'


class PollVote(db.Model):
    """Anonymous poll votes - one per user per poll."""
    __tablename__ = 'poll_votes'
    
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('poll_options.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    voted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('poll_id', 'user_id', name='_poll_user_vote_uc'),)
    
    def __repr__(self):
        return f'<PollVote on Poll {self.poll_id}>'



class QuestionPaper(db.Model):
    """Semester exam question papers."""
    __tablename__ = 'question_papers'

    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    course_code = db.Column(db.String(20), default='')
    semester = db.Column(db.String(20), nullable=False)  # e.g. "1st", "2nd", "3rd"
    year = db.Column(db.Integer, nullable=False)  # e.g. 2024, 2025
    exam_type = db.Column(db.String(30), default='Final')  # Mid, Final, Quiz
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20), default='pdf')
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    download_count = db.Column(db.Integer, default=0)

    uploader = db.relationship('User', backref='uploaded_questions')

    def __repr__(self):
        return f'<QuestionPaper {self.course_name} {self.exam_type} {self.year}>'


class ClassRoutine(db.Model):
    """Weekly class routine/schedule entries."""
    __tablename__ = 'class_routines'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(15), nullable=False)  # Saturday, Sunday, etc.
    time_slot = db.Column(db.String(30), nullable=False)  # e.g. "08:00 - 09:15"
    course_name = db.Column(db.String(100), nullable=False)
    course_code = db.Column(db.String(20), default='')
    teacher_name = db.Column(db.String(100), default='')
    room = db.Column(db.String(50), default='')
    section = db.Column(db.String(10), default='B')
    routine_type = db.Column(db.String(20), default='Theory')  # Theory, Lab
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<ClassRoutine {self.day} {self.time_slot} {self.course_name}>'


# Helper table for followers (many-to-many)
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


# Add followers relationship to User model
User.followed = db.relationship(
    'User', secondary=followers,
    primaryjoin=(followers.c.follower_id == User.id),
    secondaryjoin=(followers.c.followed_id == User.id),
    backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
)

