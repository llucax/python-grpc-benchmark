import asyncio
import test

from grpclib.client import Channel


async def say_hello(name: str) -> str:
    async with Channel("localhost", 50051) as channel:
        client = test.GreeterStub(channel)
        return (await client.say_hello(test.HelloRequest(name=name))).message


async def stream_numbers(count: int) -> list[int]:
    async with Channel("localhost", 50051) as channel:
        client = test.GreeterStub(channel)
        r: list[int] = []
        received = 0
        async for reply in client.stream_numbers(test.StreamRequest()):
            r.append(reply.number)
            received += 1
            if received >= count:
                break
        return r


if __name__ == "__main__":
    print("Calling say_hello")
    response = asyncio.run(say_hello("world"))
    print(f"Greeter client received: response={response}")
    print("Streaming numbers")
    response = asyncio.run(stream_numbers(10))
    print(f"Received numbers: {response}")
