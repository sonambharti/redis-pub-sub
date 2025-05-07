<div align='center'>
    <h1>Redis Pub Sub</h1>
</div>
<div>
    <p>
        The given project implements a system called a <code>Redis Publish-Subscribe (Pub/Sub) system<code> using Redis Streams and Consumer Groups. The system is designed to handle a large number of producers and consumers, and it provides a way to decouple the producers and consumers, making it easier to scale and maintain the system. <br>
        The whole idea of this system is to enable efficient, reliable, and scalable asynchronous communication between different components (such as microservices) by streaming data through Redis.
    </p>
</div>
<div>
    <h2>Impotant Terms: </h2>
    <ul>
        <li><strong>Stream</strong>: A Redis data structure that stores an append-only log of messages. It is like a data pipeline which stores data, then it will stream the data with each group</li> 
        <li><strong>Group</strong>: A consumer group that allows multiple consumers to share the workload of processing messages from a stream.</li> 
        <li><strong>Producer</strong>: The component that publishes data (orders) into the Redis stream.</li> 
        <li><strong>Consumer<strong>: The component that reads and processes data from the Redis stream as part of a consumer group. If we have 5 consumer in a group, then only one consumer will have the access of data.</li>
    </ul>
    <p>
        In this system: <br>
        A Producer publishes data (in this case, order information) into a Redis Stream. <br>
        The Stream acts as a data pipeline that stores the messages. <br>
        Multiple Consumer Groups are created, each containing one or more Consumers. <br>
        Each Consumer Group processes the stream independently, and within a group, each message is delivered to only one Consumer, ensuring workload distribution. <br>
        This architecture allows multiple services to consume the same data stream without interfering with each other, providing fault tolerance and scalability. <br>
        This system is particularly useful for scenarios where multiple microservices need to process the same data asynchronously, avoiding the drawbacks of REST APIs or WebSockets, such as latency, data loss, or high memory usage.
    </p>
</div>
<div>
    <h2>Steps to execute this file</h2>
    <ol>
        <li>Start docker engine.</li>
        <li>Exute the docker compose file using command <code>docker-compose up</code></li>
        <li>Execute the initialization_stram file using command <code>python -m initialization_stream</code></li>
        <li>Execute the producer file using command <code>python -m producer</code><li>
        <li>Execute the consumer1 file using command <code>python -m consumer1</code><li>
        <li>Execute the consumer2 file using command <code>python -m consumer2</code><li>
    </ol>
</div>
 
<div>
    <h3> Code Explaination</h3>
    <p>
        <strong>Redis Connection Setup (<code>redisPool.py</code>)</strong> <br>
        The redisPool.py file defines an asynchronous function redis_connect that creates a Redis connection pool using the redis.asyncio library. It connects to Redis at localhost:6379 with a maximum of 5 connections and UTF-8 decoding enabled. This connection is used by the producer and consumers to interact with Redis. <br>
    </p>
    <p>
        <strong>Stream and Consumer Group Initialization (<code>initialization_strem.py</code>)</strong><br>
        This script initializes the Redis stream and consumer groups. It defines a stream key orders and two consumer groups: email_group and fulfillment_group. The async function initialize_streams_and_groups creates these consumer groups on the stream if they do not already exist, handling the case where groups are already present. <br>
    </p>
    <p>
        <strong>Producer (<code>producer.py</code>)</strong><br>
        The producer asynchronously publishes order data to the orders stream. It serializes relevant order information (order ID and customer email) as JSON and adds it to the stream using the Redis XADD command. This simulates pushing new orders into the data pipeline.
    </p>
    <p>
        <strong>Consumers (<code>consumer1.py</code> and <code>consumer2.py</code>)</strong><br>
        <code>consumer1.py</code> acts as a consumer in the fulfillment_group consumer group with the consumer name email_consumer. It reads messages from the orders stream using the XREADGROUP command, processes each order by printing fulfillment information, and acknowledges the message to Redis. <br>
        <code>consumer2.py</code> acts as a consumer in the email_group consumer group with the consumer name fulfillment_consumer. It similarly reads messages, prints raw message data, processes fulfillment, and acknowledges messages.
        Both consumers continuously poll for new messages, blocking for up to 5 seconds if none are available.<br>
    </p>
    <p>
        <strong>Configuration (<code>config.py<code>)</strong><br>
        Contains Redis connection settings such as the Redis URL and maximum connections. These settings are referenced in the Redis connection setup but currently hardcoded values are used.
    </p>
</div>


**Real world applications:**
If we have multiple microservices to send data, we have 3 methods: through REST APIs (takes more time and if 1 service is down then we have to call 2nd task again which is tough/helerious task which lead to data loss), queuing system (fast, memory-efficient, low load on server, donot loose data in case of server down), Websocket (require so much in memory).


##  Conclusion:
The system uses Redis Streams and Consumer Groups to ensure that messages are distributed among consumers in a group, with each message processed by only one consumer. <br>
This approach is efficient for microservices communication, avoiding data loss and reducing server load compared to REST APIs or WebSockets. <br>
The docker-compose.yaml file (not detailed here) likely sets up the Redis server container for local development.<br>
In summary, this project demonstrates a Redis-based Pub/Sub system leveraging Redis Streams and Consumer Groups to build a robust data streaming and processing pipeline.
