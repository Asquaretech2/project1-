from django.contrib.auth.tokens import PasswordResetTokenGenerator

from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,myproducer,timestamp):
        return (
        text_type(myproducer.pk) + text_type(timestamp)
        # text_type(user.profile.signup_confirmation)
        )

generate_token = TokenGenerator()