from app.api_lambda import AWSLambda
from app.provider.provider import service as provider_service


provider_lambda = AWSLambda(provider_service)
post_provider = provider_lambda.post
get_provider = provider_lambda.get
list_provider = provider_lambda.list
delete_provider = provider_lambda.delete