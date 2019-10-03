from app.api_lambda import AWSLambda
from app.service_line.service_line import service as service_line_service


service_line_lambda = AWSLambda(service_line_service)
get_service_line = service_line_lambda.get
list_service_line = service_line_lambda.list
