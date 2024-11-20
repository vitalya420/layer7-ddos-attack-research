import time
import json
import psutil
import os

from flask import Flask, request, jsonify

import orjson
import ujson
import simplejson

app = Flask(__name__)


def get_memory_usage():
    process = psutil.Process()
    mem = process.memory_info()
    return mem.rss


@app.route("/json", methods=["POST"])
def json_():
    start_time = time.time()
    start_memory = get_memory_usage()

    json.loads(request.data)

    end_memory = get_memory_usage()
    end_time = time.time()

    return jsonify(
        {
            "data_size": len(request.data),
            "parsed_in": end_time - start_time,
            "memory_usage_delta": end_memory - start_memory,
            "process_id": os.getpid(),
        }
    )


@app.route("/ujson", methods=["POST"])
def ujson_():
    start_time = time.time()
    start_memory = get_memory_usage()

    ujson.loads(request.data)

    end_memory = get_memory_usage()
    end_time = time.time()

    return jsonify(
        {
            "data_size": len(request.data),
            "parsed_in": end_time - start_time,
            "memory_usage_delta": end_memory - start_memory,
            "process_id": os.getpid(),
        }
    )


@app.route("/orjson", methods=["POST"])
def orjson_():
    start_time = time.time()
    start_memory = get_memory_usage()

    orjson.loads(request.data)

    end_memory = get_memory_usage()
    end_time = time.time()

    return jsonify(
        {
            "data_size": len(request.data),
            "parsed_in": end_time - start_time,
            "memory_usage_delta": end_memory - start_memory,
            "process_id": os.getpid(),
        }
    )


@app.route("/simplejson", methods=["POST"])
def simplejson_():
    start_time = time.time()
    start_memory = get_memory_usage()

    simplejson.loads(request.data)

    end_memory = get_memory_usage()
    end_time = time.time()

    return jsonify(
        {
            "data_size": len(request.data),
            "parsed_in": end_time - start_time,
            "memory_usage_delta": end_memory - start_memory,
            "process_id": os.getpid(),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
