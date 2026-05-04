# Stack — gRPC Service (Java / Kotlin)
[DEPENDS ON: templates/base/core/git.md, templates/base/core/docs.md, templates/base/core/quality.md, templates/base/core/config.md, templates/backend/grpc.md, templates/backend/concurrency.md]

Extends the gRPC backend layer with Java/Kotlin-specific conventions for
implementing gRPC servers and clients using grpc-java.

---

## Stack
[ID: grpc-java-stack]

- Language: [Java 21+ / Kotlin 1.9+]
- gRPC library: `io.grpc:grpc-netty-shaded` + `io.grpc:grpc-stub` + `io.grpc:grpc-protobuf`
- Proto compiler: `protoc` via Gradle plugin (`com.google.protobuf`)
- Proto tooling: `buf`
- Build tool: [Gradle (Kotlin DSL) / Maven]
- Test runner: JUnit 5 + `io.grpc:grpc-testing` (InProcessServerBuilder)
- Distribution: Docker image

---

## Project structure
[ID: grpc-java-structure]

```
src/
  main/
    proto/
      [org]/[service]/v1/
        [service].proto
    java/com/[org]/[service]/
      [feature]/
        [Feature]GrpcService.java   # implements generated service base
        [Feature]Service.java       # business logic — no gRPC imports
        [Feature]Repository.java    # data access
      interceptor/
        AuthInterceptor.java
        LoggingInterceptor.java
      config/
        AppConfig.java              # typed config from env vars
      GrpcServer.java               # server bootstrap and shutdown
  test/
    java/com/[org]/[service]/
      [feature]/
        [Feature]GrpcServiceTest.java
build.gradle.kts
buf.yaml
Dockerfile
README.md
CLAUDE.md
```

---

## Service implementation
[EXTEND: grpc-implementation]

- Extend the generated `[Service]ImplBase` class and override RPC methods
- Annotate the class with `@GrpcService` (if using grpc-spring-boot-starter)
  or register manually on the `Server`
- Inject dependencies via constructor — no field injection, no statics
- Use `responseObserver.onNext(response)` then `responseObserver.onCompleted()`
  for unary calls; always call `onCompleted()` or `onError()` — never leave
  a `StreamObserver` open

---

## Server setup and shutdown
[ID: grpc-java-server]

- Build the server with `ServerBuilder.forPort(port).addService(...).intercept(...).build()`
- Call `server.start()` then `server.awaitTermination()` in the main thread
- Register a JVM shutdown hook: `Runtime.getRuntime().addShutdownHook(...)` that
  calls `server.shutdown()` then `server.awaitTermination(30, SECONDS)`
- If using Spring Boot: use `grpc-spring-boot-starter` — it manages lifecycle automatically

---

## Interceptors
[EXTEND: grpc-interceptors]

- Implement `io.grpc.ServerInterceptor` — override `interceptCall()`
- Chain with `ServerInterceptors.intercept(service, interceptor1, interceptor2, ...)`
- Access metadata in interceptors via `Metadata headers` parameter of `interceptCall()`

---

## Testing
[EXTEND: grpc-testing]

- Use `InProcessServerBuilder` and `InProcessChannelBuilder` for in-process
  tests — no port allocation, no network
- Inject a real or fake service implementation — not a mock of the gRPC interface
- JUnit 5 with `@BeforeEach` / `@AfterEach` to start and stop the in-process server
- Test naming: `methodName_stateUnderTest_expectedBehaviour`
  e.g. `getUser_userNotFound_returnsNotFoundStatus`
- Run before every commit: `./gradlew test`

---

## Commands
```
buf lint                          # lint proto files
buf generate                      # alternative: generate stubs with buf
./gradlew generateProto           # generate stubs via Gradle plugin
./gradlew run                     # run server (with application plugin)
./gradlew test                    # run tests
./gradlew build                   # compile + test + package JAR
docker build -t [name] .          # build container image
```