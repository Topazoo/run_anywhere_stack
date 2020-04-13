from database.main import Database
from config.routes import ROUTES
from api.errors import API_Error
from flask import jsonify, request, Request, Response
from api.utils import *
import json

class API:
    ''' API interface '''

    @staticmethod
    def GET(request:Request, database:str=None, collection:str=None) -> Response:
        ''' Fetch model data from the server or respond with the appropriate HTTP status code on error. 
        
            The request query string must supply the model's (class) name. It may also supply one or more optional 
            filter and sort parameters.
            --> request : The GET request sent to the server.
            <-- JSON containing the HTTP status code signifying the request's success or failure and
                a list of MongoDB records matching the supplied parameters if the request did not fail.
                GET Request Formats:
                    All - Get all records from a collection.
                        /api/
                        
                    Filtering - Get all records from a collection with field(s) matching the provided value(s).
                        /api/?filter=<<field>>:<<value>>
                        /api/?filter=<<field1>>:<<value1>>,<<field2>>:<<value2>>
                                                                            
                    Sorting - Get all records from a collection. sorted by the provieded field(s). 
                        /api/?sort=<<field>>
                        /api/?sort=<<field1>>,<<field2>>

                    Filtering + Sorting - Get all records from a collection with field(s) matching the provided 
                                        value(s) sorted by the provided field(s).
                        
                        /api/?filter=<<field1>>,<<field2>>:<<value>>&sort=<<field1>> 
                GET Response Format:
                    {"data": [JSON], "code": <<code>>}            
        '''
        
        try:
            payload = parse_query_string(request.query_string.decode()) if request.query_string.decode() else {}
            data_cursor = fetch_and_filter_data(payload, database, collection)
            sorted_data = list(sort_data(data_cursor, payload))

            return JsonResponse({'data': sorted_data}, 200 if len(sorted_data) > 0 else 404)
            
        except Exception as exception: # TODO - Throw on QA
            return JsonError('GET', exception)


    @staticmethod
    def POST(request:Request, database:str=None, collection:str=None) -> Response:
        ''' Create a new MongoDB record or respond with the appropriate HTTP status code on error. 
            
            --> request : The POST request sent to the server.
            <-- JSON containing the HTTP status code signifying the request's success or failure.
                POST Body Format:
                        { {<<field1>>: <<value1>>, <<field2>>: <<value2>>} }
                POST Response Format:
                    {"code": <<code>>}            
        '''

        try:
            payload = request.get_json(force=True) if request.data else {}
            if payload:
                payload.pop('_id', None)
                ins = insert_data(payload, database, collection)
            else:
                raise API_Error('No data supplied to POST', 500)

            return JsonResponse({'_id': str(ins.inserted_id)}, code=200)

        except Exception as exception:
            return JsonError('POST', exception)

    @staticmethod
    def PUT(request:Request, database:str=None, collection:str=None) -> Response:
        ''' Update a MongoDB record or respond with the appropriate HTTP status code on error. 
            
            The request body must supply a dictionary of 
            one or more field/value pairs to update the model with. It should also supply 
            one or more optional filter parameters matching the parameters for Django's 
            Queryset.filter() method. 
            
            *The filter parameters must match only the model being updated*
            
            --> request : The PUT request sent to the server.
            <-- JSON containing the HTTP status code signifying the request's success or failure.
                PUT Body Format:
                    { 
                        "filter": {<<field1>>: <<value1>>, <<field2>>: <<value2>>},
                        "fields": {<<field1>>: <<value1>>, <<field3>>: <<value3>>} 
                    }
                PUT Response Format:
                    {"code": <<code>>}            
        '''

        try:
            payload = request.get_json(force=True) if request.data else {}
            if payload:
                _id = payload.get('_id')
                if not getattr(update_data(payload, database, collection), 'modified_count', None): 
                    raise API_Error(f'ID [{_id}] not found', 404)
            else:
                raise API_Error('No data supplied to PUT', 500)

            return JsonResponse(code=200)

        except Exception as exception:
            return JsonError('PUT', exception)

    @staticmethod
    def DELETE(request:Request, database:str=None, collection:str=None) -> Response:
        ''' Delete a MongoDB record or respond with the appropriate HTTP status code on error. 
            
            The request body must supply filter parameters.
            *The filter parameters must match only a single model*
            
            --> request : The DELETE request sent to the server.
            <-- JSON containing the HTTP status code signifying the request's success or failure.
                DELETE Body Format:
                    { "model": <<model>>, "filter": {<<field1>>: <<value1>>, <<field2>>: <<value2>>} }
                DELETE Response Format:
                    {"code": <<code>>}            
        '''

        try: # TODO - Wrapper
            payload = request.get_json(force=True) if request.data else {}
            if payload:
                _id = payload.get('_id')
                if not getattr(delete_data(payload, database, collection), 'deleted_count', None):
                    raise API_Error(f'ID [{_id}] not found', 404)
            else:
                raise API_Error('No data supplied to DELETE', 500)

            return JsonResponse(code=200)

        except Exception as exception:
            return JsonError('DELETE', exception)


    @staticmethod
    def main() -> Response:
        ''' Called when the /api/ endpoint is sent an HTTP request. Delegates 
            to the appropriate handler based on the request method or returns a JSON
            formatted error if the method is not supported.
            --> request : The HTTP request sent to the server.
            <-- JSON containing the HTTP status code signifying the request's success or failure and
                all other data returned from the server.
        '''

        route_config = ROUTES[str(request.url_rule)]
        database = route_config.get('database')
        collection = route_config.get('collection')
        delegate = route_config.get('logic')
        
        if request.method == 'GET':
            data = API.GET(request, database, collection)

        if request.method == 'POST':
            data = API.POST(request, database, collection)

        if request.method == 'PUT':
            data = API.PUT(request, database, collection)

        if request.method == 'DELETE':
            data = API.DELETE(request, database, collection)

        return data if not delegate else delegate(request, data)