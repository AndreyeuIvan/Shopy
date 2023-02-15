ShoppingList

Models
User (extend AbstractUser, обязательно добавить поля email(uniq), phone)
Account (id, user, amount (default=0))
Reserved (id, user, product_id, number_of_units)
Storage(id, name, shop_name, unit, number_of_units, price_for_unit, price_for_kg)

User one-to-one Account
User one-to-many Reserved

Функционал

User видит только свои товары. +
User выбирает товар, number_of_units, нажимает кнопку “Add” и его товары добавляется в Reserved (уменьшается number_of_units в Product).+
User выбирает товар, number_of_units, нажимает кнопку “Remove” и его товары удаляются из Reserved (увеличивается number_of_units в Storage).
User выбирает товар и нажимает кнопку “Delete” и все его товары одного вида удаляются из Reserved (увеличивается number_of_units в Storage).

User нажимает кнопку “Buy” и все его товары удаляются из Reserved и списываются деньги с Account.
User нажимает кнопку “Clear” и все его товары удаляются из Reserved (увеличивается number_of_units в Storage).

User пользуется фильтрами и сортировкой для добавления продуктов +
Добавить фильтрацию товаров по названию магазина. +
Добавить фильтрацию товаров по названию товара. +
Добавить сортировку по price_for_unit. +
Добавить сортировку по price_for_kg. +

Товары в Product добавляет Admin через DjangoAdmin.
Пополнение Account через DjangoAdmin.

Задачи:

1. Создать модели :
   User (extend AbstractUser, обязательно добавить поля email(uniq), phone)
   Account (id, user, amount (default=0))
   Reserved (id, user, product_id, number_of_units)
   Product(id, name, shop_name, unit, number_of_units, price_for_unit, price_for_kg)
2. Создать listview для reserve.
3. Добавить аутенцификацию пользователей.
4. Создать view c запросоми на добавления(add) и изменение(edit) и удаление(delete) товара. Важно ли какой тип запроса?
5. Создать view, что удаляет товары из Reserved и списывает деньги. - В случае покупки
6. Создать view, что удаляет товары из Reserved и списывает деньги. - В случае обновления корзины
7. Во view c User использовать filter и order_by
8. Во view c Product использовать filter по name_shop.
9. Во view c Product использовать filter по name_product.
   Увелилить number of users.
10. Переписать url
11. Исправить валидаторы
12. Переписать request
13. Bulk_update

TO-DO list:

1. Лучше разбивать на отдельные приложения. Тогда у тебя будет все в разных приложения/аппках.

shops
products
DONE!

Account объединить с Users
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

2. Можно сделать поле не чувствительным к регистру и уникальным. Но для этого нужно установить в psql CREATE EXTENSION citext;

from django.contrib.postgres.fields import CICharField

class Shop(models.Model):
name = CICharField(max_length=128, unique=True) # name = models.CharField(max_length=250)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

3. В Reserved модели product user лучше все же не делать их null

class Reserved(models.Model):
user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
product = models.ForeignKey(
"Product", on_delete=models.CASCADE, null=True, blank=True
)
number_of_units = models.IntegerField(
default=0, validators=[MaxValueValidator(1000), MinValueValidator(0)]
)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Мне удалось создать через API Product без User

4. Избегай многострочных комментов кода с """ """. Их не так просто разкомментить.

5. Лучше сразу return. Такие паттерны хорошо отслеживает Sourcery
   return super().validate(data)

6. BasketViewSet(viewsets.ReadOnlyModelViewSet)
   Это сбивает с толку потому что ты потом снова определяешь методы post put и т.д.

7. Мне удалось через API вернуть больше товаров чем есть.

8. Я сделал покупку и у меня прибавилось денег. Ups!

P.S.

Надо лучше проработаь ModelViewSet и как они работают в связке с Serilizers and Models.

- CustomeOrderingFilter посмотри как у меня сделан https://github.com/veledzimovich-iTechArt/shop/blob/master/backend/units/filters.py

- Лучше исправлять опечатки
  def custome_sorting(self, queryset, ordering)
