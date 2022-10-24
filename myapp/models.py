from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    birth_date = models.DateField(blank=True, null=True)

    def baby_boomer_status(self) -> str:
        "Returns the person's baby-boomer status."
        import datetime
        if self.birth_date < datetime.date(1945, 8, 1):
            return "Pre-boomer"
        elif self.birth_date < datetime.date(1965, 1, 1):
            return "Baby boomer"
        else:
            return "Post-boomer"

    @property
    def full_name(self) -> str:
        "Returns the person's full name."
        return f"{self.first_name} {self.last_name}"

    # list［tuple］を使う場合
    GENDER = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    gender = models.CharField(max_length=1, choices=GENDER)

    # 列挙型を使う場合
    MedalType = models.TextChoices('MedalType', 'GOLD SILVER BRONZE')
    medal = models.CharField(blank=True, choices=MedalType.choices, max_length=10)

    class Meta:
        db_table = "person"
        verbose_name = "person"
        verbose_name_plural = "persons"
        ordering = ["-age"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} {self.age} {self.gender} {self.medal}"

class Fruit(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    price = models.IntegerField(blank=True, null=False)

    class Meta:
        db_table = "fruit"
        verbose_name = "fruit"
        verbose_name_plural = "fruits"

class FamousPerson(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(FamousPerson, through='Membership')

    def __str__(self) -> str:
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(FamousPerson, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.person} in {self.group}"

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self) -> str:
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self) -> str:
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self) -> str:
        return self.headline

class Dog(models.Model):
    name = models.CharField(max_length=200)
    data = models.JSONField(null=True)

    class Meta:
        db_table = "dog"
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
