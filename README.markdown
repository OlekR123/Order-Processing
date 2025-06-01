# Сервис обработки заказов на gRPC

## Оглавление
- [Описание](#описание)
- [Сущности](#сущности)
- [Методы](#методы)
- [Требования](#требования)
- [Установка](#установка)
- [Запуск сервиса](#запуск-сервиса)
- [Примеры запросов и ответов](#примеры-запросов-и-ответов)
- [Бонусные функции](#бонусные-функции)
- [Структура проекта](#структура-проекта)

## Описание
Этот проект реализует **сервис обработки заказов** для платформы электронной коммерции на основе **gRPC**.  
Сервис позволяет:  
- Создавать, получать, обновлять и отменять заказы.  
- Получать список всех заказов.  
- Транслировать обновления статусов заказов в реальном времени.  

Данные сохраняются в базе **SQLite**.

## Сущности
- **Order (Заказ)**:  
  - `id` — уникальный идентификатор.  
  - `items[]` — список товаров.  
  - `total_amount` — общая сумма.  
  - `status` — статус заказа.  

- **OrderItem (Элемент заказа)**:  
  - `id` — уникальный идентификатор.  
  - `product_name` — название товара.  
  - `quantity` — количество.  
  - `price` — цена.

## Методы
- **CreateOrder**: Создаёт новый заказ с товарами и общей суммой.  
- **GetOrder**: Получает заказ по ID.  
- **UpdateOrderStatus**: Обновляет статус заказа (например, `PENDING`, `CONFIRMED`, `SHIPPED`, `CANCELLED`).  
- **CancelOrder**: Отменяет заказ.  
- **ListOrders**: Возвращает список всех заказов.  
- **OrderStatusStream**: Транслирует обновления статусов заказов в реальном времени.

## Требования
- **Python** 3.8 или выше.  
- **protoc** (компилятор Protobuf).  
- **gRPC Python Tools** (`grpcio`, `grpcio-tools`).  
- **VS Code** (рекомендуется).  
- Поддерживаемые ОС: Windows, macOS, Linux.

## Установка
1. **Установите Python**:  
   - Скачайте Python с [официального сайта](https://www.python.org/downloads/).  
   - Убедитесь, что Python добавлен в PATH.  
   - Проверьте версию:  
     ```cmd
     python --version
     ```  
     Ожидаемый вывод: `Python 3.8.x` или выше.

2. **Установите protoc**:  
   - Скачайте с [Protobuf Releases](https://github.com/protocolbuffers/protobuf/releases).  
   - Для Windows: загрузите `protoc-<version>-win64.zip`, распакуйте, добавьте `bin/protoc.exe` в PATH.  
   - Проверьте:  
     ```cmd
     protoc --version
     ```  
     Ожидаемый вывод: `libprotoc 3.x.x`.

3. **Установите gRPC Tools**:  
   ```cmd
   pip install grpcio grpcio-tools
   ```  
   Если возникает ошибка:  
   ```cmd
   pip install --no-binary grpcio grpcio grpcio-tools
   ```

4. **Склонируйте проект**:  
   ```cmd
   git clone https://github.com/ваш-username/order-processing.git
   cd order_processing
   ```  
   Или скопируйте файлы проекта в папку `order_processing`.

5. **Сгенерируйте код Protobuf**:  
   ```cmd
   python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/order.proto
   ```  
   После выполнения в корне проекта появятся файлы:  
   - `order_pb2.py`  
   - `order_pb2_grpc.py`

## Запуск сервиса
1. **Запустите сервер**:  
   ```cmd
   python server.py
   ```  
   Ожидаемый вывод:  
   ```
   Server started on port 50051
   ```

2. **Запустите клиент** (в новом окне командной строки):  
   ```cmd
   cd order_processing
   python client.py
   ```  
   Клиент продемонстрирует работу всех методов, включая стриминг, и выведет результаты в консоль.

## Примеры запросов и ответов
### CreateOrder
**Запрос**:  
```python
items = [
    OrderItem(product_name="Laptop", quantity=1, price=1000.0),
    OrderItem(product_name="Mouse", quantity=2, price=25.0)
]
request = CreateOrderRequest(items=items, total_amount=1050.0)
```

**Ответ**:  
```
order {
  id: "<uuid>"
  items: [
    { id: "<uuid>", product_name: "Laptop", quantity: 1, price: 1000.0 },
    { id: "<uuid>", product_name: "Mouse", quantity: 2, price: 25.0 }
  ]
  total_amount: 1050.0
  status: "PENDING"
}
```

### GetOrder
**Запрос**:  
```python
request = GetOrderRequest(id="<uuid>")
```

**Ответ**:  
```
order {
  id: "<uuid>"
  items: [
    { id: "<uuid>", product_name: "Laptop", quantity: 1, price: 1000.0 },
    { id: "<uuid>", product_name: "Mouse", quantity: 2, price: 25.0 }
  ]
  total_amount: 1050.0
  status: "PENDING"
}
```

### OrderStatusStream
**Ответ (поток)**:  
```
StatusUpdate: order_id=<uuid>, status=CONFIRMED, timestamp=1697051234
StatusUpdate: order_id=<uuid>, status=SHIPPED, timestamp=1697051235
StatusUpdate: order_id=<uuid>, status=CANCELLED, timestamp=1697051236
```

## Бонусные функции
- **Хранение данных**: Заказы и обновления статусов сохраняются в SQLite (`orders.db`).  
- **Стриминг**: Реализован через `OrderStatusStream` для обновлений статусов в реальном времени.

## Структура проекта
```
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
```