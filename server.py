import grpc
from concurrent import futures
import time
import order_pb2
import order_pb2_grpc
from database import Database

class OrderService(order_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        self.db = Database()

    def CreateOrder(self, request, context):
        order_id = self.db.create_order(request.items, request.total_amount)
        order, items = self.db.get_order(order_id)
        response = order_pb2.CreateOrderResponse()
        response.order.id = order[0]
        response.order.total_amount = order[1]
        response.order.status = order[2]
        for item in items:
            order_item = response.order.items.add()
            order_item.id = item[0]
            order_item.product_name = item[1]
            order_item.quantity = item[2]
            order_item.price = item[3]
        return response

    def GetOrder(self, request, context):
        order_data = self.db.get_order(request.id)
        if not order_data:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order not found")
            return order_pb2.GetOrderResponse()
        order, items = order_data
        response = order_pb2.GetOrderResponse()
        response.order.id = order[0]
        response.order.total_amount = order[1]
        response.order.status = order[2]
        for item in items:
            order_item = response.order.items.add()
            order_item.id = item[0]
            order_item.product_name = item[1]
            order_item.quantity = item[2]
            order_item.price = item[3]
        return response

    def UpdateOrderStatus(self, request, context):
        order_data = self.db.update_order_status(request.id, request.status)
        if not order_data:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order not found")
            return order_pb2.UpdateOrderStatusResponse()
        order, items = order_data
        response = order_pb2.UpdateOrderStatusResponse()
        response.order.id = order[0]
        response.order.total_amount = order[1]
        response.order.status = order[2]
        for item in items:
            order_item = response.order.items.add()
            order_item.id = item[0]
            order_item.product_name = item[1]
            order_item.quantity = item[2]
            order_item.price = item[3]
        return response

    def CancelOrder(self, request, context):
        order_data = self.db.cancel_order(request.id)
        if not order_data:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order not found")
            return order_pb2.CancelOrderResponse()
        return order_pb2.CancelOrderResponse(message=f"Order {request.id} cancelled")

    def ListOrders(self, request, context):
        orders = self.db.list_orders()
        response = order_pb2.ListOrdersResponse()
        for order, items in orders:
            order_msg = response.orders.add()
            order_msg.id = order[0]
            order_msg.total_amount = order[1]
            order_msg.status = order[2]
            for item in items:
                order_item = order_msg.items.add()
                order_item.id = item[0]
                order_item.product_name = item[1]
                order_item.quantity = item[2]
                order_item.price = item[3]
        return response

    def OrderStatusStream(self, request, context):
        last_index = 0
        while True:
            updates = self.db.get_status_updates()
            for i, update in enumerate(updates):
                if i >= last_index:
                    yield order_pb2.OrderStatusUpdate(
                        order_id=update[0],
                        status=update[1],
                        timestamp=update[2]
                    )
                    last_index = i + 1
            time.sleep(1)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()