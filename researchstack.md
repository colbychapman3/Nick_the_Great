# Research Stack: Nick the Great Unified Agent

This document details the technical stack for the Nick the Great unified agent, compiled from research using the Context7 tool. It includes relevant documentation snippets, installation commands, and key concepts for each technology, adhering strictly to the information found within Context7.

## Node.js/Express (Backend API, gRPC Client)

*   **Context7 ID:** `/expressjs/express`
*   **Description:** Fast, unopinionated, minimalist web framework for node.
*   **Installation:**
    ```sh
    $ npm install express
    ```
*   **Basic Usage (Initializing Server):**
    ```javascript
    import express from 'express'

    const app = express()

    app.get('/', (req, res) => {
      res.send('Hello World')
    })

    app.listen(3000)
    ```
*   **Key Concepts:**
    *   `app.get('/', ...)`: Defining GET routes.
    *   `res.send()`: Sending responses.
    *   `app.listen()`: Starting the server.
    *   `res.send(bool)`: Support for JSON boolean responses.
    *   `res.send()`: Default string charset set to utf8.
    *   `res.contentType()`: Supported literal types like '.json'.
    *   `res.locals(obj)`: Bulk assignment of local variables.
    *   `res.render()`: Support for response body with status options.
    *   `res.header()`: Enhanced to send multiple Set-Cookie headers.
    *   `res.redirect()`: Requires absolute URLs.
    *   `res.sendfile()`: Responds with 403 on malicious paths.
    *   `res.render()`: Added charset support.
    *   `res.locals()`: Returns locals when called without arguments.
    *   `res.send(undefined)`: Responds with HTTP 204 No Content.
*   **Dependencies (from History.md snippets):** `express-session`, `finalhandler`, `method-override`, `morgan`, `qs`, `serve-index`, `serve-static`, `type-is`, `debug`, `ms`, `merge-descriptors`, `proxy-addr`, `ipaddr.js`, `send`, `etag`, `on-finished`, `connect`, `body-parser`, `compression`, `connect-timeout`, `cookie-parser`, `cookie-signature`, `csurf`, `errorhandler`, `http-errors`, `response-time`, `serve-favicon`, `vhost`, `fresh`, `media-typer`, `range-parser`, `vary`, `depd`, `forwarded`, `mime`, `multiparty`, `parseurl`, `on-headers`, `utils-merge`. (Note: Specific versions vary across history entries; refer to package.json for current project versions).

## React/Next.js (Frontend UI)

*   **Context7 ID:** `/reactjs/react.dev` (React), `/apollographql/apollo-client-integrations` (Next.js App Router Integration - most relevant Next.js snippet found)
*   **Description:** The React documentation website. Apollo Client support for the Next.js App Router.
*   **Installation (React - assumed via Next.js):** (No direct installation command for React itself provided in snippets, typically installed as a dependency).
*   **Installation (Next.js - assumed via project setup):** (No direct installation command for Next.js itself provided in snippets, typically part of project initialization).
*   **Basic Usage (Component Definition):**
    ```javascript
    export default function Profile() {
      return (
        <img
          src="https://i.imgur.com/MK3eW3Am.jpg"
          alt="Katherine Johnson"
        />
      )
    }
    ```
*   **Key Concepts:**
    *   **Components:** Building UI with reusable functions/classes.
    *   **JSX:** Embedding HTML-like syntax in JavaScript.
        ```jsx
        <h1>
          {user.name}
        </h1>
        ```
        ```jsx
        <img className="avatar" />
        ```
        ```jsx
        <>...</>
        ```
    *   **Props:** Passing data to components.
        ```javascript
        function Avatar({ person, size }) { /* ... */ }
        ```
    *   **State (`useState`):** Managing component-specific data.
        ```javascript
        import { useState } from 'react';
        const [state, setState] = useState(initialState)
        ```
        ```javascript
        function handleClick() {
          setCount(count + 1);
        }
        ```
        ```javascript
        setPlayer({
          ...player,
          score: player.score + 1,
        });
        ```
    *   **Effects (`useEffect`):** Synchronizing with external systems.
        ```javascript
        useEffect(() => {
          // Code here will run after *every* render
        });
        ```
        ```javascript
        useEffect(() => {
          const intervalId = setInterval(onTick, 1000);
          return () => clearInterval(intervalId);
        }, []); // Dependency array
        ```
    *   **Context (`useContext`):** Sharing data across the component tree.
        ```javascript
        import { createContext, useContext, useState } from 'react';
        const ThemeContext = createContext(null);
        // ...
        const theme = useContext(ThemeContext);
        ```
    *   **Conditional Rendering:** Using `&&` or ternary operator.
        ```javascript
        {isPacked && '✅'}
        ```
        ```javascript
        {isLoggedIn ? (
          <AdminPanel />
        ) : (
          <LoginForm />
        )}
        ```
    *   **Lists (`map`):** Rendering collections of data.
        ```javascript
        const listItems = products.map(product =>
          <li key={product.id}>
            {product.title}
          </li>
        );
        ```
    *   **Event Handling:** Responding to user interactions.
        ```javascript
        <button onClick={handleClick}>
          Click me!
        </button>
        ```
    *   **Custom Hooks:** Reusing stateful logic.
        ```javascript
        function useData(url) { /* ... */ }
        ```
    *   **Suspense:** Handling loading states for data fetching.
        ```jsx
        <Suspense fallback={<TalksLoading />}>
          <Talks confId={conf.id} />
        </Suspense>
        ```
    *   **`use client` directive:** Marking Client Components in Next.js App Router.
        ```javascript
        "use client"
        ```
    *   **TypeScript:** Defining prop types.
        ```typescript
        function MyButton({ title }: { title: string }) { /* ... */ }
        ```

