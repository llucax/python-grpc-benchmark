import asyncio

import grpc.aio
import test_pb2
import test_pb2_grpc


async def run(name: str) -> test_pb2.HelloReply:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = test_pb2_grpc.GreeterStub(channel)
        return await stub.SayHello(test_pb2.HelloRequest(name=name))


if __name__ == "__main__":
    response = asyncio.run(run("world"))
    print("Greeter client received: " + response.message)
