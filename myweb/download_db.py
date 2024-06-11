from mongoengine import connect
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myweb.settings")
django.setup()

from index.models import Author as DjangoAuthor, Quote as DjangoQuote, Tag as DjangoTag
from models_from_mongodb import Author, Quotes


with open('password.txt', 'r') as file_pass:
    password = file_pass.read()
    # print(password)

URL = f'mongodb+srv://tapxyh1445:{password}@nosqlbase.zekqidk.mongodb.net/'
connect(host=URL)

# Получение данных из MongoDB
authors = Author.objects.all()
quotes = Quotes.objects.all()

# print("MongoDB authors:", authors)
# print("MongoDB quotes:", quotes)
# for i in quotes:
#     print(i.author)


# Перенос данных в PostgreSQL
django_authors = []
for author in authors:
    django_authors.append(DjangoAuthor(fullname=author.fullname,
                                       born_date=author.born_date,
                                       born_location=author.born_location,
                                       description=author.description,
                                       message_sent=author.message_sent))
DjangoAuthor.objects.bulk_create(django_authors)

django_quotes = []
for quote in quotes:
    author, created = DjangoAuthor.objects.get_or_create(fullname=quote.author)
    django_quote, created = DjangoQuote.objects.get_or_create(quote=quote.quote, author=author)
    
    # Создание или получение объектов тегов и привязка их к цитате
    for tag_name in quote.tags:
        tag, _ = DjangoTag.objects.get_or_create(tag=tag_name)
        django_quote.tag.add(tag)

    django_quotes.append(django_quote)

# Попытка вставить данные с игнорированием конфликтов
try:
    DjangoQuote.objects.bulk_create(django_quotes, ignore_conflicts=True)
    print("Successfully transferred data to PostgreSQL.")
except IntegrityError as e:
    print(f"Failed to transfer data: {e}")
