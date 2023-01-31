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
