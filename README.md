# [Django document topics](https://docs.djangoproject.com/ja/4.1/topics/)を上から順番に読んでいく

## 事前準備

Pythonのインストール、テキストエディタのインストール、Djangoのインストールは

完了していることを前提とする。

<details>
<summary>1. プロジェクトの作成</summary>

``` PowerShell
django> django-admin startproject sample_project
django> cd sample_project
sample_project> ls
manage.py  sample_project
```

</details>

プロジェクト作成後に`{project_name}/{project_name}/settings.py`を編集する。

<details>
<summary>2. settings.pyの編集</summary>

``` vscode settings.py
LANGUAGE_CODE = "ja-JP"

TIME_ZONE = "Asia/Tokyo"
```

</details>

<details>
<summary>3. applicationのひな形作成</summary>

Projectフォルダは設定に関するファイルがメインなので、アプリケーションのひな形を作成する。

``` PowerShell
sample_project> python manage.py startapp myapp
sample_project> ls
__pycache__　migrations　__init__.py　admin.py
apps.py　models.py　tests.py　views.py
```

</details>

<details>
<summary>4. 作成したアプリひな形をsettings.pyのINSTALLED_APPSに追加</summary>

```　vscode settings.py
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "myapp.apps.MyappConfig", # 追加
]
```

</details>

事前準備はここまで。

## Models

<details>
<summary>modelの作成</summary>

``` myapp/models.py
from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()

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

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
```

