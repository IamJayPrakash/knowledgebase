import os

BASE_DIR = r"D:\Projects\knowledgebase"

EXHAUSTIVE_CONTENT = [
    # 1. Ruby on Rails
    {
        "path": "05-backend-and-runtimes/ruby-on-rails/01_ruby_on_rails_mvc_active_record.md",
        "title": "Ruby on Rails: MVC Architecture, Convention over Configuration & Active Record",
        "hinglish": "Ruby on Rails ka sabse bada fanda hai 'Convention over Configuration'. Iska matlab developer ko hazaron configuration files likhne ki zaroorat nahi hai, Rails pehle se standard conventions follow karta hai. Isme MVC (Model-View-Controller) aur Active Record ORM built-in hota hai.",
        "analogy": "A fully furnished ready-to-move apartment: instead of buying bricks, painting walls, and installing pipes from scratch, everything is pre-configured according to industry standard.",
        "points": [
            "Convention over Configuration (CoC): Database table names are plural ('users'), Models are singular ('User'), primary key is automatically 'id'.",
            "Model-View-Controller (MVC): Models handle data & business logic, Views render HTML, Controllers mediate requests and route responses.",
            "Active Record ORM: Objects wrap database rows, providing intuitive methods like `User.where(active: true).order(:created_at)`.",
            "Database Migrations: Version-controlled schema changes that can be migrated up and rolled back seamlessly (`rails db:migrate`)."
        ],
        "diagram": """[Browser HTTP Request] 
         │
         ▼
    [config/routes.rb]
         │ (Dispatches to action)
         ▼
[app/controllers/users_controller.rb]
   ├── Queries ──> [app/models/user.rb] (Active Record) ──> [PostgreSQL DB]
   └── Renders ──> [app/views/users/index.html.erb] ──> [HTML Response to Browser]""",
        "code": """# app/controllers/orders_controller.rb
class OrdersController < ApplicationController
  # GET /orders - Lists orders with eager loading
  def index
    # Line 1: Use eager loading (.includes) to prevent N+1 queries for associated items
    @orders = Order.includes(:order_items).where(status: 'completed').limit(50)
    
    # Line 2: Render JSON response or HTML view template automatically
    render json: @orders, status: :ok
  end

  # POST /orders - Creates a new order inside a database transaction
  def create
    # Line 3: Wrap multi-table inserts inside an Active Record transaction for ACID safety
    ActiveRecord::Base.transaction do
      # Line 4: Instantiate and save parent order object using strong parameters
      @order = Order.create!(order_params)
      # Line 5: Trigger background mailer worker asynchronously
      OrderMailer.with(order: @order).confirmation_email.deliver_later
    end
    
    # Line 6: Return created order payload with HTTP 201 status
    render json: @order, status: :created
  rescue ActiveRecord::RecordInvalid => e
    # Line 7: Handle validation failures gracefully
    render json: { error: e.message }, status: :unprocessable_entity
  end
end""",
        "pitch": "Ruby on Rails is a mature full-stack MVC framework built on the principle of Convention over Configuration and Don't Repeat Yourself (DRY). Active Record provides powerful database abstractions and schema migrations. While Node.js and FastAPI excel in raw microservice concurrency, Rails remains unmatched for rapid developer velocity and building robust monolithic web applications.",
        "star": "Legacy e-commerce checkout service built on Ruby on Rails experiencing N+1 query bottlenecks during flash sale transactions.",
        "action": "Audited SQL logs using Bullet gem, refactored Active Record queries with `.includes` eager loading, and offloaded confirmation email delivery to Sidekiq background workers via Redis.",
        "metrics": "Database query count per checkout dropped from 42 queries to 2 queries; average checkout response time decreased by 78% (950ms down to 210ms)."
    },

    # 2. MEAN vs MERN Stack
    {
        "path": "05-backend-and-runtimes/mean-vs-mern/01_mean_vs_mern_stack_architecture.md",
        "title": "MERN Stack vs MEAN Stack: Architecture, Trade-Offs & Selection Guide",
        "hinglish": "MERN (MongoDB, Express, React, Node) aur MEAN (MongoDB, Express, Angular, Node) me sabse bada difference frontend framework ka hai: React (MERN) ek flexible UI library hai jisme aap apni pasand ke state tools (Redux/Zustand) chunte ho, jabki Angular (MEAN) ek complete batteries-included enterprise TypeScript framework hai.",
        "analogy": "React is like buying a custom sports car where you pick your custom sound system and wheels. Angular is like buying an all-inclusive luxury SUV that comes fully equipped from the factory.",
        "points": [
            "Language & Strictness: MEAN is strictly TypeScript-first with rigid architectural patterns; MERN allows JavaScript or TypeScript with flexible structure.",
            "Data Binding: Angular uses two-way data binding (or Signals); React uses strict unidirectional (one-way) data flow.",
            "Learning Curve: MEAN has a steep learning curve due to RxJS, Dependency Injection, and Decorators; MERN has a faster onboarding curve focusing on JSX and Hooks.",
            "Enterprise Fit: MEAN is favored in large banking/insurance MNCs with large development teams; MERN dominates high-growth product startups and modern SaaS companies."
        ],
        "diagram": """┌────────────────────────────────────────────────────────┐
│                   SHARED BACKEND                       │
│    MongoDB (Database) + Express.js (API) + Node.js     │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
    [MERN Stack (React)]        [MEAN Stack (Angular)]
    - Virtual DOM / Fiber       - Real DOM / Incremental DOM
    - Unidirectional Flow       - Two-way binding / Signals
    - Flexible Ecosystem        - Built-in DI, Forms, Router
    - High Startup Adoption     - Large Banking / MNC Adoption""",
        "code": """// MERN: React State Hook (Unidirectional flow)
import React, { useState } from 'react';
// Line 1: Define state and updater function
const [email, setEmail] = useState('');
// Line 2: Explicit event handler updates state on user keystroke
<input value={email} onChange={(e) => setEmail(e.target.value)} />

// ----------------------------------------------------
// MEAN: Angular Two-Way Binding with Signal
import { Component, signal } from '@angular/core';
// Line 3: Declare reactive signal in TypeScript component
email = signal('');
// Line 4: In Angular template, two-way bind using [(ngModel)]
<input [(ngModel)]="email" />""",
        "pitch": "Both MERN and MEAN share the Node.js, Express, and MongoDB backend. The key decision lies between React and Angular. Choose MERN for fast developer velocity, rich open-source ecosystem, and dynamic UI performance. Choose MEAN when building enterprise-scale applications requiring strict architecture, built-in dependency injection, and standardized TypeScript team conventions.",
        "star": "Architecting a multi-tenant healthcare enterprise system evaluating whether to standardize on MERN or MEAN across a 40-engineer organization.",
        "action": "Analyzed team skillset, component reusability, and maintenance overhead; selected MERN paired with TypeScript and Zustand, establishing strict ESLint architectural boundaries.",
        "metrics": "Onboarding time for new engineers dropped by 45%; achieved 98% code sharing between web and React Native mobile apps."
    },

    # 3. MongoDB Deep Dive
    {
        "path": "06-databases-and-caching/nosql-mongodb/01_mongodb_architecture_indexing_sharding.md",
        "title": "MongoDB Architecture: WiredTiger Engine, Compound Indexing & Sharding",
        "hinglish": "MongoDB ek NoSQL Document Database hai jo data ko BSON (Binary JSON) format me store karta hai. Iska WiredTiger engine document-level concurrency aur compression deta hai. Heavy reads ke liye Compound Indexes aur heavy writes ke liye Sharding use karte hain.",
        "analogy": "A digital filing cabinet where every folder (document) can hold customized papers with different fields without needing to remodel the entire office building whenever a new document type arrives.",
        "points": [
            "WiredTiger Storage Engine: Provides document-level locking, Snappy/Zlib data compression, and write-ahead journaling (WAL).",
            "BSON Data Format: Extends JSON with support for binary data, dates, and 64-bit integers with fast traversal headers.",
            "Indexing Strategies: Single field, Compound indexes (following the Equality, Sort, Range - ESR rule), and Multikey indexes for array fields.",
            "Horizontal Sharding: Distributes data across multiple shard servers using a Shard Key (Hashed vs Ranged) via `mongos` routing query routers."
        ],
        "diagram": """[Application Client]
         │
         ▼
    [mongos (Query Router)]
         │
         ├── Checks [Config Servers (Metadata)]
         │
         ├── Routes to ──> [Shard 1 Replica Set] (Primary + Secondary)
         └── Routes to ──> [Shard 2 Replica Set] (Primary + Secondary)""",
        "code": """// MongoDB Aggregation Pipeline with ESR Indexing
// Line 1: Create a Compound Index following Equality, Sort, Range (ESR) rule
db.orders.createIndex({ status: 1, createdAt: -1, totalAmount: 1 });

// Line 2: Execute high-throughput aggregation pipeline
db.orders.aggregate([
  // Line 3: Stage 1 - $match filters documents using the index equality prefix
  { $match: { status: "completed" } },
  
  // Line 4: Stage 2 - $group groups revenue by user
  { 
    $group: { 
      _id: "$userId", 
      totalSpent: { $sum: "$totalAmount" },
      orderCount: { $sum: 1 }
    } 
  },
  
  // Line 5: Stage 3 - $match filters aggregated totals (HAVING clause equivalent)
  { $match: { totalSpent: { $gte: 500 } } },
  
  // Line 6: Stage 4 - $sort orders the top spenders descending
  { $sort: { totalSpent: -1 } },
  
  // Line 7: Stage 5 - $limit restricts output to top 10 results
  { $limit: 10 }
]);""",
        "pitch": "MongoDB is a document-oriented database designed for high horizontal scalability and flexible schema evolution. Powered by the WiredTiger engine, it supports ACID transactions at the multi-document level. By adhering to the ESR (Equality, Sort, Range) indexing rule and carefully choosing high-cardinality shard keys, MongoDB can effortlessly scale to billions of documents with sub-10ms response times.",
        "star": "Multi-tenant analytics platform storing 100M+ event logs suffered severe database write locking and slow query execution times exceeding 6 seconds.",
        "action": "Analyzed query performance using `explain('executionStats')`, replaced COLLSCAN queries with targeted Compound ESR indexes, and enabled hashed sharding on `{ tenantId: 'hashed' }`.",
        "metrics": "Average query latency decreased from 6,200ms to 12ms (99.8% reduction); cluster write throughput scaled from 800 ops/sec to 18,000 ops/sec."
    },

    # 4. Express.js Middleware Pipeline
    {
        "path": "05-backend-and-runtimes/node-express/02_express_middleware_architecture_and_pipeline.md",
        "title": "Express.js Architecture: Middleware Pipeline, Error Handling & Async Wrappers",
        "hinglish": "Express.js ka core architecture ek 'Middleware Pipeline' hai. Request aane par wo ek chain of functions se hokar guzarti hai (`req -> auth -> validation -> controller -> response`). Agar beech me koi error aata hai, toh `next(err)` call karne se Express direct special 4-parameter Error Handling Middleware par jump kar jata hai.",
        "analogy": "An airport security check: you pass through ticket verification, baggage scan, and body check in a strict pipeline before boarding your flight. If any checkpoint fails, you are directed immediately to the security office.",
        "points": [
            "Middleware Function Signature: `(req, res, next) => { ... }` where `next()` passes control to the subsequent middleware.",
            "Global Error Handling: Special 4-parameter middleware `(err, req, res, next)` catches unhandled exceptions centrally.",
            "Async Wrapper Pattern: Catches rejected Promises in async routes and forwards them to `next(err)`, avoiding unhandled promise rejections.",
            "Security & Parsing Middlewares: `helmet` for HTTP security headers, `cors`, `express.json()`, and `express-rate-limit`."
        ],
        "diagram": """[Incoming HTTP Request]
       │
       ▼
 [express.json()] ──> [cors()] ──> [Auth Middleware] ──> [Route Controller]
                                                              │ (Throws Error)
                                                              ▼
                                               [next(err) Invocation]
                                                              │
                                                              ▼
                                            [Global Error Handler (err, req, res, next)]""",
        "code": """// Async Handler Wrapper to eliminate try/catch boilerplate
// Line 1: Define higher-order function taking an async route controller
const asyncHandler = (fn) => (req, res, next) => {
  // Line 2: Resolve promise and automatically catch any errors forwarding to next()
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Line 3: Protected business route using the async wrapper
app.get('/api/users/:id', authMiddleware, asyncHandler(async (req, res) => {
  // Line 4: Direct async database lookup without explicit try/catch blocks
  const user = await UserModel.findById(req.params.id);
  if (!user) {
    // Line 5: Throw custom domain error if user not found
    throw new NotFoundError('User record does not exist');
  }
  // Line 6: Send JSON response
  res.status(200).json({ success: true, data: user });
}));

// Line 7: Centralized Error Handling Middleware (must have exactly 4 parameters!)
app.use((err, req, res, next) => {
  // Line 8: Log detailed error stack on the server
  console.error('[Error Pipeline]:', err.stack);
  // Line 9: Send clean, sanitized JSON error response to client
  const status = err.statusCode || 500;
  res.status(status).json({
    success: false,
    message: err.message || 'Internal Server Error'
  });
});""",
        "pitch": "Express.js is a minimalist, unopinionated routing and middleware web framework for Node.js. Its power lies in the middleware execution pipeline. By implementing centralized error handling with custom async wrapper utilities and securing endpoints with Helmet and rate limiters, developers can construct scalable, resilient enterprise REST APIs.",
        "star": "Production Node.js API server crashing periodically due to unhandled promise rejections inside asynchronous route controllers.",
        "action": "Implemented a standardized `asyncHandler` wrapper pattern across all 120 API routes and created a centralized 4-parameter error-handling middleware with structured Winston logging.",
        "metrics": "Eliminated 100% of unhandled rejection process crashes; stabilized service availability at 99.99% uptime."
    },

    # 5. JavaScript Closures Deep Dive
    {
        "path": "01-javascript/02_closures_lexical_scope_memory.md",
        "title": "JavaScript Closures, Lexical Scope & V8 Memory Management",
        "hinglish": "Closure tab banta hai jab ek inner function apne bahar wale (outer) function ke variables ko yaad rakhta hai, chahe outer function execute hokar call stack se hat chuka ho. V8 engine aise variables ko Stack se uthakar Heap memory me store karta hai taaki wo delete na hon.",
        "analogy": "A backpack that a student carries. When you leave home (outer function returns), you don't lose your notebooks and lunchbox because they are preserved inside your backpack.",
        "points": [
            "Lexical Scope: Scope is determined at compile/author time based on where functions and variables are physically written in code.",
            "Closure Formation: A function bundled together with references to its surrounding state (lexical environment).",
            "Heap Allocation: V8 moves closed-over variables to the Heap inside a hidden `[[Scopes]]` array property.",
            "Primary Uses: Data encapsulation (private variables), Function Currying, Memoization, and Custom React Hooks.",
            "Memory Leak Pitfall: Forgotten closures holding references to large objects or DOM elements that the Garbage Collector cannot reclaim."
        ],
        "diagram": """[Global Execution Context]
       │
       ▼ Calls outer()
[outer() Execution Context]
   ├── Allocates secretToken = "ABC" on V8 Heap
   └── Returns inner() function
       │
       ▼ outer() popped from Call Stack
[inner() Executed Later]
   └── Reads secretToken directly from [[Scopes]] Closure on the Heap!""",
        "code": """// Production Data Encapsulation using Closures
function createSecureVault() {
  // Line 1: Private variable allocated on V8 Heap (inaccessible from outside)
  let privateBalance = 1000;
  
  // Line 2: Return an object containing public methods that hold closure over privateBalance
  return {
    // Line 3: Method to view balance safely
    getBalance: function() {
      return privateBalance;
    },
    // Line 4: Method to deposit funds with business validation
    deposit: function(amount) {
      if (amount <= 0) throw new Error('Deposit amount must be positive');
      privateBalance += amount;
      return privateBalance;
    },
    // Line 5: Method to withdraw funds with overdraft protection
    withdraw: function(amount) {
      if (amount > privateBalance) throw new Error('Insufficient funds');
      privateBalance -= amount;
      return privateBalance;
    }
  };
}

// Line 6: Instantiate vault
const myVault = createSecureVault();
console.log(myVault.getBalance()); // 1000
myVault.deposit(500);
console.log(myVault.getBalance()); // 1500
console.log(myVault.privateBalance); // undefined (Data privacy enforced!)""",
        "pitch": "A closure in JavaScript is created when a function retains access to its lexical scope even when executed outside that scope. Under the hood, the V8 engine identifies closed-over variables and allocates them in heap memory rather than on the call stack. We utilize closures extensively for data privacy, currying, and custom React hooks. However, we must ensure references are released when no longer needed to avoid memory leaks.",
        "star": "Memory leak in a single-page analytics application where browser RAM increased by 400MB over an hour of usage, eventually causing browser tab crashes.",
        "action": "Captured Chrome DevTools Heap Snapshots and identified that a resize event listener was retaining a closure reference to a 50MB charting dataset; detached the listener and set the reference to `null` on component unmount.",
        "metrics": "Eliminated the 400MB memory leak; reduced steady-state browser memory consumption from 580MB down to 42MB."
    },

    # 6. JavaScript Prototypes Deep Dive
    {
        "path": "01-javascript/03_prototypes_and_prototypal_inheritance.md",
        "title": "JavaScript Prototypes, Prototype Chain & ES6 Class Transpilation",
        "hinglish": "JavaScript classical object-oriented language nahi hai, balki prototypal inheritance use karta hai. Har object ke paas ek hidden link hota hai `__proto__` jo uske parent prototype object ko point karta hai. Jab aap koi property access karte ho aur wo object me nahi milti, toh JS prototype chain upar traverse karta hai jab tak `Object.prototype` (null) na mil jaye.",
        "analogy": "Inheriting family heirlooms: if you don't own a car, you ask your parents. If they don't own one, you check your grandparents. If nobody has it, the search returns undefined.",
        "points": [
            "Prototype Object: Every JavaScript function has a `prototype` property used when instances are created with `new`.",
            "Prototype Chain (`__proto__` / `[[Prototype]]`): The internal lookup chain linking an object instance to its constructor's prototype.",
            "Method Sharing: Defining methods on `.prototype` saves memory because all instances share the exact same function reference in memory.",
            "ES6 `class` Syntax: Syntactic sugar over constructor functions and prototypal inheritance."
        ],
        "diagram": """[myArray Instance] ──(__proto__)──> [Array.prototype] ──(__proto__)──> [Object.prototype] ──(__proto__)──> null
   (e.g. [1, 2])                      (e.g. .map, .filter)               (e.g. .toString, .valueOf)""",
        "code": """// Classical Constructor vs Modern Class Transpilation
// Line 1: Constructor Function
function Vehicle(make, model) {
  // Line 2: Instance properties assigned to 'this'
  this.make = make;
  this.model = model;
}

// Line 3: Attach shared method to prototype to conserve memory across 100,000 instances
Vehicle.prototype.getDetails = function() {
  return `${this.make} ${this.model}`;
};

// Line 4: Inheriting Constructor Function
function ElectricCar(make, model, batteryCapacity) {
  // Line 5: Call parent constructor passing current instance 'this'
  Vehicle.call(this, make, model);
  this.batteryCapacity = batteryCapacity;
}

// Line 6: Link prototype chain using Object.create
ElectricCar.prototype = Object.create(Vehicle.prototype);
// Line 7: Re-link constructor reference back to ElectricCar
ElectricCar.prototype.constructor = ElectricCar;

// Line 8: Instantiate object
const tesla = new ElectricCar('Tesla', 'Model 3', '75kWh');
console.log(tesla.getDetails()); // 'Tesla Model 3'
console.log(tesla instanceof Vehicle); // true""",
        "pitch": "JavaScript implements inheritance through objects linking to other objects via the prototype chain. When accessing a property, the V8 engine first checks the instance itself; if not found, it traverses the `[[Prototype]]` link up to `Object.prototype` before returning `undefined`. Methods attached to the prototype are shared across all instances, saving significant heap memory.",
        "star": "Data grid component initializing 50,000 row objects where methods were defined inside the constructor function, causing 150MB of duplicate function objects in RAM.",
        "action": "Refactored the row model to attach formatting methods to the prototype definition, enabling all 50,000 instances to share a single method reference in memory.",
        "metrics": "Heap memory footprint dropped from 185MB to 22MB (88% reduction); object instantiation speed increased by 3.5x."
    },

    # 7. JavaScript This Keyword
    {
        "path": "01-javascript/04_this_keyword_call_apply_bind.md",
        "title": "The 'this' Keyword: 5 Binding Rules, Call, Apply, Bind & Arrow Functions",
        "hinglish": "JavaScript me `this` function define karte waqt fix nahi hota, balki call-site (function kaise call hua hai) par depend karta hai. Iske 5 golden rules hain: Default binding, Implicit binding, Explicit binding (`call`, `apply`, `bind`), `new` binding, aur Arrow functions (jo lexical `this` inherit karte hain).",
        "analogy": "The word 'here': depending on who says 'I am here', 'here' means a completely different room or city!",
        "points": [
            "Rule 1: Default Binding: In standalone function invocation, `this` points to `global` / `window` (or `undefined` in strict mode).",
            "Rule 2: Implicit Binding: When a function is called as an object method (`obj.fn()`), `this` points to `obj`.",
            "Rule 3: Explicit Binding: Using `.call(thisArg, arg1, arg2)`, `.apply(thisArg, [args])`, or `.bind(thisArg)` forces `this` to point to `thisArg`.",
            "Rule 4: `new` Binding: When invoked with `new Constructor()`, `this` points to the brand new empty object being created.",
            "Rule 5: Arrow Functions: Arrow functions do NOT have their own `this`. They lexically inherit `this` from their enclosing scope at definition time."
        ],
        "diagram": """[How was the function called?]
       │
       ├── Called with 'new'? ───────────────> this = Brand New Object
       ├── Called with call/apply/bind? ─────> this = Specified Object
       ├── Called on an object (obj.fn())? ──> this = Containing Object
       └── Standalone function call? ─────────> this = undefined (strict) / window""",
        "code": """// Explicit Binding & Polyfill for Function.prototype.bind
// Line 1: Attach customBind polyfill to Function prototype
Function.prototype.customBind = function(context, ...boundArgs) {
  // Line 2: Keep reference to original function
  const targetFn = this;
  
  // Line 3: Return a new function that can accept additional runtime arguments
  return function(...runtimeArgs) {
    // Line 4: Combine initial bound arguments with runtime arguments
    const combinedArgs = [...boundArgs, ...runtimeArgs];
    // Line 5: Execute target function explicitly bound to context
    return targetFn.apply(context, combinedArgs);
  };
};

// Line 6: Example object
const developer = { name: 'Jay Prakash', role: 'Technical Lead' };

function introduce(greeting, punctuation) {
  return `${greeting}, I am ${this.name}, working as ${this.role}${punctuation}`;
}

// Line 7: Bind introduce function to developer object
const boundIntro = introduce.customBind(developer, 'Hello');
console.log(boundIntro('!')); // "Hello, I am Jay Prakash, working as Technical Lead!" """,
        "pitch": "The `this` keyword in JavaScript is execution-context dependent and determined at call time. It resolves through five precedence rules: `new` binding, explicit binding (`call`/`apply`/`bind`), implicit object binding, and default binding. Unlike regular functions, arrow functions do not have their own `this` binding and lexically inherit it from the parent enclosing scope.",
        "star": "Callback event handlers inside a legacy React class component losing context (`Cannot read property 'setState' of undefined`) when passed down to child components.",
        "action": "Diagnosed loss of implicit binding when passing unbound callback references; resolved by binding methods in the constructor and transitioning to arrow function class fields.",
        "metrics": "Eliminated runtime `TypeError` exceptions across 18 customer-facing UI forms."
    },

    # 8. High-Level Design: TinyURL
    {
        "path": "07-system-design/01_hld_url_shortener_tinyurl.md",
        "title": "System Design: Scalable URL Shortener (TinyURL / Bitly)",
        "hinglish": "TinyURL ka kaam ek lambi URL (jaise 200 characters) ko ek chhote 7-character code (jaise tinyurl.com/aB3x9Z) me convert karna hai. Isme Base62 encoding aur pre-generated Key Generation Service (KGS) use karke zero-collision URL generation achieve karte hain.",
        "analogy": "A coat check at a concert: you hand over your bulky winter jacket, receive a small plastic token with a number, and later redeem that token to get your exact jacket back.",
        "points": [
            "Traffic & Scale: 100M URLs created/month, 10:1 read-to-write ratio (1 Billion reads/month).",
            "Storage Calculation: 7 characters in Base62 ($62^7 \\approx 3.5 \\text{ Trillion}$ unique URLs), requiring ~3.5TB storage over 5 years.",
            "Encoding Approach: Pre-generate unique IDs using a Key Generation Service (KGS) to avoid runtime hash collisions and race conditions.",
            "Caching Strategy: Cache the top 20% most popular URLs in Redis (Pareto Principle), reducing database reads by 80%."
        ],
        "diagram": """[Client Browser]
       │
       ├── 1. POST /api/shorten { longUrl }
       │        │
       │        ▼
       │   [API Gateway / Load Balancer]
       │        │
       │        ▼
       │   [URL Service] ──> Fetches token from [Key Generation Service (KGS)]
       │        │
       │        └── Writes to [PostgreSQL / NoSQL DB] & [Redis Cache]
       │
       └── 2. GET /{shortCode}
                │
                ▼
           [API Gateway] ──> [Redis Cache (Hit: 2ms)] ──(Miss: 15ms)──> [Database]
                │
                ▼ (Returns HTTP 301 / 302 Redirect to longUrl)""",
        "code": """// Base62 Encoding Utility for TinyURL
const BASE62_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';

// Line 1: Converts integer ID (from KGS or Auto-Increment) into 7-character Base62 string
function encodeBase62(num) {
  let encoded = '';
  // Line 2: Continually divide by 62 taking modulo remainder
  while (num > 0) {
    const remainder = num % 62;
    encoded = BASE62_CHARS[remainder] + encoded;
    num = Math.floor(num / 62);
  }
  // Line 3: Pad with leading zeros to ensure uniform 7-character slug
  return encoded.padStart(7, '0');
}

// Line 4: Decodes 7-character string back to unique integer ID
function decodeBase62(str) {
  let decoded = 0;
  for (let i = 0; i < str.length; i++) {
    const charIndex = BASE62_CHARS.indexOf(str[i]);
    decoded = decoded * 62 + charIndex;
  }
  return decoded;
}

console.log(encodeBase62(1253019)); // "0005Fzb"
console.log(decodeBase62("0005Fzb")); // 1253019""",
        "pitch": "Designing TinyURL requires high availability, low latency redirection, and scalable key generation. We utilize Base62 encoding capable of supporting 3.5 trillion unique URLs with 7 characters. To prevent hash collisions and database locks, we implement a Key Generation Service (KGS) that pre-allocates token ranges to worker nodes. A Redis Cache-Aside layer handles the 10:1 read-to-write ratio, serving 80% of redirects in sub-5ms.",
        "star": "Architected a high-volume marketing link tracking platform for an ad network generating 500M clicks/month.",
        "action": "Replaced on-the-fly MD5 hashing with a distributed Snowflake ID generator and Base62 encoding, backed by Redis cluster caching with LRU eviction.",
        "metrics": "Redirect latency dropped from 140ms to 4ms; system handled peak traffic spikes of 25,000 requests/sec with zero key collision errors."
    },

    # 9. TCS / Infosys / Accenture / Capgemini Company Pack
    {
        "path": "11-interview-master-cheatsheets/service-mnc-tier/tcs_interview_guide.md",
        "title": "TCS Technical Interview Guide: High-Frequency Questions & Simple Pointers",
        "hinglish": "TCS ke technical interview me sabse zyada focus basic fundamentals, clean code, OOPs concepts, SQL queries, aur web basics par hota hai. Yahan complex algorithm se zyada clear concepts aur communication dekhte hain.",
        "analogy": "A foundation inspection of a building: they want to confirm the foundation pillars are strong before checking the luxury penthouse design.",
        "points": [
            "Difference between `var`, `let`, and `const` (Scope, Re-declaration, Hoisting).",
            "Difference between `==` and `===` (Loose equality with type coercion vs Strict equality).",
            "OOPs 4 Pillars: Encapsulation (Capsule/Data hiding), Abstraction (ATM screen), Inheritance (Parent-Child), Polymorphism (Overloading & Overriding).",
            "SQL Basics: Primary Key vs Unique Key, `UNION` vs `UNION ALL`, `HAVING` vs `WHERE` clause.",
            "React Basics: Props vs State, Virtual DOM advantage, Lifecycle of a component."
        ],
        "diagram": """[TCS Interview Round Flow]
 ├── 1. Self Introduction & Project Overview (2 mins)
 ├── 2. Core Language Basics (JS / Java / Python) (10 mins)
 ├── 3. SQL Query Writing (5 mins)
 ├── 4. Problem Solving / Logic Check (10 mins)
 └── 5. Questions for Interviewer (3 mins)""",
        "code": """// High Frequency TCS Code Question: Reverse a String without built-in reverse()
function reverseString(str) {
  // Line 1: Initialize empty result string
  let reversed = '';
  // Line 2: Loop backwards from last index down to 0
  for (let i = str.length - 1; i >= 0; i--) {
    // Line 3: Append character to result
    reversed += str[i];
  }
  return reversed;
}

// High Frequency TCS Code Question: Find Second Largest Number in Array
function getSecondLargest(arr) {
  let largest = -Infinity;
  let second = -Infinity;
  
  for (const n of arr) {
    if (n > largest) {
      second = largest;
      largest = n;
    } else if (n > second && n !== largest) {
      second = n;
    }
  }
  return second;
}

console.log(reverseString('TCSInterview')); // "weivretnISCT"
console.log(getSecondLargest([12, 35, 1, 10, 34, 1])); // 34""",
        "pitch": "For TCS technical interviews, success relies on clear, structured communication. Begin each answer with a crisp 1-sentence definition, explain with a practical daily life example, state 2-3 key technical differences point-wise, and mention the code syntax cleanly.",
        "star": "Clearing TCS Digital / Innovator technical interview bands for enterprise digital transformation assignments.",
        "action": "Structured responses using point-wise technical explanations, followed by clean whiteboard code showing variable dry runs.",
        "metrics": "Scored highest grade assessment rating and fast-track placement into premium cloud architecture accounts."
    },

    # 10. JLL / Nagarro / Startup Interview Guide
    {
        "path": "11-interview-master-cheatsheets/mid-tier-and-startups/jll_interview_guide.md",
        "title": "JLL & Product Startup Technical Interview Guide: Real-World Scenario Rounds",
        "hinglish": "JLL, Nagarro, aur high-growth startups me theoretical definitions se zyada practical problem-solving aur real-world project challenges pooche jaate hain: 'Agar server pe 100% CPU spike ho gaya toh kaise debug karoge?', 'React me unwanted re-renders kaise rokoge?'",
        "analogy": "A flight simulator test: instead of asking what an airplane rudder is, they put you in bad weather and see how you land the plane safely.",
        "points": [
            "Debugging Production Issues: How to analyze Node.js memory leaks with Heap Snapshots and CPU profiling.",
            "React Optimization: Preventing re-renders using `React.memo`, `useMemo`, `useCallback`, and window virtualization for large tables.",
            "API Design & Security: Handling JWT expiration, Refresh token rotation in HTTP-only cookies, Rate limiting, and CORS.",
            "Database Tuning: Diagnosing slow SQL queries with `EXPLAIN ANALYZE`, adding missing compound indexes, preventing N+1 queries."
        ],
        "diagram": """[Startup / JLL Scenario Interview Framework]
 Problem Stated (e.g. 100% CPU Spike)
        │
        ├── 1. Immediate Mitigation (Rollback / Add Replica Pods)
        ├── 2. Telemetry & Root Cause Analysis (Profiling / Logs)
        ├── 3. Code / Architectural Fix (Worker Threads / Cache)
        └── 4. Long-Term Monitoring & Alerts (Prometheus / Grafana)""",
        "code": """// Production Refresh Token Rotation Pattern (JLL / Startup Favorite)
import jwt from 'jsonwebtoken';

// Line 1: Route to handle token refresh with security rotation
app.post('/api/auth/refresh', async (req, res) => {
  // Line 2: Read refresh token securely from HTTP-only cookie
  const refreshToken = req.cookies.refreshToken;
  if (!refreshToken) return res.status(401).json({ error: 'No token provided' });

  try {
    // Line 3: Verify token signature
    const decoded = jwt.verify(refreshToken, process.env.REFRESH_TOKEN_SECRET);
    
    // Line 4: Check if refresh token exists in Redis (Detect reuse attacks!)
    const isTokenValid = await redisClient.get(`token:${decoded.userId}`);
    if (isTokenValid !== refreshToken) {
      // Possible token reuse/theft! Revoke all tokens immediately
      await redisClient.del(`token:${decoded.userId}`);
      return res.status(403).json({ error: 'Compromised token detected' });
    }

    // Line 5: Issue new Access Token (15 mins) and new Refresh Token (7 days)
    const newAccessToken = jwt.sign({ userId: decoded.userId }, process.env.ACCESS_TOKEN_SECRET, { expiresIn: '15m' });
    const newRefreshToken = jwt.sign({ userId: decoded.userId }, process.env.REFRESH_TOKEN_SECRET, { expiresIn: '7d' });

    // Line 6: Rotate refresh token in Redis
    await redisClient.setEx(`token:${decoded.userId}`, 7 * 24 * 3600, newRefreshToken);

    // Line 7: Send new cookie and access token
    res.cookie('refreshToken', newRefreshToken, { httpOnly: true, secure: true, sameSite: 'Strict' });
    return res.json({ accessToken: newAccessToken });
  } catch (err) {
    return res.status(403).json({ error: 'Invalid token' });
  }
});""",
        "pitch": "In JLL and mid-tier product interviews, interviewers assess hands-on debugging, security architecture, and system scalability. Highlighting security patterns like Refresh Token Rotation and telemetry-driven root cause analysis demonstrates maturity beyond code syntax to production ownership.",
        "star": "Resolving customer session hijacking vulnerability on a real-estate management enterprise portal.",
        "action": "Designed and deployed a stateful Refresh Token Rotation protocol using Redis key-value storage and secure SameSite cookies.",
        "metrics": "Eliminated replay attack risks across 250,000 corporate user logins with zero authentication downtime."
    }
]

def generate_exhaustive_files():
    for item in EXHAUSTIVE_CONTENT:
        target_path = os.path.join(BASE_DIR, item["path"])
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        points_md = "\n".join([f"- {p}" for p in item["points"]])

        content = f"""# {item['title']}

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** {item['hinglish']}
>
> **Real-World Analogy:** {item['analogy']}

---

## 2. 📌 Core Mechanics & Key Points
{points_md}

---

## 3. 📊 Visual Architecture Diagram

```text
{item['diagram']}
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```javascript
{item['code']}
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "Can you explain {item['title'].split(':')[0]} and your production experience with it?"
>
> **You:** "{item['pitch']}"

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** {item['star']}
* **Task / Challenge:** Resolving critical production bottlenecks, scaling limits, or security vulnerabilities under active business pressure.
* **Action Taken:** {item['action']}
* **Result & Business Impact:** {item['metrics']}

🗣️ **Script to Tell Interviewer:**
*"In one of my core projects, {item['star'].lower()} I spearheaded the solution by {item['action'].lower()}, successfully achieving {item['metrics'].lower()}."*
"""
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated: {target_path}")

    print("All exhaustive domain files generated successfully!")

if __name__ == "__main__":
    generate_exhaustive_files()
