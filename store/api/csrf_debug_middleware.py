
print("CSRF DEBUG MIDDLEWARE IMPORTED")

class CSRFDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print("\n" + "=" * 80)
        # print("CSRF DEBUG")

        # print("METHOD:", request.method)
        # print("-" * 60)
        print("PATH:", request.path)
        print("METHOD:", request.method)
        print("ORIGIN:", request.META.get("HTTP_ORIGIN"))
        print("REFERER:",request.META.get("HTTP_REFERER"))
        print("COOKIE csrftoken:", request.COOKIES.get("csrftoken"))
        print("COOKIE sessionid:", request.COOKIES.get("sessionid"))
        print("HEADER X-CSRFToken:", request.META.get("HTTP_X_CSRFTOKEN"))
        print("=" * 80)


        # print("COOKIE CSRF     :", request.COOKIES.get("csrftoken"))
        # print("COOKIE SESSION   :",request.COOKIES.get("sessionid"))

        # print("HEADER CSRF    :", request.META.get("HTTP_X_CSRFTOKEN"))
        # print("ORIGIN    :", request.META.get("HTTP_ORIGIN"))
        # print("REFERER     :",request.META.get("HTTP_REFERER"))

        # print("=" * 80 + "\n")

        response = self.get_response(request)

        return response

