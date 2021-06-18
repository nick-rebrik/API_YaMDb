import pytest


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_superuser(
        username='NNNTestUser', email='NNNadmin@yamdb.fake', password='1234567'
    )


@pytest.fixture
def token(admin):
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(admin)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@pytest.fixture
def user_client(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token["access"]}')
    return client
  