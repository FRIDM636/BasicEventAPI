from flask_sqlalchemy import SQLAlchemy
import datetime 

db = SQLAlchemy()


class EventModel(db.Model):
    __tablename__ = "events"

    EventID = db.Column(db.Integer, primary_key=True)
    epoch = db.Column(db.Integer)
    stop = db.Column(db.Boolean)
    tags = db.Column(db.String(128))

    def __init__(self, EventID, stop = False, tags = ''):
        self.EventID = EventID
        self.epoch = int(datetime.datetime.now().timestamp()/1000)
        self.stop = stop
        self.tags = f"#{tags}#"

    def json(self):
        return {'EventID':self.EventID,
                'epoch': self.epoch, 
                'stop': self.stop, 
                'tags': self.tags}
    
    def add_event(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_event(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_event(cls, EventID):
        return cls.query.filter_by(EventID=EventID).first()
        