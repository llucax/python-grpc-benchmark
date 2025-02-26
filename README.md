> [!IMPORTANT]
> This project is archived because [grpclib]'s author said there are [no plans for further development](https://github.com/vmagamedov/grpclib/issues/197#issuecomment-2249641932), so performance seems to be less important when choosing which library to use.
> 
> Also, if you are still interested, please check the results in [#2](https://github.com/llucax/python-grpc-benchmark/issues/2), as there are a few improvements to the way things are measured there.

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
writing, **about 2 times faster** than [grpcio] for a single request-reply
roundtrip, and **about 1.5 times faster** than [grpcio] for streaming 10
numbers. Some preliminary tests show that for streaming numbers more
continuously (100.000 numbers), **the throughput of [grpcio] is about 30%
higher than [betterproto]/[grpclib]**.

Also some basic memory benchmarks show that [betterproto]/[grpclib] uses less
memory than [grpcio] (about 40% less memory for a single request-reply and
about 70% less momory for streaming 10 numbers, resulting in the same reduction
of minor page faults).

For both libraries memory consumption seem to stay stable when processing more
messages (request-reply or streaming).

```console
$ ./benchmark 
grpcio
        1 request-reply:       100 loops, best of 5: 2.98 msec per loop
                                40352 KB max | 109;53936 in;voluntary context switches | 0;27767 major;minor page faults
        streaming 10 numbers:  100 loops, best of 5: 2.86 msec per loop
                                45548 KB max | 201;77380 in;voluntary context switches | 0;25620 major;minor page faults
grpclib
        1 request-reply:       200 loops, best of 5: 1.39 msec per loop
                                28560 KB max | 50;16684 in;voluntary context switches | 0;13323 major;minor page faults
        streaming 10 numbers:  100 loops, best of 5: 2.25 msec per loop
                                26840 KB max | 54;8232 in;voluntary context switches | 0;10396 major;minor page faults
```

Doing some tests with streaming more numbers (100.000) shows that
[betterproto]/[grpclib] has a better throughput than [grpcio] (about 9.500
numbers/second vs 12.500 numbers/second, so around 30% more throughput). The
memory consumption remains lower in [betterproto]/[grpclib] than in [grpcio]
though (about 60% less).

It might be worth crafting a benchmark more oriented to test throughput to get
more conclusive results.

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
* [GNU time](https://www.gnu.org/software/time/) (for memory usage statistics)

### Building

Run `./build` to build the Docker image for the server and generate the Python
bindings for the clients.

### Running

Run `./benchmark` to run the benchmark (to get slighly more stable results you
might want to use `sudo nice -n-10 ./benchmark`).

### Cleanning up

Run `./clean` to remove generated files and the generated Docker image.

[betterproto]: https://github.com/danielgtaylor/python-betterproto
[grpclib]: https://github.com/vmagamedov/grpclib
[grpcio]: https://grpc.github.io/grpc/python/
