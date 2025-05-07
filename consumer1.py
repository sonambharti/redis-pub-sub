import json
import asyncio
from redisPool import redis_connect

# Stream and Consumer Group configurations
STREAM_KEY = 'orders'
# GROUP_NAME = 'email_group'  # Same group name
GROUP_NAME = 'fulfillment_group'  # Same group name
CONSUMER_NAME = 'email_consumer'  # Different consumer name

async def process_email(order_data):
    print(f"Processing fulfillment for order {order_data['order_id']} with items {order_data['customer_email']}")

async def consume_messages():
    redis_client = await redis_connect()

    while True:
        try:
            # Fetch messages from the group
            entries = await redis_client.xreadgroup(
                groupname=GROUP_NAME,
                consumername=CONSUMER_NAME,
                streams={STREAM_KEY: '>'},
                count=10,
                block=5000
            )

            if entries:
                for stream, messages in entries:
                    for message_id, data in messages:
                        order_data = json.loads(data['order'])
                        await process_email(order_data)
                        await redis_client.xack(STREAM_KEY, GROUP_NAME, message_id)
            else:
                print("No new messages. Waiting...")

        except Exception as e:
            print(f"Error consuming messages: {e}")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(consume_messages())
