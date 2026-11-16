#Здравствуйте, как вы помните я говорил вам на той неделе что уже делал практис 2 но не полностью поэтому если не возражаете то я бы хотел просто вписать свои коды здесь. (просто не придумал более креативное решение)
from django.contrib.auth import get_user_model
from unfold.forms import AdminPasswordChangeForm as UnfoldAdminPasswordChangeForm
from unfold.forms import UserChangeForm as UnfoldUserChangeForm
from unfold.forms import UserCreationForm as UnfoldUserCreationForm

User = get_user_model()


class CustomUserCreationForm(UnfoldUserCreationForm):
    """User creation form for Unfold admin without username requirement."""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class CustomUserChangeForm(UnfoldUserChangeForm):
    """User change form for Unfold admin without username requirement."""

    class Meta:
        model = User
        fields = '__all__'


class CustomAdminPasswordChangeForm(UnfoldAdminPasswordChangeForm):
    """Password change form for custom user in Unfold admin."""

    pass

 