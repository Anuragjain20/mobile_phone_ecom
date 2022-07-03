import random
from django.contrib.auth.base_user import BaseUserManager
import faker.providers
from django.core.management.base import BaseCommand
from faker import Faker
from authen.models import Profile, CustomUser
from shop.models import Mobile, Company, Color, Category,Images
from django.core.files.uploadedfile import SimpleUploadedFile
# class Provider(faker.providers.BaseProvider):
#     def ecommerce_category(self):
#         return self.random_element(CATEGORIES)

#     def ecommerce_products(self):
#         return self.random_element(PRODUCTS)


phone_img = [
    "C:\\Users\\anura\\Downloads\\41t61osAZHL._SS200_.jpg", 
    "C:\\Users\\anura\\Downloads\\41ooFy-KgoL._SS200_.jpg",
        "C:\\Users\\anura\\Downloads\\41ZGJxnJu1S._SS200_.jpg",
    "C:\\Users\\anura\\Downloads\\31+XBGBHC6S._SS200_.jpg",
    "C:\\Users\\anura\\Downloads\\31yDekSW0yS._SS200_.jpg",

]
logos = [
    "C:\\Users\\anura\\Downloads\\samsung-logo-png-1290.png",
    "C:\\Users\\anura\\Downloads\\png-apple-logo-9707.png",
    "C:\\Users\\anura\\Downloads\\oppo-logo-40753.png"

]


class Command(BaseCommand):
    help = "Command information"

    def handle(self, *args, **kwargs):

        fake = Faker(["nl_NL"])

        for _ in range(10):
            Profile.objects.create(
                name=fake.name(),
                user = CustomUser.objects.create(
                    email=fake.email(),
                    password=fake.password(),
                    is_verified=True,
                ),
                phone=fake.phone_number(),
                address=fake.address(),
                city=fake.city(),
                country=fake.country(),
                zipcode=fake.postcode(),
                image=SimpleUploadedFile(
                    name=f"{random.randint(1,100)}.jpg",
                   content=open("C:\\Users\\anura\\Downloads\\download.jpeg", 'rb').read(), content_type='image/jpeg'
                ),
                is_brand_owner=True,
                is_client=False,
            )

        for _ in range(5):
            Color.objects.create(
                name=fake.color_name(),
                hex=fake.hex_color(),
            )
        for i in range(3):
            Company.objects.create(
                name=fake.company(),
                owner=random.choice(Profile.objects.all()),
                address=fake.address(),
                city=fake.city(),
                country=fake.country(),
                zipcode=fake.postcode(),
                logo=SimpleUploadedFile(
                    name=logos[i],
                    content=open(logos[i], 'rb').read(),
                    content_type='image/png'
                ),
            )

        for _ in range(30):
            Mobile.objects.create(
                title=fake.name(),
                price=random.randint(1000,100000),
                color=random.choice(Color.objects.all()),
                features=fake.text(),
                company=random.choice(Company.objects.all()),
                quatity=random.randint(1,10),
                category=random.choice(Category.objects.all()),
            )

        for i in range(50):
            Images.objects.create(
                image=SimpleUploadedFile(
                    name=f"{i}.jpg",
                    content=open(phone_img[i%len(phone_img)], 'rb').read(),
                    content_type='image/jpeg'
                ),
                mobile=random.choice(Mobile.objects.all()),
            )
