import grpc
import order_pb2
import order_pb2_grpc
import time

def create_order(stub):
    items = [
        order_pb2.OrderItem(product_name="Laptop", quantity=1, price=1000.0),
        order_pb2.OrderItem(product_name="Mouse", quantity=2, price=25.0)
    ]
    request = order_pb2.CreateOrderRequest(items=items, total_amount=1050.0)
    response = stub.CreateOrder(request)
    print("CreateOrder:", response.order)
    return response.order.id

def get_order(stub, order_id):
    request = order_pb2.GetOrderRequest(id=order_id)
    response = stub.GetOrder(request)
    print("GetOrder:", response.order)

def update_order_status(stub, order_id, status):
    request = order_pb2.UpdateOrderStatusRequest(id=order_id, status=status)
    response = stub.UpdateOrderStatus(request)
    print(f"UpdateOrderStatus ({status}):", response.order)

def cancel_order(stub, order_id):
    request = order_pb2.CancelOrderRequest(id=order_id)
    response = stub.CancelOrder(request)
    print("CancelOrder:", response.message)

def list_orders(stub):
    request = order_pb2.ListOrdersRequest()
    response = stub.ListOrders(request)
    print("ListOrders:", [order for order in response.orders])

def stream_order_status(stub):
    request = order_pb2.ListOrdersRequest()
    print("Streaming OrderStatusUpdates...")
    for update in stub.OrderStatusStream(request):
        print(f"StatusUpdate: order_id={update.order_id}, status={update.status}, timestamp={update.timestamp}")

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = order_pb2_grpc.OrderServiceStub(channel)
        
        order_id = create_order(stub)
        get_order(stub, order_id)
        update_order_status(stub, order_id, "CONFIRMED")
        update_order_status(stub, order_id, "SHIPPED")
        cancel_order(stub, order_id)
        list_orders(stub)
        
        stream_order_status(stub)
        time.sleep(10)

if __name__ == '__main__':
    run()