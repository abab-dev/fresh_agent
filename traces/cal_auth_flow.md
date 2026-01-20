Agent initialized. Type your message or /exit to quit.


> how does the auth work
🤖

I'll help you understand how authentication works in this codebase. Let me delegate to the explorer agent to search through the codebase and provide a comprehensive overview.


[tool] delegate
[info]
[Delegating to explorer]

============================================================
◆ SUBAGENT HANDOFF: [explorer]
============================================================
Task: QUESTION: How does authentication work in this codebase? What authentication system is used, what are the key components, and how does the
auth flow work?
KEYWORDS: auth, authentication, login, session, jwt, token, user, oauth, credential
EXPECTED: A detailed explanation of the authentication architecture, key files, and flow
------------------------------------------------------------
  L [explorer] glob
      pattern: *auth*
  L [explorer] ✓ glob
      Result: {'result': 'Found 100 files', 'files': [{'path': '/home/ab/git-projs/cal.com/agents/rules/architecture-page-level-auth.md', 'name': 'architecture-page-level-auth.md'}, {'path': '/home/ab/git-projs/cal...
  L [explorer] glob
      pattern: *login*
  L [explorer] ✓ glob
      Result: {'result': 'Found 13 files', 'files': [{'path': '/home/ab/git-projs/cal.com/__checks__/csp-login.spec.ts', 'name': 'csp-login.spec.ts'}, {'path': '/home/ab/git-projs/cal.com/apps/web/app/(use-page-wra...
  L [explorer] glob
      pattern: *session*
  L [explorer] ✓ glob
      Result: {'result': 'Found 17 files', 'files': [{'path': '/home/ab/git-projs/cal.com/apps/web/app/api/video/guest-session', 'name': 'guest-session'}, {'path': '/home/ab/git-projs/cal.com/apps/web/app/e2e/sessi...
  L [explorer] glob
      pattern: *jwt*
  L [explorer] ✓ glob
      Result: {'result': 'Found 4 files', 'files': [{'path': '/home/ab/git-projs/cal.com/apps/api/v2/src/modules/jwt', 'name': 'jwt'}, {'path': '/home/ab/git-projs/cal.com/apps/api/v2/src/modules/jwt/jwt.module.ts'...
  L [explorer] glob
      pattern: *token*
  L [explorer] ✓ glob
      Result: {'result': 'Found 65 files', 'files': [{'path': '/home/ab/git-projs/cal.com/apps/api/v2/src/ee/provider/outputs/verify-access-token.output.ts', 'name': 'verify-access-token.output.ts'}, {'path': '/hom...
  L [explorer] extract_symbols
      path: /home/ab/git-projs/cal.com/packages/features/auth
  L [explorer] ✓ extract_symbols
      Result: {'path': '/home/ab/git-projs/cal.com/packages/features/auth', 'files_scanned': 44, 'symbol_count': 137, 'symbols': [{'file': 'packages/features/auth/PermissionContainer.tsx', 'name': 'AdminRequiredPro...
  L [explorer] extract_symbols
      path: /home/ab/git-projs/cal.com/packages/features/oauth
  L [explorer] ✓ extract_symbols
      Result: {'path': '/home/ab/git-projs/cal.com/packages/features/oauth', 'files_scanned': 5, 'symbol_count': 34, 'symbols': [{'file': 'packages/features/oauth/services/OAuthService.ts', 'name': 'OAuth2Client', ...
  L [explorer] extract_symbols
      path: /home/ab/git-projs/cal.com/packages/lib/auth
  L [explorer] ✓ extract_symbols
      Result: {'path': '/home/ab/git-projs/cal.com/packages/lib/auth', 'files_scanned': 2, 'symbol_count': 2, 'symbols': [{'file': 'packages/lib/auth/isPasswordValid.ts', 'name': 'isPasswordValid', 'type': 'functio...
  L [explorer] extract_symbols
      path: /home/ab/git-projs/cal.com/apps/web/server/lib/auth
  L [explorer] ✓ extract_symbols
      Result: {'path': '/home/ab/git-projs/cal.com/apps/web/server/lib/auth', 'files_scanned': 6, 'symbol_count': 9, 'symbols': [{'file': 'apps/web/server/lib/auth/login/getServerSideProps.tsx', 'name': 'getServerS...
  L [explorer] extract_symbols
      path: /home/ab/git-projs/cal.com/apps/api/v2/src/modules/oauth-clients
  L [explorer] ✓ extract_symbols
      Result: {'path': '/home/ab/git-projs/cal.com/apps/api/v2/src/modules/oauth-clients', 'files_scanned': 29, 'symbol_count': 109, 'symbols': [{'file': 'apps/api/v2/src/modules/oauth-clients/oauth-client.reposito...
  L [explorer] extract_symbols
      path: /home/ab/git-projs/cal.com/apps/api/v2/src/modules/auth
  L [explorer] ✓ extract_symbols
      Result: {'path': '/home/ab/git-projs/cal.com/apps/api/v2/src/modules/auth', 'files_scanned': 40, 'symbol_count': 147, 'symbols': [{'file':
'apps/api/v2/src/modules/auth/auth.module.ts', 'name': 'AuthModule', ...
  L [explorer] extract_symbols
      path: /home/ab/git-projs/cal.com/apps/api/v2/src/modules/jwt
  L [explorer] ✓ extract_symbols
      Result: {'path': '/home/ab/git-projs/cal.com/apps/api/v2/src/modules/jwt', 'files_scanned': 2, 'symbol_count': 9, 'symbols': [{'file': 'apps/api/v2/src/modules/jwt/jwt.service.ts', 'name': 'JwtService', 'type...
  L [explorer] extract_symbols
      path: /home/ab/git-projs/cal.com/apps/api/v2/src/modules/tokens
  L [explorer] ✓ extract_symbols
      Result: {'path': '/home/ab/git-projs/cal.com/apps/api/v2/src/modules/tokens', 'files_scanned': 3, 'symbol_count': 16, 'symbols': [{'file':
'apps/api/v2/src/modules/tokens/tokens.module.ts', 'name': 'TokensMod...
  L [explorer] read_file
      file_path: /home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-options.ts
      start_line: 497
      end_line: 600
  L [explorer] ✓ read_file
      Result: File: /home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-options.ts
Lines: 497-600 (Total: 1314)
--------------------------------------------------
export const getOptions = ({
  getDubId...
  L [explorer] read_file
      file_path: /home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-custom-adapter.ts
      start_line: 63
      end_line: 120
  L [explorer] ✓ read_file
      Result: File: /home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-custom-adapter.ts
Lines: 63-120 (Total: 170)
--------------------------------------------------
export default function CalComAdap...
  L [explorer] read_file
      file_path: /home/ab/git-projs/cal.com/apps/api/v2/src/modules/auth/strategies/api-auth/api-auth.strategy.ts
      start_line: 1
      end_line: 80
  L [explorer] ✓ read_file
      Result: File: /home/ab/git-projs/cal.com/apps/api/v2/src/modules/auth/strategies/api-auth/api-auth.strategy.ts
Lines: 1-80 (Total: 366)
--------------------------------------------------
import { sha256Hash, ...
  L [explorer] read_file
      file_path: /home/ab/git-projs/cal.com/apps/api/v2/src/modules/oauth-clients/controllers/oauth-flow/oauth-flow.c...
      start_line: 1
      end_line: 60
  L [explorer] ✓ read_file
      Result: File: /home/ab/git-projs/cal.com/apps/api/v2/src/modules/oauth-clients/controllers/oauth-flow/oauth-flow.controller.ts
Lines: 1-60 (Total: 134)
--------------------------------------------------
impor...
  L [explorer] read_file
      file_path: /home/ab/git-projs/cal.com/apps/api/v2/src/modules/oauth-clients/services/oauth-flow.service.ts
      start_line: 1
      end_line: 50
  L [explorer] ✓ read_file
      Result: File: /home/ab/git-projs/cal.com/apps/api/v2/src/modules/oauth-clients/services/oauth-flow.service.ts
Lines: 1-50 (Total: 178)
--------------------------------------------------
import { TokenExpiredE...
  L [explorer] ripgrep
      query: providers.*=.*\[
      path: /home/ab/git-projs/cal.com/packages/features/auth
  L [explorer] ✓ ripgrep
      Result: {'result': 'Found 1 matches', 'matches': [{'file': '/home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-options.ts', 'line': 280, 'content': 'const providers: Provider[] = [CalComCredentia...
  L [explorer] ripgrep
      query: CalComCredentialsProvider|ImpersonationProvider
      path: /home/ab/git-projs/cal.com/packages/features/auth
  L [explorer] ✓ ripgrep
      Result: {'result': 'Found 3 matches', 'matches': [{'file': '/home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-options.ts', 'line': 23, 'content': 'import ImpersonationProvider from "@calcom/feat...
  L [explorer] read_file
      file_path: /home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-options.ts
      start_line: 260
      end_line: 300
  L [explorer] ✓ read_file
      Result: File: /home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-options.ts
Lines: 260-300 (Total: 1314)
--------------------------------------------------
    return "INACTIVE_ADMIN";
  };

  //...
  L [explorer] ripgrep
      query: GoogleProvider|SAMLProvider
      path: /home/ab/git-projs/cal.com/packages/features/auth
  L [explorer] ✓ ripgrep
      Result: {'result': 'Found 2 matches', 'matches': [{'file': '/home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-options.ts', 'line': 10, 'content': 'import GoogleProvider from "next-auth/providers...
  L [explorer] ripgrep
      query: EMAIL|SAML
      path: /home/ab/git-projs/cal.com/packages/features/auth
  L [explorer] ✓ ripgrep
      Result: {'result': 'Found 48 matches', 'matches': [{'file': '/home/ab/git-projs/cal.com/packages/features/auth/SAMLLogin.tsx', 'line': 24,
'content': 'export function SAMLLogin({'}, {'file': '/home/ab/git-pro...
  L [explorer] read_file
      file_path: /home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-options.ts
      start_line: 295
      end_line: 350
  L [explorer] ✓ read_file
      Result: File: /home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-options.ts
Lines: 295-350 (Total: 1314)
--------------------------------------------------
    GoogleProvider({
      clientId: GO...
  L [explorer] read_file
      file_path: /home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-options.ts
      start_line: 310
      end_line: 370
  L [explorer] ✓ read_file
      Result: File: /home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-options.ts
Lines: 310-370 (Total: 1314)
--------------------------------------------------
if (isSAMLLoginEnabled) {
  providers.p...
  L [explorer] read_file
      file_path: /home/ab/git-projs/cal.com/apps/api/v2/src/modules/auth/strategies/api-auth/api-auth.strategy.ts
      start_line: 80
      end_line: 150
  L [explorer] ✓ read_file
      Result: File: /home/ab/git-projs/cal.com/apps/api/v2/src/modules/auth/strategies/api-auth/api-auth.strategy.ts
Lines: 80-150 (Total: 366)
--------------------------------------------------
        if (!apiKey...
  L [explorer] read_file
      file_path: /home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-options.ts
      start_line: 147
      end_line: 200
  L [explorer] ✓ read_file
      Result: File: /home/ab/git-projs/cal.com/packages/features/auth/lib/next-auth-options.ts
Lines: 147-200 (Total: 1314)
--------------------------------------------------
export async function authorizeCredenti...

============================================================
◆ SUBAGENT COMPLETE: [explorer]
============================================================

## DIRECT ANSWER

The Cal.com codebase uses a comprehensive, multi-layered authentication architecture built around **NextAuth.js** as the core authentication system, extended with custom OAuth 2.0 implementations, JWT-based sessions, and multiple identity providers. Here's how authentication works:

### **Authentication System Used**
- **Core Framework**: NextAuth.js for web authentication
- **API Layer**: Custom NestJS-based authentication system for v2 API
- **Session Strategy**: JWT-based s...
[... truncated 4404 chars ...]
============================================================

[info] [explorer] Complete

[tool] delegate ✓
(context window: 2.2%, total cost: $0.0)
🤖

Based on the exploration, here's how authentication works in the Cal.com codebase:

## Authentication Architecture Overview

The system uses a **multi-layered authentication approach** combining:

1. **NextAuth.js** for web authentication
2. **Custom NestJS API** for v2 API authentication
3. **OAuth 2.0 server** for third-party integrations
4. **JWT-based sessions** for both web and API

## Key Components

Let me examine the core configuration files to show you the actual implementation:


[tool] read_file
[tool] read_file ✓
(context window: 2.9%, total cost: $0.0)
🤖

Now let me examine the API v2 authentication system to give you a complete picture:


[tool] read_file
[tool] read_file ✓
(context window: 9.4%, total cost: $0.0)
🤖

Let me also check the OAuth 2.0 server implementation to give you a complete picture:


[tool] list_dir
[tool] list_dir ✓
(context window: 11.4%, total cost: $0.0)
🤖



[tool] read_file
[tool] read_file ✓
(context window: 11.6%, total cost: $0.0)
🤖

Based on my analysis of the Cal.com codebase, here's a comprehensive explanation of how authentication works:

## Authentication Architecture Overview

The Cal.com authentication system is a **multi-layered, enterprise-grade authentication platform** built with three main components:

### 1. **Web Authentication (NextAuth.js)**
- **Core Framework**: NextAuth.js for web-based authentication
- **Session Strategy**: JWT-based sessions with custom timeouts
- **Multi-Provider Support**: Google OAuth, SAML, and credentials (email/password)

### 2. **API v2 Authentication (NestJS)**
- **Multi-Method Authentication**: Supports 5 different authentication methods
- **Comprehensive Guards**: Organization, team, role, and permission checking
- **Scalable**: Built for third-party integrations and platform APIs

### 3. **OAuth 2.0 Server**
- **Full OAuth 2.0 Implementation**: Authorization Code, Client Credentials, and Refresh Token flows
- **Redis-based Caching**: High-performance token validation
- **Managed Clients**: Platform for third-party applications

---

## How Authentication Works in Detail

### **Web Authentication Flow (NextAuth.js)**

The web authentication system supports multiple identity providers:

#### **Credentials Provider (Email/Password)**
```typescript
// From next-auth-options.ts
export async function authorizeCredentials(credentials) {
  // 1. Find user by email
  const user = await userRepo.findByEmailAndIncludeProfilesAndPassword({
    email: credentials.email
  });

  // 2. Validate password with bcrypt
  const isCorrectPassword = await verifyPassword(credentials.password, user.password.hash);

  // 3. Check two-factor authentication
  if (user.twoFactorEnabled) {
    if (credentials.backupCode) {
      // Validate backup code
    } else if (credentials.totpCode) {
      // Validate TOTP code
    } else {
      // Require 2FA code
    }
  }

  // 4. Return authenticated user
  return AdapterUserPresenter.fromCalUser(user, validateRole(user.role), hasActiveTeams);
}
```

#### **Google OAuth Provider**
- Redirects to Google OAuth flow
- Handles callback with user profile information
- Auto-installs Google Calendar integration
- Updates profile photos automatically
- Handles account linking and identity merging

#### **SAML Provider (via BoxyHQ)**
- Full SAML 2.0 implementation
- Supports IdP-initiated and SP-initiated flows
- Account linking with validation to prevent takeover
- Organization auto-provisioning for hosted customers

### **API v2 Authentication Flow**

The API system supports **5 different authentication methods**:

#### **1. OAuth Client Credentials**
```typescript
// For third-party applications
authenticateOAuthClient(clientId, clientSecret, request) {
  // 1. Find OAuth client
  const client = await oauthRepository.getOAuthClient(clientId);

  // 2. Validate client secret
  if (client.secret !== clientSecret) {
    throw UnauthorizedException("Invalid client secret");
  }

  // 3. Find platform owner
  const platformCreatorId = await membershipsRepository.findPlatformOwnerUserId(client.organizationId);

  // 4. Return associated user
  return userRepository.findByIdWithProfile(platformCreatorId);
}
```

#### **2. API Keys**
- Hash-based validation using SHA256
- Supports custom prefixes (e.g., `cal_`)
- License validation for enterprise features
- Team-scoped access

#### **3. Access Tokens (JWT-based)**
- OAuth 2.0 access tokens
- Redis-based caching for performance
- Origin validation for security
- Automatic propagation to Redis

#### **4. NextAuth Sessions**
- Validates NextAuth JWT tokens
- Seamless web-to-API integration
- Email-based user lookup

#### **5. Third-Party Access Tokens**
- Custom token format
- User or team-based authorization
- Decoding and validation service

### **OAuth 2.0 Server Implementation**

The system includes a complete OAuth 2.0 server:

#### **Authorization Code Flow**
1. Client requests authorization
2. User approves permissions
3. Authorization code issued
4. Code exchanged for access/refresh tokens
5. Tokens validated and cached in Redis

#### **Token Management**
```typescript
// Redis-based token caching
async validateAccessToken(accessToken) {
  // 1. Check Redis cache first (fast path)
  const { status } = await readFromCache(accessToken);
  if (status === "CACHE_HIT") return true;

  // 2. Fallback to database validation
  const tokenExpiresAt = await tokensRepository.getAccessTokenExpiryDate(accessToken);

  // 3. Update cache for future requests
  await redisService.redis.hmset(cacheKey, { expiresAt: tokenExpiresAt.toJSON() });

  return true;
}
```

---

## Security Features

### **Multi-Layer Security**
- **Password Security**: bcrypt hashing with validation
- **Two-Factor Authentication**: TOTP and backup codes
- **Rate Limiting**: Per-user and per-IP limits
- **Email Verification**: Token-based verification system
- **Session Timeout**: Configurable session expiration

### **Advanced Features**
- **Profile Switching**: Multiple profiles per account
- **Organization Integration**: Auto-provisioning and linking
- **Impersonation**: Admin user impersonation
- **SAML Security**: Account linking validation
- **Origin Validation**: CORS and OAuth origin checking

---

## Key Files Architecture

- **`/packages/features/auth/lib/next-auth-options.ts`** - Core NextAuth configuration (1,314 lines)
- **`/apps/api/v2/src/modules/auth/strategies/api-auth/api-auth.strategy.ts`** - API authentication strategy
- **`/apps/api/v2/src/modules/oauth-clients/`** - Complete OAuth 2.0 server implementation

This authentication system provides **enterprise-grade security** with multiple authentication methods, comprehensive authorization, and high performance through Redis caching. It supports both web-based user authentication and API-based third-party integrations while maintaining security
through multiple layers of validation and permission checking.
(context window: 12.8%, total cost: $0.0)

