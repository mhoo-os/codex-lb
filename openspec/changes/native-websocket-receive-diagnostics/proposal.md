# Native WebSocket receive diagnostics

## Why
Native receive failures currently lose their transport failure phase when converted into the safe generic stream error. Operators cannot distinguish helper faults, liveness timeouts, and receive failures.

## What Changes
Add bounded server-log diagnostics at the native WebSocket adapter for receive exceptions and close frames. Preserve existing downstream messages, error classification, routing, and retry behavior. Do not log exception text, close reasons, frames, headers, account identity, or call identifiers.

## Impact
Affected spec: proxy-runtime-observability. No settings, database migrations, dependencies, or new public endpoints.
