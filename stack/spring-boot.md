# Stack — Spring Boot Application
[DEPENDS ON: base/git.md, base/docs.md, base/quality.md, backend/config.md, backend/http.md, backend/api.md, backend/database.md, backend/observability.md, backend/auth.md, backend/quality.md, backend/features.md, backend/messaging.md]

A Java or Kotlin backend built with Spring Boot. Covers project structure,
layers, dependency injection, JPA, Spring Security, validation, and testing.

---

## Stack
[ID: spring-boot-stack]

- Language: [Java 21+ / Kotlin 1.9+]
- Framework: Spring Boot 3.x
- Build tool: [Maven / Gradle (Kotlin DSL preferred)]
- Persistence: Spring Data JPA + Hibernate
- Database migrations: Flyway
- Validation: Jakarta Bean Validation (`@Valid`, `@NotNull`, etc.)
- Security: Spring Security 6+
- Test runner: JUnit 5 + Mockito + Testcontainers
- Production server: embedded Tomcat (default) / embedded Undertow
- Distribution: Docker image / [platform]

---

## Project structure
[ID: spring-boot-structure]

```
src/
  main/
    java/com/[org]/[app]/
      [feature]/
        [Feature]Controller.java    # REST controller — thin
        [Feature]Service.java       # business logic
        [Feature]Repository.java    # Spring Data JPA repository
        [Feature].java              # JPA entity
        [Feature]Request.java       # request DTO
        [Feature]Response.java      # response DTO
      common/
        exception/
          GlobalExceptionHandler.java  # @RestControllerAdvice
          AppException.java
        config/
          SecurityConfig.java
          OpenApiConfig.java
      Application.java              # @SpringBootApplication entry point
  test/
    java/com/[org]/[app]/
      [feature]/
        [Feature]ControllerTest.java
        [Feature]ServiceTest.java
        [Feature]RepositoryTest.java
src/main/resources/
  application.yml                   # base config
  application-dev.yml               # dev overrides
  application-prod.yml              # prod overrides
  db/migration/                     # Flyway migration scripts
build.gradle.kts                    # or pom.xml
Dockerfile
README.md
CLAUDE.md
```

---

## Layers
[ID: spring-boot-layers]

- **Controller**: `@RestController` — decode HTTP request, delegate to service,
  return response DTO. No business logic.
- **Service**: `@Service` — all business logic. Calls repositories and external
  clients. Annotated with `@Transactional` where needed.
- **Repository**: `@Repository` — extends `JpaRepository<Entity, ID>`. Custom
  queries via `@Query` (JPQL) or query methods. No business logic.
- **Entity**: `@Entity` — JPA mapping only. No service or HTTP concerns on the entity.
- Never skip a layer — controllers do not call repositories directly.

---

## DTOs and validation
[ID: spring-boot-dto]

- Separate request and response DTOs — never expose JPA entities as API responses
- Use Java records or Kotlin data classes for DTOs (immutable by default)
- Annotate request DTOs with Bean Validation constraints (`@NotBlank`,
  `@Size`, `@Email`, etc.)
- Enable validation on controllers with `@Valid` on `@RequestBody` parameters
- `@RestControllerAdvice` in `GlobalExceptionHandler` catches
  `MethodArgumentNotValidException` and returns RFC 9457 error responses

---

## Configuration
[EXTEND: backend-config]

- All config in `application.yml` — use Spring profiles (`dev`, `prod`, `test`)
  for environment-specific overrides
- Bind config to typed `@ConfigurationProperties` classes — never read
  `@Value` directly in services or controllers
- Secrets via environment variables or a secrets manager — never in
  `application.yml` committed to source control

---

## Database and migrations
[EXTEND: backend-database]

- Flyway manages all schema changes — migration scripts in
  `src/main/resources/db/migration/` named `V<n>__<description>.sql`
- Never modify a migration script that has already been applied
- Use Spring Data JPA `findBy*` query methods for simple queries;
  `@Query` with JPQL for complex ones — no raw SQL strings except
  for native queries; annotate these
- Avoid `FetchType.EAGER` — use `FetchType.LAZY` and load associations
  explicitly to prevent N+1 queries

---

## Security
[EXTEND: backend-auth]

- Spring Security filter chain configured in `SecurityConfig`
- JWT validation via a `OncePerRequestFilter` — parse and validate token,
  set `SecurityContextHolder` authentication
- Method-level authorization with `@PreAuthorize` on service methods —
  not on controllers
- CSRF disabled for stateless REST APIs; enabled for server-rendered apps
- CORS configured explicitly in `SecurityConfig` — never use `@CrossOrigin`
  on individual controllers

---

## Feature flags (if applicable)
[EXTEND: backend-features]

- Use FF4j, Unleash Java SDK, or LaunchDarkly Java SDK as a Spring `@Bean`
- Inject the flag service via constructor injection — no static access

---

## Messaging (if applicable)
[EXTEND: backend-messaging]

- Spring Kafka or Spring AMQP for broker integration
- `@KafkaListener` / `@RabbitListener` methods delegate immediately to a
  service method — keep listener methods thin
- Configure consumers as `@Bean` in a dedicated `MessagingConfig` class

---

## Testing
[EXTEND: base-testing]

- Unit tests (JUnit 5 + Mockito): test service logic with mocked dependencies —
  no Spring context loaded
- Slice tests: `@WebMvcTest` for controllers, `@DataJpaTest` for repositories —
  load only the relevant slice, not the full context
- Integration tests (Testcontainers): spin up real PostgreSQL and any broker
  via `@Testcontainers` — test the full request/response cycle
- No mocking of the database in integration tests
- Test naming: `methodName_stateUnderTest_expectedBehaviour`
  e.g. `createUser_duplicateEmail_throwsConflictException`
- Run before every commit: `./gradlew test` (or `mvn test`)

---

## Git conventions
[EXTEND: base-git]

- Do not commit `.env`, `*.class`, `build/`, `target/`, `.gradle/`
- Flyway migrations are committed — never modify a committed migration
- Tag releases with `vX.Y.Z`

---

## Commands
```
./gradlew bootRun              # develop — hot reload with spring-boot-devtools
./gradlew build                # compile + test + package
./gradlew test                 # run tests
./gradlew flywayMigrate        # apply DB migrations (if using Flyway plugin)
docker build -t [name] .       # build container image
```