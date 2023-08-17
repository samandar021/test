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

```
# Second task
## API Endpoints

### Endpoint for VK directly

Конечные точки API будут доступны по следующим URL-адресам:
```
API профиля ВКонтакте: http://localhost:8000/api/v1/profile/?profile=<имя пользователя>
API лайков ВКонтакте: http://localhost:8000/api/v1/likes/?link=<post_link>
API для последних 10 сообщений и получения сведений об одном сообщении:
   http://localhost:8000/api/v1/posts/?profile=<username>
   
```
 Как получить доступ к API endpoints, предоставленным вашим проектом Django, для использования данных из базы данных
```
API профиля ВКонтакте: http://localhost:8000/profile/?profile=<profile_id>
API лайков ВКонтакте: http://localhost:8000/likes/?link=<post_url>
```
# Installation

```
1 - clone repo
    git clone https://github.com/samandar021/test.git
    
2 - create a virtual environment and activate
    pip3 install virtualenv
    virtualenv venv
    venv\Scripts\activate(windows) or source venv/bin/activate(unix-based systems)
    
3 - cd into project "cd payme-sample"

4 - Install dependencies
pip3 install -r requirements.txt


5 - Run app
python3 manage.py migrate
python3 manage.py runserver

or 

docker-compose build
docker-compose up
```

 