## React Native (Mobile App UI)

*   **Context7 ID:** `/facebook/react-native-website`
*   **Description:** The React Native website and docs.
*   **Installation (Project Creation):**
    ```shell
    npx react-native@latest init AwesomeProject
    ```
*   **Key Concepts:**
    *   **Components:** Building UI with native components (`View`, `Text`, `Button`, `TextInput`, etc.).
    *   **JSX:** Embedding UI elements in JavaScript/TypeScript.
    *   **State (`useState`):** Managing component-specific data.
        ```typescript
        import React, {useState} from 'react';
        const [count, setCount] = useState(0);
        ```
    *   **Effects (`useEffect`):** Handling side effects.
        ```javascript
        useEffect(() => {
          const toggle = setInterval(() => { /* ... */ }, 1000);
          return () => clearInterval(toggle);
        });
        ```
    *   **Styling (`StyleSheet`):** Defining styles for components.
        ```javascript
        const styles = StyleSheet.create({
          container: {
            flex: 1,
            justifyContent: 'center',
            alignItems: 'center',
          },
        });
        ```
    *   **Layout (`Flexbox`):** Arranging components.
        ```javascript
        {
          flexDirection: 'row',
          justifyContent: 'center',
          alignItems: 'center',
        }
        ```
        Includes `rowGap`, `columnGap`, `gap`.
    *   **Event Handling:** Responding to user interactions (`onPress`, `onChangeText`).
        ```javascript
        <Button onPress={() => setCount(count + 1)} title="Click me!" />
        ```
    *   **Navigation:** Moving between screens (examples show basic navigation with parameters).
        ```typescript
        navigation.navigate('Profile', {name: 'Jane'})
        ```
    *   **API Modules:** Accessing native device capabilities (`Linking`, `Clipboard`, `ToastAndroid`, `PushNotificationIOS`, `useColorScheme`, `useWindowDimensions`, `InteractionManager`).
        ```javascript
        await Linking.openURL(url);
        ```
        ```javascript
        Clipboard.setString('hello world');
        ```
        ```javascript
        ToastAndroid.show('A pikachu appeared nearby !', ToastAndroid.SHORT);
        ```
        ```typescript
        import {useColorScheme} from 'react-native';
        ```
        ```typescript
        const {height, width} = useWindowDimensions();
        ```
        ```typescript
        InteractionManager.runAfterInteractions(() => onShown());
        ```
    *   **Performance Optimization:** `FlatList` with `getItemLayout`.
        ```typescript
        getItemLayout={(data, index) => (
          {length: ITEM_HEIGHT, offset: ITEM_HEIGHT * index, index}
        )}
        ```
    *   **TypeScript:** Defining prop types and using type safety.
        ```typescript
        type BlinkProps = {
          text: string;
        };
        const Blink = (props: BlinkProps) => { /* ... */ }
        ```
    *   **App Entry Point:** `AppRegistry.registerComponent`.
        ```typescript
        AppRegistry.registerComponent('Appname', () => App);
        ```
    *   **Native Integration:** Examples show initializing React Native in Android Activity (Kotlin).

## Python (Agent Core, Task Modules, CLI)

*   **Context7 ID:** `/python/cpython`
*   **Description:** The Python programming language.
*   **Installation (Virtual Environment):**
    *   MacOS/Linux:
        ```bash
        $ python3 -m venv .venv
        $ source .venv/bin/activate
        ```
    *   Windows:
        ```batchfile
        % .venv\Scripts\activate.bat
        ```
