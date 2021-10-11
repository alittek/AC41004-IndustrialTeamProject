from main.models import Therapist, Athlete 
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType

Therapist.objects.all().delete()
Athlete.objects.all().delete()
User.objects.all().delete()


t1 = Therapist.objects.create(pk=1, first_name="Fred", last_name="Fire")
t2 = Therapist.objects.create(pk=2,first_name="John", last_name="Smith")
                                                                         
Athlete.objects.create(pk=1,therapist=t1, first_name="Jane", last_name="Jones", contact_nb="07743544644", email="jane.jones@hotmail.com", phone_nb="07743544644", injury="right hamstring injury from horeback riding")
Athlete.objects.create(pk=2,therapist=t1, first_name="Alina", last_name="Littek", contact_nb="07742567567", email="alina.littek@mail.com", phone_nb="01232093434", injury="Left Quadricep injury")
Athlete.objects.create(pk=3,therapist=t2, first_name="Paul", last_name="Hoxley", contact_nb="9384294888", email="paul.hoxley@hotmail.com", phone_nb="8302984392", injury="Left hamstring injury from surfing")

usert1 = User.objects.create_user(username="joe", password="password")
usera1 = User.objects.create_user(username="bill", password="password")
content_type = ContentType.objects.get_for_model(User)
try:
    permission_is_therapist = Permission.objects.get(
        codename='is_therapist',
        content_type=content_type,
    )

    permission_is_athlete = Permission.objects.get(
        codename='is_athlete',
        content_type=content_type,
    )
except:
    permission_is_therapist = Permission.objects.create(
        codename='is_therapist',
        content_type=content_type,
    )

    permission_is_athlete = Permission.objects.create(
        codename='is_athlete',
        content_type=content_type,
    )
usert1.user_permissions.add(permission_is_therapist)
usera1.user_permissions.add(permission_is_athlete)
