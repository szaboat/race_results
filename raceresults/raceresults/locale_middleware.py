from django.utils import translation


class SetLocaleMiddleware():
    def process_request(self, request):
        user_language = 'hu'
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language