*   **Installation (Dependencies):**
    *   Using `pip`:
        ```bash
        $ pip install -r requirements.txt
        ```
    *   Using `uv`:
        ```bash
        uv sync
        ```
        ```bash
        source .venv/bin/activate
        ```
*   **Key Concepts:**
    *   **Basic Syntax:** Variables, loops, functions, classes.
    *   **Data Structures:** Lists, dictionaries, sets, tuples.
        ```python
        >>> cnt = Counter()
        >>> for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
        ...     cnt[word] += 1
        ...
        >>> cnt
        Counter({'blue': 3, 'red': 2, 'green': 1})
        ```
        ```python
        >>> for f in sorted(set(basket)):
        ...     print(f)
        ...
        apple
        banana
        orange
        pear
        ```
        ```python
        class LastUpdatedOrderedDict(OrderedDict):
            'Store items in the order the keys were last added'
            def __setitem__(self, key, value):
                super().__setitem__(key, value)
                self.move_to_end(key)
        ```
    *   **Functions:** Defining and calling functions.
        ```python
        def f(x):
            return x*x
        ```
    *   **Classes:** Object-oriented programming.
        ```python
        class C(B):
            def method(self, arg):
                super().method(arg)
        ```
        Subclassing immutable types requires overriding `__new__`.
    *   **Modules:** Importing and using code from other files.
        ```python
        import logging
        import mylib
        ```
    *   **Error Handling:** `try...except`.
    *   **File I/O:** Reading and writing files.
        ```python
        >>> with open('eggs.csv', newline='') as csvfile:
        ...     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        ...     for row in spamreader:
        ...         print(', '.join(row))
        ```
        ```python
        >>> with open('names.csv', newline='') as csvfile:
        ...     reader = csv.DictReader(csvfile)
        ...     for row in reader:
        ...         print(row['first_name'], row['last_name'])
        ```
        ```python
        >>> p = Path('my_text_file')
        >>> p.write_text('Text file contents')
        >>> p.read_text()
        ```
        ```python
        TemporaryFile(mode='w+b', buffering=-1, encoding=None, newline=None, suffix=None, prefix=None, dir=None, *, errors=None)
        ```
    *   **Networking:** Making HTTP requests (`urllib.request`), secure connections (`ssl`, `smtplib`).
        ```python
        import urllib.request
        local_filename, headers = urllib.request.urlretrieve('http://python.org/')
        ```
        ```python
        >>> conn = context.wrap_socket(socket.socket(socket.AF_INET),
        ...                            server_hostname="www.python.org")
        >>> conn.connect(("www.python.org", 443))
        ```
        ```python
        >>> import ssl, smtplib
        >>> smtp = smtplib.SMTP("mail.python.org", port=587)
        >>> context = ssl.create_default_context()
        >>> smtp.starttls(context=context)
        ```
    *   **Concurrency/Parallelism:** `asyncio`, `multiprocessing`.
        ```python
        import asyncio
        async def main():
            await test() # Awaiting a coroutine
        ```
        ```python
        async def wait_for(aw, timeout): # Waiting for awaitables with timeout
            """
            Wait for the *aw* :ref:`awaitable <asyncio-awaitables>`
            to complete with a timeout.
            ...
            """
        ```
        ```python
        async def worker(name, queue): # Asyncio Queue usage
            while True:
                sleep_for = await queue.get()
                await asyncio.sleep(sleep_for)
                queue.task_done()
        ```
        ```python
        get_nowait() # Get from queue without blocking
        ```
        ```python
        from multiprocessing import Pool # Using multiprocessing Pool
        import time

        def f(x):
            return x*x

        if __name__ == '__main__':
            with Pool(processes=4) as pool:
                result = pool.apply_async(f, (10,))
                print(result.get(timeout=1))
        ```
        ```python
        >>> with SharedMemoryManager() as smm: # SharedMemoryManager with context manager
        ...     sl = smm.ShareableList(range(2000))
        ...     # ... process with multiple processes ...
        ...     total_result = sum(sl)
        ```
    *   **Command Line Interfaces (`argparse`):** Parsing command-line arguments.
        ```python
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("echo") # Positional argument
        args = parser.parse_args()
        print(args.echo)
        ```
        ```python
        parser.add_argument('--foo', default=42) # Default value
        ```
        ```python
        parser.add_argument('--foo', nargs='?', const='c', default='d') # Nargs with question mark
        ```
        ```python
        parser.add_argument('filename') # Positional and optional arguments
        parser.add_argument('-c', '--count')
        parser.add_argument('-v', '--verbose', action='store_true')
        ```
        ```python
        parser = argparse.ArgumentParser(prog='PROG', prefix_chars='+/') # Custom prefix characters
        ```
        ```python
        parser = argparse.ArgumentParser(prog='PROG') # Mutually exclusive argument group
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--foo', action='store_true')
        group.add_argument('--bar', action='store_false')
        ```
        ```python
        parser.add_argument('bar', dest='bar') # Setting destination attribute name
        ```
        Handling wrong number of arguments results in an error and usage message.
    *   **Testing (`unittest`, `unittest.mock`):** Writing and running tests.
        ```python
        if __name__ == '__main__':
            unittest.main() # Using unittest.main
        ```
        ```python
        from unittest.mock import MagicMock # Basic MagicMock usage
        thing = ProductionClass()
        thing.method = MagicMock(return_value=3)
        thing.method(3, 4, 5, key='value')
        thing.method.assert_called_with(3, 4, 5, key='value')
        ```
        ```python
        mock = Mock(return_value=3) # Setting return values in Mock constructor
        mock()
        ```
        ```python
        mock = Mock(spec=3) # Using Mock objects with isinstance()
        isinstance(mock, int)
        ```
        ```python
        with self.assertWarns(SomeWarning): # Using assertWarns as a context manager
            do_something()
        ```
    *   **Regular Expressions (`re`):** Pattern matching.
        ```python
        "$" # Matching end of string
        ```
        ```python
        >>> m = re.match(r"(?P<first_name>\\w+) (?P<last_name>\\w+)", "Malcolm Reynolds") # Extracting named subgroups
        >>> m.groupdict()
        {'first_name': 'Malcolm', 'last_name': 'Reynolds'}
        ```
    *   **Logging (`logging`):** Recording application events.
        ```python
        import logging
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='myapp.log', level=logging.INFO) # Basic configuration
        logger.info('Started')
        ```
        ```python
        # Logging to multiple destinations with different formats
        import logging
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='/tmp/myapp.log',
                            filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        ```
        ```python
        import json # Structured Logging with JSON Serialization
        import logging

        class StructuredMessage:
            def __init__(self, message, /, **kwargs):
                self.message = message
                self.kwargs = kwargs

            def __str__(self):
                return '%s >>> %s' % (self.message, json.dumps(self.kwargs))

        _ = StructuredMessage
        logging.info(_('message 1', foo='bar', bar='baz', num=123, fnum=123.456))
        ```
        ```yaml
        # Defining Logging Object Connections with YAML
        formatters:
          brief: {}
          precise: {}
        handlers:
          h1:
           formatter: brief
          h2:
           formatter: precise
        loggers:
          foo.bar.baz:
            handlers: [h1, h2]
        ```
        ```python
        def basicConfig(**kwargs): # Basic Configuration function signature
            pass
        ```
    *   **String Formatting:** f-strings.
        ```python
        >>> who = 'nobody'
        >>> nationality = 'Spanish'
        >>> f'{who.title()} expects the {nationality} Inquisition!'
        'Nobody expects the Spanish Inquisition!'
        ```
    *   **String Manipulation:** `split()`.
        ```python
        >>> '1,2,3'.split(',')
        ['1', '2', '3']
        ```
    *   **Encoding:** Specifying source code encoding.
        ```python
        #!/usr/bin/env python
        # -*- coding: latin-1 -*-
        ```
    *   **Data Conversion:** Bytes to Integer.
        ```python
        def from_bytes(bytes, byteorder='big', signed=False):
            pass
        ```
    *   **Mathematical Functions:** `math.sqrt()`.
        ```python
        .. function:: sqrt(x)

           Return the square root of *x*.
        ```
    *   **Itertools:** `roundrobin()`.
        ```python
        >>> list(roundrobin('abc', 'd', 'ef'))
        ['a', 'd', 'e', 'b', 'f', 'c']
        ```
    *   **Subprocess:** `subprocess.check_output()`.
        ```python
        >>> subprocess.check_output(
        ...     "ls non_existent_file; exit 0",
        ...     stderr=subprocess.STDOUT,
        ...     shell=True)
        'ls: non_existent_file: No such file or directory\n'
        ```
    *   **Email:** Creating internationalized headers.
        ```python
        from email.message import Message
        from email.header import Header
        msg = Message()
        h = Header('p\xf6stal', 'iso-8859-1')
        msg['Subject'] = h
        ```
    *   **Decimal:** Precision and rounding.
        ```python
        >>> getcontext().prec = 6
        >>> Decimal('3.1415926535') + Decimal('2.7182818285')
        Decimal('5.85987')
        ```
    *   **Pathlib:** `Path.read_text()`, `Path.glob()`.
        ```python
        >>> sorted(Path('.').glob('*.py'))
        [PosixPath('pathlib.py'), PosixPath('setup.py'), PosixPath('test_pathlib.py')]
        ```
    *   **SQLite:** Connecting, creating tables, using placeholders.
        ```python
        import sqlite3
        con = sqlite3.connect("tutorial.db")
        ```
        ```python
        cur.execute("CREATE TABLE movie(title, year, score)")
        ```
        ```python
        cur.executemany("INSERT INTO lang VALUES(:name, :year)", data)
        cur.execute("SELECT * FROM lang WHERE first_appeared = ?", params)
        ```

