import redis
import asyncio
from redisPool import redis_connect

# Stream and Consumer Group configurations
STREAM_KEY = 'orders'
CONSUMER_GROUPS = ['email_group', 'fulfillment_group']

async def initialize_streams_and_groups():
    for group in CONSUMER_GROUPS:
        try:
            # Create the stream and consumer group if they don't exist
            redis_client = await redis_connect()
            await redis_client.xgroup_create(name=STREAM_KEY, groupname=group, id='0-0', mkstream=True)
            print(f"Consumer group '{group}' created on stream '{STREAM_KEY}'.")
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP" in str(e):
                print(f"Consumer group '{group}' already exists. Skipping creation.")
            else:
                raise e

if __name__ == '__main__':
    asyncio.run(initialize_streams_and_groups())
