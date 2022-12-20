from oauth2_provider.oauth2_validators import OAuth2Validator


class CustomOAuth2Validator(OAuth2Validator):
    oidc_claim_scope = None  # return all claims irrespective of granted scopes

    def get_additional_claims(self, request):
        # request.user is the Django User object (which we overwrite with Registration object)
        return {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "full_name": ' '.join([request.user.first_name, request.user.last_name]),
            "primary_email": request.user.primary_email,
            "username": request.user.username,
        }
