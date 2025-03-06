from django.http import Http404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.serializer import ExpenseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main.models import *

class ExpenseList(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        expense = Expense.objects.all()
        data = ExpenseSerializer(expense, many=True).data
        return Response(data, status=status.HTTP_200_OK)

#stvaranje novog expense
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetailView(APIView):
    
    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        expense = self.get_object(pk)
        data = ExpenseSerializer(expense).data
        return Response(data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        expense = self.get_object(pk)
        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense = self.get_object(pk)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)