from django.middleware.csrf import CsrfViewMiddleware

class CSRFTraceMiddleware(CsrfViewMiddleware):

    def process_view(self, request, callback, callback_args, callback_kwargs):

        print("\n" + "=" * 80)

        print("PATH:", request.path)

        print("COOKIE TOKEN :", request.COOKIES.get("csrftoken"))

        print("HEADER TOKEN :", request.META.get("HTTP_X_CSRFTOKEN"))

        print("ORIGIN :", request.META.get("HTTP_ORIGIN"))

        print("REFERER :", request.META.get("HTTP_REFERER"))

        result = super().process_view(
            request,
            callback,
            callback_args,
            callback_kwargs,
        )

        print("PROCESS_VIEW RESULT =", result)

        print("=" * 80)

        return result