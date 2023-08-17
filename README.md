# First Task

## SQL Query Task

В нашей базе данных Postgresql есть следующие таблицы: «clients», «orders» и «client_orders». Мы можем использовать следующий SQL-запрос, чтобы найти и отобразить покупателей в возрасте от 18 до 65 лет, которые купили только 2 продукта, и все продукты от той же категории.

```sql
SELECT
    clients.id,
    CONCAT(clients.first_name, ' ', clients.last_name) AS Name,
    orders.category AS Category,
    STRING_AGG(DISTINCT orders.product, ', ' ORDER BY orders.product ASC) AS Products
FROM
    clients
JOIN
    client_orders ON clients.id = client_orders.client_id
JOIN
    orders ON client_orders.order_id = orders.id
WHERE
    clients.age BETWEEN 18 AND 65
GROUP BY
    clients.id, clients.first_name, clients.last_name, orders.category
HAVING
    COUNT(DISTINCT orders.product) = 2
    AND COUNT(DISTINCT orders.category) = 1
ORDER BY
    clients.id;
