from app.api_lambda import AWSLambda
from .users import service as user_service


user_lambda = AWSLambda(user_service)
post_user = user_lambda.post
get_user = user_lambda.get
delete_user = user_lambda.delete
put_user = user_lambda.delete
list_user = user_lambda.list