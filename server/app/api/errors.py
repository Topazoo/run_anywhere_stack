class API_Error(Exception):
    ''' Error thrown by the API on a bad request (as opposed to an exception). '''
    
    def __init__(self, message, code):
        super(Exception, self).__init__(message)
        self.code = code
