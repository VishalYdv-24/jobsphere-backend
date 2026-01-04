from django.shortcuts import render
from .serializers import CompanySerializer
from rest_framework import status,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Company

# Create your views here.
class CompanyListView(APIView):
    # get company list
        """
        GET -> Public
        POST -> Admin
        """

      #   get companies list 
        def get(self,request):
            companies = Company.objects.all()
            serializer = CompanySerializer(companies, many=True)
            return Response(
                  serializer.data,
                  status=status.HTTP_200_OK
            )
        
      #   add company into the list only admin ca do it
        def post(self,request):
            #   if not request.user.is_staff:
            #         return Response(
            #               {"error" : "Only admin can add companies"},
            #               status=status.HTTP_403_FORBIDDEN
            #         )
              serializer = CompanySerializer(data=request.data)
              if serializer.is_valid():
                    serializer.save()
                    return Response(
                          {
                                "message" : "Company added successfully",
                                'data' : serializer.data
                          },
                          status=status.HTTP_201_CREATED
                    )
              
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

# retrive single company detail and perform put and delete oprations
class CompanyDetailView(APIView):
      """
      GET -> public
      DELETE -> Admin only
      PATCH -> Admin only

      """
      
      # get object
      def get_object(self,pk):
            try :
                  return Company.objects.get(pk=pk)
            except Company.DoesNotExist:
                  return None
            
      # retrive single company detail
      def get(self,request,pk):
            company = self.get_object(pk)

            if not company:
                  return Response(
                        {"error": "Company not found"},
                        status=status.HTTP_404_NOT_FOUND
                  )
            
            serializer = CompanySerializer(company)
            return Response(
                  serializer.data,
                  status=status.HTTP_200_OK
            )


      # delete company from list
      def delete(self,request,pk):

            if not request.user.is_staff:
                  return Response(
                        {"error" : "Only admin can delete company"},
                        status=status.HTTP_403_FORBIDDEN
                  )
            company = self.get_object(pk)
            if not company:
                  return Response(
                      {"error": "Company not found"},
                      status=status.HTTP_404_NOT_FOUND
                  )

            company.delete()
            return Response(
                  {"message" : "company deleted successfully!"},
                  status=status.HTTP_200_OK
            )
      
      # update company detail using patch onyl admin can
      def patch(self,request,pk):
            if not request.user.is_staff:
                  return Response(
                        {"error" : "Only admin can update/edit company"},
                        status=status.HTTP_403_FORBIDDEN
                  )

            company = self.get_object(pk)
            if not company:
                  return Response(
                        {"error" : "Company not found"},
                        status=status.HTTP_404_NOT_FOUND
                  )
            
            serializer = CompanySerializer(company, data=request.data, partial = True)
            if serializer.is_valid():
                  serializer.save()
                  return Response(
                        {
                              'message' : 'Company updated successfully',
                              'data' : serializer.data,
                        },
                        status=status.HTTP_200_OK

                  )        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)