## gRPC (Inter-service Communication)

*   **Context7 ID:** `/grpc/grpc.io`
*   **Description:** Repository for the gRPC website and documentation.
*   **Installation (Python):**
    ```sh
    pip install grpcio-tools
    ```
*   **Installation (Node.js):** (Assumed via npm, no specific command snippet provided).
*   **Key Concepts:**
    *   **Protocol Buffers (`.proto`):** Defining services and messages.
        ```protobuf
        service HelloService {
          rpc SayHello (HelloRequest) returns (HelloResponse);
        }

        message HelloRequest {
          string greeting = 1;
        }

        message HelloResponse {
          string reply = 1;
        }
        ```
        Includes definitions for simple, server-streaming, client-streaming, and bidirectional streaming RPCs.
    *   **RPC Types:**
        *   **Unary:** Single request, single response (`GetFeature`).
            ```protobuf
            // Obtains the feature at a given position.
            rpc GetFeature(Point) returns (Feature) {}
            ```
        *   **Server Streaming:** Single request, stream of responses (`ListFeatures`).
            ```protobuf
            rpc ListFeatures(Rectangle) returns (stream Feature) {}
            ```
        *   **Client Streaming:** Stream of requests, single response (`RecordRoute`).
            ```protobuf
            rpc RecordRoute(stream Point) returns (RouteSummary) {}
            ```
        *   **Bidirectional Streaming:** Stream of requests, stream of responses (`RouteChat`).
            ```protobuf
            rpc RouteChat(stream RouteNote) returns (stream RouteNote) {}
            ```
    *   **Code Generation:** Using `protoc` to generate client and server code from `.proto` files.
        ```sh
        protoc --go_out=. --go_opt=paths=source_relative \
            --go-grpc_out=. --go-grpc_opt=paths=source_relative \
            helloworld/helloworld.proto
        ```
    *   **Server Implementation:** Implementing the defined service methods.
        *   Python:
            ```python
            def GetFeature(self, request, context):
                feature = get_feature(self.db, request)
                if feature is None:
                    return route_guide_pb2.Feature(name="", location=request)
                else:
                    return feature
            ```
            ```python
            def ListFeatures(self, request, context):
                # ... yield features ...
                pass
            ```
            ```python
            def RouteChat(self, request_iterator, context):
                # ... process stream and yield notes ...
                pass
            ```
        *   Node.js:
            ```javascript
            function getServer() {
              var server = new grpc.Server();
              server.addService(routeguide.RouteGuide.service, { /* ... */ });
              return server;
            }
            var routeServer = getServer();
            routeServer.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => {
              routeServer.start();
            });
            ```
            ```javascript
            function getFeature(call, callback) {
              callback(null, checkFeature(call.request));
            }
            ```
        *   Java:
            ```java
            private class GreeterImpl extends GreeterGrpc.GreeterImplBase {
              @Override
              public void sayHello(HelloRequest req, StreamObserver<HelloReply> responseObserver) { /* ... */ }
              @Override
              public void sayHelloAgain(HelloRequest req, StreamObserver<HelloReply> responseObserver) { /* ... */ }
            }
            ```
            ```java
            @Override
            public StreamObserver<Point> recordRoute(final StreamObserver<RouteSummary> responseObserver) { /* ... */ }
            ```
            ```java
            @Override
            public StreamObserver<RouteNote> routeChat(final StreamObserver<RouteNote> responseObserver) { /* ... */ }
            ```
        *   Kotlin:
            ```kotlin
            private class HelloWorldService : GreeterGrpcKt.GreeterCoroutineImplBase() {
              override suspend fun sayHello(request: HelloRequest) = helloReply { /* ... */ }
              override suspend fun sayHelloAgain(request: HelloRequest) = helloReply { /* ... */ }
            }
            ```
            ```kotlin
            override suspend fun recordRoute(requests: Flow<Point>): RouteSummary { /* ... */ }
            ```
            ```kotlin
            override fun routeChat(requests: Flow<RouteNote>): Flow<RouteNote> = flow { /* ... */ }
            ```
        *   C++:
            ```cpp
            Status GetFeature(ServerContext* context, const Point* point,
                              Feature* feature) override { /* ... */ }
            ```
            ```cpp
            class GreeterServiceImpl final : public Greeter::Service { /* ... */ }
            ```
            Asynchronous server implementation involves a completion queue and `HandleRpcs` loop.
    *   **Client Implementation:** Creating stubs and making RPC calls.
        *   Python:
            ```python
            channel = grpc.insecure_channel('localhost:50051')
            stub = route_guide_pb2_grpc.RouteGuideStub(channel)
            ```
        *   Node.js:
            ```javascript
            var PROTO_PATH = __dirname + '/../../protos/route_guide.proto';
            var grpc = require('@grpc/grpc-js');
            var protoLoader = require('@grpc/proto-loader');
            var packageDefinition = protoLoader.loadSync(PROTO_PATH, { /* ... */ });
            var protoDescriptor = grpc.loadPackageDefinition(packageDefinition);
            var routeguide = protoDescriptor.routeguide;
            // ... create stub ...
            stub.getFeature(point, function(err, feature) { /* ... */ });
            ```
        *   Java:
            ```java
            public RouteGuideClient(ManagedChannelBuilder<?> channelBuilder) {
              channel = channelBuilder.build();
              blockingStub = RouteGuideGrpc.newBlockingStub(channel);
              asyncStub = RouteGuideGrpc.newStub(channel);
            }
            ```
            ```java
            Iterator<Feature> features;
            try {
              features = blockingStub.listFeatures(request);
            } catch (StatusRuntimeException e) { /* ... */ }
            ```
            ```java
            // Client-side streaming with async stub
            StreamObserver<Point> requestObserver = asyncStub.recordRoute(responseObserver);
            ```
        *   Kotlin:
            ```kotlin
            val request = point(latitude, longitude)
            val feature = stub.getFeature(request)
            ```
        *   C++:
            ```cpp
            auto channel = grpc::CreateChannel(server_name, channel_creds);
            std::unique_ptr<Greeter::Stub> stub(Greeter::NewStub(channel));
            grpc::Status s = stub->sayHello(&context, *request, response);
            ```
        *   Objective-C:
            ```objectivec
            [[service getFeatureWithMessage:point responseHandler:handler callOptions:nil] start];
            ```
        *   gRPC-Web (JavaScript):
            ```javascript
            const client = new ExampleServiceClient('https://api.example.com');
            client.getExampleData(request, {}, (err, response) => { /* ... */ });
            ```
    *   **Authentication:** SSL/TLS, custom auth headers.
        ```cpp
        auto channel_creds = grpc::SslCredentials(grpc::SslCredentialsOptions());
        auto channel = grpc::CreateChannel(server_name, channel_creds);
        ```
        ```javascript
        const channelCreds = grpc.credentials.createSsl(rootCert);
        const metaCallback = (_params, callback) => {
            const meta = new grpc.Metadata();
            meta.add('custom-auth-header', 'token');
            callback(null, meta);
        }
        const callCreds = grpc.credentials.createFromMetadataGenerator(metaCallback);
        const combCreds = grpc.credentials.combineChannelCredentials(channelCreds, callCreds);
        const stub = new helloworld.Greeter('myservice.example.com', combCreds);
        ```
    *   **Interceptors:** Modifying requests/responses (gRPC-Web example).
        ```javascript
        /** @override */
        SimpleUnaryInterceptor.prototype.intercept = function(request, invoker) { /* ... */ };
        ```

