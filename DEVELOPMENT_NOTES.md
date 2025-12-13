## Implementation Walkthrough:
1. Planning stage - studying the technical requirements. Choosing the method for obtaining geolocation data - via API or database.
2. Writing the initial simplest version - basic endpoints, testing in Swagger. Endpoints and their logic are located in a separate API folder.
3. Adding a Pydantic model for the response.
4. Adding validation for correct IP address format (v4/v6).
5. Adding Ruff/Mypy checks in the code and summary/description to endpoints for additional information in Swagger and in the specification.
6. Adding unit and API tests using pytest.
8. Adding a global error handler for unified error representation everywhere.
9. Adding a README.md file.
10. Adding logic for generating the specification - openapi.yaml file.
11. Adding DEVELOPMENT_NOTES.md.

## Total Time Spent:
Approximate time (~7 hours).

## Challenges & Solutions:
1. - Problem: It is impossible to accurately test obtaining your own IP, since I get 127.0.0.1, i.e., localhost.
   - Solution: Considering a quick deploy test server for verification.
2. - Problem: The ip-api.com API returns a field "as". "as" is a reserved keyword in Python.
   - Solution: Alias in Pydantic (as_: str = Field(alias="as"))

## GenAI Usage

### Typical cases of my successful usage in this project:
- Used GenAI to generate template code for FastAPI endpoints and models. This significantly accelerated development and reduced the number of syntax errors.
- Consulted GenAI for explanations of mypy and FastAPI errors. AI helped quickly find the cause and suggested a working solution, saving debugging time.
- Asked GenAI to generate unit tests for asynchronous functions with mocks. The generated examples were useful, but sometimes required manual adjustments for the specifics of the project.
- Used AI to check English descriptions, summaries, and comments in the code. This helped avoid grammatical mistakes and made the documentation more professional.

### Limitations:
AI could not always take into account the specifics of my project or the latest changes in libraries, so some suggestions required additional verification. Overall, AI handles the generation of very specific and small code snippets well, which almost always require refinement after testing. But this still saves time during development.

### AI tools:
For initial project creation, debugging errors, and so on, I used OpenAI GPT-4 (via Epam Dial platform). Later, for checking all code and documentation, I used Claude (Sonnet 4.5).

## API Design Decisions:
The project structure is typical for a modern FastAPI application and provides clear separation of concerns. At the project root are the main files for launching (main.py), documentation (README.md, openapi.yaml), configuration (requirements.txt, ruff.toml), and helper scripts (generate_openapi.py). All business logic is grouped in the api folder, where models (api_models.py), routers (routers.py), utilities (utils.py), and tests (tests) are separated. Such organization simplifies code navigation, makes project maintenance and scaling easier, and allows different team members to work on separate parts independently. A separate file for the OpenAPI specification (openapi.yaml) enables a design-first approach and ensures high-quality API documentation.

I chose the code-first approach because it is a better option when starting a new project, especially when the exact requirements for the project structure and API are not yet clearly defined.
In this case, it is more efficient to first build the project and then generate the specification from the code, rather than spending a lot of time manually creating the specification and developing the project based on it.

However, this structure is suitable for starting a POC. As the project grows and becomes more complex, it is better to switch, for example, to Hexagonal Architecture.

## Third-Party API Selection:

### Why I chose ip-api.com, trade-offs:

I chose to use an API for several reasons:
- Fast start
- Always up-to-date data
- Less storage/memory
- Zero maintenance (no need to write an update mechanism or track versions)
- Simple deployment (no dependencies on local files) However, as the load increases, in production it makes sense to switch to using a local database.

Cons / Trade-offs:

- External dependency: Your service relies on the availability and reliability of the third-party API.
- Network latency: Each request requires a network call, which can increase response times.
- Rate limits and quotas: Most APIs have usage limits, which can restrict scalability.
- Data privacy: User IP addresses are sent to an external service, which may not be acceptable for all use cases.
- Limited control: You cannot customize or optimize the data or responses as you could with a local database.
- Downtime risk: If the API provider experiences downtime, your service may be impacted.

## Production Readiness:
To prepare project to production we should at least do next steps:
1. Caching Layer (Redis).
2. Rate Limiting - Protection against abuse via a rate limiter (for example, using the slowapi library).
3. Structured Logging - Replace print() with structured logging.
4. Metrics & Monitoring - Prometheus metrics + Grafana dashboards.
5. Configuration Management - Pydantic Settings.
6. Retry Logic & Circuit Breaker - several retries on failure and a breaker if it fails for too long. For example, using the Tenacity library.
7. Health Check endpoint - required for Kubernetes.
8. API Key Authentication.
9. Read geolocation data from a local database when the API is unavailable.
10. CI/CD Pipeline.
