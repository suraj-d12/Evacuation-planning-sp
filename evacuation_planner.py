from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class EvacuationPlan(Base):
    __tablename__ = 'evacuation_plans'

    id = Column(Integer, primary_key=True)
    days_ahead = Column(Integer)
    max_threat_level = Column(Float)
    affected_population = Column(Integer)
    evacuation_time = Column(Float)

    # Add more columns for detailed plan information
    evacuation_routes = Column(String)  # Store as JSON string
    evacuation_priority = Column(String)  # Store as JSON string
    resource_allocation = Column(String)  # Store as JSON string
    weather_conditions = Column(String)  # Store as JSON string
    earthquake_magnitude = Column(Float)
    landslide_risk = Column(Float)
    created_at = Column(String)  # Timestamp of plan creation

engine = create_engine('postgresql://username:password@localhost/dbname')
Session = sessionmaker(bind=engine)

# In your main function:
session = Session()
for days, plan in plans.items():
    db_plan = EvacuationPlan(
        days_ahead=days,
        max_threat_level=np.max(plan['threat_level']),
        affected_population=np.sum(plan['affected_areas']),
        evacuation_time=plan['evacuation_time']
    )
    session.add(db_plan)
session.commit()
