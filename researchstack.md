# Research Stack: Nick the Great

This document details the core technologies used in the Nick the Great project, including relevant code snippets, version information (where available from documentation), and key concepts based on research using Context7 and project file analysis.

## 1. Next.js (`/vercel/next.js`)

**Description:** The React Framework.

**Key Concepts & Features:**
- **Pages Router & App Router:** Supports both routing paradigms.
- **Data Fetching:** `getStaticProps`, `getServerSideProps`, `fetch` in Server Components.
- **Client Components:** Use `'use client'` directive. Hooks like `useRouter`, `usePathname`, `useSearchParams`.
- **API Routes:** Building backend endpoints within the Next.js application.
- **Middleware:** Intercepting requests for logic like authentication or redirects.
- **Static File Serving:** Serving assets from the `public` directory.
- **Metadata API:** Defining `robots.txt`, `sitemap.xml`, etc.
- **Third-Party Libraries:** Integration with external services and libraries.

**Code Snippets:**

*   **`getStaticProps` (TypeScript):** Fetch data at build time.
    ```typescript
    import type { InferGetStaticPropsType, GetStaticProps } from 'next'

    type Repo = {
      name: string
      stargazers_count: number
    }

    export const getStaticProps = (async (context) => {
      const res = await fetch('https://api.github.com/repos/vercel/next.js')
      const repo = await res.json()
      return { props: { repo } }
    }) satisfies GetStaticProps<{
      repo: Repo
    }>

    export default function Page({
      repo,
    }: InferGetStaticPropsType<typeof getStaticProps>) {
      return repo.stargazers_count
    }
    ```
*   **`getServerSideProps` (JavaScript):** Fetch data on each request.
    ```javascript
    export async function getServerSideProps() {
      // Fetch data from external API
      const res = await fetch('https://api.github.com/repos/vercel/next.js')
      const repo = await res.json()
      // Pass data to the page via props
      return { props: { repo } }
    }

    export default function Page({ repo }) {
      return (
        <main>
          <p>{repo.stargazers_count}</p>
        </main>
      )
    }
    ```
*   **Client Component Search Param Update (JavaScript):**
    ```jsx
    'use client'

    export default function ExampleClientComponent() {
      const router = useRouter()
      const pathname = usePathname()
      const searchParams = useSearchParams()

      // Get a new searchParams string by merging the current
      // searchParams with a provided key/value pair
      const createQueryString = useCallback(
        (name, value) => {
          const params = new URLSearchParams(searchParams)
          params.set(name, value)

          return params.toString()
        },
        [searchParams]
      )

      return (
        <>
          <p>Sort By</p>

          {/* using useRouter */}
          <button
            onClick={() => {
              // <pathname>?sort=asc
              router.push(pathname + '?' + createQueryString('sort', 'asc'))
            }}
          >
            ASC
          </button>

          {/* using <Link> */}
          <Link
            href={
              // <pathname>?sort=desc
              pathname + '?' + createQueryString('sort', 'desc')
            }
          >
            DESC
          </Link>
        </>
      )
    }
    ```
*   **Basic Middleware (TypeScript):**
    ```typescript
    import { NextResponse, NextRequest } from 'next/server'

    // This function can be marked `async` if using `await` inside
    export function middleware(request: NextRequest) {
      return NextResponse.redirect(new URL('/home', request.url))
    }

    export const config = {
      matcher: '/about/:path*',
    }
    ```

**Version:** Latest stable or canary recommended for new features (e.g., `next@latest` or `next@canary`). The project's `package.json` should be consulted for the specific version used.

## 2. TypeScript (`/microsoft/typescript`)

**Description:** A superset of JavaScript that compiles to clean JavaScript output.

**Key Concepts & Features:**
- **Static Typing:** Defining types for variables, function parameters, return values, objects, etc.
- **Interfaces:** Defining contracts for object shapes.
- **Classes:** Object-oriented programming features.
- **Generics:** Creating reusable components that work with various types.
- **Enums:** Defining sets of named constants.
- **Modules:** Organizing code into reusable units (ES Modules syntax).
- **Type Inference:** Automatic deduction of types by the compiler.
- **Compiler Options (`tsconfig.json`):** Configuring the TypeScript compiler behavior.

**Code Snippets:**

*   **Basic Interface and Class:**
    ```typescript
    interface I {
        id: number;
    }

    class C implements I {
        id: number;
    }
    ```
*   **Generic Function:**
    ```typescript
    function identity<T>(arg: T): T {
        return arg;
    }
    ```
*   **Enum Definition:**
    ```typescript
    enum Color {
        Red,
        Green,
        Blue,
    }
    let c: Color = Color.Green;
    ```
