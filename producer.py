import redis
import json
from redisPool import redis_connect
import asyncio

# Redis connection
# redis_client = redis_connect()

STREAM_KEY = 'orders'

async def publish_order(order_data):
    redis_client = await redis_connect()

    # Publish to email stream
    email_data = {
        'order_id': order_data['order_id'],
        'customer_email': order_data['customer_email']
    }
    await redis_client.xadd('orders', {'order': json.dumps(email_data)})

    # Publish to fulfillment stream
    # await redis_client.xadd('orders_fulfillment', {'order': json.dumps(order_data)})

if __name__ == '__main__':
    # Example order data
    order = {
        'order_id': '12345',
        'customer_email': 'customer@example.com',
        'items': ['item1', 'item2'],
        'total': 99.99
    }
    asyncio.run(publish_order(order))
