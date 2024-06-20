class ApiResult:
    '''Class to wrap all the essential information from an API request.'''

    def __init__(self, status_code: int = 200) -> None:
        self.__status_code: int = status_code
        self.__response = None
        self.__error_message: str = None

    # Getters:
    def get_status_code(self) -> int:
        '''Gets the current status code.'''
        return self.__status_code

    def get_response(self):
        '''Gets the current response.'''
        return self.__response

    def get_error_message(self) -> str:
        '''Gets the current error message.'''
        return self.__error_message

    # Setters:
    def set_status_code(self, status_code: int) -> None:
        '''Sets a new status code value.'''
        self.__status_code = status_code

    def set_response(self, response) -> None:
        '''Sets a new response value.'''
        self.__response = response

    def set_error_message(self, error_message: str) -> None:
        '''Sets a new error message value.'''
        self.__error_message = error_message
