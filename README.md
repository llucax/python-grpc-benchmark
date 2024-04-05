# Python gRPC implementations performance comparison

This repository hosts a simple benchmark comparing [Google's
protobuf/grpc.aio](https://grpc.github.io/grpc/python/) with
[betterproto]/[grpclib].

While evaluating switching from Google to [betterproto] (because of all the
annoyances listed in [betterproto]) I was a bit concerned about performance
after bumping into an (old) [issue saying `grpclib` is 2 times slower than
`grpcio`](https://github.com/vmagamedov/grpclib/issues/81). Since the issue was
too old, I decided to run a simple benchmark to see how the two libraries
compare, to also get some feel about how fast/slow [betterproto] is.

Also the performance comparison in the issue was using the sync version of
[grpcio], as it was before `grpc.aio` was available.

## Results

My results show that [betterproto]/[grpclib] is actually, at the time of
writing, about 2 times **faster** than [grpcio]:

```console
$ ./benchmark 
Benchmarking grpcio: 100 loops, best of 5: 3.75 msec per loop
Benchmarking grpclib: 200 loops, best of 5: 1.25 msec per loop
```

### Test conditions

* AMD Ryzen 7 PRO 5850U CPU
* 32 GB RAM
* Python 3.11.8

* [grpcio] tests

    ```
    grpcio==1.62.1
    grpcio-tools==1.62.1
    protobuf==4.25.3
    ```

* [grpclib] tests

    ```
    betterproto==2.0.0b6
    black==24.3.0
    click==8.1.7
    grpcio==1.62.1
    grpcio-tools==1.62.0
    grpclib==0.4.7
    h2==4.1.0
    hpack==4.0.0
    hyperframe==6.0.1
    isort==5.13.2
    Jinja2==3.1.3
    MarkupSafe==2.1.5
    multidict==6.0.5
    mypy-extensions==1.0.0
    packaging==24.0
    pathspec==0.12.1
    platformdirs==4.2.0
    protobuf==4.25.3
    python-dateutil==2.9.0.post0
    six==1.16.0
    ```

* server

  * g++ 11.4.0
  * libgrpc++ 1.30.2
  * libprotobuf23 3.12.4

## Running the benchmark

### Requirements

* Python 3.11+ (it probably works with other versions)
* Docker (for the server)

### Building

Run `./build` to build the Docker image for the server and generate the Python bindings for the clients.

### Running

Run `./benchmark` to run the benchmark.

### Cleanning up

Run `./clean` to remove generated files and the generated Docker image.

[betterproto]: https://github.com/danielgtaylor/python-betterproto
[grpclib]: https://github.com/vmagamedov/grpclib
[grpcio]: https://grpc.github.io/grpc/python/