## MongoDB (Data Persistence)

*   **Context7 ID:** `/mongodb/docs`
*   **Description:** The MongoDB Documentation Project Source.
*   **Installation:** (Not covered in snippets, assumed to be set up).
*   **Connection:**
    *   Shell:
        ```bash
        mongosh "mongodb://localhost" --apiVersion 1 --username myDatabaseUser
        ```
        ```bash
        mongosh "mongodb+srv://mongodb0.example.com/?authSource=admin&replicaSet=myRepl" --apiVersion 1 --username myDatabaseUser
        ```
        ```javascript
        db = connect("localhost:27017/myDatabase")
        ```
        ```javascript
        cluster = Mongo("mongodb://mymongo.example.net:27017/?replicaSet=myMongoCluster")
        ```
    *   Standard URI formats for various drivers:
        ```bash
        mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?authSource=admin&replicaSet=myRepl
        ```
        ```bash
        mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@cluster0.example.mongodb.net/?retryWrites=true&w=majority
        ```
*   **Key Concepts:**
    *   **Documents:** Basic data structure (BSON).
        ```javascript
        {
           field1: value1,
           field2: value2,
           ...
        }
        ```
        Includes embedded documents with dot notation access.
    *   **Collections:** Grouping documents.
    *   **Databases:** Grouping collections.
        ```javascript
        use myDB
        ```
        ```javascript
        myDB = cluster.getDB("myDB");
        ```
    *   **CRUD Operations:**
        *   **Insert:** `insertOne()`, `insertMany()`, `insert()`.
            ```javascript
            db.inventory.insertOne(
               { item: "canvas", qty: 100, tags: ["cotton"], size: { h: 28, w: 35.5, uom: "cm" } }
            )
            ```
            ```javascript
            db.inventory.insertMany([ /* ... */ ])
            ```
            `insert()` automatically adds `_id` if not specified.
        *   **Read (Find):** `find()`.
            ```javascript
            db.inventory.find( {} ) // All documents
            ```
            ```javascript
            db.inventory.find( { quantity: { $lt: 20 } } ) // With query operator
            ```
            ```javascript
            db.bios.find( { contribs: "UNIX" } ) // Array querying
            ```
            Includes `$in`, `$all`, `$size` operators for arrays.
        *   **Update:** `updateOne()`, `updateMany()`, `replaceOne()`, `findAndModify()`, `findOneAndUpdate()`, `findOneAndReplace()`, `bulkWrite()`.
            ```javascript
            db.products.updateOne(
               { _id: 100 },
               { $set: { "details.make": "Kustom Kidz" } } // Updating embedded field
            )
            ```
            ```javascript
            db.products.updateOne(
               { _id: 100 },
               { $set: { /* multiple fields */ } }
            )
            ```
            ```javascript
            db.products.updateOne(
               { sku: "abc123" },
               { $inc: { quantity: -2, "metrics.orders": 1 } } // $inc operator
            )
            ```
            `updateMany` example with `$set` and `$currentDate`.
            `bulkWrite` for multiple operations with write concern.
        *   **Delete:** `deleteOne()`, `deleteMany()`.
            ```javascript
            db.collection.deleteOne( { status: "D" } )
            ```
    *   **Aggregation Framework:** `aggregate()`.
        ```javascript
        db.runCommand(
           {
             aggregate: "<collection>" || 1,
             pipeline: [ <stage>, <...> ],
             /* ... options ... */
           }
        )
        ```
        Includes stages like `$match`, `$group` (`$sum`), `$sort`, `$limit`, `$project`, `$unwind`, `$lookup`, `$setWindowFields`, `$search` (within `$lookup`).
        ```javascript
        { $sort : { count : -1 } } // Sorting
        ```
        ```javascript
        { $unwind: <field path> } // Unwinding arrays
        ```
        ```javascript
        { $project: { /* include/exclude fields */ } } // Projecting fields
        ```
        Comparison to SQL aggregation.
    *   **Indexing:** `createIndex()`.
        ```javascript
        db.<collection>.createIndex( { <arrayField>: <sortOrder> } ) // Single field
        ```
        ```javascript
        db.<collection>.createIndex( { <field1>: <sortOrder>, <field2>: <sortOrder>, ... } ) // Compound index
        ```
    *   **Transactions:** `startSession()`, `startTransaction()`, `commitTransaction()`, `abortTransaction()`.
        ```javascript
        session = db.getMongo().startSession( { readPreference: { mode: "primary" } } );
        session.startTransaction( { readConcern: { level: "snapshot" }, writeConcern: { w: "majority" } } );
        // ... operations ...
        commitWithRetry(session); // Example retry logic
        session.endSession();
        ```
        Includes `runTransactionWithRetry` function example.
    *   **Explain:** `explain()`, `cursor.explain()`.
        ```javascript
        db.runCommand(
           {
             explain: <command>,
             verbosity: <string>,
             comment: <any>
           }
        )
        ```
    *   **Administration:** `listCollections()`, `shutdown()`.
        ```javascript
        db.adminCommand(
           {
              listCollections: 1,
              nameOnly: true,
              filter: { type: { $ne: "view" } }
           }
        )
        ```
        ```javascript
        db.adminCommand( { shutdown: 1 } )
        ```

