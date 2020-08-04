from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb import settings
from users.models import YamUser
from users.permissions import IsAdmin
from users.serializers import YamUsersSerializer


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = YamUser.objects.all()
    serializer_class = YamUsersSerializer
    lookup_field = 'username'


    @action(detail=False, methods=('GET', 'PATCH'),
            permission_classes=(IsAuthenticated, ))
    def me(self, request):
        user = get_object_or_404(YamUser, id=request.user.id)

        if request.method == 'GET':
            serializer = YamUsersSerializer(user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = YamUsersSerializer(user,
                                            data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
def email_code(request):
    data = {
        'email': request.data.get('email'),
        'username': request.data.get('email'),
    }

    serializer = YamUsersSerializer(data=data)

    if serializer.is_valid():
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject=settings.MAIL_SUBJECT,
            message=f'{settings.MAIL_TEXT}{confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=(data['email'],),
            fail_silently=False,
        )
        return Response({serializer.data['email']},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
def get_token(request):
    email = request.data['email']
    confirmation_code = request.data['confirmation_code']

    try:
        user = YamUser.objects.get(email=email)
    except ObjectDoesNotExist:
        raise NotAcceptable(detail='No such e-mail')

    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        return Response(data={'token': str(refresh.access_token)},
                        status=status.HTTP_200_OK)

    raise NotAcceptable(detail='error code')
