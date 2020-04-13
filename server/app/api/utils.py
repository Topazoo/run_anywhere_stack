
from database.main import Database
from api.errors import API_Error

from bson import ObjectId
from pymongo.cursor import Cursor

from flask import jsonify, Response
import json, logging

def JsonResponse(content: dict = {}, code: int = 200) -> Response:
    ''' Format an API JSON response.
        --> content [dict] : A dictionary of JSON serializable objects to return. Optional.
        
        --> code [int]: The HTTP status code to return. Optional.
        
        <-- The JSON formatted response. { <<content>>, "code": <<code>> }
    '''

    content['code'] = code
    
    return jsonify(**content)


def JsonError(method: str, exception: Exception) -> Response:
    ''' Format an API JSON error response.
        --> method : The HTTP request method that generated the error (e.g. POST).
        
        --> exception : The error generated.
        
        <-- A JSON formatted error response : { "msg" <<error_message>>, "code": <<code>> }.
    '''

    error_msg = '{} - {}'.format(method, str(exception)) 
    error_code = exception.code if type(exception) == API_Error else 500
    
    logging.critical(error_msg)

    return JsonResponse({'msg': error_msg}, error_code)


def parse_query_pairs(payload: str) -> dict:
    ''' Parse out one or more key/value pairs from a query string
        (e.g. /api/?param=key:value || /api/?param=key1:value1,key2:value2).
    
        --> payload : The arguments supplied with the parameter (The key value pairs in string form).
        <-- The parsed key/value pairs.
    '''

    pairs = {}
    for pair_tuple in map(lambda pair: pair.split(':'), [pair for pair in payload.split(',')]):
        pairs[pair_tuple[0]] = pair_tuple[1]

    return pairs


def parse_query_params(payload: str) -> list:
    ''' Parse out one or more parameter values pairs from a query string
        (e.g. /api/?param=value || /api/?param=value1,value2).
    
        --> payload : The arguments supplied with the parameter (The values in string form).
        <-- The parsed values.
    '''

    return [(value, 1) for value in payload.split(',')]


def parse_query_string(payload: str) -> dict:
    ''' Parse out the filter and sort from a query string
    
        --> payload : The arguments supplied with the parameter (The values in string form).
        <-- The parsed values.
    '''

    dict_payload = {}
    query_params = payload.split('&')
    for param in query_params:
        args = param.split('=')
        if args[0] == 'filter':
            dict_payload[args[0]] = parse_query_pairs(args[1])
        if args[0] == 'sort':
            dict_payload[args[0]] = parse_query_params(args[1])

    return dict_payload


def fetch_and_filter_data(request_params: dict, database:str=None, collection:str=None) -> list:
    ''' Fetch records from the database matching a filter supplied in an HTTP request.
        Ensure fields supplied in the filter exist for the model. If no filter is supplied
        all objects are retrived.
    
        --> request_params : The parameters sent with the request (in querystring or body).
        <-- A list containing the MongoDB data matching the supplied filter or all objects in a collection.
    '''

    mongo_filter = request_params.get('filter', {}) 
    if request_params.get('sort'):
        [mongo_filter.update({s[0]: {'$exists': True}}) for s in request_params.get('sort')]

    with Database(database,collection) as db:
        return db.find(mongo_filter)
    

def sort_data(data: Cursor, request_params: dict) -> list:
    ''' Sorts a data according to the parameters sent in an HTTP request.
        --> data : The cursor of data to apply the sort to.
        --> request_params : The parameters sent with the request (in querystring or body).
        <-- A queryset containing the sorted data.
    '''

    mongo_sort = request_params.get('sort', {})
    if mongo_sort != {}:
        return data.sort(mongo_sort)
    
    return data


def insert_data(request_params: dict, database:str=None, collection:str=None):
    ''' Add data to the collection with the parameters sent in an HTTP request.
        --> request_params [dict] : The parameters sent with the request (in querystring or body).
    '''

    mongo_fields = request_params.copy()
    with Database(database,collection) as db:
        return db.insert_one(mongo_fields)


def update_data(request_params: dict, database:str=None, collection:str=None):
    ''' Add data to the collection with the parameters sent in an HTTP request.
        --> request_params [dict] : The parameters sent with the request (in querystring or body).
    '''

    mongo_fields = request_params.copy()
    _id = mongo_fields.pop('_id', None)
    
    if _id:
        with Database(database,collection) as db:
            return db.update_one({'_id': ObjectId(_id)}, {'$set': mongo_fields})
    else:
        raise API_Error('No ID supplied', 400)


def delete_data(request_params: dict, database:str=None, collection:str=None):
    ''' Delete data from the collection with the parameters sent in an HTTP request.
        --> request_params [dict] : The parameters sent with the request (in querystring or body).
    '''

    mongo_fields = request_params.copy()
    if mongo_fields.get('_id'):
        with Database(database,collection) as db:
            return db.delete_one({'_id': ObjectId(mongo_fields.pop('_id', None))})
    else:
        raise API_Error('No ID supplied', 400)
