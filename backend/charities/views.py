from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS 
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsCharityOwner, IsBenefactor
from charities.models import Task
from charities.serializers import (
    TaskSerializer, CharitySerializer, BenefactorSerializer
)


class BenefactorRegistration(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # TODO: Handle request method validation in a more reusable way if needed.
        try:
            # Check if the user has a valid authentication token
            if hasattr(request.user, 'auth_token'):
                # FIXME: Consider renaming the serializer variable to follow Python's snake_case convention.
                benefactor_serializer = BenefactorSerializer(data=request.data, context={'user': request.user})
                
                # Check if the serializer data is valid
                if benefactor_serializer.is_valid():
                    # Save the serializer (user already passed in the context)
                    benefactor_serializer.save()
                    
                    # Return success response with the username
                    return Response(
                        data={'message': f'Congratulations {request.user.username}, you registered as a Benefactor!'},
                        status=status.HTTP_200_OK
                    )
                else:
                    # Return error for invalid serializer with correct status code
                    return Response(
                        data={'message': benefactor_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST  # Specify the correct status for bad request
                    )
            else:
                # Return an error if the token is not found
                return Response(
                    data={'error': 'Token not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except KeyError as e:  # Specific exception handling
            # Handle key errors (e.g., missing data in request)
            return Response(
                data={'error': f'Missing required data: {e}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # FIXME: Improve exception handling to be more granular. Catch specific exceptions.
            return Response(
                data={'error': f'There was an internal server error: {e}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CharityRegistration(APIView):
    pass


class Tasks(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all_related_tasks_to_user(self.request.user)

    def post(self, request, *args, **kwargs):
        data = {
            **request.data,
            "charity_id": request.user.charity.id
        }
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsCharityOwner, ]

        return [permission() for permission in self.permission_classes]

    def filter_queryset(self, queryset):
        filter_lookups = {}
        for name, value in Task.filtering_lookups:
            param = self.request.GET.get(value)
            if param:
                filter_lookups[name] = param
        exclude_lookups = {}
        for name, value in Task.excluding_lookups:
            param = self.request.GET.get(value)
            if param:
                exclude_lookups[name] = param

        return queryset.filter(**filter_lookups).exclude(**exclude_lookups)


class TaskRequest(APIView):
    pass


class TaskResponse(APIView):
    pass


class DoneTask(APIView):
    pass