from flask_restful import Resource,reqparse
from models.event import EventModel, db



class Event(Resource):
    parser = reqparse.RequestParser()
    # This will check the passed json body if it contains all records
    # this will allow us to through errors automatically instead of checking them maunually 
    parser.add_argument('tags', type=str, required=False)
    parser.add_argument('stop', type=bool, required=False)

    
    def get(self, EventID):
        '''
        This method used to an event by a given ID
        '''
        event = EventModel.find_event(EventID)
        if event:
            return event.json()
        return {'message': 'event not found'}, 404
    
    def post(self, EventID):
        '''
        This function is used to add a new event to the database
        Put may do the same but we prefer to separate them for future extension 
        '''
        if EventModel.find_event(EventID):
            return {'message': f'An event with EventID {EventID} already exists'}, 400

        # The parser will detect automatically if the body is not well formatted so it 
        # it will throw a 400 bad request error reponse
        data = Event.parser.parse_args()
        event = EventModel(EventID, **data)

        # if the server cannot add the event to database throw this 500 error reponse
        try:
            event.add_event()
        except Exception as error:
            return {'message': f'Server error occured when trying to save event {error}'}, 500

        return event.json(), 201

    def put(self, EventID):
        '''
        This function is used to upate or add an event if it does 
        not exists, we will not go through input check or more details
        this is just an illstration basic project
        '''
        event = EventModel.find_event(EventID)

        if not event:
            # Same case as adding a new event
            data = Event.parser.parse_args()
            #** is used to unpack the dictionnnary
            event = EventModel(EventID, **data)
        # use this to update stop or tags
        else:
            data = Event.parser.parse_args()
            # you may check data compatiblity here
            if data['stop'] is not None:    event.stop = data['stop'] 
            if data['tags']:
                # the format of tags: #tag1##tag2##tag3#
                # if tag exist or empty don't add it
                # you may set another rules of tag length, chars to remove...
                if data['tags'] not in event.tags.split('##'):
                    event.tags += f"#{data['tags']}#"
        try:
            event.add_event()
        except:
            return {'message': 'Server error when trying to update event'}, 500
        
        return event.json(), 200

    def delete(self, EventID):
        '''
        This function used to delete an event from the database
        we may mock this function to force authentication.
        '''
        event = EventModel.find_event(EventID)

        if event:
            try:
                event.delete_event()
            except:
                return {'message': 'Server error when trying to delete event'}, 500
        else:
            return {'message': 'event not found'}, 404

        return '', 204


class Allevents(Resource):
    '''
    This class is used to isolate 
    the CRUD class (event)
    we may implements other endpoints here 
    '''
    def get(self):
        '''
        This method is used to get all te events in the database
        '''
        try:
            return {'events': [i.json() for i in EventModel.query.all()]}
        except Exception as error:
            return {'message': f'Server error when trying to get all events\n: {error}'}, 500