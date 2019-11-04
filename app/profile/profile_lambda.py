from app.api_lambda import AWSLambda
from app.profile.profile import service as profile_service


profile_lambda = AWSLambda(profile_service)
post_profile = profile_lambda.post
get_profile = profile_lambda.get
list_profile = profile_lambda.list
delete_profile = profile_lambda.delete