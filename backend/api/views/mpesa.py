from rest_framework.views import APIView
from rest_framework.response import Response


class MpesaCallbackAPIView(APIView):

    permission_classes = []

    authentication_classes = []

    def post(self, request):

        payload = request.data

        # verify transaction

        # update transaction

        # create tickets

        return Response({
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        })
    