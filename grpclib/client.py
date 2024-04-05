import asyncio
import test

from grpclib.client import Channel


async def run(name: str) -> test.HelloReply:
    async with Channel("localhost", 50051) as channel:
        client = test.GreeterStub(channel)
        return await client.say_hello(test.HelloRequest(name=name))


if __name__ == "__main__":
    response = asyncio.run(run("world"))
    print("Greeter client received:", response.message)