[Field Types](https://docs.djangoproject.com/ja/4.1/ref/models/fields/#field-types)

</details>

<details>
<summary>modelの内容をDBに反映させる</summary>

``` PowerShell
sample_project> python manage.py makemigrations
Migrations for 'myapp':
  myapp\migrations\0001_initial.py
    - Create model Person
```

``` PowerShell
sample_project> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, myapp, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying myapp.0001_initial... OK
  Applying sessions.0001_initial... OK
```

</details>

modelの内容をDBに反映させるための`myapp/migrations/0001_initial.py`が作成される。

<details>
<summary>djangoで生成されたsqlを確認してみる</summary>

``` PowerShell
sample_project> python manage.py sqlmigrate myapp 0001
BEGIN;
--
-- Create model Person
--
CREATE TABLE "myapp_person" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "first_name" varchar(30) NOT NULL, "last_name" varchar(30) NOT NULL, "age" integer NOT NULL, "gender" varchar(1) NOT NULL);
COMMIT;
```

</details>

from django.db import models
from myapp.models import Person, Fruit

model(DBの定義)を作成したら、`python manage.py shell`でDBにアクセスできる。

`pip install django-extensions`して、

`settings.py`の`INSTALLED_APPS`に`django_extensions`を追加すると

`python manage.py shell_plus`でもDBにアクセスできる。

<details>
<summary>参考: shell-plus</summary>

``` Django shell
sample_project> python manage.py shell_plus --plain
# Shell Plus Model Imports
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from myapp.models import Fruit, Person
# Shell Plus Django Imports
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When
from django.utils import timezone
from django.urls import reverse
from django.db.models import Exists, OuterRef, Subquery
Python 3.10.8 (tags/v3.10.8:aaaf517, Oct 11 2022, 16:50:30) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```

</details>

<details>
<summary>作成したmodelのimport</summary>

``` PowerShell
sample_project> python manage.py shell
Python 3.10.8 (tags/v3.10.8:aaaf517, Oct 11 2022, 16:50:30) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from myapp.models import Person, Fruit
>>>
```

models.pyで定義したPersonクラスとFruitクラスの中身。

``` myapp/models.py
from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()

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
        return f"{self.first_name} {self.last_name} {self.age} \
            {self.gender} {self.medal}"

class Fruit(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    price = models.IntegerField(blank=True, null=False)

    class Meta:
        db_table = "fruit"
        verbose_name = "fruit"
        verbose_name_plural = "fruits"
```

</details>

<details>
<summary>データを確認する(SELECT * FROM person;)</summary>

データがないので、空のリストが返ってくる。

``` Django shell
>>> Person.objects.all()
<QuerySet []>
>>>
```

</details>

<details>
<summary>データを追加する(INSERT INTO person(first_name,last_name) VALUES ("John","Smith);)</summary>

``` Django shell
>>> Person.objects.create(first_name="John", last_name="Smith", age=40, gender="M", medal="GOLD")
<Person: John Smith 40 M GOLD>
```

</details>

<details>
<summary>データを更新(UPDATE person SET age = 43;)</summary>

``` Django shell
>>> p = Person.objects.get()
>>> p
<Person: John Smith 40 M GOLD>
>>> p.age=43
>>> p
<Person: John Smith 43 M GOLD>
```

</details>

<details>
<summary>データを削除する(DELETE FROM person where id = 1;)</summary>

``` Django shell
>>> Person.objects.all()
<QuerySet [<Person: John Smith 40 M GOLD>, <Person: Jane Smith 20 F SILVER>]>
>>> Person.objects.get(first_name="John").delete()
(1, {'myapp.Person': 1})
>>> Person.objects.all()
<QuerySet [<Person: Jane Smith 20 F SILVER>]>
>>> Person.objects.all().delete()
(1, {'myapp.Person': 1})
>>> Person.objects.all()
<QuerySet []>
```

</details>

| Field Options | Description | Examples |
| --- | --- | ---: |
|null|True の場合、Django はデータベース内に NULL として空の値を保持します。デフォルトは False です。|null=True|
|blank|True の場合、フィールドはブランクになることが許容されます。デフォルトは False です。|blank=True|
|choices|2タプルの sequence を使用します。デフォルトのフォームウィジェットが標準のテキストボックスではなくセレクトボックスになり、与えられた選択肢を選ぶように制限されます。|choices=GENDER GENDERは[("M", "Male"),("F", "Female")]|
|default|そのフィールドのデフォルト値です。このオプションには特定の値または呼び出し可能オブジェクトを渡すことができます。呼び出し可能オブジェクトの場合、新しくオブジェクトが生成される度に呼び出されます。||
|help_text|フォームウィジェットとともに表示される追加の「ヘルプ」テキストです。この値はフィールドがフォームとして利用されない場合でもドキュメントとして役に立ちます。||
|primary_key|True の場合、設定したフィールドはそのモデルの主キーとなります。|primary_key=True|
|unique|True の場合、そのフィールドはテーブル上で一意となる制約を受けます|unique=True|

[Django 4.1 models field-options](https://docs.djangoproject.com/ja/4.1/topics/db/models/#field-options)

### Relationships

| Relationships | Fields | Examples |
| ---: | --- | --- |
|Many To One|ForeignKey|[manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)](https://docs.djangoproject.com/ja/4.1/topics/db/examples/many_to_one/)|
|Many To Many|ManyToManyField|[toppings = models.ManyToManyField(Topping)](https://docs.djangoproject.com/ja/4.1/topics/db/examples/many_to_many/#many-to-many-relationships)|
|One To One|OnetoOneField|[place = models.OneToOneField(Place,on_delete=models.CASCADE,primary_key=True)](https://docs.djangoproject.com/ja/4.1/topics/db/examples/one_to_one/)|

#### [ManytoManyにおける追加フィールド](https://docs.djangoproject.com/ja/4.1/topics/db/models/#extra-fields-on-many-to-many-relationships)

>たとえば、ミュージシャンが所属する音楽グループを追跡するアプリについて考えてみましょう。ミュージシャンとグループの間には多対多の関係があるので、この関係を表すのに ManyToManyField が使えます。しかし、ある人がそのグループに加入した日などといった多くの詳細情報も集めたいとします。
>このような場合、 Django ではそのような多対多リレーションを規定するのに使われるモデルを指定することができます。そうすることで、中間モデルに追加のフィールドを配置することができます。中間モデルは、 through 引数で中間として振る舞うモデルを指定することで、 ManyToManyField に紐付けることができます。ミュージシャンの例では、コードはこのようになるでしょう:

``` Python
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
```

<details>
<summary>Django shell</summary>

``` Python
>>> from myapp.models import FamousPerson, Group, Membership
>>> import datetime
>>> ringo = FamousPerson.objects.create(name='Ringo Starr')
>>> paul = FamousPerson.objects.create(name='Paul McCartney')
>>> beatles = Group.objects.create(name='The Beatles')
>>> m1 = Membership(person=ringo, group=beatles,
...     date_joined=datetime.date(1962, 8, 16),
...     invite_reason='Needed a new drummer.')
>>> m1.save()
>>> m2 = Membership(person=paul, group=beatles,
...     date_joined=datetime.date(1959, 8, 1),
...     invite_reason='Wanted to form a band.')
>>> m2.save()
>>> beatles.members.all()
<QuerySet [<FamousPerson: Ringo Starr>, <FamousPerson: Paul McCartney>]>
# Add a new member to the group.
>>> john = FamousPerson.objects.create(name='John Lennon')
>>> john.save()
>>> beatles.members.add(john, through_defaults={'date_joined': datetime.date(1960, 8, 1)})
>>> beatles.members.all()
<QuerySet [<FamousPerson: Ringo Starr>, <FamousPerson: Paul McCartney>, <FamousPerson: John Lennon>]>
>>> beatles.members.create(name="George Harrison", through_defaults={'date_joined': datetime.date(1960, 8, 1)})
<FamousPerson: George Harrison>
>>> beatles.members.all()
<QuerySet [<FamousPerson: Ringo Starr>, <FamousPerson: Paul McCartney>, <FamousPerson: John Lennon>, <FamousPerson: George Harrison>]>
>>> beatles.members.set([john, paul, ringo, george], through_defaults={'date_joined': datetime.date(1960, 8, 1)})
>>> beatles.members.all()
<QuerySet [<FamousPerson: John Lennon>, <FamousPerson: Paul McCartney>, <FamousPerson: Ringo Starr>, <FamousPerson: George Harrison>]>
>>> beatles.members.through.objects.all()
<QuerySet [<Membership: The Beatles - John Lennon>, <Membership: The Beatles - Paul McCartney>, <Membership: The Beatles - Ringo Starr>, <Membership: The Beatles - George Harrison>]>
>>> beatles.members.remove(ringo)
>>> beatles.members.all()
<QuerySet [<FamousPerson: Paul McCartney>, <FamousPerson: John Lennon>, <FamousPerson: George Harrison>]>
>>> FamousPerson.objects.all()
<QuerySet [<FamousPerson: Ringo Starr>, <FamousPerson: Paul McCartney>, <FamousPerson: John Lennon>, <FamousPerson: George Harrison>]>
>>> Membership.objects.all()
<QuerySet [<Membership: Membership object (5)>, <Membership: Membership object (6)>, <Membership: Membership object (7)>, <Membership: Membership object (8)>]>
>>> beatles.members.clear()
>>> Membership.objects.all()
<QuerySet []>
>>> Membership.objects.all()
<QuerySet []>
>>> beatles.members.all()
<QuerySet []>
>>> FamousPerson.objects.all()
<QuerySet [<FamousPerson: Ringo Starr>, <FamousPerson: Paul McCartney>, <FamousPerson: John Lennon>, <FamousPerson: George Harrison>]>
```

</details>

#### Meta オプション

```
from django.db import models

class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:
        db_table = 'bulls'
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"
```

| Option Name | Description |
| :---: | --- |
|app_label|If a model is defined outside of an application in INSTALLED_APPS, it must declare which app it belongs to|
|db_table|The name of the database table to use for the model|
|get_latest_by|The name of a field or a list of field names in the model, typically DateField, DateTimeField, or IntegerField. This specifies the default field(s) to use in your model Manager’s latest() and earliest() methods.|

[Model Meta options](https://docs.djangoproject.com/ja/4.1/ref/models/options/#model-meta-options)

### Sounds Useful Topics

[Performing raw SQL queries](https://docs.djangoproject.com/ja/4.1/topics/db/sql/#performing-raw-sql-queries)

[Examples of model relationship API usage](https://docs.djangoproject.com/ja/4.1/topics/db/examples/)

[Manager](https://docs.djangoproject.com/ja/4.1/topics/db/managers/#django.db.models.Manager)

## QuerySets

[QuerySets](https://docs.djangoproject.com/ja/4.1/topics/db/queries/#querysets)

Models

``` Python 3
from datetime import date

from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.headline
```

<details>
<summary>オブジェクトを作る</summary>

``` Python 3
>>> from myapp.models import Author, Blog, Entry, FamousPerson, Fruit, Group, Membership, Person
>>> b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
>>> b
<Blog: Beatles Blog>
>>> b.tagline
'All the latest Beatles news.'
>>> b.save()
>>> Blog.objects.create(name='ホロライブログ', tagline='最新情報ですね��')
<Blog: ホロライブログ>
>>> Blog.objects.all()
<QuerySet [<Blog: Beatles Blog>, <Blog: ホロライブログ>]>
```

この例では内部で `INSERT SQL` 文が処理されます。明示的に `save()` を呼ぶまで Django はデータベースを操作しません。

`save()` メソッドは値を返しません。

</details>

<details>
<summary>ForeignKey と ManyToManyField フィールドを扱う</summary>

``` python 3
>>> b = Blog(name='hololive', tagline='vtuver')
>>> b.save()
>>> entry = Entry(blog=b, headline='latest news!',
    body_text='test post text.',
    pub_date=datetime.date(2022, 10, 22),
    mod_date=datetime.date(2022, 10, 22),
    n_comments=1, n_pingbacks=1, rating=3)
>>> entry.save()
>>> entry = Entry.objects.get(pk=1)
>>> entry
<Entry: latest news!>
>>> entry.blog
<Blog: hololive>
>>> entry.blog.tagline
'vtuver'
>>>
```

Authorsを追加する

``` python 3
>>> joe = Author.objects.create(name='Joe')
>>> entry.authors.add(joe)
>>> entry.authors
<django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x0000025CBCC4A4A0>
>>> entry.authors.all()
<QuerySet [<Author: Joe>]>
>>> john = Author.objects.create(name="John")
>>> paul = Author.objects.create(name="Paul")
>>> george = Author.objects.create(name="George")
>>> ringo = Author.objects.create(name="Ringo")
>>> entry.authors.add(john, paul, george, ringo)
>>> entry.authors.all()
<QuerySet [<Author: Joe>, <Author: John>, <Author: Paul>, <Author: George>, <Author: Ringo>]>
>>>
```

Query Filters

``` python 3
>>> Entry.objects.filter(blog__name__startswith='Beatles')
<QuerySet []>
>>> Entry.objects.filter(blog__name__startswith='hololive')
<QuerySet [<Entry: latest news!>]>
>>> Entry.objects.filter(authors__name__startswith='J')
<QuerySet [<Entry: latest news!>]>
>>> Entry.objects.filter(pub_date__year=2006)
<QuerySet []>
>>> Entry.objects.filter(pub_date__year=2022)
<QuerySet [<Entry: latest news!>]>
# filter chaining
>>> Entry.objects.filter(headline__startswith='What')\
...     .exclude(pub_date__gte=datetime.date.today())\
...     .filter(pub_date__gte=datetime.date(2005, 1, 30))
<QuerySet []>
>>>
```

</details>

<details>
<summary>Filed Lookup</summary>

>ルックアップに指定するフィールドはモデルが持つフィールド名でなければなりません。ただし1つだけ例外があり、 ForeignKey の場合にはフィールド名の末尾に _id を付けた名前を指定することができます。その場合、value パラメータには外部モデルのプライマリーキーの生の値を書くことが期待されます。例えば、次のように書くことができます。

[フィールドルックアップ](https://docs.djangoproject.com/ja/4.1/topics/db/queries/#field-lookups)

``` python 3
>>> Entry.objects.filter(blog_id=1)
<QuerySet [<Entry: latest news!>]>
```

exact & iexact

 ``` python 3
 >>> Entry.objects.get(headline__exact="Cat bites dog")
Traceback (most recent call last):
myapp.models.Entry.DoesNotExist: Entry matching query does not exist.
>>> Entry.objects.get(headline__exact="latest news!")
<Entry: latest news!>
>>> Blog.objects.get(name__iexact="beatles blog")
<Blog: Beatles Blog>
 ```

contains & icontains

``` python 3
>>> Entry.objects.get(headline__contains='Lennon')
Traceback (most recent call last):
myapp.models.Entry.DoesNotExist: Entry matching query does not exist.
>>> Entry.objects.get(headline__contains='news')
<Entry: latest news!>
>>> Entry.objects.get(headline__icontains='NEWS')
<Entry: latest news!>
```

in, gt, gte, lt, lte, range, year, month, day, week_day, isnull, search, regex, iregex

``` python 3
>>> start_date = datetime.date(2005, 1, 1)
>>> end_date = datetime.date(2005, 3, 31)
>>> Entry.objects.filter(pub_date__range=(start_date, end_date))
>>> Entry.objects.get(title__regex=r'^(An?|The) +')
>>> Entry.objects.get(title__iregex=r'^(an?|the) +')
```

</details>

<details>
<summary>フィルターはモデルのフィールドを参照できる</summary>

>もしモデルのフィールドの値を、同じモデルの他のフィールドと比較したい時にはどうすればいいのでしょう？
>
>そのような比較を行うために、Django は F 式 を用意しています。 F() のインスタンスは、クエリの中でモデルのフィールドへの参照として振る舞います。したがって、この参照をクエリの中で使うことで、同じモデルのインスタンスの異なる2つのフィールドの値を比較することができます。
>
>たとえば、pingback の数よりコメントの数が多いすべてのブログエントリーのリストを検索するには、pingback の数を参照する F() オブジェクトを作り、その F() オブジェクトをクエリの中で次のように使います。

``` python 3
>>> from django.db.models import F
>>> Entry.objects.filter(number_of_comments__gt=F('number_of_pingbacks'))
```

>Django は F() オブジェクトで、定数と他の F() オブジェクトの両方で、加算、減算、乗算、除算、モジュロ、べき乗の算術を使うことをサポートしています。コメント数がピングバックの 2 倍以上のブログエントリを全て見つけるには、クエリを修正します。

``` python 3
>>> Entry.objects.filter(number_of_comments__gt=F('number_of_pingbacks') * 2)
```

[フィルターはモデルのフィールドを参照できる](https://docs.djangoproject.com/ja/4.1/topics/db/queries/#filters-can-reference-fields-on-the-model)
</details>

Querying JSONField

``` python 3
class Dog(models.Model):
    name = models.CharField(max_length=200)
    data = models.JSONField(null=True)

    class Meta:
        db_table = "dog"
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

```

<details>
<summary>Storing and querying for None</summary>

``` Python 3
>>> Dog.objects.create(name='Max', data=None)
<Dog: Max>
>>> Dog.objects.create(name='Archie', data=Value('null'))
Traceback (most recent call last):
  File "<console>", line 1, in <module>
NameError: name 'Value' is not defined
>>> Dog.objects.create(name='Archie', data='null')
<Dog: Archie>
>>> Dog.objects.filter(data=None)
<QuerySet []>
>>> Dog.objects.filter(data='null')
<QuerySet [<Dog: Archie>]>
>>> Dog.objects.filter(data__isnull=True)
<QuerySet [<Dog: Max>]>
>>> Dog.objects.filter(data__isnull=False)
<QuerySet [<Dog: Archie>]>
>>>
```

</details>

<details>
<summary>Key, index, and path transforms</summary>

``` Python 3
>>> Dog.objects.create(name='Rufus', data={
...     'bread': 'labrador',
...     'owner': {
...         'name': 'Bob',
...         'other_pets' : [{
...             'name': 'Fishy',
...         }],
...     },
... })
<Dog: Rufus>
```

</details>

<details>
<summary>Multiple keys can be chained together to form a path lookup:</summary>

``` Python 3
>>> Dog.objects.filter(data__owner__name='Bob')
<QuerySet [<Dog: Rufus>]>
```

</details>

<details>
<summary>If the key is an integer, it will be interpreted as an index transform in an array:</summary>

``` Python 3
>>> Dog.objects.filter(data__owner__other_pets__0__name='Fishy')
<QuerySet [<Dog: Rufus>]>
```

</details>

If the key you wish to query by clashes with the name of another lookup, use the contains lookup instead.

<details>
<summary>To query for missing keys, use the isnull lookup:</summary>

``` Python 3
>>> Dog.objects.create(name='Shop', data={'breed': 'collie'})
<Dog: Shop>
>>> Dog.objects.filter(data__owner__isnull=True)
<QuerySet [<Dog: Archie>, <Dog: Max>, <Dog: Shop>]>
>>>
```

</details>

Containment and key lookups

<details>
<summary>The contains lookup is overridden on JSONField. </summary>

``` Python 3
>>> Dog.objects.create(name='Rufus', data={'breed': 'labrador', 'owner': 'Bob'})
<Dog: Rufus>
>>> Dog.objects.create(name='Meg', data={'breed': 'collie', 'owner': 'Bob'})
<Dog: Meg>
>>> Dog.objects.create(name='Fred', data={})
<Dog: Fred>
>>> Dog.objects.filter(data__contains={'owner': 'Bob'})
django.db.utils.NotSupportedError: contains lookup is not supported on this database backend.
# contains is not supported on Oracle and SQLite.
# Its backend is SQLite now.
```

</details>

<details>
<summary>contained_by</summary>

``` Python 3
>>> Dog.objects.create(name='Rufus', data={'breed': 'labrador', 'owner': 'Bob'})
<Dog: Rufus>
>>> Dog.objects.create(name='Meg', data={'breed': 'collie', 'owner': 'Bob'})
<Dog: Meg>
>>> Dog.objects.create(name='Fred', data={})
<Dog: Fred>
>>> Dog.objects.filter(data__contained_by={'breed': 'collie', 'owner': 'Bob'})
django.db.utils.NotSupportedError: contained_by lookup is not supported on this database backend.
# contains is not supported on Oracle and SQLite.
# Its backend is SQLite now.
```

</details>

<details>
<summary>has_key</summary>

``` Python 3
>>> Dog.objects.create(name='Rufus', data={'breed': 'labrador'})
<Dog: Rufus>
>>> Dog.objects.create(name='Meg', data={'breed': 'collie', 'owner': 'Bob'})
<Dog: Meg>
>>> Dog.objects.filter(data__has_key='owner')
<QuerySet [<Dog: Meg>, <Dog: Meg>, <Dog: Meg>, <Dog: Rufus>, <Dog: Rufus>, <Dog: Rufus>]>
```

</details>

<details>
<summary>has_keys</summary>

``` Python 3
>>> Dog.objects.filter(data__has_keys=['breed', 'owner'])
<QuerySet [<Dog: Meg>, <Dog: Meg>, <Dog: Meg>, <Dog: Rufus>, <Dog: Rufus>]>
```

</details>

<details>
<summary>has_any_keys</summary>

``` Python 3
>>> Dog.objects.filter(data__has_any_keys=['owner', 'breed'])
<QuerySet [<Dog: Meg>, <Dog: Meg>, <Dog: Meg>, <Dog: Rufus>, <Dog: Rufus>, <Dog: Rufus>, <Dog: Rufus>, <Dog: Shop>]>
```

</details>

Q オブジェクトを用いた複雑な検索

>キーワード引数のクエリ（filter() など）は、"AND "結合される。-- などのキーワード引数によるクエリは、互いに "AND" されます。より複雑なクエリ (たとえば OR 文を含むクエリ) を実行する必要がある場合は、Q オブジェクトを使用します。
>
>Q オブジェクト (django.db.models.Q) は、キーワード引数のコレクションをカプセル化するた めに使われるオブジェクトです。これらのキーワード引数は、上の 「フィールド検索」 のように指定します。

<details>
<summary>Q Object Examples</summary>

``` Python 3
Q(question__startswith='What')
```

``` Python 3
Q(question__startswith='Who') | Q(question__startswith='What')
```

>Qオブジェクトを`&`、 `|`、 `^`演算子で組み合わせ、親文字でグループ化することで、任意の複雑な文を構成することができます。
>また、Q オブジェクトは `~` 演算子で否定することができ、通常の問い合わせと否定（NOT）問い合わせの両方を組み合わせた検索が可能です。

``` Python 3
Q(question__startswith='Who') | ~Q(pub_date__year=2005)
```

>キーワード引数を取る各検索関数 (例: filter(), exclude(), get()) には、位置引数 (名前なし) として 1 つ以上の Q オブジェクトを渡すことも可能です。
>検索関数に複数の Q オブジェクト引数を指定した場合、それらの引数は "AND" 処理されます。

``` Python 3
Poll.objects.get(
    Q(question__startswith='Who'),
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
)
```

``` SQL
SELECT * from polls WHERE question LIKE 'Who%'
    AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')
```

>ルックアップ関数は、Qオブジェクトとキーワード引数を混在して使用することができます。ルックアップ関数に提供されたすべての引数（キーワード引数であれ、Qオブジェクトであれ）は、一緒に「AND」されます。
>しかし、Qオブジェクトが提供される場合、それはキーワード引数の定義の前になければなりません。

``` Python 3
Poll.objects.get(
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
    question__startswith='Who',
)
```

</details>

