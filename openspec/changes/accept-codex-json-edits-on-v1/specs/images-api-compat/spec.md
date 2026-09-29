## ADDED Requirements

### Requirement: Public edit route accepts native Codex JSON references
The system SHALL accept `application/json` edit requests containing a prompt and data-URL `images` on `/v1/images/edits` through the same parser and edit pipeline as `/backend-api/codex/images/edits`. It SHALL preserve multipart upload support, authentication, capability/model policy, input validation and existing request-size limits. JSON bodies MUST NOT inherit the multipart admission exemption, including when Content-Encoding is identity.

#### Scenario: Codex uses a public API base URL
- **WHEN** the same valid JSON image-edit request is sent to either edit route
- **THEN** the prompt and ordered reference bytes reach the same edit pipeline and a successful upstream result returns the same public response

#### Scenario: JSON references are invalid
- **WHEN** JSON images are empty or malformed
- **THEN** the request returns a structured input error and does not start upstream generation

#### Scenario: Unauthorized public JSON edits
- **WHEN** an unauthenticated JSON edit request without Content-Encoding passes generic header admission and targets the public route requiring authentication
- **THEN** it returns an authentication error before consuming the request body

#### Scenario: JSON bodies exceed generic admission
- **WHEN** a JSON edit body exceeds the configured raw or decompressed limit, including with identity encoding
- **THEN** it returns 413 and does not start upstream generation

#### Scenario: Existing multipart SDK request
- **WHEN** an authorized multipart edit request targets the public route
- **THEN** existing ordered upload, cleanup and bounded admission behavior is preserved
