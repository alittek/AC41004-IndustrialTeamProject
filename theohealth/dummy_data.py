from main.models import Therapist, Athlete 
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType

# create permissions for auth.User
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

# clear database
Therapist.objects.all().delete()
Athlete.objects.all().delete()
User.objects.all().delete()

# create new Users, Athletes and Therapists

# Therapists
user_joe = User.objects.create_user(username="joe", password="password")
user_annabel = User.objects.create_user(username="annabel", password="password")

user_joe.user_permissions.add(permission_is_therapist)
user_annabel.user_permissions.add(permission_is_therapist)

therapist_joe = Therapist.objects.create(pk=1, first_name="Joe", last_name="Johnson", auth_user=user_joe)
therapist_annabel = Therapist.objects.create(pk=2,first_name="Annabel", last_name="Smith", auth_user=user_annabel)

# Athletes
user_bill = User.objects.create_user(username="bill", password="password")
user_fiona = User.objects.create_user(username="fiona", password="password")
user_paul = User.objects.create_user(username="paul", password="password")
user_kenna = User.objects.create_user(username="kenna", password="password")
user_skye = User.objects.create_user(username="skye", password="password")
user_theresa = User.objects.create_user(username="theresa", password="password")

user_bill.user_permissions.add(permission_is_athlete)
user_fiona.user_permissions.add(permission_is_athlete)
user_paul.user_permissions.add(permission_is_athlete)
user_kenna.user_permissions.add(permission_is_athlete)
user_skye.user_permissions.add(permission_is_athlete)
user_theresa.user_permissions.add(permission_is_athlete)

Athlete.objects.create(
        pk=1,
        therapist=therapist_joe, 
        first_name="Bill",
        last_name="Jones", 
        contact_nb="07743544644", 
        email="example@mail.com", 
        phone_nb="07743544644", 
        injury="right hamstring injury from horeback riding", 
        auth_user=user_bill)

Athlete.objects.create(
        pk=2,
        therapist=therapist_joe, 
        first_name="Fiona", 
        last_name="Fey", 
        contact_nb="07742567567", 
        email="example@mail.com", 
        phone_nb="01232093434", 
        injury="Left Quadricep injury", 
        auth_user=user_fiona)

Athlete.objects.create(
        pk=3,
        therapist=therapist_joe, 
        first_name="Paul", 
        last_name="Hoxley", 
        contact_nb="9384294888", 
        email="paul.hoxley@hotmail.com", 
        phone_nb="8302984392", 
        injury="Left hamstring injury from surfing", 
        auth_user=user_paul)

Athlete.objects.create(
        pk=4,
        therapist=therapist_annabel, 
        first_name="Kenna", 
        last_name="McHenna", 
        contact_nb="9384294888", 
        email="kenna.mchenna@mail.us", 
        phone_nb="8302984392", 
        injury="Left hamstring injury from surfing", 
        auth_user=user_kenna)

Athlete.objects.create(
        pk=5,
        therapist=therapist_annabel, 
        first_name="Skye", 
        last_name="Smith", 
        contact_nb="9384294888", 
        email="smith-skye", 
        phone_nb="8302984392", 
        injury="Left hamstring injury from surfing", 
        auth_user=user_skye)

Athlete.objects.create(
        pk=6,
        therapist=therapist_annabel, 
        first_name="Theresa", 
        last_name="Tefal", 
        contact_nb="14122220-240", 
        email="customer-support@tefal.org", 
        phone_nb="8302984392", 
        injury="Left hamstring injury from a fan accident in Taiwan", 
        auth_user=user_theresa)

