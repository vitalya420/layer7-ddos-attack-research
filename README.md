## Layer 7 DoS Attacks: The Threat of Large JSON Payloads

In the ever-changing cybersecurity landscape, organizations face a multitude of threats that can affect their systems and data. One such threat is Layer 7 Denial of Service (DoS) attacks, which target the application layer of the OSI model. This article delves into the mechanics of Layer 7 DoS attacks, focusing on the use of payloads. Large JSON files are the preferred method of attack.

### What is a Layer 7 DoS Attack?
Layer 7 DoS attacks are designed to overwhelm web applications by exhausting their resources. Make it inaccessible to legitimate users. Unlike traditional DoS attacks that flood the network with traffic lights (Layer 3 or Layer 4), Layer 7 attacks leverage the application layer. It targets specific web application processes. Which makes it especially difficult. Because it is difficult to detect and alleviate

### The Role of JSON in Web Applications
JavaScript Object Notation (JSON) is a simple data format that is easy for humans to read and write. and easy for machines to parse and manipulate It is widely used in web applications to transmit data between the application and the client. Due to its popularity, JSON has become a target for attackers looking to exploit web applications.

### How Large JSON Payloads are Used in DoS Attacks
In a Layer 7 DoS attack using a large JSON payload, the attacker sends an overly large JSON request to the target application. Here's how these types of attacks usually occur:

- Payload Creation: An attacker creates a JSON payload that is significantly larger than the application was designed to handle. This may involve sending large arrays. Deeply nested objects or just big data
- Sending requests : The attacker then sends these large JSON payloads to the target server. This often uses automation tools to generate a large number of requests in a short period of time...
- Processing degradation: When the server receives these requests It will try to process those requests. Large payloads can use a lot of CPU and memory resources. This results in reduced performance or even complete disruption of service.
- Impact on legitimate users: As servers struggle to cope with the high volume of requests. Legitimate users may experience slow response times or complete inability to access the application...

### The Impact of Concurrent Requests with Large JSON Payloads
When an application encounters interactive requests containing JSON values, how those requests are handled can have a significant impact on performance and the experience of legitimate users. See in detail what happens in such cases:

#### Interactive requests and JSON parsing
In an ideal scenario, a server with multiple CPU cores can handle concurrent requests efficiently. Each request can be processed in parallel, allowing the server to parse the JSON payloads simultaneously across different processes. However, if the server lacks sufficient cores to manage these concurrent requests effectively, several issues can arise.

#### Throttling of JSON Parsing
When a server is overloaded with concurrent requests and there are not enough CPU cores to handle those requests. Parsing JSON can become a bottleneck. The server may have trouble keeping up with the volume of incoming requests. This results in throttling. This means that processing JSON values ​​will be significantly slower. This is because users queue requests and process them sequentially rather than in parallel.

#### Impact on Response Times
As a result, the time required to parse each JSON payload increases. This latency affects not only requests with JSON payloads, but also requests from legitimate users. If the server is busy processing the payload It may take longer to respond to other users. This results in increased latency and poor user performance. Sometimes, when the server is overloaded, The server may abandon requests from legitimate users. This results in failed transactions or lack of service availability.

#### RAM Usage Considerations
In addition to CPU limitations, interactive use of JSON values ​​also affects the server's RAM usage. Each of these requests requires shared memory.

### Conducting Experiments: Testing JSON Parsing Performance
In this chapter, we will experiment on a local computer to evaluate the performance of various libraries. For parsing JSON values, we will create a large JSON value using Python and then test different libraries. to see how well these libraries handle parsing.

#### Generating a Large Dummy JSON Payload
We will create a function to create a more user-friendly JSON structure. The following Python code defines two functions: `generate` and `generate_large`.

- `generate(k: int)`: This function creates a deep JSON structure where each key contains another JSON object, recursively. The depth of the nesting is determined by the parameter `k`.
- `generate_large(root_k: int, depth_k: int)`: This function generates a main JSON object with `root_k` keys, each containing a deeply nested JSON structure created by the generate function.

