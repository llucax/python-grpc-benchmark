import asyncio

import grpc.aio

import test_pb2
import test_pb2_grpc


async def say_hello(name: str) -> str:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = test_pb2_grpc.GreeterStub(channel)
        return (await stub.SayHello(test_pb2.HelloRequest(name=name))).message

async def stream_numbers(count: int) -> list[int]:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = test_pb2_grpc.GreeterStub(channel)
        r: list[int] = []
        received = 0
        async for reply in stub.StreamNumbers(test_pb2.StreamRequest()):
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
