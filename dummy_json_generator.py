from functools import lru_cache
import json
import time
import sys
import ujson
import orjson
import simplejson

sys.setrecursionlimit(20000)


@lru_cache
def generate(k: int = 500) -> str:
    """Function to generate deep json like {"_": {"_": "_"}}"""
    if k == 0:
        return '{"_":"_"}'
    return '{"_":' + generate(k - 1) + "}"


def generate_large(root_k: int = 50000, depth_k: int = 500):
    """Generate main json where root key is N and item deep json"""
    segment = generate(k=depth_k)
    buff = "{"
    for i in range(root_k):
        buff += f'"{i}": {segment}, '
    else:
        buff = buff.removesuffix(", ")
        buff += "}"

    return buff


def signle_perfomance_test(root_k, depth_k):
    json_ = generate_large(root_k, depth_k)
    size_mb = len(json_) / 1024 / 1024
    print(f"Root keys {root_k} each {depth_k} deep. Size: {size_mb:02f} megabytes.")

    start = time.time()
    json.loads(json_)
    end = time.time()
    builtin_json = end - start

    print(f"json.loads() took {builtin_json} seconds")

    try:
        start = time.time()
        ujson.loads(json_)
        end = time.time()
        ujson_ = end - start
        print(f"ujson.loads() took {ujson_} seconds")
    except:
        print("ujson.loads() crashed")

    try:
        start = time.time()
        orjson.loads(json_)
        end = time.time()
        orjson_ = end - start
        print(f"orjson.loads() took {orjson_} seconds")
    except:
        print("orjson.loads() crashed")

    try:
        start = time.time()
        simplejson.loads(json_)
        end = time.time()
        simplejson_ = end - start
        print(f"simplejson.loads() took {simplejson_} seconds")
    except:
        print("simplejson.loads() crashed")


def do_perf_test():
    # signle_perfomance_test(5000, 100)
    # signle_perfomance_test(5000, 500)
    # signle_perfomance_test(5000, 1000)
    # signle_perfomance_test(5000, 2000)

    # signle_perfomance_test(10000, 100)
    # signle_perfomance_test(10000, 500)
    # signle_perfomance_test(10000, 1000)
    # signle_perfomance_test(10000, 2000)

    signle_perfomance_test(20000, 500)
    signle_perfomance_test(30000, 500)
    signle_perfomance_test(40000, 500)
    signle_perfomance_test(50000, 500)


if __name__ == "__main__":
    do_perf_test()