```python
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
```

#### Next Steps
Once we have the large JSON payload generated, we can proceed to test the parsing performance using different libraries. Common libraries to consider for this experiment include:

| Test Case                          | Size (MB) | `json.loads()` (s) | `ujson.loads()` (s) | `orjson.loads()` (s) | `simplejson.loads()` (s) |
|------------------------------------|-----------|---------------------|----------------------|-----------------------|---------------------------|
| Root keys 5000, depth 100         | 2.95      | 0.207217            | 0.190318             | 0.110517              | 0.212702                  |
| Root keys 5000, depth 500         | 14.39     | 1.305549            | 1.271735             | 0.545227              | 1.075610                  |
| Root keys 5000, depth 1000        | 28.70     | 2.059699            | 2.022422             | 1.050982              | 2.094231                  |
| Root keys 5000, depth 2000        | 57.31     | 4.413788            | Crashed              | Crashed               | 4.461842                  |
| Root keys 10000, depth 100        | 5.90      | 0.424457            | 0.401273             | 0.226453              | 0.431495                  |
| Root keys 10000, depth 500        | 28.79     | 2.237729            | 2.150449             | 1.041351              | 2.374964                  |
| Root keys 10000, depth 1000       | 57.40     | 4.680663            | 4.597174             | 2.171437              | 4.767709                  |
| Root keys 10000, depth 2000       | 114.62    | 10.570827           | Crashed              | Crashed               | 10.409506                 |
| Root keys 20000, depth 500        | 57.59     | 5.787016            | 5.127688             | 2.535750              | 6.022697                  |
| Root keys 30000, depth 500        | 86.39     | 10.099687           | 8.137667             | 3.441961              | 8.587251                  |
| Root keys 40000, depth 500        | 115.19    | 11.379025           | 10.988368            | 4.867329              | 12.593404                 |
| Root keys 50000, depth 500        | 143.99    | 14.866508           | 14.947576            | 6.052979              | 15.279562                 |


### Sending Large JSON to API

In this experiment, I will send a JSON payload to `httpbin.org/post` in a single request to measure the response time, which will be close to the JSON parsing time. Below is a summary of the results:

| Test Case                          | Size (MB) | Time to Send (s) | Response Code | Response Time (s) |
|------------------------------------|-----------|-------------------|----------------|--------------------|
| Root keys 500, depth 100          | 0.29      | 0.374103          | 200 (OK)       | 3.084404           |
| Root keys 1000, depth 100         | 0.59      | 1.891199          | 200 (OK)       | 7.827239           |
| Root keys 5000, depth 100         | 2.95      | 8.025489          | 200 (OK)       | 24.291202          |
| Root keys 5000, depth 200         | 5.81      | 14.397732         | 502 (Bad Gateway) | 32.784367         |

### Explanation of the Table

- **Test Case**: Describes the configuration of the JSON payload, including the number of root keys and the depth of each key.
- **Size (MB)**: The size of the generated JSON payload in megabytes.
- **Time to Send (s)**: The time taken to send the JSON payload to the API, measured in seconds.
- **Response Code**: The HTTP response code returned by the API, indicating the result of the request.
- **Response Time (s)**: The time taken by the API to respond to the request, measured in seconds.

This table provides a clear overview of the performance of sending large JSON payloads to an API, highlighting the time taken for both sending the request and receiving the response, as well as the success or failure of each request.

### Summary
The results of this experiment indicate that the server struggled to handle large JSON payloads, particularly when sending requests to httpbin.org. The limitations observed can be attributed to the fact that it is one of the cheapest server options available on Amazon Web Services, which may not be equipped to efficiently process large amounts of data.

In the future, I will conduct a Denial of Service (DoS) attack on my own web application to further illustrate the impact of large JSON payloads and to provide a clearer understanding of how such attacks can affect server performance.