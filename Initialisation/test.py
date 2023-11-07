import datetime, diabetes, pickle
from sqlalchemy import create_engine, select, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy setup
DATABASE_URI = 'postgresql://user:password@postgres-service:5432/mydatabase'  # Replace with your actual database URI
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define a Model class to store model data
class Model(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    referencepickle = Column(String, nullable=False)  # Store the path to the pickle file

# Create tables in the database if they don't exist
Base.metadata.create_all(engine)

# Function to get the last item inserted into the models table
def get_last_item():
    session = Session()
    last_item = session.query(Model).order_by(Model.id.desc()).first()
    session.close()
    return last_item

# Function to insert a new entry into the models table
def insert_new_entry(modelData):
    session = Session()
    new_model = Model(timestamp=datetime.datetime.now(), referencepickle=modelData)
    session.add(new_model)
    session.commit()
    session.close()
    print(f'New entry added with pickle reference: {modelData}')

# Test the functions
if __name__ == '__main__':
    # Test get_last_item
    last_item = get_last_item()
    if last_item:
        print(f'Last item id: {last_item.id}, timestamp: {last_item.timestamp}, pickle: {last_item.referencepickle}')
    else:
        print('No items found in the models table.')

    # Test insert_new_entry
    model = diabetes.load_model("model.pkl")
    modelData = pickle.dump(model)
    insert_new_entry(modelData)