## AbacusAI / ACI (AI Integration)

*   **Context7 ID:** `/aipotheosis-labs/aci` (Most relevant result for "AbacusAI" research)
*   **Description:** ACI.dev is the open source platform that connects your AI agents to 600+ tool integrations with multi-tenant auth, granular permissions, and access through direct function calling or a unified MCP server.
*   **Installation:**
    *   Clone repository:
        ```bash
        git clone https://github.com/aipotheosis-labs/aci.git
        ```
    *   Navigate to backend:
        ```bash
        cd aci/backend
        ```
    *   Install backend dependencies (`uv`):
        ```bash
        uv sync
        ```
        ```bash
        source .venv/bin/activate
        ```
    *   Install backend dependencies (`pip`):
        ```bash
        $ pip install -r requirements.txt
        ```
    *   Activate virtual environment (Windows):
        ```batchfile
        % .venv\Scripts\activate.bat
        ```
    *   Activate virtual environment (MacOS/Linux):
        ```bash
        $ source .venv/bin/activate
        ```
    *   Copy environment file:
        ```bash
        cp .env.example .env
        ```
    *   Install backend pre-commit hooks:
        ```bash
        pre-commit install
        ```
    *   Install frontend dependencies (`npm`):
        ```Bash
        npm install --legacy-peer-deps
        ```
    *   Install frontend pre-commit hooks:
        ```Bash
        pre-commit install
        ```
