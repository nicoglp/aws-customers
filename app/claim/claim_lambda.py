from app.api_lambda import AWSLambda
from app.claim.claims import service as claims_service

claim_lambda = AWSLambda(claims_service)
post_claim = claim_lambda.post
get_claim = claim_lambda.get
list_claim = claim_lambda.list
delete_claim = claim_lambda.delete