from django.shortcuts import render
from rest_framework.views import APIView
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework import generics, status
from rest_framework.response import Response

# Define API functions such as GET, POST and DELETE
class ReservationList(APIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get(self, request, format=None):
        # get the date  and period from the query parameters (if none, default to empty string)
        date = request.query_params.get("date", "")
        period = request.query_params.get("period", "")
        reservationCode = request.query_params.get("reservationCode", "")

        if reservationCode:
            # filter the queryset based on only reservationCode
            reservations = Reservation.objects.filter(reservationCode=reservationCode)
        elif date and period:
            #filter the queryset based on date and period
            reservations = Reservation.objects.filter(date=date, period=period)
        elif date:
            # filter the queryset based only on date
            reservations = Reservation.objects.filter(date=date)
        else:
            #get all reservations
            reservations = Reservation.objects.all()

        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        # serialize the data from POST request
        serializer = ReservationSerializer(data=request.data) 

        #Validate the data
        if serializer.is_valid():
            # save the new reservation object: convert into Reservation Object and save in the database
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # if the data is not valid, return an error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, format=None):
        # get the date and period from query parameters
        #date = request.query_params.get("date")
        #period = request.query_params.get("period")
        reservationCode = request.query_params.get("reservationCode")

        if reservationCode is None:
            return Response({'error': 'Reservation Code is required'}, status=status.HTTP_204_NO_CONTENT)

        # try to find the reservation object
        try: 
            reservation = Reservation.objects.get(reservationCode=reservationCode)
            reservation.delete()
            return Response({'message': 'Reservation deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Reservation.DoesNotExist:
            return Response({'error': 'Reservation not found'}, status=status.HTTP_404_NOT_FOUND)    


