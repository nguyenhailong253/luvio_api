import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from luvio_api.common.constants import DEFAULT_LOGGER
from luvio_api.common.domain_api_utils import store_suburb_and_address_data
from luvio_api.integrations import DomainApiClient

logger = logging.getLogger(DEFAULT_LOGGER)


@api_view(["GET"])
def get_address_suggestions(request: Request) -> Response:
    """
    Handling GET requests for address suggestions using a search term
    Outsourcing to Domain API instead of implementing our own for now
    """
    # query param for search term should already be urlencoded from the front end
    search_term = request.query_params.get("term", None)
    if search_term:
        logger.info(f"Address search term: {search_term}")
        domain_client = DomainApiClient()
        suggestions = domain_client.get_address_suggestions(search_term)

        # Store the address from Domain to our DB
        store_suburb_and_address_data(suggestions)
        return Response(suggestions)
    logger.error(f"Address search term not provided: {search_term}")
    return Response(
        {"message": "A search term must be provided"},
        status=status.HTTP_400_BAD_REQUEST,
    )
