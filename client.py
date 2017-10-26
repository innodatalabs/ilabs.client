from ilabs.client.ilabs_api import send_request, ILabsApi

ILabsApi.URL_API_BASE = 'http://localhost:8080/v99'
api = ILabsApi(user_key='asasasa')
api.ping()
