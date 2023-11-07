import datetime, pickle, diabetes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, DateTime

# SQLAlchemy setup
app = Flask(__name__)
app.config['SECRET_KEY'] = "Banana73"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@postgres-service:5432/mydatabase'  # Replace with your actual database URI

db = SQLAlchemy(app)

class aggregatedmodel(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.now())
    referencepickle = Column(Text, nullable=False)

# Function to get the last item inserted into the models table
def get_last_item():
    last_item = aggregatedmodel.query.order_by(aggregatedmodel.id.desc()).first()
    return last_item

# Function to insert a new entry into the models table
def insert_new_entry(modelData):
    new_model = aggregatedmodel(referencepickle=modelData)
    db.session.add(new_model)
    db.session.commit()
    print(f'New entry added with pickle reference: {modelData}')

# Test the functions
if __name__ == '__main__':
    with app.app_context():
        # Test get_last_item
        last_item = get_last_item()
        if last_item:
            print(f'Last item id: {last_item.id}, timestamp: {last_item.timestamp}, pickle: {last_item.referencepickle}')
        else:
            print('No items found in the models table.')

        # Test insert_new_entry
        model = diabetes.load_model("model.pkl")
        modelData = pickle.dumps(model)  # Use pickle.dumps to serialize the model
        insert_new_entry(modelData)