*   **Local Development:**
    *   Start backend services (Docker Compose):
        ```bash
        docker compose up --build
        ```
    *   Start frontend dev server:
        ```Bash
        npm run dev
        ```
    *   Configure frontend environment variables (`.env`):
        ```Shell
        NEXT_PUBLIC_API_URL=http://localhost:8000
        NEXT_PUBLIC_DEV_PORTAL_URL=http://localhost:3000
        NEXT_PUBLIC_ENVIRONMENT=local
        NEXT_PUBLIC_AUTH_URL=https://8367878.propelauthtest.com
        ```
    *   Expose local server with ngrok:
        ```bash
        ngrok http http://localhost:8000
        ```
*   **Database Management (Backend):**
    *   Apply migrations:
        ```bash
        docker compose exec runner alembic upgrade head
        ```
    *   Generate migration:
        ```bash
        docker compose exec runner alembic revision --autogenerate -m "description of changes"
        ```
    *   Check migrations:
        ```bash
        docker compose exec runner alembic check
        ```
    *   Revert migration:
        ```bash
        docker compose exec runner alembic downgrade -1
        ```
    *   Seed database:
        ```bash
        docker compose exec runner ./scripts/seed_db.sh
        ```
*   **Testing (Backend):**
    *   Run tests:
        ```bash
        docker compose exec runner pytest
        ```
