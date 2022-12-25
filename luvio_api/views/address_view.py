from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from luvio_api.common.domain_api_utils import store_suburb_and_address_data
from luvio_api.integrations import DomainApiClient


@api_view(["GET"])
def get_address_suggestions(request: Request):
    # query param for search term should already be urlencoded from the front end
    search_term = request.query_params.get("term")
    domain_client = DomainApiClient()
    suggestions = domain_client.get_address_suggestions(search_term)

    # Store the address from Domain to our DB
    store_suburb_and_address_data(suggestions)
    return Response(suggestions)
