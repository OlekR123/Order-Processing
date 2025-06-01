Сервис обработки заказов на gRPC 🚀
Оглавление 📋

Описание
Сущности
Методы
Требования
Установка
Запуск сервиса
Примеры запросов и ответов
Бонусные функции
Структура проекта

Описание
Этот проект реализует сервис обработки заказов для платформы электронной коммерции на основе gRPC.Он позволяет:  

Создавать, получать, обновлять и отменять заказы.  
Получать список заказов.  
Транслировать обновления статусов заказов в реальном времени.

Данные хранятся в SQLite.
Сущности 🗃️

Order (Заказ): id, items[], total_amount, status.
OrderItem (Элемент заказа): id, product_name, quantity, price.

Методы ⚙️

CreateOrder: Создаёт новый заказ с товарами и общей суммой.
GetOrder: Получает заказ по ID.
UpdateOrderStatus: Обновляет статус заказа (например, PENDING, CONFIRMED, SHIPPED, CANCELLED).
CancelOrder: Отменяет заказ.
ListOrders: Возвращает список всех заказов.
OrderStatusStream: Транслирует обновления статусов заказов в реальном времени.

Требования 📦

Python 3.8+
protoc (Protobuf Compiler)
gRPC Python Tools (grpcio, grpcio-tools)
VS Code (рекомендуется)
ОС: Windows, macOS или Linux

Установка 🛠️

Установите Python:

Скачайте с официального сайта.
Добавьте Python в PATH.
Проверьте:  python --version

Ожидаемый вывод: Python 3.8.x или выше.


Установите protoc:

Скачайте с Protobuf Releases.
Для Windows: распакуйте protoc-<version>-win64.zip, добавьте bin/protoc.exe в PATH.
Проверьте:  protoc --version

Ожидаемый вывод: libprotoc 3.x.x.


Установите gRPC Tools:
pip install grpcio grpcio-tools

Если ошибка:  
pip install --no-binary grpcio grpcio grpcio-tools


Склонируйте проект:
git clone https://github.com/ваш-username/order-processing.git
cd order_processing


Сгенерируйте код Protobuf:
python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/order.proto



Запуск сервиса ▶️

Запустите сервер:
python server.py

Ожидаемый вывод: Server started on port 50051.

Запустите клиент (в новом окне командной строки):
cd order_processing
python client.py



Примеры запросов и ответов 📜
CreateOrder
Запрос:
items = [
    OrderItem(product_name="Laptop", quantity=1, price=1000.0),
    OrderItem(product_name="Mouse", quantity=2, price=25.0)
]
request = CreateOrderRequest(items=items, total_amount=1050.0)

Ответ:
order {
  id: "<uuid>"
  items: [
    { id: "<uuid>", product_name: "Laptop", quantity: 1, price: 1000.0 },
    { id: "<uuid>", product_name: "Mouse", quantity: 2, price: 25.0 }
  ]
  total_amount: 1050.0
  status: "PENDING"
}

GetOrder
Запрос:
request = GetOrderRequest(id="<uuid>")

Ответ:
order {
  id: "<uuid>"
  items: [
    { id: "<uuid>", product_name: "Laptop", quantity: 1, price: 1000.0 },
    { id: "<uuid>", product_name: "Mouse", quantity: 2, price: 25.0 }
  ]
  total_amount: 1050.0
  status: "PENDING"
}

OrderStatusStream
Ответ (поток):
StatusUpdate: order_id=<uuid>, status=CONFIRMED, timestamp=1697051234
StatusUpdate: order_id=<uuid>, status=SHIPPED, timestamp=1697051235
StatusUpdate: order_id=<uuid>, status=CANCELLED, timestamp=1697051236

Бонусные функции 🎁

Хранение данных: Данные сохраняются в SQLite (orders.db).
Стриминг: Обновления статусов в реальном времени через OrderStatusStream.

Структура проекта 📁
order_processing/
    __pycache__/              (автоматически создаётся Python)
        database.cpython-311.pyc
        order_pb2_grpc.cpython-311.pyc
        order_pb2.cpython-311.pyc
    proto/
        order.proto
    client.py
    database.py
    order_pb2_grpc.py         (сгенерирован из order.proto)
    order_pb2.py              (сгенерирован из order.proto)
    orders.db                 (база данных SQLite)
    README.md
    server.py