*   **Testing (Frontend):**
    *   Run unit tests (watch mode):
        ```Bash
        npm run test
        ```
    *   Generate coverage report:
        ```Bash
        npm run test:coverage
        ```
*   **Code Quality:**
    *   Run linters (frontend):
        ```Bash
        npm run lint
        ```
    *   Format code (frontend):
        ```Bash
        npm run format
        ```
    *   VS Code settings for Python with Ruff:
        ```json
        {
            "[python]": {
              "editor.formatOnSave": true,
              "editor.defaultFormatter": "charliermarsh.ruff",
              "editor.codeActionsOnSave": {
                "source.organizeImports.ruff": "always"
              }
            }
        }
        ```
*   **Admin CLI:**
    *   Show help:
        ```bash
        docker compose exec runner python -m aci.cli --help
        ```
    *   Available commands: `create-agent`, `create-project`, `create-random-api-key`, `delete-app`, `fuzzy-test-function-execution`, `get-app`, `rename-app`, `update-agent`, `upsert-app`, `upsert-functions`.
    *   Create random API key:
        ```bash
        docker compose exec runner python -m aci.cli create-random-api-key --visibility-access public
        ```
    *   Create app:
        ```bash
        docker compose exec runner python -m aci.cli create-app --app-file ./apps/brave_search/app.json --secrets-file ./apps/brave_search/.app.secrets.json
        ```
*   **Deployment (AWS CDK):**
    *   Synthesize CloudFormation template:
        ```Bash
        $ cdk synth
        ```
*   **Frontend Directory Structure:**
    ```
    src
    ├── app (Next.js App Router folder)
    ├── components
    │   ├── ...
    │   └── ui
    ├── hooks
    │   └── use-mobile.tsx
    └── lib
    │   ├── api
    │   ├── types
    │   └── utils.ts
    └── __test__
        ├── apps
        ├── linked-accounts
        ├── project-setting
        └── ...
    ```
*   **Production Environment Variables (Vercel Example):**
    ```Shell
    NEXT_PUBLIC_API_URL=https://api.aci.dev
    NEXT_PUBLIC_DEV_PORTAL_URL=https://platform.aci.dev
    NEXT_PUBLIC_ENVIRONMENT=production
    NEXT_PUBLIC_AUTH_URL=<actual_production_propelauth_endpoint>
    ```

This research provides the foundational technical details, commands, and concepts necessary for implementing the unified agent system in Phase 4, strictly based on the information available through Context7.