*   **Type Alias:**
    ```typescript
    type Point = {
        x: number;
        y: number;
    };

    function printCoord(pt: Point) {
        console.log("The coordinate's x value is " + pt.x);
        console.log("The coordinate's y value is " + pt.y);
    }

    printCoord({ x: 100, y: 100 });
    ```

**Version:** Check `package.json` for the specific version used. Install with `npm install -D typescript`.

## 3. Python (`/python/cpython`)

**Description:** The Python programming language.

**Key Concepts & Features:**
- **Core Data Types:** Numbers (int, float), Strings, Lists, Tuples, Dictionaries, Sets, Booleans.
- **Control Flow:** `if/elif/else`, `for`, `while`, `break`, `continue`.
- **Functions:** Defining functions with `def`, arguments, return values, lambda functions.
- **Classes:** Object-oriented programming with classes, inheritance, methods.
- **Modules & Packages:** Organizing code using modules (`.py` files) and packages (directories with `__init__.py`). `import` statement.
- **Standard Library:** Rich set of built-in modules.
    - `os`: Interacting with the operating system (files, directories, processes).
    - `sys`: System-specific parameters and functions (command-line args, paths).
    - `json`: Working with JSON data.
    - `datetime`: Date and time manipulation.
    - `requests` (third-party, but common): Making HTTP requests.
- **Error Handling:** `try...except...finally` blocks.
- **Virtual Environments:** Isolating project dependencies (`venv`).

**Code Snippets:**

*   **Reading Command Line Arguments:**
    ```python
    import sys
    print(sys.argv)
    ```
*   **Working with Files (os module):**
    ```python
    import os
    # Get current working directory
    cwd = os.getcwd()
    # Change directory
    os.chdir('/path/to/dir')
    # List directory contents
    contents = os.listdir('.')
    ```
*   **Working with JSON:**
    ```python
    import json
    # Parse JSON string
    data = json.loads('{"name": "John", "age": 30}')
    # Convert Python dict to JSON string
    json_string = json.dumps({"city": "New York"})
    ```
*   **Working with Dates (datetime module):**
    ```python
    from datetime import date, datetime
    today = date.today()
    now = datetime.now()
    print(today.strftime("%Y-%m-%d"))
    print(now.isoformat())
    ```

**Version:** Check system installation or virtual environment (`python --version`).

## 4. gRPC (`/grpc/grpc.io`)

**Description:** A high-performance, open source universal RPC framework. Uses Protocol Buffers by default.

**Key Concepts & Features:**
- **Protocol Buffers (`.proto`):** Language-neutral mechanism for serializing structured data. Define services and message types.
- **Service Definition:** Defining RPC methods within a service block in `.proto`.
- **RPC Types:**
    - Unary: Client sends single request, server sends single response.
    - Server Streaming: Client sends single request, server sends stream of responses.
    - Client Streaming: Client sends stream of requests, server sends single response.
    - Bidirectional Streaming: Client and server send streams of requests/responses independently.
