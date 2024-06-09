from src import app, db
from models.train_data import TrainingData
from models.user import Admin

app.app_context().push()
if __name__ == '__main__':
    db.create_all()