- **Code Generation:** Using `grpc_tools.protoc` (Python) or other language-specific tools to generate client stubs and server base classes from `.proto` files.
- **Channels:** Representing a connection to a gRPC server.
- **Stubs:** Client-side representation of the service used to make RPC calls.
- **Servers:** Implementing the service interface and running the gRPC server.
- **Async Support:** Many implementations offer asynchronous APIs (e.g., Python's `grpc.aio`).

**Code Snippets (Python Focus):**

*   **`.proto` Service Definition:**
    ```protobuf
    syntax = "proto3";

    service Greeter {
      rpc SayHello (HelloRequest) returns (HelloReply) {}
    }

    message HelloRequest {
      string name = 1;
    }

    message HelloReply {
      string message = 1;
    }
    ```
*   **Generating Python Code:**
    ```sh
    python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. your_service.proto
    ```
*   **Creating Client Stub (Python):**
    ```python
    import grpc
    import your_service_pb2
    import your_service_pb2_grpc

    channel = grpc.insecure_channel('localhost:50051')
    stub = your_service_pb2_grpc.GreeterStub(channel)
    ```
*   **Making Unary Call (Python):**
    ```python
    request = your_service_pb2.HelloRequest(name='World')
    response = stub.SayHello(request)
    print("Greeter client received: " + response.message)
    ```
*   **Implementing Server (Python):**
    ```python
    import grpc
    from concurrent import futures
    import your_service_pb2
    import your_service_pb2_grpc

    class Greeter(your_service_pb2_grpc.GreeterServicer):
        def SayHello(self, request, context):
            return your_service_pb2.HelloReply(message=f"Hello, {request.name}!")

    def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        your_service_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
        server.add_insecure_port("[::]:50051")
        server.start()
        server.wait_for_termination()

    if __name__ == '__main__':
        serve()
    ```

**Version:** Check installed packages (`pip show grpcio grpcio-tools`).

## 5. MongoDB (`/mongodb/docs`, `/mongodb/docs-pymongo`)

**Description:** A NoSQL document database. Stores data in flexible, JSON-like documents (BSON).

**Key Concepts & Features:**
- **Documents:** BSON objects, analogous to rows in relational databases.
- **Collections:** Groupings of documents, analogous to tables.
- **Databases:** Containers for collections.
- **CRUD Operations:** Create (insert), Read (find), Update, Delete.
- **Query Language:** Rich query capabilities using query documents. Operators like `$eq`, `$gt`, `$lt`, `$in`, `$regex`, logical operators (`$and`, `$or`, `$not`).
- **Aggregation Framework:** Processing data records and returning computed results. Stages like `$match`, `$group`, `$project`, `$sort`, `$limit`, `$unwind`, `$lookup`.
- **Indexing:** Improving query performance. Single field, compound, multikey, text, geospatial indexes.
- **Drivers:** Official drivers for various languages (e.g., PyMongo for synchronous Python, Motor for asynchronous Python).
- **Transactions:** ACID-compliant multi-document transactions.

**Code Snippets (PyMongo Focus):**

*   **Connecting (PyMongo):**
    ```python
    from pymongo import MongoClient
    # Replace with your connection string
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase'] # Select database
    collection = db['mycollection'] # Select collection
    ```
*   **Inserting a Document (PyMongo):**
    ```python
    result = collection.insert_one({"name": "Alice", "age": 30, "city": "New York"})
    print(f"Inserted document with id: {result.inserted_id}")
    ```
*   **Finding Documents (PyMongo):**
    ```python
    # Find one document
    doc = collection.find_one({"name": "Alice"})
    print(doc)

    # Find multiple documents
    cursor = collection.find({"age": {"$gt": 25}})
    for document in cursor:
        print(document)
    ```
*   **Updating a Document (PyMongo):**
    ```python
    result = collection.update_one({"name": "Alice"}, {"$set": {"age": 31}})
    print(f"Matched {result.matched_count} document(s) and modified {result.modified_count} document(s)")
    ```
*   **Deleting a Document (PyMongo):**
    ```python
    result = collection.delete_one({"name": "Alice"})
    print(f"Deleted {result.deleted_count} document(s)")
    ```
*   **Aggregation Example (PyMongo):**
    ```python
    pipeline = [
        {"$match": {"status": "A"}},
        {"$group": {"_id": "$cust_id", "total": {"$sum": "$price"}}},
        {"$sort": {"total": -1}}
    ]
    results = db.orders.aggregate(pipeline)
    for result in results:
        print(result)
    ```

**Version:** Check installed packages (`pip show pymongo`). Consult `/mongodb/docs` for general MongoDB server versions and features.

## 6. Node.js (`/nodejs/node`)

**Description:** Node.js JavaScript runtime built on Chrome's V8 JavaScript engine.

**Key Concepts & Features:**
- **Asynchronous Event-Driven Architecture:** Non-blocking I/O model.
- **Event Loop:** Orchestrates asynchronous operations.
- **Modules:** CommonJS (`require`) and ES Modules (`import`).
- **npm (Node Package Manager):** Managing project dependencies (`package.json`).
- **Core Modules:**
    - `fs`: File system operations (async and sync).
    - `path`: Handling file paths.
    - `http`/`https`: Creating HTTP/HTTPS servers and clients.
    - `os`: Operating system information.
    - `events`: Implementing event emitters and listeners.
    - `child_process`: Spawning child processes (`exec`, `spawn`, `fork`).
    - `async_hooks`/`async_context`: Tracking asynchronous resources and context propagation.
- **Streams:** Handling streaming data (Readable, Writable, Duplex, Transform).
- **Buffers:** Working with binary data.
- **Error Handling:** Callback patterns (error-first), Promises (`.catch()`), `try...catch` with `async/await`.

**Code Snippets:**

*   **Reading a File Asynchronously (fs module):**
    ```javascript
    const fs = require('node:fs');

    fs.readFile('/etc/passwd', 'utf8', (err, data) => {
      if (err) {
        console.error(err);
        return;
      }
      console.log(data);
    });
    ```
*   **Creating an HTTP Server (http module):**
    ```javascript
    const http = require('node:http');

    const server = http.createServer((req, res) => {
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end('Hello World\n');
    });

    server.listen(3000, '127.0.0.1', () => {
      console.log('Server running at http://127.0.0.1:3000/');
    });
    ```
*   **Using Promises with `fs.promises`:**
    ```javascript
    const fs = require('node:fs/promises');

    async function readFileAsync() {
      try {
        const data = await fs.readFile('/etc/passwd', 'utf8');
        console.log(data);
      } catch (err) {
        console.error(err);
      }
    }
    readFileAsync();
    ```
*   **Spawning a Child Process (`exec`):**
    ```javascript
    const { exec } = require('node:child_process');
    exec('ls -lh /usr', (error, stdout, stderr) => {
      if (error) {
        console.error(`exec error: ${error}`);
        return;
      }
      console.log(`stdout: ${stdout}`);
      console.error(`stderr: ${stderr}`);
    });
    ```

**Version:** Check system installation (`node -v`).

## 7. Express.js (`/expressjs/express`)

**Description:** Fast, unopinionated, minimalist web framework for Node.js.

**Key Concepts & Features:**
- **Routing:** Defining how the application responds to client requests to specific endpoints (URIs) and HTTP methods (`app.get()`, `app.post()`, etc.). Route parameters, query strings.
- **Middleware:** Functions that have access to the request object (`req`), the response object (`res`), and the next middleware function in the application’s request-response cycle (`next`). Used for logging, authentication, data validation, error handling, etc.
- **Request Object (`req`):** Contains information about the incoming request (e.g., `req.params`, `req.query`, `req.body`, `req.headers`).
- **Response Object (`res`):** Used to send a response back to the client (e.g., `res.send()`, `res.json()`, `res.status()`, `res.render()`, `res.redirect()`).
- **Application Object (`app`):** Instance of Express used to configure routes, middleware, and settings.
- **Templating Engines:** Integration with view engines (like EJS, Pug, Handlebars) for rendering dynamic HTML (`res.render()`).
- **Static Files:** Serving static assets like CSS, JavaScript, images (`express.static()` middleware).
- **Error Handling:** Defining error-handling middleware functions.

**Code Snippets:**

*   **Basic Server Setup:**
    ```javascript
    import express from 'express'; // Or const express = require('express');

    const app = express();
    const port = 3000;

    app.get('/', (req, res) => {
      res.send('Hello World!');
    });

    app.listen(port, () => {
      console.log(`Example app listening on port ${port}`);
    });
    ```
*   **Basic Routing:**
    ```javascript
    // GET method route
    app.get('/users/:userId', (req, res) => {
      res.send(`User ID: ${req.params.userId}`);
    });

    // POST method route
    app.post('/users', (req, res) => {
      res.send('Got a POST request');
    });
    ```
*   **Using Middleware:**
    ```javascript
    // Simple logger middleware
    const myLogger = function (req, res, next) {
      console.log('LOGGED');
      next(); // Pass control to the next middleware
    };
    app.use(myLogger);

    // Middleware for parsing JSON request bodies
    app.use(express.json());
    ```
*   **Serving Static Files:**
    ```javascript
    app.use(express.static('public')); // Serve files from 'public' directory
    ```
*   **Basic Error Handling:**
    ```javascript
    app.use((err, req, res, next) => {
      console.error(err.stack);
      res.status(500).send('Something broke!');
    });
    ```

**Version:** Check `package.json` for the specific version used.

## 8. AbacusAI (`abacusai` Python Client)

**Description:** AI platform (based on project usage). Interaction via Python client library.

**Key Concepts & Features (Inferred from `generate_book.py`):**
- **API Client:** Uses `abacusai.ApiClient` initialized with an API key.
- **Text Generation:** Utilizes `client.text_generation()` method.
- **Model Selection:** Can specify the underlying AI model (e.g., `claude-3-opus-20240229`).
- **Parameters:** Accepts prompt, max_tokens, temperature, etc.
- **Response Handling:** Accesses generated text via `response.generations[0].text`.
- **Environment Variable:** Requires `ABACUSAI_API_KEY`.

**Code Snippets (from `ebooks/generate_book.py`):**

*   **Initialization:**
    ```python
    import os
    from dotenv import load_dotenv
    from abacusai import ApiClient

    load_dotenv()
    api_key = os.getenv('ABACUSAI_API_KEY')
    client = ApiClient(api_key)
    ```
*   **Text Generation Call:**
    ```python
    prompt = "Your detailed prompt here..."
    try:
        response = client.text_generation(
            prompt=prompt,
            max_tokens=2000,
            temperature=0.7,
            model="claude-3-opus-20240229" # Example model
        )
        generated_text = response.generations[0].text
        # Process generated_text
    except Exception as e:
        print(f"Error generating text: {e}")
    ```

**Version:** Check installed packages (`pip show abacusai`). No specific version information was found via Context7.
