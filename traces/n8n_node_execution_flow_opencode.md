# Trace workflow execution flow (@explore subagent)

**Session ID:** ses_40ad74935ffexepPjm7MXEv3ap
**Created:** 1/25/2026, 12:37:24 PM
**Updated:** 1/25/2026, 12:41:16 PM

---

## User

I need to trace the flow of how a workflow JSON object sent from the frontend gets unmarshaled/unrolled and executed in the n8n codebase. Please:

1. Find the API endpoint that receives workflow JSON from the frontend
2. Trace how the JSON is processed and validated
3. Identify where the workflow execution engine takes over
4. Locate the core workflow execution logic
5. Find where individual nodes are executed

Focus on the key transition points from HTTP request to workflow execution. Look in packages/cli for API endpoints and packages/core for execution logic.

---

## Assistant (Explore · big-pickle · 13.8s)

_Thinking:_




I'll help you trace the workflow execution flow in n8n from frontend request to execution. Let me start by exploring the codebase structure and then follow the key transition points.

```
Tool: glob

**Input:**
```json
{
  "pattern": "packages/cli/**/*.ts"
}
```
**Output:**
```
/home/ab/git-projs/n8n/packages/cli/src/utils/cors.util.ts
/home/ab/git-projs/n8n/packages/cli/src/utils/__tests__/cors.util.test.ts
/home/ab/git-projs/n8n/packages/cli/src/credentials/credentials.service.ts
/home/ab/git-projs/n8n/packages/cli/test/migration/1766064542000-add-workflow-publish-scope-to-project-roles.test.ts
/home/ab/git-projs/n8n/packages/cli/test/setup-test-folder.ts
/home/ab/git-projs/n8n/packages/cli/test/migration/1763048000000-activate-execute-workflow-trigger-workflows.test.ts
/home/ab/git-projs/n8n/packages/cli/test/migration/1760020838000-unique-role-names.test.ts
/home/ab/git-projs/n8n/packages/cli/test/shared/external-secrets/utils.ts
/home/ab/git-projs/n8n/packages/cli/test/shared/helpers.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/dynamic-credentials.ee/credential-resolvers.api.test.ts
/home/ab/git-projs/n8n/packages/cli/src/wait-tracker.ts
/home/ab/git-projs/n8n/packages/cli/src/workflow-execute-additional-data.ts
/home/ab/git-projs/n8n/packages/cli/src/utils/handlebars.util.ts
/home/ab/git-projs/n8n/packages/cli/src/utils/validate-database-type.ts
/home/ab/git-projs/n8n/packages/cli/src/utils/sliding-window.ts
/home/ab/git-projs/n8n/packages/cli/src/utils/__tests__/circuit-breaker.test.ts
/home/ab/git-projs/n8n/packages/cli/src/utils/__tests__/validate-database-type.test.ts
/home/ab/git-projs/n8n/packages/cli/src/utils/__tests__/sliding-window.test.ts
/home/ab/git-projs/n8n/packages/cli/src/utils/circuit-breaker.ts
/home/ab/git-projs/n8n/packages/cli/src/sso.ee/sso-helpers.ts
/home/ab/git-projs/n8n/packages/cli/src/sso.ee/__tests__/sso-helpers.test.ts
/home/ab/git-projs/n8n/packages/cli/src/response-helper.ts
/home/ab/git-projs/n8n/packages/cli/src/scaling/worker-status.service.ee.ts
/home/ab/git-projs/n8n/packages/cli/src/ldap.ee/ldap.service.ee.ts
/home/ab/git-projs/n8n/packages/cli/src/ldap.ee/__tests__/ldap.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/ldap.ee/constants.ts
/home/ab/git-projs/n8n/packages/cli/src/load-nodes-and-credentials.ts
/home/ab/git-projs/n8n/packages/cli/src/credentials-helper.ts
/home/ab/git-projs/n8n/packages/cli/src/deprecation/deprecation.service.ts
/home/ab/git-projs/n8n/packages/cli/src/credentials/dynamic-credential-storage.interface.ts
/home/ab/git-projs/n8n/packages/cli/src/deprecation/__tests__/deprecation.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/credentials/__tests__/credentials.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/credentials/__tests__/dynamic-credentials-proxy.test.ts
/home/ab/git-projs/n8n/packages/cli/src/credentials/__tests__/credentials.controller.test.ts
/home/ab/git-projs/n8n/packages/cli/src/command-registry.ts
/home/ab/git-projs/n8n/packages/cli/src/concurrency/concurrency-control.service.ts
/home/ab/git-projs/n8n/packages/cli/src/concurrency/__tests__/concurrency-control.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/active-executions.ts
/home/ab/git-projs/n8n/packages/cli/src/abstract-server.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/load-nodes-and-credentials.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/manual-execution.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/workflow-runner.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/wait-tracker.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/active-executions.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/response-helper.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/license.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/credentials-helper.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/workflow-execute-additional-data.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/active-workflow-manager.test.ts
/home/ab/git-projs/n8n/packages/cli/test/migration/migration-test-helpers.test.ts
/home/ab/git-projs/n8n/packages/cli/src/utils/compression.util.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/workflow-helpers.test.ts
/home/ab/git-projs/n8n/packages/cli/test/teardown.ts
/home/ab/git-projs/n8n/packages/cli/test/setup.ts
/home/ab/git-projs/n8n/packages/cli/test/setup-mocks.ts
/home/ab/git-projs/n8n/packages/cli/test/shared/mock-objects.ts
/home/ab/git-projs/n8n/packages/cli/test/shared/mocking.ts
/home/ab/git-projs/n8n/packages/cli/test/shared/test-data.ts
/home/ab/git-projs/n8n/packages/cli/src/zod-alias-support.ts
/home/ab/git-projs/n8n/packages/cli/test/extend-expect.ts
/home/ab/git-projs/n8n/packages/cli/src/utils.ts
/home/ab/git-projs/n8n/packages/cli/src/typed-emitter.ts
/home/ab/git-projs/n8n/packages/cli/src/utils/object-to-error.ts
/home/ab/git-projs/n8n/packages/cli/src/utils/__tests__/object-to-error.test.ts
/home/ab/git-projs/n8n/packages/cli/src/utils/__tests__/get-item-count-by-connection-type.test.ts
/home/ab/git-projs/n8n/packages/cli/src/utils/get-item-count-by-connection-type.ts
/home/ab/git-projs/n8n/packages/cli/src/sso.ee/saml/views/init-sso-post.ts
/home/ab/git-projs/n8n/packages/cli/src/sso.ee/saml/service-provider.ee.ts
/home/ab/git-projs/n8n/packages/cli/src/sso.ee/saml/schema/saml-schema-assertion-2.0.xsd.ts
/home/ab/git-projs/n8n/packages/cli/src/sso.ee/saml/schema/metadata-exchange.xsd.ts
/home/ab/git-projs/n8n/packages/cli/src/ldap.ee/helpers.ee.ts
/home/ab/git-projs/n8n/packages/cli/src/index.ts
/home/ab/git-projs/n8n/packages/cli/src/ldap.ee/__tests__/helpers.test.ts
/home/ab/git-projs/n8n/packages/cli/src/ldap.ee/ldap.controller.ee.ts
/home/ab/git-projs/n8n/packages/cli/src/ldap.ee/types.ts
/home/ab/git-projs/n8n/packages/cli/src/evaluation.ee/test-runs.types.ee.ts
/home/ab/git-projs/n8n/packages/cli/src/evaluation.ee/__tests__/test-runs.controller.ee.test.ts
/home/ab/git-projs/n8n/packages/cli/src/evaluation.ee/test-runs.controller.ee.ts
/home/ab/git-projs/n8n/packages/cli/src/evaluation.ee/test-runner/evaluation-metrics.ee.ts
/home/ab/git-projs/n8n/packages/cli/src/evaluation.ee/test-runner/__tests__/evaluation-metrics.ee.test.ts
/home/ab/git-projs/n8n/packages/cli/src/evaluation.ee/test-runner/test-run-cleanup.service.ee.ts
/home/ab/git-projs/n8n/packages/cli/src/errors/response-errors/invalid-mfa-recovery-code-error.ts
/home/ab/git-projs/n8n/packages/cli/src/crash-journal.ts
/home/ab/git-projs/n8n/packages/cli/src/credential-types.ts
/home/ab/git-projs/n8n/packages/cli/src/credentials/__tests__/credentials.test-data.ts
/home/ab/git-projs/n8n/packages/cli/src/concurrency/concurrency-queue.ts
/home/ab/git-projs/n8n/packages/cli/src/concurrency/__tests__/concurrency-queue.test.ts
/home/ab/git-projs/n8n/packages/cli/src/collaboration/collaboration.message.ts
/home/ab/git-projs/n8n/packages/cli/src/collaboration/collaboration.service.ts
/home/ab/git-projs/n8n/packages/cli/src/collaboration/__tests__/collaboration.state.test.ts
/home/ab/git-projs/n8n/packages/cli/src/collaboration/collaboration.state.ts
/home/ab/git-projs/n8n/packages/cli/src/activation-errors.service.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/project.test-data.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/node-types.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/external-hooks.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/controller.registry.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/command-registry.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/credentials-overwrites.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/utils.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/credential-types.test.ts

(Results are truncated. Consider using a more specific path or pattern.)
```
```

---

## Assistant (Explore · big-pickle · 2.4s)

_Thinking:_





```
Tool: glob

**Input:**
```json
{
  "pattern": "packages/cli/**/workflow*.ts"
}
```
**Output:**
```
/home/ab/git-projs/n8n/packages/cli/test/integration/shared/workflow-fixtures.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/workflow-history-compaction.service.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/workflows/workflows.controller.test.ts
/home/ab/git-projs/n8n/packages/cli/src/services/pruning/__tests__/workflow-history-compaction.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/services/pruning/workflow-history-compaction.service.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/__tests__/workflows.controller.test.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflows.controller.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/database/repositories/workflow-history.repository.test.ts
/home/ab/git-projs/n8n/packages/cli/src/commands/import/workflow.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/workflow-helpers.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/workflow-history-manager.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/workflow-history.api.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/workflows/workflow.service.ee.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/workflows/workflows.controller-with-active-workflow-manager.ee.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/workflows/workflows.controller.ee.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/workflows/workflow-index.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/workflows/workflow.service.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/shared/db/workflow-statistics.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/shared/db/workflow-publish-history.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/shared/db/workflow-history.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/public-api/workflows.test.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-history/workflow-history.service.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-history/workflow-history.controller.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-history/workflow-history-manager.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-history/__tests__/workflow-history-helper.test.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-history/__tests__/workflow-history.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-history/__tests__/workflow-history.controller.test.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-history/workflow-history-helper.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow.service.ee.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow.request.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow.service.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-validation.service.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/database/repositories/workflow-dependency.repository.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/database/repositories/workflow-publish-history.repository.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/database/repositories/workflow.repository.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/commands/unpublish/workflow.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/commands/update/workflow.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/commands/publish/workflow.test.ts
/home/ab/git-projs/n8n/packages/cli/src/workflow-helpers.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-finder.service.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/__tests__/workflow-execution.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/__tests__/workflow-validation.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/__tests__/workflow.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-execution.service.ts
/home/ab/git-projs/n8n/packages/cli/src/workflow-execute-additional-data.ts
/home/ab/git-projs/n8n/packages/cli/src/workflow-runner.ts
/home/ab/git-projs/n8n/packages/cli/src/services/__tests__/workflow-statistics.service.integration.test.ts
/home/ab/git-projs/n8n/packages/cli/src/services/workflow-statistics.service.ts
/home/ab/git-projs/n8n/packages/cli/src/modules/workflow-index/workflow-index.service.ts
/home/ab/git-projs/n8n/packages/cli/src/modules/workflow-index/__tests__/workflow-index.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/public-api/v1/handlers/workflows/workflows.handler.ts
/home/ab/git-projs/n8n/packages/cli/src/public-api/v1/handlers/workflows/workflows.service.ts
/home/ab/git-projs/n8n/packages/cli/src/modules/dynamic-credentials.ee/workflow-status.controller.ts
/home/ab/git-projs/n8n/packages/cli/src/modules/dynamic-credentials.ee/__tests__/workflow-status.controller.test.ts
/home/ab/git-projs/n8n/packages/cli/src/modules/breaking-changes/rules/v2/__tests__/workflow-hooks-deprecated.rule.test.ts
/home/ab/git-projs/n8n/packages/cli/src/modules/breaking-changes/rules/v2/workflow-hooks-deprecated.rule.ts
/home/ab/git-projs/n8n/packages/cli/src/middlewares/list-query/dtos/workflow.select.dto.ts
/home/ab/git-projs/n8n/packages/cli/src/middlewares/list-query/dtos/workflow.filter.dto.ts
/home/ab/git-projs/n8n/packages/cli/src/errors/response-errors/workflow-validation.error.ts
/home/ab/git-projs/n8n/packages/cli/src/commands/unpublish/workflow.ts
/home/ab/git-projs/n8n/packages/cli/src/commands/update/workflow.ts
/home/ab/git-projs/n8n/packages/cli/src/commands/publish/workflow.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/workflow-runner.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/workflow-execute-additional-data.test.ts
/home/ab/git-projs/n8n/packages/cli/src/__tests__/workflow-helpers.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/shared/workflow.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/workflow-tag-mapping.repository.integration.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/workflows/workflow-sharing.service.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/services/workflow-static-data.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-sharing.service.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow.formatter.ts
/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-static-data.service.ts
/home/ab/git-projs/n8n/packages/cli/src/services/workflow-loader.service.ts
/home/ab/git-projs/n8n/packages/cli/src/middlewares/list-query/dtos/workflow.sort-by.dto.ts
/home/ab/git-projs/n8n/packages/cli/src/errors/workflow-history-version-not-found.error.ts
/home/ab/git-projs/n8n/packages/cli/src/errors/workflow-missing-id.error.ts
/home/ab/git-projs/n8n/packages/cli/src/errors/workflow-crashed.error.ts
/home/ab/git-projs/n8n/packages/cli/src/databases/repositories/__tests__/workflow-statistics.integration.test.ts
/home/ab/git-projs/n8n/packages/cli/src/controllers/workflow-statistics.controller.ts
/home/ab/git-projs/n8n/packages/cli/src/controllers/workflow-statistics.types.ts
/home/ab/git-projs/n8n/packages/cli/src/commands/list/workflow.ts
/home/ab/git-projs/n8n/packages/cli/src/commands/export/workflow.ts
```
```

---

## Assistant (Explore · big-pickle · 2.5s)

_Thinking:_





```
Tool: glob

**Input:**
```json
{
  "pattern": "packages/cli/**/execut*.ts"
}
```
**Output:**
```
/home/ab/git-projs/n8n/packages/cli/test/integration/executions.controller.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/database/repositories/execution.repository.test.ts
/home/ab/git-projs/n8n/packages/cli/src/executions/__tests__/execution.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/executions/__tests__/executions.controller.test.ts
/home/ab/git-projs/n8n/packages/cli/src/executions/execution.types.ts
/home/ab/git-projs/n8n/packages/cli/src/executions/execution.service.ts
/home/ab/git-projs/n8n/packages/cli/src/executions/executions.controller.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/execution-context-propagation.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/execution.service.integration.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/shared/execution-context-helpers.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/execution.repository.test.ts
/home/ab/git-projs/n8n/packages/cli/src/services/pruning/__tests__/executions-pruning.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/services/pruning/executions-pruning.service.ts
/home/ab/git-projs/n8n/packages/cli/src/modules/mcp/__tests__/execute-workflow.tool.test.ts
/home/ab/git-projs/n8n/packages/cli/src/modules/mcp/tools/execute-workflow.tool.ts
/home/ab/git-projs/n8n/packages/cli/src/execution-lifecycle/execution-lifecycle-hooks.ts
/home/ab/git-projs/n8n/packages/cli/src/executions/__tests__/execution-recovery.service.integration.test.ts
/home/ab/git-projs/n8n/packages/cli/src/executions/__tests__/execution-data.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/executions/execution-data.service.ts
/home/ab/git-projs/n8n/packages/cli/src/executions/execution-recovery.service.ts
/home/ab/git-projs/n8n/packages/cli/src/executions/execution.utils.ts
/home/ab/git-projs/n8n/packages/cli/src/execution-lifecycle/__tests__/execution-lifecycle-hooks.test.ts
/home/ab/git-projs/n8n/packages/cli/src/execution-lifecycle/execute-error-workflow.ts
/home/ab/git-projs/n8n/packages/cli/src/errors/execution-already-resuming.error.ts
/home/ab/git-projs/n8n/packages/cli/src/databases/repositories/__tests__/execution.repository.test.ts
/home/ab/git-projs/n8n/packages/cli/src/commands/execute.ts
/home/ab/git-projs/n8n/packages/cli/src/commands/__tests__/execute.test.ts
/home/ab/git-projs/n8n/packages/cli/src/commands/__tests__/execute-batch.test.ts
/home/ab/git-projs/n8n/packages/cli/src/commands/execute-batch.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/shared/db/executions.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/public-api/executions.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/services/execution-metadata.service.test.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/executions-pruning.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/services/__tests__/execution-metadata.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/services/execution-metadata.service.ts
/home/ab/git-projs/n8n/packages/cli/src/public-api/v1/handlers/executions/executions.handler.ts
/home/ab/git-projs/n8n/packages/cli/src/executions/execution.service.ee.ts
/home/ab/git-projs/n8n/packages/cli/src/errors/execution-not-found-error.ts
```
```

---

## Assistant (Explore · big-pickle · 2.6s)

_Thinking:_




Now let me look at the main entry point and routing to understand the API structure:

```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/cli/src/index.ts"
}
```
**Output:**
```
<file>
00001| export {};
00002| 

(End of file - total 2 lines)
</file>
```
```

---

## Assistant (Explore · big-pickle · 26.7s)

_Thinking:_




Let me look at the main server file:

```
Tool: glob

**Input:**
```json
{
  "pattern": "packages/cli/src/server.ts"
}
```
**Output:**
```
/home/ab/git-projs/n8n/packages/cli/src/server.ts
```
```

---

## Assistant (Explore · big-pickle · 4.3s)

_Thinking:_





```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/cli/src/server.ts"
}
```
**Output:**
```
<file>
00001| import { inDevelopment, inProduction } from '@n8n/backend-common';
00002| import { DatabaseConfig, SecurityConfig, WorkflowsConfig } from '@n8n/config';
00003| import { Time } from '@n8n/constants';
00004| import type { APIRequest, AuthenticatedRequest } from '@n8n/db';
00005| import { Container, Service } from '@n8n/di';
00006| import cookieParser from 'cookie-parser';
00007| import express from 'express';
00008| import { access as fsAccess } from 'fs/promises';
00009| import helmet from 'helmet';
00010| import isEmpty from 'lodash/isEmpty';
00011| import { InstanceSettings, installGlobalProxyAgent } from 'n8n-core';
00012| import { jsonParse } from 'n8n-workflow';
00013| import { resolve } from 'path';
00014| 
00015| import { AbstractServer } from '@/abstract-server';
00016| import { AuthService } from '@/auth/auth.service';
00017| import { CLI_DIR, EDITOR_UI_DIST_DIR, inE2ETests } from '@/constants';
00018| import { ControllerRegistry } from '@/controller.registry';
00019| import { CredentialsOverwrites } from '@/credentials-overwrites';
00020| import { MessageEventBus } from '@/eventbus/message-event-bus/message-event-bus';
00021| import { EventService } from '@/events/event.service';
00022| import { LogStreamingEventRelay } from '@/events/relays/log-streaming.event-relay';
00023| import type { ICredentialsOverwrite } from '@/interfaces';
00024| import { isLdapEnabled } from '@/ldap.ee/helpers.ee';
00025| import { LoadNodesAndCredentials } from '@/load-nodes-and-credentials';
00026| import { handleMfaDisable, isMfaFeatureEnabled } from '@/mfa/helpers';
00027| import { PostHogClient } from '@/posthog';
00028| import { isApiEnabled, loadPublicApiVersions } from '@/public-api';
00029| import { Push } from '@/push';
00030| import * as ResponseHelper from '@/response-helper';
00031| import type { FrontendService } from '@/services/frontend.service';
00032| 
00033| import '@/controllers/active-workflows.controller';
00034| import '@/controllers/annotation-tags.controller.ee';
00035| import '@/controllers/auth.controller';
00036| import '@/controllers/binary-data.controller';
00037| import '@/controllers/ai.controller';
00038| import '@/controllers/dynamic-node-parameters.controller';
00039| import '@/controllers/invitation.controller';
00040| import '@/controllers/me.controller';
00041| import '@/controllers/node-types.controller';
00042| import '@/controllers/oauth/oauth1-credential.controller';
00043| import '@/controllers/oauth/oauth2-credential.controller';
00044| import '@/controllers/orchestration.controller';
00045| import '@/controllers/owner.controller';
00046| import '@/controllers/password-reset.controller';
00047| import '@/controllers/project.controller';
00048| import '@/controllers/role.controller';
00049| import '@/controllers/tags.controller';
00050| import '@/controllers/translation.controller';
00051| import '@/controllers/folder.controller';
00052| import '@/controllers/users.controller';
00053| import '@/controllers/user-settings.controller';
00054| import '@/controllers/workflow-statistics.controller';
00055| import '@/controllers/api-keys.controller';
00056| import '@/credentials/credentials.controller';
00057| import '@/eventbus/event-bus.controller';
00058| import '@/events/events.controller';
00059| import '@/executions/executions.controller';
00060| import '@/license/license.controller';
00061| import '@/evaluation.ee/test-runs.controller.ee';
00062| import '@/workflows/workflow-history/workflow-history.controller';
00063| import '@/workflows/workflows.controller';
00064| import '@/webhooks/webhooks.controller';
00065| 
00066| import { ChatServer } from './chat/chat-server';
00067| import { MfaService } from './mfa/mfa.service';
00068| import { PubSubRegistry } from './scaling/pubsub/pubsub.registry';
00069| 
00070| @Service()
00071| export class Server extends AbstractServer {
00072| 	private endpointPresetCredentials: string;
00073| 
00074| 	private presetCredentialsLoaded: boolean;
00075| 
00076| 	private frontendService?: FrontendService;
00077| 
00078| 	constructor(
00079| 		private readonly loadNodesAndCredentials: LoadNodesAndCredentials,
00080| 		private readonly postHogClient: PostHogClient,
00081| 		private readonly eventService: EventService,
00082| 		private readonly instanceSettings: InstanceSettings,
00083| 	) {
00084| 		super();
00085| 
00086| 		this.testWebhooksEnabled = true;
00087| 		this.webhooksEnabled = !this.globalConfig.endpoints.disableProductionWebhooksOnMainProcess;
00088| 	}
00089| 
00090| 	async start() {
00091| 		if (!this.globalConfig.endpoints.disableUi) {
00092| 			const { FrontendService } = await import('@/services/frontend.service');
00093| 			this.frontendService = Container.get(FrontendService);
00094| 			await import('@/controllers/module-settings.controller');
00095| 			await import('@/controllers/third-party-licenses.controller');
00096| 		}
00097| 
00098| 		this.presetCredentialsLoaded = false;
00099| 
00100| 		this.endpointPresetCredentials = this.globalConfig.credentials.overwrite.endpoint;
00101| 
00102| 		await super.start();
00103| 		this.logger.debug(`Server ID: ${this.instanceSettings.hostId}`);
00104| 
00105| 		if (inDevelopment && process.env.N8N_DEV_RELOAD === 'true') {
00106| 			void this.loadNodesAndCredentials.setupHotReload();
00107| 		}
00108| 
00109| 		this.eventService.emit('server-started');
00110| 	}
00111| 
00112| 	private async registerAdditionalControllers() {
00113| 		if (!inProduction && this.instanceSettings.isMultiMain) {
00114| 			await import('@/controllers/debug.controller');
00115| 		}
00116| 
00117| 		if (isLdapEnabled()) {
00118| 			const { LdapService } = await import('@/ldap.ee/ldap.service.ee');
00119| 			await import('@/ldap.ee/ldap.controller.ee');
00120| 			await Container.get(LdapService).init();
00121| 		}
00122| 
00123| 		if (inE2ETests) {
00124| 			await import('@/controllers/e2e.controller');
00125| 		}
00126| 
00127| 		if (isMfaFeatureEnabled()) {
00128| 			await Container.get(MfaService).init();
00129| 			await import('@/controllers/mfa.controller');
00130| 		}
00131| 
00132| 		if (!this.globalConfig.endpoints.disableUi) {
00133| 			await import('@/controllers/cta.controller');
00134| 		}
00135| 
00136| 		if (!this.globalConfig.tags.disabled) {
00137| 			await import('@/controllers/tags.controller');
00138| 		}
00139| 
00140| 		// ----------------------------------------
00141| 		// SAML
00142| 		// ----------------------------------------
00143| 
00144| 		// initialize SamlService if it is licensed, even if not enabled, to
00145| 		// set up the initial environment
00146| 		try {
00147| 			const { SamlService } = await import('@/sso.ee/saml/saml.service.ee');
00148| 			await Container.get(SamlService).init();
00149| 			await import('@/sso.ee/saml/routes/saml.controller.ee');
00150| 		} catch (error) {
00151| 			this.logger.warn(`SAML initialization failed: ${(error as Error).message}`);
00152| 		}
00153| 
00154| 		if (this.globalConfig.diagnostics.enabled) {
00155| 			await import('@/controllers/telemetry.controller');
00156| 			await import('@/controllers/posthog.controller');
00157| 		}
00158| 
00159| 		// ----------------------------------------
00160| 		// OIDC
00161| 		// ----------------------------------------
00162| 
00163| 		try {
00164| 			// in the short term, we load the OIDC module here to ensure it is initialized
00165| 			// ideally we want to migrate this to a module and be able to load it dynamically
00166| 			// when the license changes, but that requires some refactoring
00167| 			const { OidcService } = await import('@/sso.ee/oidc/oidc.service.ee');
00168| 			await Container.get(OidcService).init();
00169| 			await import('@/sso.ee/oidc/routes/oidc.controller.ee');
00170| 		} catch (error) {
00171| 			this.logger.warn(`OIDC initialization failed: ${(error as Error).message}`);
00172| 		}
00173| 
00174| 		// ----------------------------------------
00175| 		// Source Control
00176| 		// ----------------------------------------
00177| 
00178| 		try {
00179| 			const { SourceControlService } = await import(
00180| 				'@/environments.ee/source-control/source-control.service.ee'
00181| 			);
00182| 			await Container.get(SourceControlService).init();
00183| 			await import('@/environments.ee/source-control/source-control.controller.ee');
00184| 		} catch (error) {
00185| 			this.logger.warn(`Source control initialization failed: ${(error as Error).message}`);
00186| 		}
00187| 
00188| 		try {
00189| 			await import('@/environments.ee/variables/variables.controller.ee');
00190| 		} catch (error) {
00191| 			this.logger.warn(`Variables initialization failed: ${(error as Error).message}`);
00192| 		}
00193| 	}
00194| 
00195| 	async configure(): Promise<void> {
00196| 		if (this.globalConfig.endpoints.metrics.enable) {
00197| 			const { PrometheusMetricsService } = await import('@/metrics/prometheus-metrics.service');
00198| 			await Container.get(PrometheusMetricsService).init(this.app);
00199| 		}
00200| 
00201| 		const { frontendService } = this;
00202| 		if (frontendService) {
00203| 			await this.externalHooks.run('frontend.settings', [await frontendService.getSettings()]);
00204| 		}
00205| 
00206| 		await this.postHogClient.init();
00207| 
00208| 		const publicApiEndpoint = this.globalConfig.publicApi.path;
00209| 
00210| 		// ----------------------------------------
00211| 		// Public API
00212| 		// ----------------------------------------
00213| 
00214| 		if (isApiEnabled()) {
00215| 			const { apiRouters, apiLatestVersion } = await loadPublicApiVersions(publicApiEndpoint);
00216| 			this.app.use(...apiRouters);
00217| 			if (frontendService) {
00218| 				(await frontendService.getSettings()).publicApi.latestVersion = apiLatestVersion;
00219| 			}
00220| 		}
00221| 
00222| 		// Extract BrowserId from headers
00223| 		this.app.use((req: APIRequest, _, next) => {
00224| 			req.browserId = req.headers['browser-id'] as string;
00225| 			next();
00226| 		});
00227| 
00228| 		// Parse cookies for easier access
00229| 		this.app.use(cookieParser());
00230| 
00231| 		const { restEndpoint, app } = this;
00232| 
00233| 		const push = Container.get(Push);
00234| 		push.setupPushHandler(restEndpoint, app);
00235| 
00236| 		if (push.isBidirectional) {
00237| 			const { CollaborationService } = await import('@/collaboration/collaboration.service');
00238| 
00239| 			const collaborationService = Container.get(CollaborationService);
00240| 			collaborationService.init();
00241| 		} else {
00242| 			this.logger.warn(
00243| 				'Collaboration features are disabled because push is configured unidirectional. Use N8N_PUSH_BACKEND=websocket environment variable to enable them.',
00244| 			);
00245| 		}
00246| 
00247| 		if (this.globalConfig.executions.mode === 'queue') {
00248| 			const { ScalingService } = await import('@/scaling/scaling.service');
00249| 			await Container.get(ScalingService).setupQueue();
00250| 		}
00251| 
00252| 		await handleMfaDisable();
00253| 
00254| 		await this.registerAdditionalControllers();
00255| 
00256| 		// Reinitialize the PubSubRegistry
00257| 		Container.get(PubSubRegistry).init();
00258| 
00259| 		// register all known controllers
00260| 		Container.get(ControllerRegistry).activate(app);
00261| 
00262| 		// ----------------------------------------
00263| 		// Options
00264| 		// ----------------------------------------
00265| 
00266| 		// Returns all the available timezones
00267| 		const tzDataFile = resolve(CLI_DIR, 'dist/timezones.json');
00268| 		this.app.get(`/${this.restEndpoint}/options/timezones`, (_, res) =>
00269| 			res.sendFile(tzDataFile, { dotfiles: 'allow' }),
00270| 		);
00271| 
00272| 		this.configureSettingsRoute();
00273| 
00274| 		// ----------------------------------------
00275| 		// EventBus Setup
00276| 		// ----------------------------------------
00277| 		const eventBus = Container.get(MessageEventBus);
00278| 		await eventBus.initialize();
00279| 		Container.get(LogStreamingEventRelay).init();
00280| 
00281| 		// ----------------------------------------
00282| 		// Workflow Indexing Setup
00283| 		// ----------------------------------------
00284| 		await this.initializeWorkflowIndexing();
00285| 
00286| 		if (this.endpointPresetCredentials !== '') {
00287| 			// POST endpoint to set preset credentials
00288| 			const overwriteEndpointMiddleware =
00289| 				Container.get(CredentialsOverwrites).getOverwriteEndpointMiddleware();
00290| 
00291| 			if (overwriteEndpointMiddleware) {
00292| 				this.app.use(`/${this.endpointPresetCredentials}`, overwriteEndpointMiddleware);
00293| 			}
00294| 
00295| 			const authenticationEnforced = overwriteEndpointMiddleware !== null;
00296| 			this.app.post(
00297| 				`/${this.endpointPresetCredentials}`,
00298| 				async (req: express.Request, res: express.Response) => {
00299| 					// If authentication is enforced we can allow multiple overwrites
00300| 					if (!this.presetCredentialsLoaded || authenticationEnforced) {
00301| 						const body = req.body as ICredentialsOverwrite;
00302| 
00303| 						if (req.contentType !== 'application/json') {
00304| 							ResponseHelper.sendErrorResponse(
00305| 								res,
00306| 								new Error(
00307| 									'Body must be a valid JSON, make sure the content-type is application/json',
00308| 								),
00309| 							);
00310| 							return;
00311| 						}
00312| 
00313| 						await Container.get(CredentialsOverwrites).setData(body, true, true);
00314| 
00315| 						this.presetCredentialsLoaded = true;
00316| 
00317| 						ResponseHelper.sendSuccessResponse(res, { success: true }, true, 200);
00318| 					} else {
00319| 						ResponseHelper.sendErrorResponse(res, new Error('Preset credentials can be set once'));
00320| 					}
00321| 				},
00322| 			);
00323| 		}
00324| 
00325| 		const maxAge = Time.days.toMilliseconds;
00326| 		const cacheOptions = inE2ETests || inDevelopment ? {} : { maxAge };
00327| 		const { staticCacheDir } = Container.get(InstanceSettings);
00328| 
00329| 		// Protect type files with authentication regardless of UI availability
00330| 		const authService = Container.get(AuthService);
00331| 		const protectedTypeFiles = ['/types/nodes.json', '/types/credentials.json'];
00332| 		protectedTypeFiles.forEach((path) => {
00333| 			this.app.get(
00334| 				path,
00335| 				authService.createAuthMiddleware({ allowSkipMFA: true, allowSkipPreviewAuth: true }),
00336| 				async (_, res: express.Response) => {
00337| 					res.setHeader('Cache-Control', 'no-cache, must-revalidate');
00338| 					res.sendFile(path.substring(1), {
00339| 						root: staticCacheDir,
00340| 					});
00341| 				},
00342| 			);
00343| 		});
00344| 
00345| 		if (frontendService) {
00346| 			this.app.use(
00347| 				[
00348| 					'/icons/{@:scope/}:packageName/*path/*file.svg',
00349| 					'/icons/{@:scope/}:packageName/*path/*file.png',
00350| 				],
00351| 				async (req, res) => {
00352| 					// eslint-disable-next-line prefer-const
00353| 					let { scope, packageName } = req.params;
00354| 					if (scope) packageName = `@${scope}/${packageName}`;
00355| 					const filePath = this.loadNodesAndCredentials.resolveIcon(packageName, req.originalUrl);
00356| 					if (filePath) {
00357| 						try {
00358| 							await fsAccess(filePath);
00359| 							return res.sendFile(filePath, { maxAge, dotfiles: 'allow' });
00360| 						} catch {}
00361| 					}
00362| 					res.sendStatus(404);
00363| 				},
00364| 			);
00365| 
00366| 			const serveSchemas: express.RequestHandler = async (req, res) => {
00367| 				const { node, version, resource, operation } = req.params;
00368| 				const filePath = this.loadNodesAndCredentials.resolveSchema({
00369| 					node,
00370| 					resource,
00371| 					operation,
00372| 					version,
00373| 				});
00374| 
00375| 				if (filePath) {
00376| 					try {
00377| 						await fsAccess(filePath);
00378| 						return res.sendFile(filePath, { ...cacheOptions, dotfiles: 'allow' });
00379| 					} catch {}
00380| 				}
00381| 				res.sendStatus(404);
00382| 			};
00383| 			this.app.use('/schemas/:node/:version{/:resource}{/:operation}.json', serveSchemas);
00384| 
00385| 			const isTLSEnabled =
00386| 				this.globalConfig.protocol === 'https' && !!(this.sslKey && this.sslCert);
00387| 			const isPreviewMode = process.env.N8N_PREVIEW_MODE === 'true';
00388| 			const cspDirectives = jsonParse<{ [key: string]: Iterable<string> }>(
00389| 				Container.get(SecurityConfig).contentSecurityPolicy,
00390| 				{
00391| 					errorMessage: 'The contentSecurityPolicy is not valid JSON.',
00392| 				},
00393| 			);
00394| 			const cspReportOnly = Container.get(SecurityConfig).contentSecurityPolicyReportOnly;
00395| 			const securityHeadersMiddleware = helmet({
00396| 				contentSecurityPolicy: isEmpty(cspDirectives)
00397| 					? false
00398| 					: {
00399| 							useDefaults: false,
00400| 							reportOnly: cspReportOnly,
00401| 							directives: {
00402| 								...cspDirectives,
00403| 							},
00404| 						},
00405| 				xFrameOptions:
00406| 					isPreviewMode || inE2ETests || inDevelopment ? false : { action: 'sameorigin' },
00407| 				dnsPrefetchControl: false,
00408| 				// This is only relevant for Internet-explorer, which we do not support
00409| 				ieNoOpen: false,
00410| 				// This is already disabled in AbstractServer
00411| 				xPoweredBy: false,
00412| 				// Enable HSTS headers only when n8n handles TLS.
00413| 				// if n8n is behind a reverse-proxy, then these headers needs to be configured there
00414| 				strictTransportSecurity: isTLSEnabled
00415| 					? {
00416| 							maxAge: 180 * Time.days.toSeconds,
00417| 							includeSubDomains: false,
00418| 							preload: false,
00419| 						}
00420| 					: false,
00421| 			});
00422| 
00423| 			// Route all UI urls to index.html to support history-api
00424| 			const nonUIRoutes: readonly string[] = [
00425| 				'favicon.ico',
00426| 				'assets',
00427| 				'static',
00428| 				'types',
00429| 				'healthz',
00430| 				'metrics',
00431| 				'e2e',
00432| 				this.restEndpoint,
00433| 				this.endpointPresetCredentials,
00434| 				isApiEnabled() ? '' : publicApiEndpoint,
00435| 				...this.globalConfig.endpoints.additionalNonUIRoutes.split(':'),
00436| 			].filter((u) => !!u);
00437| 			const nonUIRoutesRegex = new RegExp(`^/(${nonUIRoutes.join('|')})/?.*$`);
00438| 			const historyApiHandler: express.RequestHandler = (req, res, next) => {
00439| 				const {
00440| 					method,
00441| 					headers: { accept },
00442| 				} = req;
00443| 				if (
00444| 					method === 'GET' &&
00445| 					accept &&
00446| 					(accept.includes('text/html') || accept.includes('*/*')) &&
00447| 					!req.path.endsWith('.wasm') &&
00448| 					!nonUIRoutesRegex.test(req.path)
00449| 				) {
00450| 					res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate, proxy-revalidate');
00451| 					securityHeadersMiddleware(req, res, () => {
00452| 						res.sendFile('index.html', { root: staticCacheDir, maxAge: 0, lastModified: false });
00453| 					});
00454| 				} else {
00455| 					next();
00456| 				}
00457| 			};
00458| 			const setCustomCacheHeader = (res: express.Response) => {
00459| 				if (/^\/types\/(nodes|credentials).json$/.test(res.req.url)) {
00460| 					res.setHeader('Cache-Control', 'no-cache, must-revalidate');
00461| 				}
00462| 			};
00463| 
00464| 			this.app.use(
00465| 				'/',
00466| 				historyApiHandler,
00467| 				express.static(staticCacheDir, {
00468| 					...cacheOptions,
00469| 					setHeaders: setCustomCacheHeader,
00470| 				}),
00471| 				express.static(EDITOR_UI_DIST_DIR, cacheOptions),
00472| 			);
00473| 		} else {
00474| 			this.app.use('/', express.static(staticCacheDir, cacheOptions));
00475| 		}
00476| 
00477| 		installGlobalProxyAgent();
00478| 	}
00479| 
00480| 	private configureSettingsRoute() {
00481| 		const { frontendService } = this;
00482| 		const authService = Container.get(AuthService);
00483| 
00484| 		if (frontendService) {
00485| 			// Returns the current settings for the UI
00486| 			this.app.get(
00487| 				`/${this.restEndpoint}/settings`,
00488| 				authService.createAuthMiddleware({ allowSkipMFA: false, allowUnauthenticated: true }),
00489| 				ResponseHelper.send(async (req: AuthenticatedRequest) => {
00490| 					return req.user
00491| 						? await frontendService.getSettings()
00492| 						: await frontendService.getPublicSettings();
00493| 				}),
00494| 			);
00495| 		}
00496| 	}
00497| 
00498| 	private async initializeWorkflowIndexing() {
00499| 		if (Container.get(WorkflowsConfig).indexingEnabled) {
00500| 			if (Container.get(DatabaseConfig).isLegacySqlite) {
00501| 				this.logger.warn(
00502| 					'Workflow indexing is disabled because legacy Sqlite databases are not supported. Please migrate the database to enable workflow indexing.',
00503| 				);
00504| 				return;
00505| 			}
00506| 			const { WorkflowIndexService } = await import(
00507| 				'@/modules/workflow-index/workflow-index.service'
00508| 			);
00509| 			Container.get(WorkflowIndexService).init();
00510| 		}
00511| 	}
00512| 
00513| 	protected setupPushServer(): void {
00514| 		const { restEndpoint, server, app } = this;
00515| 		Container.get(Push).setupPushServer(restEndpoint, server, app);
00516| 		Container.get(ChatServer).setup(server, app);
00517| 	}
00518| }
00519| 

(End of file - total 519 lines)
</file>
```
```

---

## Assistant (Explore · big-pickle · 3.3s)

_Thinking:_




Now let me examine the key controllers that handle workflow execution:

```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/cli/src/workflows/workflows.controller.ts"
}
```
**Output:**
```
<file>
00001| import {
00002| 	ActivateWorkflowDto,
00003| 	ImportWorkflowFromUrlDto,
00004| 	ROLE,
00005| 	TransferWorkflowBodyDto,
00006| } from '@n8n/api-types';
00007| import { Logger } from '@n8n/backend-common';
00008| import { GlobalConfig } from '@n8n/config';
00009| import type { Project } from '@n8n/db';
00010| import {
00011| 	SharedWorkflow,
00012| 	WorkflowEntity,
00013| 	ProjectRelationRepository,
00014| 	ProjectRepository,
00015| 	TagRepository,
00016| 	SharedWorkflowRepository,
00017| 	WorkflowRepository,
00018| 	AuthenticatedRequest,
00019| } from '@n8n/db';
00020| import {
00021| 	Body,
00022| 	Delete,
00023| 	Get,
00024| 	Licensed,
00025| 	Param,
00026| 	Patch,
00027| 	Post,
00028| 	ProjectScope,
00029| 	Put,
00030| 	Query,
00031| 	RestController,
00032| } from '@n8n/decorators';
00033| import { PROJECT_OWNER_ROLE_SLUG } from '@n8n/permissions';
00034| // eslint-disable-next-line n8n-local-rules/misplaced-n8n-typeorm-import
00035| import { In, type FindOptionsRelations } from '@n8n/typeorm';
00036| import axios from 'axios';
00037| import express from 'express';
00038| import { UnexpectedError, calculateWorkflowChecksum } from 'n8n-workflow';
00039| import { v4 as uuid } from 'uuid';
00040| 
00041| import { BadRequestError } from '@/errors/response-errors/bad-request.error';
00042| import { ForbiddenError } from '@/errors/response-errors/forbidden.error';
00043| import { InternalServerError } from '@/errors/response-errors/internal-server.error';
00044| import { NotFoundError } from '@/errors/response-errors/not-found.error';
00045| import { EventService } from '@/events/event.service';
00046| import { ExecutionService } from '@/executions/execution.service';
00047| import { ExternalHooks } from '@/external-hooks';
00048| import { validateEntity } from '@/generic-helpers';
00049| import type { IWorkflowResponse } from '@/interfaces';
00050| import { License } from '@/license';
00051| import { listQueryMiddleware } from '@/middlewares';
00052| import * as ResponseHelper from '@/response-helper';
00053| import { FolderService } from '@/services/folder.service';
00054| import { NamingService } from '@/services/naming.service';
00055| import { ProjectService } from '@/services/project.service.ee';
00056| import { TagService } from '@/services/tag.service';
00057| import { UserManagementMailer } from '@/user-management/email';
00058| import * as utils from '@/utils';
00059| import * as WorkflowHelpers from '@/workflow-helpers';
00060| import { userHasScopes } from '@/permissions.ee/check-access';
00061| 
00062| import { WorkflowExecutionService } from './workflow-execution.service';
00063| import { WorkflowFinderService } from './workflow-finder.service';
00064| import { WorkflowHistoryService } from './workflow-history/workflow-history.service';
00065| import { WorkflowRequest } from './workflow.request';
00066| import { WorkflowService } from './workflow.service';
00067| import { EnterpriseWorkflowService } from './workflow.service.ee';
00068| import { CredentialsService } from '../credentials/credentials.service';
00069| 
00070| @RestController('/workflows')
00071| export class WorkflowsController {
00072| 	constructor(
00073| 		private readonly logger: Logger,
00074| 		private readonly externalHooks: ExternalHooks,
00075| 		private readonly tagRepository: TagRepository,
00076| 		private readonly enterpriseWorkflowService: EnterpriseWorkflowService,
00077| 		private readonly workflowHistoryService: WorkflowHistoryService,
00078| 		private readonly tagService: TagService,
00079| 		private readonly namingService: NamingService,
00080| 		private readonly workflowRepository: WorkflowRepository,
00081| 		private readonly workflowService: WorkflowService,
00082| 		private readonly workflowExecutionService: WorkflowExecutionService,
00083| 		private readonly sharedWorkflowRepository: SharedWorkflowRepository,
00084| 		private readonly license: License,
00085| 		private readonly mailer: UserManagementMailer,
00086| 		private readonly credentialsService: CredentialsService,
00087| 		private readonly projectRepository: ProjectRepository,
00088| 		private readonly projectService: ProjectService,
00089| 		private readonly projectRelationRepository: ProjectRelationRepository,
00090| 		private readonly eventService: EventService,
00091| 		private readonly globalConfig: GlobalConfig,
00092| 		private readonly folderService: FolderService,
00093| 		private readonly workflowFinderService: WorkflowFinderService,
00094| 		private readonly executionService: ExecutionService,
00095| 	) {}
00096| 
00097| 	@Post('/')
00098| 	async create(req: WorkflowRequest.Create) {
00099| 		if (req.body.id) {
00100| 			const workflowExists = await this.workflowRepository.existsBy({ id: req.body.id });
00101| 			if (workflowExists) {
00102| 				throw new BadRequestError(`Workflow with id ${req.body.id} exists already.`);
00103| 			}
00104| 		}
00105| 		// @ts-expect-error: We shouldn't accept this because it can
00106| 		// mess with relations of other workflows
00107| 		delete req.body.shared;
00108| 
00109| 		// @ts-expect-error: We shouldn't accept this, this will be set when activating
00110| 		if (req.body.activeVersionId || req.body.active) {
00111| 			this.logger.warn(
00112| 				'Creating a workflow as active is not supported. The workflow will be created as inactive.',
00113| 				{ userId: req.user.id },
00114| 			);
00115| 
00116| 			// @ts-expect-error: We shouldn't accept this
00117| 			delete req.body.activeVersionId;
00118| 			// @ts-expect-error: We shouldn't accept this
00119| 			delete req.body.activeVersion;
00120| 			req.body.active = false;
00121| 		}
00122| 
00123| 		const { autosaved = false } = req.body;
00124| 
00125| 		const newWorkflow = new WorkflowEntity();
00126| 
00127| 		Object.assign(newWorkflow, req.body);
00128| 
00129| 		newWorkflow.versionId = uuid();
00130| 
00131| 		await validateEntity(newWorkflow);
00132| 
00133| 		await this.externalHooks.run('workflow.create', [newWorkflow]);
00134| 
00135| 		const { tags: tagIds } = req.body;
00136| 
00137| 		if (tagIds?.length && !this.globalConfig.tags.disabled) {
00138| 			newWorkflow.tags = await this.tagRepository.findMany(tagIds);
00139| 		}
00140| 
00141| 		await WorkflowHelpers.replaceInvalidCredentials(newWorkflow);
00142| 
00143| 		WorkflowHelpers.addNodeIds(newWorkflow);
00144| 
00145| 		if (this.license.isSharingEnabled()) {
00146| 			// This is a new workflow, so we simply check if the user has access to
00147| 			// all used credentials
00148| 
00149| 			const allCredentials = await this.credentialsService.getMany(req.user, {
00150| 				includeGlobal: true,
00151| 			});
00152| 
00153| 			try {
00154| 				this.enterpriseWorkflowService.validateCredentialPermissionsToUser(
00155| 					newWorkflow,
00156| 					allCredentials,
00157| 				);
00158| 			} catch (error) {
00159| 				throw new BadRequestError(
00160| 					'The workflow you are trying to save contains credentials that are not shared with you',
00161| 				);
00162| 			}
00163| 		}
00164| 
00165| 		const { manager: dbManager } = this.projectRepository;
00166| 
00167| 		let project: Project | null = null;
00168| 		const savedWorkflow = await dbManager.transaction(async (transactionManager) => {
00169| 			const { parentFolderId } = req.body;
00170| 			let { projectId } = req.body;
00171| 
00172| 			if (projectId === undefined) {
00173| 				const personalProject = await this.projectRepository.getPersonalProjectForUserOrFail(
00174| 					req.user.id,
00175| 					transactionManager,
00176| 				);
00177| 				// Chat users are not allowed to create workflows even within their personal project,
00178| 				// so even though we found the project ensure it gets found via expected scope too.
00179| 				projectId = personalProject.id;
00180| 			}
00181| 
00182| 			project = await this.projectService.getProjectWithScope(
00183| 				req.user,
00184| 				projectId,
00185| 				['workflow:create'],
00186| 				transactionManager,
00187| 			);
00188| 
00189| 			if (project === null) {
00190| 				throw new BadRequestError(
00191| 					"You don't have the permissions to save the workflow in this project.",
00192| 				);
00193| 			}
00194| 
00195| 			const workflow = await transactionManager.save<WorkflowEntity>(newWorkflow);
00196| 
00197| 			if (parentFolderId) {
00198| 				try {
00199| 					const parentFolder = await this.folderService.findFolderInProjectOrFail(
00200| 						parentFolderId,
00201| 						project.id,
00202| 						transactionManager,
00203| 					);
00204| 					await transactionManager.update(WorkflowEntity, { id: workflow.id }, { parentFolder });
00205| 				} catch {}
00206| 			}
00207| 
00208| 			const newSharedWorkflow = this.sharedWorkflowRepository.create({
00209| 				role: 'workflow:owner',
00210| 				projectId: project.id,
00211| 				workflow,
00212| 			});
00213| 
00214| 			await transactionManager.save<SharedWorkflow>(newSharedWorkflow);
00215| 
00216| 			await this.workflowHistoryService.saveVersion(
00217| 				req.user,
00218| 				workflow,
00219| 				workflow.id,
00220| 				autosaved,
00221| 				transactionManager,
00222| 			);
00223| 
00224| 			return await this.workflowFinderService.findWorkflowForUser(
00225| 				workflow.id,
00226| 				req.user,
00227| 				['workflow:read'],
00228| 				{
00229| 					em: transactionManager,
00230| 					includeTags: true,
00231| 					includeParentFolder: true,
00232| 					includeActiveVersion: true,
00233| 				},
00234| 			);
00235| 		});
00236| 
00237| 		if (!savedWorkflow) {
00238| 			this.logger.error('Failed to create workflow', { userId: req.user.id });
00239| 			throw new InternalServerError('Failed to save workflow');
00240| 		}
00241| 
00242| 		if (tagIds && !this.globalConfig.tags.disabled && savedWorkflow.tags) {
00243| 			savedWorkflow.tags = this.tagService.sortByRequestOrder(savedWorkflow.tags, {
00244| 				requestOrder: tagIds,
00245| 			});
00246| 		}
00247| 
00248| 		const savedWorkflowWithMetaData =
00249| 			this.enterpriseWorkflowService.addOwnerAndSharings(savedWorkflow);
00250| 
00251| 		// @ts-expect-error: This is added as part of addOwnerAndSharings but
00252| 		// shouldn't be returned to the frontend
00253| 		delete savedWorkflowWithMetaData.shared;
00254| 
00255| 		await this.externalHooks.run('workflow.afterCreate', [savedWorkflow]);
00256| 		this.eventService.emit('workflow-created', {
00257| 			user: req.user,
00258| 			workflow: newWorkflow,
00259| 			publicApi: false,
00260| 			projectId: project!.id,
00261| 			projectType: project!.type,
00262| 			uiContext: req.body.uiContext,
00263| 		});
00264| 
00265| 		const scopes = await this.workflowService.getWorkflowScopes(req.user, savedWorkflow.id);
00266| 
00267| 		const checksum = await calculateWorkflowChecksum(savedWorkflow);
00268| 
00269| 		return { ...savedWorkflowWithMetaData, scopes, checksum };
00270| 	}
00271| 
00272| 	@Get('/', { middlewares: listQueryMiddleware })
00273| 	async getAll(req: WorkflowRequest.GetMany, res: express.Response) {
00274| 		try {
00275| 			const userCanListProjectFolders = req.listQueryOptions?.filter?.projectId
00276| 				? await userHasScopes(req.user, ['folder:list'], false, {
00277| 						projectId: req.listQueryOptions?.filter?.projectId as string,
00278| 					})
00279| 				: true;
00280| 
00281| 			const { workflows: data, count } = await this.workflowService.getMany(
00282| 				req.user,
00283| 				req.listQueryOptions,
00284| 				!!req.query.includeScopes,
00285| 				userCanListProjectFolders && !!req.query.includeFolders,
00286| 				!!req.query.onlySharedWithMe,
00287| 			);
00288| 
00289| 			res.json({ count, data });
00290| 		} catch (maybeError) {
00291| 			const error = utils.toError(maybeError);
00292| 			ResponseHelper.reportError(error);
00293| 			ResponseHelper.sendErrorResponse(res, error);
00294| 		}
00295| 	}
00296| 
00297| 	@Get('/new')
00298| 	async getNewName(req: WorkflowRequest.NewName) {
00299| 		const projectId = req.query.projectId;
00300| 		if (
00301| 			!(await this.projectService.getProjectWithScope(req.user, projectId, ['workflow:create']))
00302| 		) {
00303| 			throw new ForbiddenError(
00304| 				"You don't have the permissions to create a workflow in this project.",
00305| 			);
00306| 		}
00307| 		const requestedName = req.query.name ?? this.globalConfig.workflows.defaultName;
00308| 
00309| 		const name = await this.namingService.getUniqueWorkflowName(requestedName);
00310| 		return { name };
00311| 	}
00312| 
00313| 	@Get('/from-url')
00314| 	async getFromUrl(
00315| 		req: AuthenticatedRequest,
00316| 		_res: express.Response,
00317| 		@Query query: ImportWorkflowFromUrlDto,
00318| 	) {
00319| 		const projectId = query.projectId;
00320| 		if (
00321| 			!(await this.projectService.getProjectWithScope(req.user, projectId, ['workflow:create']))
00322| 		) {
00323| 			throw new ForbiddenError(
00324| 				"You don't have the permissions to create a workflow in this project.",
00325| 			);
00326| 		}
00327| 		let workflowData: IWorkflowResponse | undefined;
00328| 		try {
00329| 			const { data } = await axios.get<IWorkflowResponse>(query.url);
00330| 			workflowData = data;
00331| 		} catch (error) {
00332| 			throw new BadRequestError('The URL does not point to valid JSON file!');
00333| 		}
00334| 
00335| 		// Do a very basic check if it is really a n8n-workflow-json
00336| 		if (
00337| 			workflowData?.nodes === undefined ||
00338| 			!Array.isArray(workflowData.nodes) ||
00339| 			workflowData.connections === undefined ||
00340| 			typeof workflowData.connections !== 'object' ||
00341| 			Array.isArray(workflowData.connections)
00342| 		) {
00343| 			throw new BadRequestError(
00344| 				'The data in the file does not seem to be a n8n workflow JSON file!',
00345| 			);
00346| 		}
00347| 
00348| 		return workflowData;
00349| 	}
00350| 
00351| 	@Get('/:workflowId')
00352| 	@ProjectScope('workflow:read')
00353| 	async getWorkflow(req: WorkflowRequest.Get) {
00354| 		const { workflowId } = req.params;
00355| 
00356| 		if (this.license.isSharingEnabled()) {
00357| 			const relations: FindOptionsRelations<WorkflowEntity> = {
00358| 				shared: {
00359| 					project: {
00360| 						projectRelations: true,
00361| 					},
00362| 				},
00363| 			};
00364| 
00365| 			if (!this.globalConfig.tags.disabled) {
00366| 				relations.tags = true;
00367| 			}
00368| 
00369| 			const workflow = await this.workflowFinderService.findWorkflowForUser(
00370| 				workflowId,
00371| 				req.user,
00372| 				['workflow:read'],
00373| 				{
00374| 					includeTags: !this.globalConfig.tags.disabled,
00375| 					includeParentFolder: true,
00376| 					includeActiveVersion: true,
00377| 				},
00378| 			);
00379| 
00380| 			if (!workflow) {
00381| 				throw new NotFoundError(`Workflow with ID "${workflowId}" does not exist`);
00382| 			}
00383| 
00384| 			const enterpriseWorkflowService = this.enterpriseWorkflowService;
00385| 
00386| 			const workflowWithMetaData = enterpriseWorkflowService.addOwnerAndSharings(workflow);
00387| 
00388| 			await enterpriseWorkflowService.addCredentialsToWorkflow(workflowWithMetaData, req.user);
00389| 
00390| 			// @ts-expect-error: This is added as part of addOwnerAndSharings but
00391| 			// shouldn't be returned to the frontend
00392| 			delete workflowWithMetaData.shared;
00393| 
00394| 			const scopes = await this.workflowService.getWorkflowScopes(req.user, workflowId);
00395| 			const checksum = await calculateWorkflowChecksum(workflow);
00396| 
00397| 			return { ...workflowWithMetaData, scopes, checksum };
00398| 		}
00399| 
00400| 		// sharing disabled
00401| 
00402| 		const workflow = await this.workflowFinderService.findWorkflowForUser(
00403| 			workflowId,
00404| 			req.user,
00405| 			['workflow:read'],
00406| 			{
00407| 				includeTags: !this.globalConfig.tags.disabled,
00408| 				includeParentFolder: true,
00409| 				includeActiveVersion: true,
00410| 			},
00411| 		);
00412| 
00413| 		if (!workflow) {
00414| 			this.logger.warn('User attempted to access a workflow without permissions', {
00415| 				workflowId,
00416| 				userId: req.user.id,
00417| 			});
00418| 			throw new NotFoundError(
00419| 				'Could not load the workflow - you can only access workflows owned by you',
00420| 			);
00421| 		}
00422| 
00423| 		const scopes = await this.workflowService.getWorkflowScopes(req.user, workflowId);
00424| 		const checksum = await calculateWorkflowChecksum(workflow);
00425| 
00426| 		return { ...workflow, scopes, checksum };
00427| 	}
00428| 
00429| 	/**
00430| 	 * Checks whether a workflow with the given ID exists.
00431| 	 *
00432| 	 * @note We cannot use @ProjectScope here because we want to check for the id's existence
00433| 	 *       Adding a scope would disable the route if the user didn't have access to the workflow
00434| 	 */
00435| 	@Get('/:workflowId/exists')
00436| 	async exists(req: WorkflowRequest.Get) {
00437| 		const exists = await this.workflowRepository.existsBy({ id: req.params.workflowId });
00438| 		return { exists };
00439| 	}
00440| 
00441| 	@Patch('/:workflowId')
00442| 	@ProjectScope('workflow:update')
00443| 	async update(req: WorkflowRequest.Update) {
00444| 		const { workflowId } = req.params;
00445| 		const forceSave = req.query.forceSave === 'true';
00446| 
00447| 		let updateData = new WorkflowEntity();
00448| 		const { tags, parentFolderId, aiBuilderAssisted, expectedChecksum, autosaved, ...rest } =
00449| 			req.body;
00450| 
00451| 		// TODO: Add zod validation for entire `rest` object before assigning to `updateData`
00452| 		if (
00453| 			rest.settings?.timeSavedMode !== undefined &&
00454| 			!['fixed', 'dynamic'].includes(rest.settings.timeSavedMode)
00455| 		) {
00456| 			throw new BadRequestError('Invalid timeSavedMode');
00457| 		}
00458| 
00459| 		Object.assign(updateData, rest);
00460| 
00461| 		const isSharingEnabled = this.license.isSharingEnabled();
00462| 		if (isSharingEnabled) {
00463| 			updateData = await this.enterpriseWorkflowService.preventTampering(
00464| 				updateData,
00465| 				workflowId,
00466| 				req.user,
00467| 			);
00468| 		}
00469| 
00470| 		const updatedWorkflow = await this.workflowService.update(req.user, updateData, workflowId, {
00471| 			tagIds: tags,
00472| 			parentFolderId,
00473| 			forceSave: isSharingEnabled ? forceSave : true,
00474| 			expectedChecksum,
00475| 			aiBuilderAssisted,
00476| 			autosaved,
00477| 		});
00478| 
00479| 		const scopes = await this.workflowService.getWorkflowScopes(req.user, workflowId);
00480| 		const checksum = await calculateWorkflowChecksum(updatedWorkflow);
00481| 
00482| 		return { ...updatedWorkflow, scopes, checksum };
00483| 	}
00484| 
00485| 	@Delete('/:workflowId')
00486| 	@ProjectScope('workflow:delete')
00487| 	async delete(req: AuthenticatedRequest, _res: Response, @Param('workflowId') workflowId: string) {
00488| 		const workflow = await this.workflowService.delete(req.user, workflowId);
00489| 		if (!workflow) {
00490| 			this.logger.warn('User attempted to delete a workflow without permissions', {
00491| 				workflowId,
00492| 				userId: req.user.id,
00493| 			});
00494| 			throw new ForbiddenError(
00495| 				'Could not delete the workflow - workflow was not found in your projects',
00496| 			);
00497| 		}
00498| 
00499| 		return true;
00500| 	}
00501| 
00502| 	@Post('/:workflowId/archive')
00503| 	@ProjectScope('workflow:delete')
00504| 	async archive(
00505| 		req: AuthenticatedRequest,
00506| 		_res: Response,
00507| 		@Param('workflowId') workflowId: string,
00508| 	) {
00509| 		const workflow = await this.workflowService.archive(req.user, workflowId);
00510| 		if (!workflow) {
00511| 			this.logger.warn('User attempted to archive a workflow without permissions', {
00512| 				workflowId,
00513| 				userId: req.user.id,
00514| 			});
00515| 			throw new ForbiddenError(
00516| 				'Could not archive the workflow - workflow was not found in your projects',
00517| 			);
00518| 		}
00519| 
00520| 		const checksum = await calculateWorkflowChecksum(workflow);
00521| 
00522| 		return { ...workflow, checksum };
00523| 	}
00524| 
00525| 	@Post('/:workflowId/unarchive')
00526| 	@ProjectScope('workflow:delete')
00527| 	async unarchive(
00528| 		req: AuthenticatedRequest,
00529| 		_res: Response,
00530| 		@Param('workflowId') workflowId: string,
00531| 	) {
00532| 		const workflow = await this.workflowService.unarchive(req.user, workflowId);
00533| 		if (!workflow) {
00534| 			this.logger.warn('User attempted to unarchive a workflow without permissions', {
00535| 				workflowId,
00536| 				userId: req.user.id,
00537| 			});
00538| 			throw new ForbiddenError(
00539| 				'Could not unarchive the workflow - workflow was not found in your projects',
00540| 			);
00541| 		}
00542| 
00543| 		const checksum = await calculateWorkflowChecksum(workflow);
00544| 
00545| 		return { ...workflow, checksum };
00546| 	}
00547| 
00548| 	@Post('/:workflowId/activate')
00549| 	@ProjectScope('workflow:publish')
00550| 	async activate(
00551| 		req: WorkflowRequest.Activate,
00552| 		_res: unknown,
00553| 		@Param('workflowId') workflowId: string,
00554| 		@Body body: ActivateWorkflowDto,
00555| 	) {
00556| 		const { versionId, name, description, expectedChecksum } = body;
00557| 
00558| 		const workflow = await this.workflowService.activateWorkflow(req.user, workflowId, {
00559| 			versionId,
00560| 			name,
00561| 			description,
00562| 			expectedChecksum,
00563| 		});
00564| 
00565| 		const scopes = await this.workflowService.getWorkflowScopes(req.user, workflowId);
00566| 		const checksum = await calculateWorkflowChecksum(workflow);
00567| 
00568| 		return { ...workflow, scopes, checksum };
00569| 	}
00570| 
00571| 	@Post('/:workflowId/deactivate')
00572| 	@ProjectScope('workflow:publish')
00573| 	async deactivate(req: WorkflowRequest.Deactivate) {
00574| 		const { workflowId } = req.params;
00575| 
00576| 		const workflow = await this.workflowService.deactivateWorkflow(req.user, workflowId);
00577| 
00578| 		const scopes = await this.workflowService.getWorkflowScopes(req.user, workflowId);
00579| 		const checksum = await calculateWorkflowChecksum(workflow);
00580| 
00581| 		return { ...workflow, scopes, checksum };
00582| 	}
00583| 
00584| 	@Post('/:workflowId/run')
00585| 	@ProjectScope('workflow:execute')
00586| 	async runManually(req: WorkflowRequest.ManualRun, _res: unknown) {
00587| 		if (!req.body.workflowData.id) {
00588| 			throw new UnexpectedError('You cannot execute a workflow without an ID');
00589| 		}
00590| 
00591| 		if (req.params.workflowId !== req.body.workflowData.id) {
00592| 			throw new UnexpectedError('Workflow ID in body does not match workflow ID in URL');
00593| 		}
00594| 
00595| 		if (this.license.isSharingEnabled()) {
00596| 			const workflow = this.workflowRepository.create(req.body.workflowData);
00597| 
00598| 			const safeWorkflow = await this.enterpriseWorkflowService.preventTampering(
00599| 				workflow,
00600| 				workflow.id,
00601| 				req.user,
00602| 			);
00603| 			req.body.workflowData.nodes = safeWorkflow.nodes;
00604| 		}
00605| 
00606| 		return await this.workflowExecutionService.executeManually(
00607| 			req.body,
00608| 			req.user,
00609| 			req.headers['push-ref'],
00610| 		);
00611| 	}
00612| 
00613| 	@Licensed('feat:sharing')
00614| 	@Put('/:workflowId/share')
00615| 	@ProjectScope('workflow:share')
00616| 	async share(req: WorkflowRequest.Share) {
00617| 		const { workflowId } = req.params;
00618| 		const { shareWithIds } = req.body;
00619| 
00620| 		if (
00621| 			!Array.isArray(shareWithIds) ||
00622| 			!shareWithIds.every((userId) => typeof userId === 'string')
00623| 		) {
00624| 			throw new BadRequestError('Bad request');
00625| 		}
00626| 
00627| 		const workflow = await this.workflowFinderService.findWorkflowForUser(workflowId, req.user, [
00628| 			'workflow:share',
00629| 		]);
00630| 
00631| 		if (!workflow) {
00632| 			throw new ForbiddenError();
00633| 		}
00634| 
00635| 		let newShareeIds: string[] = [];
00636| 		const { manager: dbManager } = this.projectRepository;
00637| 		await dbManager.transaction(async (trx) => {
00638| 			const currentPersonalProjectIDs = workflow.shared
00639| 				.filter((sw) => sw.role === 'workflow:editor')
00640| 				.map((sw) => sw.projectId);
00641| 			const newPersonalProjectIDs = shareWithIds;
00642| 
00643| 			const toShare = utils.rightDiff(
00644| 				[currentPersonalProjectIDs, (id) => id],
00645| 				[newPersonalProjectIDs, (id) => id],
00646| 			);
00647| 
00648| 			const toUnshare = utils.rightDiff(
00649| 				[newPersonalProjectIDs, (id) => id],
00650| 				[currentPersonalProjectIDs, (id) => id],
00651| 			);
00652| 
00653| 			await trx.delete(SharedWorkflow, {
00654| 				workflowId,
00655| 				projectId: In(toUnshare),
00656| 			});
00657| 
00658| 			await this.enterpriseWorkflowService.shareWithProjects(workflow.id, toShare, trx);
00659| 
00660| 			newShareeIds = toShare;
00661| 		});
00662| 
00663| 		this.eventService.emit('workflow-sharing-updated', {
00664| 			workflowId,
00665| 			userIdSharer: req.user.id,
00666| 			userIdList: shareWithIds,
00667| 		});
00668| 
00669| 		const projectsRelations = await this.projectRelationRepository.findBy({
00670| 			projectId: In(newShareeIds),
00671| 			role: { slug: PROJECT_OWNER_ROLE_SLUG },
00672| 		});
00673| 
00674| 		await this.mailer.notifyWorkflowShared({
00675| 			sharer: req.user,
00676| 			newShareeIds: projectsRelations.map((pr) => pr.userId),
00677| 			workflow,
00678| 		});
00679| 	}
00680| 
00681| 	@Put('/:workflowId/transfer')
00682| 	@ProjectScope('workflow:move')
00683| 	async transfer(
00684| 		req: AuthenticatedRequest,
00685| 		_res: unknown,
00686| 		@Param('workflowId') workflowId: string,
00687| 		@Body body: TransferWorkflowBodyDto,
00688| 	) {
00689| 		return await this.enterpriseWorkflowService.transferWorkflow(
00690| 			req.user,
00691| 			workflowId,
00692| 			body.destinationProjectId,
00693| 			body.shareCredentials,
00694| 			body.destinationParentFolderId,
00695| 		);
00696| 	}
00697| 
00698| 	@Get('/:workflowId/executions/last-successful')
00699| 	@ProjectScope('workflow:read')
00700| 	async getLastSuccessfulExecution(
00701| 		_req: AuthenticatedRequest,
00702| 		_res: unknown,
00703| 		@Param('workflowId') workflowId: string,
00704| 	) {
00705| 		const lastExecution = await this.executionService.getLastSuccessfulExecution(workflowId);
00706| 
00707| 		return lastExecution ?? null;
00708| 	}
00709| 
00710| 	@Post('/with-node-types')
00711| 	async getWorkflowsWithNodesIncluded(req: AuthenticatedRequest, res: express.Response) {
00712| 		try {
00713| 			const hasPermission = req.user.role.slug === ROLE.Owner || req.user.role.slug === ROLE.Admin;
00714| 
00715| 			if (!hasPermission) {
00716| 				res.json({ data: [], count: 0 });
00717| 				return;
00718| 			}
00719| 
00720| 			const { nodeTypes } = req.body as { nodeTypes: string[] };
00721| 			const workflows = await this.workflowService.getWorkflowsWithNodesIncluded(
00722| 				req.user,
00723| 				nodeTypes,
00724| 			);
00725| 
00726| 			res.json({
00727| 				data: workflows,
00728| 				count: workflows.length,
00729| 			});
00730| 		} catch (maybeError) {
00731| 			const error = utils.toError(maybeError);
00732| 			ResponseHelper.reportError(error);
00733| 			ResponseHelper.sendErrorResponse(res, error);
00734| 		}
00735| 	}
00736| }
00737| 

(End of file - total 737 lines)
</file>
```
```

---

## Assistant (Explore · big-pickle · 3.6s)

_Thinking:_




Now let me look at the workflow execution service to understand how execution starts:

```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-execution.service.ts"
}
```
**Output:**
```
<file>
00001| import { Logger } from '@n8n/backend-common';
00002| import { GlobalConfig } from '@n8n/config';
00003| import type { Project, User, CreateExecutionPayload } from '@n8n/db';
00004| import { ExecutionRepository, WorkflowRepository } from '@n8n/db';
00005| import { Service } from '@n8n/di';
00006| import type { Response } from 'express';
00007| import { DirectedGraph, ErrorReporter, anyReachableRootHasRunData } from 'n8n-core';
00008| import type {
00009| 	IDeferredPromise,
00010| 	IExecuteData,
00011| 	IExecuteResponsePromiseData,
00012| 	INode,
00013| 	INodeExecutionData,
00014| 	IPinData,
00015| 	IRunExecutionData,
00016| 	IWorkflowExecuteAdditionalData,
00017| 	WorkflowExecuteMode,
00018| 	IWorkflowExecutionDataProcess,
00019| 	IWorkflowBase,
00020| } from 'n8n-workflow';
00021| import {
00022| 	SubworkflowOperationError,
00023| 	UnexpectedError,
00024| 	Workflow,
00025| 	createRunExecutionData,
00026| } from 'n8n-workflow';
00027| 
00028| import { ExecutionDataService } from '@/executions/execution-data.service';
00029| import { SubworkflowPolicyChecker } from '@/executions/pre-execution-checks';
00030| import type { IWorkflowErrorData } from '@/interfaces';
00031| import { NodeTypes } from '@/node-types';
00032| import { TestWebhooks } from '@/webhooks/test-webhooks';
00033| import * as WorkflowExecuteAdditionalData from '@/workflow-execute-additional-data';
00034| import { WorkflowRunner } from '@/workflow-runner';
00035| import type { WorkflowRequest } from '@/workflows/workflow.request';
00036| 
00037| @Service()
00038| export class WorkflowExecutionService {
00039| 	constructor(
00040| 		private readonly logger: Logger,
00041| 		private readonly errorReporter: ErrorReporter,
00042| 		private readonly executionRepository: ExecutionRepository,
00043| 		private readonly workflowRepository: WorkflowRepository,
00044| 		private readonly nodeTypes: NodeTypes,
00045| 		private readonly testWebhooks: TestWebhooks,
00046| 		private readonly workflowRunner: WorkflowRunner,
00047| 		private readonly globalConfig: GlobalConfig,
00048| 		private readonly subworkflowPolicyChecker: SubworkflowPolicyChecker,
00049| 		private readonly executionDataService: ExecutionDataService,
00050| 	) {}
00051| 
00052| 	async runWorkflow(
00053| 		workflowData: IWorkflowBase,
00054| 		node: INode,
00055| 		data: INodeExecutionData[][],
00056| 		additionalData: IWorkflowExecuteAdditionalData,
00057| 		mode: WorkflowExecuteMode,
00058| 		responsePromise?: IDeferredPromise<IExecuteResponsePromiseData>,
00059| 	) {
00060| 		const nodeExecutionStack: IExecuteData[] = [
00061| 			{
00062| 				node,
00063| 				data: {
00064| 					main: data,
00065| 				},
00066| 				source: null,
00067| 			},
00068| 		];
00069| 
00070| 		const executionData = createRunExecutionData({
00071| 			executionData: {
00072| 				nodeExecutionStack,
00073| 			},
00074| 		});
00075| 
00076| 		// Start the workflow
00077| 		const runData: IWorkflowExecutionDataProcess = {
00078| 			userId: additionalData.userId,
00079| 			executionMode: mode,
00080| 			executionData,
00081| 			workflowData,
00082| 		};
00083| 
00084| 		return await this.workflowRunner.run(runData, true, undefined, undefined, responsePromise);
00085| 	}
00086| 
00087| 	private isDestinationNodeATrigger(destinationNode: string, workflow: IWorkflowBase) {
00088| 		const node = workflow.nodes.find((n) => n.name === destinationNode);
00089| 
00090| 		if (node === undefined) {
00091| 			return false;
00092| 		}
00093| 
00094| 		const nodeType = this.nodeTypes.getByNameAndVersion(node.type, node.typeVersion);
00095| 
00096| 		return nodeType.description.group.includes('trigger');
00097| 	}
00098| 
00099| 	async executeManually(
00100| 		payload: WorkflowRequest.ManualRunPayload,
00101| 		user: User,
00102| 		pushRef?: string,
00103| 	): Promise<{ executionId: string } | { waitingForWebhook: boolean }> {
00104| 		// Check whether this workflow is active.
00105| 		const workflowIsActive = await this.workflowRepository.isActive(payload.workflowData.id);
00106| 
00107| 		// For manual testing always set to not active
00108| 		payload.workflowData.active = false;
00109| 		payload.workflowData.activeVersionId = null;
00110| 
00111| 		// TODO: Will be fixed on the FE side with CAT-1808
00112| 		if ('triggerToStartFrom' in payload) {
00113| 			Reflect.deleteProperty(payload, 'runData');
00114| 		}
00115| 
00116| 		let data: IWorkflowExecutionDataProcess | undefined;
00117| 
00118| 		// Case 1: Partial execution to a destination node, and we have enough runData to start the execution.
00119| 		if (isPartialExecution(payload)) {
00120| 			if (this.partialExecutionFulfilsPreconditions(payload)) {
00121| 				data = {
00122| 					destinationNode: payload.destinationNode,
00123| 					executionMode: 'manual',
00124| 					runData: payload.runData,
00125| 					pinData: payload.workflowData.pinData,
00126| 					pushRef,
00127| 					workflowData: payload.workflowData,
00128| 					userId: user.id,
00129| 					dirtyNodeNames: payload.dirtyNodeNames,
00130| 					agentRequest: payload.agentRequest,
00131| 				};
00132| 			} else {
00133| 				payload = upgradeToFullManualExecutionFromUnknownTrigger(payload);
00134| 			}
00135| 		}
00136| 
00137| 		// Case 2: Full execution from a known trigger.
00138| 		if (isFullExecutionFromKnownTrigger(payload)) {
00139| 			// Check if we need a webhook.
00140| 			if (
00141| 				triggerHasNoPinnedData(payload) &&
00142| 				(await this.testWebhooks.needsWebhook({
00143| 					userId: user.id,
00144| 					workflowEntity: payload.workflowData,
00145| 					additionalData: await WorkflowExecuteAdditionalData.getBase({
00146| 						userId: user.id,
00147| 						workflowId: payload.workflowData.id,
00148| 					}),
00149| 					pushRef,
00150| 					triggerToStartFrom: payload.triggerToStartFrom,
00151| 					destinationNode: payload.destinationNode,
00152| 					workflowIsActive,
00153| 				}))
00154| 			) {
00155| 				return { waitingForWebhook: true };
00156| 			}
00157| 
00158| 			data = {
00159| 				executionMode: 'manual',
00160| 				pinData: payload.workflowData.pinData,
00161| 				pushRef,
00162| 				workflowData: payload.workflowData,
00163| 				userId: user.id,
00164| 				triggerToStartFrom: payload.triggerToStartFrom,
00165| 				agentRequest: payload.agentRequest,
00166| 				destinationNode: payload.destinationNode,
00167| 			};
00168| 		}
00169| 
00170| 		// Case 3: Full execution from an unknown trigger.
00171| 		if (isFullExecutionFromUnknownTrigger(payload)) {
00172| 			const pinnedTrigger = this.selectPinnedTrigger(
00173| 				payload.workflowData,
00174| 				payload.destinationNode.nodeName,
00175| 				payload.workflowData.pinData ?? {},
00176| 			);
00177| 
00178| 			if (
00179| 				pinnedTrigger === undefined &&
00180| 				(await this.testWebhooks.needsWebhook({
00181| 					userId: user.id,
00182| 					workflowEntity: payload.workflowData,
00183| 					additionalData: await WorkflowExecuteAdditionalData.getBase({
00184| 						userId: user.id,
00185| 						workflowId: payload.workflowData.id,
00186| 					}),
00187| 					pushRef,
00188| 					destinationNode: payload.destinationNode,
00189| 					workflowIsActive,
00190| 				}))
00191| 			) {
00192| 				return { waitingForWebhook: true };
00193| 			}
00194| 
00195| 			data = {
00196| 				executionMode: 'manual',
00197| 				pinData: payload.workflowData.pinData,
00198| 				pushRef,
00199| 				workflowData: payload.workflowData,
00200| 				userId: user.id,
00201| 				agentRequest: payload.agentRequest,
00202| 				destinationNode: payload.destinationNode,
00203| 				triggerToStartFrom: pinnedTrigger ? { name: pinnedTrigger.name } : undefined,
00204| 			};
00205| 		}
00206| 
00207| 		if (data) {
00208| 			const offloadingManualExecutionsInQueueMode =
00209| 				this.globalConfig.executions.mode === 'queue' &&
00210| 				process.env.OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS === 'true';
00211| 
00212| 			/**
00213| 			 * Historically, manual executions in scaling mode ran in the main process,
00214| 			 * so some execution details were never persisted in the database.
00215| 			 *
00216| 			 * Currently, manual executions in scaling mode are offloaded to workers,
00217| 			 * so we persist all details to give workers full access to them.
00218| 			 */
00219| 			if (data.executionMode === 'manual' && offloadingManualExecutionsInQueueMode) {
00220| 				data.executionData = createRunExecutionData({
00221| 					startData: {
00222| 						startNodes: data.startNodes,
00223| 						destinationNode: data.destinationNode,
00224| 					},
00225| 					resultData: {
00226| 						pinData: data.pinData,
00227| 						// Set this to null so `createRunExecutionData` doesn't initialize it.
00228| 						// Otherwise this would be treated as a partial execution.
00229| 						runData: data.runData ?? null,
00230| 					},
00231| 					manualData: {
00232| 						userId: data.userId,
00233| 						dirtyNodeNames: data.dirtyNodeNames,
00234| 						triggerToStartFrom: data.triggerToStartFrom,
00235| 					},
00236| 					// Set this to null so `createRunExecutionData` doesn't initialize it.
00237| 					// Otherwise this would be treated as a resumed execution after waiting.
00238| 					executionData: null,
00239| 				});
00240| 			}
00241| 
00242| 			const executionId = await this.workflowRunner.run(data);
00243| 			return { executionId };
00244| 		}
00245| 
00246| 		throw new UnexpectedError('`executeManually` was called with an unexpected payload', {
00247| 			extra: { payload },
00248| 		});
00249| 	}
00250| 
00251| 	async executeChatWorkflow(
00252| 		workflowData: IWorkflowBase,
00253| 		executionData: IRunExecutionData,
00254| 		user: User,
00255| 		httpResponse?: Response,
00256| 		streamingEnabled?: boolean,
00257| 		executionMode: WorkflowExecuteMode = 'chat',
00258| 	) {
00259| 		const data: IWorkflowExecutionDataProcess = {
00260| 			executionMode,
00261| 			workflowData,
00262| 			userId: user.id,
00263| 			executionData,
00264| 			streamingEnabled,
00265| 			httpResponse,
00266| 		};
00267| 
00268| 		const executionId = await this.workflowRunner.run(data, undefined, true);
00269| 
00270| 		return {
00271| 			executionId,
00272| 		};
00273| 	}
00274| 
00275| 	/** Executes an error workflow */
00276| 	async executeErrorWorkflow(
00277| 		workflowId: string,
00278| 		workflowErrorData: IWorkflowErrorData,
00279| 		runningProject: Project,
00280| 	): Promise<void> {
00281| 		// Wrap everything in try/catch to make sure that no errors bubble up and all get caught here
00282| 		try {
00283| 			const workflowData = await this.workflowRepository.get(
00284| 				{ id: workflowId },
00285| 				{ relations: ['activeVersion'] },
00286| 			);
00287| 			if (workflowData === null) {
00288| 				// The workflow could not be found
00289| 				this.logger.error(
00290| 					`Calling Error Workflow for "${workflowErrorData.workflow.id}". Could not find workflow "${workflowId}"`,
00291| 					{ workflowId },
00292| 				);
00293| 				return;
00294| 			}
00295| 
00296| 			if (workflowData.activeVersion === null) {
00297| 				// The workflow is not active
00298| 				this.logger.error(
00299| 					`Calling Error Workflow for "${workflowErrorData.workflow.id}". Workflow "${workflowId}" is not active and cannot be executed`,
00300| 					{ workflowId },
00301| 				);
00302| 				return;
00303| 			}
00304| 
00305| 			const executionMode = 'error';
00306| 			const workflowInstance = new Workflow({
00307| 				id: workflowId,
00308| 				name: workflowData.name,
00309| 				nodeTypes: this.nodeTypes,
00310| 				nodes: workflowData.activeVersion.nodes,
00311| 				connections: workflowData.activeVersion.connections,
00312| 				active: true,
00313| 				staticData: workflowData.staticData,
00314| 				settings: workflowData.settings,
00315| 			});
00316| 
00317| 			try {
00318| 				const failedNode = workflowErrorData.execution?.lastNodeExecuted
00319| 					? workflowInstance.getNode(workflowErrorData.execution?.lastNodeExecuted)
00320| 					: undefined;
00321| 				await this.subworkflowPolicyChecker.check(
00322| 					workflowInstance,
00323| 					workflowErrorData.workflow.id!,
00324| 					failedNode ?? undefined,
00325| 				);
00326| 			} catch (error) {
00327| 				const initialNode = workflowInstance.getStartNode();
00328| 				if (initialNode) {
00329| 					const errorWorkflowPermissionError = new SubworkflowOperationError(
00330| 						`Another workflow: (ID ${workflowErrorData.workflow.id}) tried to invoke this workflow to handle errors.`,
00331| 						"Unfortunately current permissions do not allow this. Please check that this workflow's settings allow it to be called by others",
00332| 					);
00333| 
00334| 					// Create a fake execution and save it to DB.
00335| 					const fakeExecution = this.executionDataService.generateFailedExecutionFromError(
00336| 						'error',
00337| 						errorWorkflowPermissionError,
00338| 						initialNode,
00339| 					);
00340| 
00341| 					const fullExecutionData: CreateExecutionPayload = {
00342| 						data: fakeExecution.data,
00343| 						mode: fakeExecution.mode,
00344| 						finished: false,
00345| 						stoppedAt: new Date(),
00346| 						workflowData,
00347| 						waitTill: null,
00348| 						status: fakeExecution.status,
00349| 						workflowId: workflowData.id,
00350| 					};
00351| 
00352| 					await this.executionRepository.createNewExecution(fullExecutionData);
00353| 				}
00354| 				this.logger.info('Error workflow execution blocked due to subworkflow settings', {
00355| 					erroredWorkflowId: workflowErrorData.workflow.id,
00356| 					errorWorkflowId: workflowId,
00357| 				});
00358| 				return;
00359| 			}
00360| 
00361| 			let node: INode;
00362| 			let workflowStartNode: INode | undefined;
00363| 			const { errorTriggerType } = this.globalConfig.nodes;
00364| 			for (const nodeName of Object.keys(workflowInstance.nodes)) {
00365| 				node = workflowInstance.nodes[nodeName];
00366| 				if (node.type === errorTriggerType) {
00367| 					workflowStartNode = node;
00368| 				}
00369| 			}
00370| 
00371| 			if (workflowStartNode === undefined) {
00372| 				this.logger.error(
00373| 					`Calling Error Workflow for "${workflowErrorData.workflow.id}". Could not find "${errorTriggerType}" in workflow "${workflowId}"`,
00374| 				);
00375| 				return;
00376| 			}
00377| 
00378| 			const parentExecution =
00379| 				workflowErrorData.execution?.id && workflowErrorData.workflow?.id
00380| 					? {
00381| 							executionId: workflowErrorData.execution.id,
00382| 							workflowId: workflowErrorData.workflow.id,
00383| 							executionContext: workflowErrorData.execution.executionContext,
00384| 						}
00385| 					: undefined;
00386| 
00387| 			// Can execute without webhook so go on
00388| 			// Initialize the data of the webhook node
00389| 			const nodeExecutionStack: IExecuteData[] = [];
00390| 			nodeExecutionStack.push({
00391| 				node: workflowStartNode,
00392| 				data: {
00393| 					main: [
00394| 						[
00395| 							{
00396| 								json: workflowErrorData,
00397| 							},
00398| 						],
00399| 					],
00400| 				},
00401| 				source: null,
00402| 				...(parentExecution && {
00403| 					metadata: {
00404| 						parentExecution,
00405| 					},
00406| 				}),
00407| 			});
00408| 
00409| 			const runExecutionData = createRunExecutionData({
00410| 				executionData: {
00411| 					nodeExecutionStack,
00412| 				},
00413| 			});
00414| 
00415| 			const runData: IWorkflowExecutionDataProcess = {
00416| 				executionMode,
00417| 				executionData: runExecutionData,
00418| 				workflowData,
00419| 				projectId: runningProject.id,
00420| 			};
00421| 
00422| 			await this.workflowRunner.run(runData);
00423| 		} catch (error) {
00424| 			this.errorReporter.error(error);
00425| 			this.logger.error(
00426| 				// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
00427| 				`Calling Error Workflow for "${workflowErrorData.workflow.id}": "${error.message}"`,
00428| 				{ workflowId: workflowErrorData.workflow.id },
00429| 			);
00430| 		}
00431| 	}
00432| 
00433| 	/**
00434| 	 * Select the pinned trigger node to use as starter for a manual execution.
00435| 	 *
00436| 	 * Finds all pinned trigger nodes in the workflow, then returns the first pinned trigger
00437| 	 * that is a parent of the destination node. Webhook triggers are prioritized over other
00438| 	 * trigger types in the sorting order.
00439| 	 *
00440| 	 * @param workflow The workflow containing the nodes and connections
00441| 	 * @param destinationNode The name of the node to find a pinned trigger for
00442| 	 * @param pinData Pin data mapping node names to their pinned data
00443| 	 * @returns The pinned trigger node if found, undefined otherwise
00444| 	 */
00445| 	selectPinnedTrigger(
00446| 		workflow: IWorkflowBase,
00447| 		destinationNode: string,
00448| 		pinData: IPinData,
00449| 	): INode | undefined {
00450| 		const allPinnedTriggers = this.findAllPinnedTriggers(workflow, pinData);
00451| 
00452| 		if (allPinnedTriggers.length === 0) return undefined;
00453| 
00454| 		const destinationParents = new Set(
00455| 			new Workflow({
00456| 				nodes: workflow.nodes,
00457| 				connections: workflow.connections,
00458| 				active: workflow.activeVersionId !== null,
00459| 				nodeTypes: this.nodeTypes,
00460| 			}).getParentNodes(destinationNode),
00461| 		);
00462| 
00463| 		const trigger = allPinnedTriggers.find((a) => destinationParents.has(a.name));
00464| 
00465| 		return trigger;
00466| 	}
00467| 
00468| 	private findAllPinnedTriggers(workflow: IWorkflowBase, pinData?: IPinData) {
00469| 		return workflow.nodes
00470| 			.filter(
00471| 				(node) =>
00472| 					!node.disabled &&
00473| 					pinData?.[node.name] &&
00474| 					['trigger', 'webhook'].some((suffix) => node.type.toLowerCase().endsWith(suffix)) &&
00475| 					node.type !== 'n8n-nodes-base.respondToWebhook',
00476| 			)
00477| 			.sort((a) => (a.type.endsWith('webhook') ? -1 : 1));
00478| 	}
00479| 
00480| 	/**
00481| 	 * Checks if there is enough run data to run this as a partial execution and
00482| 	 * that we're not having the edge case that the destination node itself is a
00483| 	 * trigger.
00484| 	 */
00485| 	private partialExecutionFulfilsPreconditions(
00486| 		payload: WorkflowRequest.PartialManualExecutionToDestinationPayload,
00487| 	): boolean {
00488| 		// If the destination is a trigger node, we treat it as a full execution.
00489| 		if (this.isDestinationNodeATrigger(payload.destinationNode.nodeName, payload.workflowData)) {
00490| 			return false;
00491| 		}
00492| 
00493| 		// If we have enough run data to reach the destination from a trigger it's a partial execution.
00494| 		// Otherwise it's a full execution.
00495| 		return anyReachableRootHasRunData(
00496| 			DirectedGraph.fromNodesAndConnections(
00497| 				payload.workflowData.nodes,
00498| 				payload.workflowData.connections,
00499| 			),
00500| 			payload.destinationNode.nodeName,
00501| 			payload.runData,
00502| 		);
00503| 	}
00504| }
00505| 
00506| /**
00507|  * Type guard to check if payload is a PartialManualExecutionToDestinationPayload.
00508|  *
00509|  * A partial execution payload has both `destinationNode` and `runData`.
00510|  * This indicates execution to a specific node using existing run data.
00511|  */
00512| function isPartialExecution(
00513| 	payload: WorkflowRequest.ManualRunPayload,
00514| ): payload is WorkflowRequest.PartialManualExecutionToDestinationPayload {
00515| 	return 'destinationNode' in payload && 'runData' in payload;
00516| }
00517| 
00518| /**
00519|  * Type guard to check if payload is a FullManualExecutionFromKnownTriggerPayload.
00520|  *
00521|  * A known trigger payload has `triggerToStartFrom` specified but no `runData`.
00522|  * This indicates the user has selected a specific trigger node to start the execution from.
00523|  */
00524| function isFullExecutionFromKnownTrigger(
00525| 	payload: WorkflowRequest.ManualRunPayload,
00526| ): payload is WorkflowRequest.FullManualExecutionFromKnownTriggerPayload {
00527| 	return 'triggerToStartFrom' in payload;
00528| }
00529| 
00530| /**
00531|  * Type guard to check if payload is a FullManualExecutionFromUnknownTriggerPayload.
00532|  *
00533|  * An unknown trigger payload has neither `triggerToStartFrom` nor `runData`.
00534|  * The trigger will need to be determined.
00535|  */
00536| function isFullExecutionFromUnknownTrigger(
00537| 	payload: WorkflowRequest.ManualRunPayload,
00538| ): payload is WorkflowRequest.FullManualExecutionFromUnknownTriggerPayload {
00539| 	if ('triggerToStartFrom' in payload) {
00540| 		return false;
00541| 	}
00542| 	return !('runData' in payload);
00543| }
00544| 
00545| function triggerHasNoPinnedData(
00546| 	payload: WorkflowRequest.FullManualExecutionFromKnownTriggerPayload,
00547| ) {
00548| 	return payload.workflowData.pinData?.[payload.triggerToStartFrom.name] === undefined;
00549| }
00550| 
00551| function upgradeToFullManualExecutionFromUnknownTrigger(
00552| 	payload: WorkflowRequest.PartialManualExecutionToDestinationPayload,
00553| ): WorkflowRequest.FullManualExecutionFromUnknownTriggerPayload {
00554| 	// If the payload has runData or executionData, remove them to convert to full execution.
00555| 	return {
00556| 		workflowData: payload.workflowData,
00557| 		destinationNode: payload.destinationNode,
00558| 		agentRequest: payload.agentRequest,
00559| 	};
00560| }
00561| 

(End of file - total 561 lines)
</file>
```
```

---

## Assistant (Explore · big-pickle · 3.8s)

_Thinking:_




Now let me look at the WorkflowRunner which is the core execution engine:

```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/cli/src/workflow-runner.ts"
}
```
**Output:**
```
<file>
00001| /* eslint-disable @typescript-eslint/no-unsafe-argument */
00002| /* eslint-disable @typescript-eslint/no-unsafe-member-access */
00003| 
00004| /* eslint-disable @typescript-eslint/no-unsafe-assignment */
00005| import { Logger } from '@n8n/backend-common';
00006| import { ExecutionsConfig } from '@n8n/config';
00007| import { ExecutionRepository } from '@n8n/db';
00008| import { Container, Service } from '@n8n/di';
00009| import type { ExecutionLifecycleHooks } from 'n8n-core';
00010| import { ErrorReporter, InstanceSettings, WorkflowExecute } from 'n8n-core';
00011| import type {
00012| 	ExecutionError,
00013| 	IDeferredPromise,
00014| 	IExecuteResponsePromiseData,
00015| 	IPinData,
00016| 	IRun,
00017| 	WorkflowExecuteMode,
00018| 	IWorkflowExecutionDataProcess,
00019| } from 'n8n-workflow';
00020| import {
00021| 	createRunExecutionData,
00022| 	ExecutionCancelledError,
00023| 	ManualExecutionCancelledError,
00024| 	TimeoutExecutionCancelledError,
00025| 	Workflow,
00026| } from 'n8n-workflow';
00027| import PCancelable from 'p-cancelable';
00028| 
00029| import { ActiveExecutions } from '@/active-executions';
00030| import { ExecutionNotFoundError } from '@/errors/execution-not-found-error';
00031| import { MaxStalledCountError } from '@/errors/max-stalled-count.error';
00032| // eslint-disable-next-line import-x/no-cycle
00033| import {
00034| 	getLifecycleHooksForRegularMain,
00035| 	getLifecycleHooksForScalingWorker,
00036| 	getLifecycleHooksForScalingMain,
00037| } from '@/execution-lifecycle/execution-lifecycle-hooks';
00038| import { ExecutionDataService } from '@/executions/execution-data.service';
00039| import { CredentialsPermissionChecker } from '@/executions/pre-execution-checks';
00040| import { ManualExecutionService } from '@/manual-execution.service';
00041| import { NodeTypes } from '@/node-types';
00042| import type { ScalingService } from '@/scaling/scaling.service';
00043| import type { Job, JobData } from '@/scaling/scaling.types';
00044| import * as WorkflowExecuteAdditionalData from '@/workflow-execute-additional-data';
00045| import { WorkflowStaticDataService } from '@/workflows/workflow-static-data.service';
00046| 
00047| import { EventService } from './events/event.service';
00048| 
00049| @Service()
00050| export class WorkflowRunner {
00051| 	private scalingService: ScalingService;
00052| 
00053| 	constructor(
00054| 		private readonly logger: Logger,
00055| 		private readonly errorReporter: ErrorReporter,
00056| 		private readonly activeExecutions: ActiveExecutions,
00057| 		private readonly executionRepository: ExecutionRepository,
00058| 		private readonly workflowStaticDataService: WorkflowStaticDataService,
00059| 		private readonly nodeTypes: NodeTypes,
00060| 		private readonly credentialsPermissionChecker: CredentialsPermissionChecker,
00061| 		private readonly instanceSettings: InstanceSettings,
00062| 		private readonly manualExecutionService: ManualExecutionService,
00063| 		private readonly executionDataService: ExecutionDataService,
00064| 		private readonly eventService: EventService,
00065| 		private readonly executionsConfig: ExecutionsConfig,
00066| 	) {}
00067| 
00068| 	/** The process did error */
00069| 	async processError(
00070| 		error: ExecutionError | ExecutionNotFoundError,
00071| 		startedAt: Date,
00072| 		executionMode: WorkflowExecuteMode,
00073| 		executionId: string,
00074| 		hooks?: ExecutionLifecycleHooks,
00075| 	) {
00076| 		// This means the execution was probably cancelled and has already
00077| 		// been cleaned up.
00078| 		//
00079| 		// FIXME: This is a quick fix. The proper fix would be to not remove
00080| 		// the execution from the active executions while it's still running.
00081| 		if (
00082| 			error instanceof ExecutionNotFoundError ||
00083| 			error instanceof ExecutionCancelledError ||
00084| 			(typeof error.message === 'string' && error.message.includes('cancelled'))
00085| 		) {
00086| 			return;
00087| 		}
00088| 
00089| 		this.logger.error(`Problem with execution ${executionId}: ${error.message}. Aborting.`);
00090| 		this.errorReporter.error(error, { executionId });
00091| 
00092| 		const isQueueMode = this.executionsConfig.mode === 'queue';
00093| 
00094| 		// in queue mode, first do a sanity run for the edge case that the execution was not marked as stalled
00095| 		// by Bull even though it executed successfully, see https://github.com/OptimalBits/bull/issues/1415
00096| 
00097| 		if (isQueueMode) {
00098| 			const executionWithoutData = await this.executionRepository.findSingleExecution(executionId, {
00099| 				includeData: false,
00100| 			});
00101| 			if (executionWithoutData?.finished === true && executionWithoutData?.status === 'success') {
00102| 				// false positive, execution was successful
00103| 				return;
00104| 			}
00105| 		}
00106| 
00107| 		const fullRunData: IRun = {
00108| 			data: createRunExecutionData({
00109| 				resultData: {
00110| 					error: {
00111| 						...error,
00112| 						message: error.message,
00113| 						stack: error.stack,
00114| 					},
00115| 					runData: {},
00116| 				},
00117| 			}),
00118| 			finished: false,
00119| 			mode: executionMode,
00120| 			startedAt,
00121| 			stoppedAt: new Date(),
00122| 			status: 'error',
00123| 		};
00124| 
00125| 		// Remove from active execution with empty data. That will
00126| 		// set the execution to failed.
00127| 		this.activeExecutions.finalizeExecution(executionId, fullRunData);
00128| 
00129| 		await hooks?.runHook('workflowExecuteAfter', [fullRunData]);
00130| 	}
00131| 
00132| 	/** Run the workflow
00133| 	 * @param realtime This is used in queue mode to change the priority of an execution, making sure they are picked up quicker.
00134| 	 */
00135| 	async run(
00136| 		data: IWorkflowExecutionDataProcess,
00137| 		loadStaticData?: boolean,
00138| 		realtime?: boolean,
00139| 		restartExecutionId?: string,
00140| 		responsePromise?: IDeferredPromise<IExecuteResponsePromiseData>,
00141| 	): Promise<string> {
00142| 		// Register a new execution
00143| 		const executionId = await this.activeExecutions.add(data, restartExecutionId);
00144| 
00145| 		const { id: workflowId, nodes } = data.workflowData;
00146| 		try {
00147| 			await this.credentialsPermissionChecker.check(workflowId, nodes);
00148| 		} catch (error) {
00149| 			// Create a failed execution with the data for the node, save it and abort execution
00150| 			const runData = this.executionDataService.generateFailedExecutionFromError(
00151| 				data.executionMode,
00152| 				error,
00153| 				error.node,
00154| 			);
00155| 			const lifecycleHooks = getLifecycleHooksForRegularMain(data, executionId);
00156| 			await lifecycleHooks.runHook('workflowExecuteBefore', [undefined, data.executionData]);
00157| 			await lifecycleHooks.runHook('workflowExecuteAfter', [runData]);
00158| 			responsePromise?.reject(error);
00159| 			this.activeExecutions.finalizeExecution(executionId);
00160| 			return executionId;
00161| 		}
00162| 
00163| 		if (responsePromise) {
00164| 			this.activeExecutions.attachResponsePromise(executionId, responsePromise);
00165| 		}
00166| 
00167| 		// @TODO: Reduce to true branch once feature is stable
00168| 		const shouldEnqueue =
00169| 			process.env.OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS === 'true'
00170| 				? this.executionsConfig.mode === 'queue'
00171| 				: this.executionsConfig.mode === 'queue' && data.executionMode !== 'manual';
00172| 
00173| 		if (shouldEnqueue) {
00174| 			await this.enqueueExecution(executionId, workflowId, data, loadStaticData, realtime);
00175| 		} else {
00176| 			await this.runMainProcess(executionId, data, loadStaticData, restartExecutionId);
00177| 		}
00178| 
00179| 		// only run these when not in queue mode or when the execution is manual,
00180| 		// since these calls are now done by the worker directly
00181| 		if (
00182| 			this.executionsConfig.mode !== 'queue' ||
00183| 			this.instanceSettings.instanceType === 'worker' ||
00184| 			data.executionMode === 'manual' ||
00185| 			data.executionMode === 'chat'
00186| 		) {
00187| 			const postExecutePromise = this.activeExecutions.getPostExecutePromise(executionId);
00188| 			postExecutePromise.catch((error) => {
00189| 				if (error instanceof ExecutionCancelledError) return;
00190| 				this.errorReporter.error(error, {
00191| 					extra: { executionId, workflowId },
00192| 				});
00193| 				this.logger.error('There was an error in the post-execution promise', {
00194| 					error,
00195| 					executionId,
00196| 					workflowId,
00197| 				});
00198| 			});
00199| 		}
00200| 
00201| 		return executionId;
00202| 	}
00203| 
00204| 	/** Run the workflow in current process */
00205| 
00206| 	private async runMainProcess(
00207| 		executionId: string,
00208| 		data: IWorkflowExecutionDataProcess,
00209| 		loadStaticData?: boolean,
00210| 		restartExecutionId?: string,
00211| 	): Promise<void> {
00212| 		const workflowId = data.workflowData.id;
00213| 		if (loadStaticData === true && workflowId) {
00214| 			data.workflowData.staticData =
00215| 				await this.workflowStaticDataService.getStaticDataById(workflowId);
00216| 		}
00217| 
00218| 		// Soft timeout to stop workflow execution after current running node
00219| 		// Changes were made by adding the `workflowTimeout` to the `additionalData`
00220| 		// So that the timeout will also work for executions with nested workflows.
00221| 		let executionTimeout: NodeJS.Timeout;
00222| 
00223| 		const workflowSettings = data.workflowData.settings ?? {};
00224| 		let workflowTimeout = workflowSettings.executionTimeout ?? this.executionsConfig.timeout; // initialize with default
00225| 		if (workflowTimeout > 0) {
00226| 			workflowTimeout = Math.min(workflowTimeout, this.executionsConfig.maxTimeout);
00227| 		}
00228| 
00229| 		let pinData: IPinData | undefined;
00230| 		if (['manual', 'evaluation'].includes(data.executionMode)) {
00231| 			pinData = data.pinData ?? data.workflowData.pinData;
00232| 		}
00233| 
00234| 		const workflow = new Workflow({
00235| 			id: workflowId,
00236| 			name: data.workflowData.name,
00237| 			nodes: data.workflowData.nodes,
00238| 			connections: data.workflowData.connections,
00239| 			active: data.workflowData.activeVersionId !== null,
00240| 			nodeTypes: this.nodeTypes,
00241| 			staticData: data.workflowData.staticData,
00242| 			settings: workflowSettings,
00243| 			pinData,
00244| 		});
00245| 
00246| 		const additionalData = await WorkflowExecuteAdditionalData.getBase({
00247| 			userId: data.userId,
00248| 			workflowId: workflow.id,
00249| 			executionTimeoutTimestamp:
00250| 				workflowTimeout <= 0 ? undefined : Date.now() + workflowTimeout * 1000,
00251| 			workflowSettings,
00252| 		});
00253| 		// TODO: set this in queue mode as well
00254| 		additionalData.restartExecutionId = restartExecutionId;
00255| 		additionalData.streamingEnabled = data.streamingEnabled;
00256| 
00257| 		additionalData.executionId = executionId;
00258| 
00259| 		this.logger.debug(
00260| 			`Execution for workflow ${data.workflowData.name} was assigned id ${executionId}`,
00261| 			{ executionId },
00262| 		);
00263| 		let workflowExecution: PCancelable<IRun>;
00264| 		await this.executionRepository.setRunning(executionId); // write
00265| 
00266| 		try {
00267| 			const lifecycleHooks = getLifecycleHooksForRegularMain(data, executionId);
00268| 			additionalData.hooks = lifecycleHooks;
00269| 
00270| 			lifecycleHooks.addHandler('sendResponse', (response) => {
00271| 				this.activeExecutions.resolveResponsePromise(executionId, response);
00272| 			});
00273| 
00274| 			if (data.streamingEnabled) {
00275| 				lifecycleHooks.addHandler('sendChunk', (chunk) => {
00276| 					data.httpResponse?.write(JSON.stringify(chunk) + '\n');
00277| 					data.httpResponse?.flush?.();
00278| 				});
00279| 			}
00280| 
00281| 			additionalData.setExecutionStatus = WorkflowExecuteAdditionalData.setExecutionStatus.bind({
00282| 				executionId,
00283| 			});
00284| 
00285| 			additionalData.sendDataToUI = WorkflowExecuteAdditionalData.sendDataToUI.bind({
00286| 				pushRef: data.pushRef,
00287| 			});
00288| 
00289| 			if (data.executionData !== undefined) {
00290| 				this.logger.debug(`Execution ID ${executionId} had Execution data. Running with payload.`, {
00291| 					executionId,
00292| 				});
00293| 				const workflowExecute = new WorkflowExecute(
00294| 					additionalData,
00295| 					data.executionMode,
00296| 					data.executionData,
00297| 				);
00298| 				workflowExecution = workflowExecute.processRunExecutionData(workflow);
00299| 			} else {
00300| 				workflowExecution = this.manualExecutionService.runManually(
00301| 					data,
00302| 					workflow,
00303| 					additionalData,
00304| 					executionId,
00305| 					pinData,
00306| 				);
00307| 			}
00308| 
00309| 			this.activeExecutions.attachWorkflowExecution(executionId, workflowExecution);
00310| 
00311| 			if (workflowTimeout > 0) {
00312| 				let timeout = Math.min(workflowTimeout, this.executionsConfig.maxTimeout) * 1000; // as milliseconds
00313| 				if (data.startedAt && data.startedAt instanceof Date) {
00314| 					// If startedAt is set, we calculate the timeout based on the startedAt time
00315| 					// This is useful for executions that were waiting in a waiting state
00316| 					// and we want to ensure the timeout is relative to when the execution started.
00317| 					const now = Date.now();
00318| 					timeout = Math.max(timeout - (now - data.startedAt.getTime()), 0);
00319| 				}
00320| 				if (timeout === 0) {
00321| 					this.activeExecutions.stopExecution(
00322| 						executionId,
00323| 						new TimeoutExecutionCancelledError(executionId),
00324| 					);
00325| 				} else {
00326| 					executionTimeout = setTimeout(() => {
00327| 						void this.activeExecutions.stopExecution(
00328| 							executionId,
00329| 							new TimeoutExecutionCancelledError(executionId),
00330| 						);
00331| 					}, timeout);
00332| 				}
00333| 			}
00334| 
00335| 			workflowExecution
00336| 				.then((fullRunData) => {
00337| 					clearTimeout(executionTimeout);
00338| 					if (workflowExecution.isCanceled) {
00339| 						fullRunData.finished = false;
00340| 					}
00341| 					fullRunData.status = this.activeExecutions.getStatus(executionId);
00342| 					this.activeExecutions.resolveExecutionResponsePromise(executionId);
00343| 					this.activeExecutions.finalizeExecution(executionId, fullRunData);
00344| 				})
00345| 				.catch(
00346| 					async (error) =>
00347| 						await this.processError(
00348| 							error,
00349| 							new Date(),
00350| 							data.executionMode,
00351| 							executionId,
00352| 							additionalData.hooks,
00353| 						),
00354| 				);
00355| 		} catch (error) {
00356| 			await this.processError(
00357| 				error,
00358| 				new Date(),
00359| 				data.executionMode,
00360| 				executionId,
00361| 				additionalData.hooks,
00362| 			);
00363| 
00364| 			throw error;
00365| 		}
00366| 	}
00367| 
00368| 	private async enqueueExecution(
00369| 		executionId: string,
00370| 		workflowId: string,
00371| 		data: IWorkflowExecutionDataProcess,
00372| 		loadStaticData?: boolean,
00373| 		realtime?: boolean,
00374| 	): Promise<void> {
00375| 		const jobData: JobData = {
00376| 			workflowId,
00377| 			executionId,
00378| 			loadStaticData: !!loadStaticData,
00379| 			pushRef: data.pushRef,
00380| 			streamingEnabled: data.streamingEnabled,
00381| 		};
00382| 
00383| 		if (!this.scalingService) {
00384| 			const { ScalingService } = await import('@/scaling/scaling.service');
00385| 			this.scalingService = Container.get(ScalingService);
00386| 			await this.scalingService.setupQueue();
00387| 		}
00388| 
00389| 		// TODO: For realtime jobs should probably also not do retry or not retry if they are older than x seconds.
00390| 		//       Check if they get retried by default and how often.
00391| 		let job: Job;
00392| 		let lifecycleHooks: ExecutionLifecycleHooks;
00393| 		try {
00394| 			job = await this.scalingService.addJob(jobData, { priority: realtime ? 50 : 100 });
00395| 
00396| 			lifecycleHooks = getLifecycleHooksForScalingMain(data, executionId);
00397| 
00398| 			// Normally also workflow should be supplied here but as it only used for sending
00399| 			// data to editor-UI is not needed.
00400| 			await lifecycleHooks.runHook('workflowExecuteBefore', [undefined, data.executionData]);
00401| 		} catch (error) {
00402| 			// We use "getLifecycleHooksForScalingWorker" as "getLifecycleHooksForScalingMain" does not contain the
00403| 			// "workflowExecuteAfter" which we require.
00404| 			const lifecycleHooks = getLifecycleHooksForScalingWorker(data, executionId);
00405| 			await this.processError(error, new Date(), data.executionMode, executionId, lifecycleHooks);
00406| 			throw error;
00407| 		}
00408| 
00409| 		const workflowExecution: PCancelable<IRun> = new PCancelable(
00410| 			async (resolve, reject, onCancel) => {
00411| 				onCancel.shouldReject = false;
00412| 				onCancel(async () => {
00413| 					await this.scalingService.stopJob(job);
00414| 
00415| 					// We use "getLifecycleHooksForScalingWorker" as "getLifecycleHooksForScalingMain" does not contain the
00416| 					// "workflowExecuteAfter" which we require.
00417| 					const lifecycleHooks = getLifecycleHooksForScalingWorker(data, executionId);
00418| 					const error = new ManualExecutionCancelledError(executionId);
00419| 					await this.processError(
00420| 						error,
00421| 						new Date(),
00422| 						data.executionMode,
00423| 						executionId,
00424| 						lifecycleHooks,
00425| 					);
00426| 
00427| 					reject(error);
00428| 				});
00429| 
00430| 				try {
00431| 					await job.finished();
00432| 				} catch (error) {
00433| 					if (
00434| 						error instanceof Error &&
00435| 						typeof error.message === 'string' &&
00436| 						error.message.includes('job stalled more than maxStalledCount')
00437| 					) {
00438| 						error = new MaxStalledCountError(error);
00439| 						this.eventService.emit('job-stalled', {
00440| 							executionId: job.data.executionId,
00441| 							workflowId: job.data.workflowId,
00442| 							hostId: this.instanceSettings.hostId,
00443| 							jobId: job.id.toString(),
00444| 						});
00445| 					}
00446| 
00447| 					// We use "getLifecycleHooksForScalingWorker" as "getLifecycleHooksForScalingMain" does not contain the
00448| 					// "workflowExecuteAfter" which we require.
00449| 					const lifecycleHooks = getLifecycleHooksForScalingWorker(data, executionId);
00450| 
00451| 					await this.processError(
00452| 						error,
00453| 						new Date(),
00454| 						data.executionMode,
00455| 						executionId,
00456| 						lifecycleHooks,
00457| 					);
00458| 
00459| 					reject(error);
00460| 				}
00461| 
00462| 				const fullExecutionData = await this.executionRepository.findSingleExecution(executionId, {
00463| 					includeData: true,
00464| 					unflattenData: true,
00465| 				});
00466| 				if (!fullExecutionData) {
00467| 					return reject(new Error(`Could not find execution with id "${executionId}"`));
00468| 				}
00469| 
00470| 				const runData: IRun = {
00471| 					finished: fullExecutionData.finished,
00472| 					mode: fullExecutionData.mode,
00473| 					startedAt: fullExecutionData.startedAt,
00474| 					stoppedAt: fullExecutionData.stoppedAt,
00475| 					status: fullExecutionData.status,
00476| 					data: fullExecutionData.data,
00477| 					jobId: job.id.toString(),
00478| 				};
00479| 
00480| 				this.activeExecutions.finalizeExecution(executionId, runData);
00481| 
00482| 				// Normally also static data should be supplied here but as it only used for sending
00483| 				// data to editor-UI is not needed.
00484| 				await lifecycleHooks.runHook('workflowExecuteAfter', [runData]);
00485| 
00486| 				resolve(runData);
00487| 			},
00488| 		);
00489| 
00490| 		workflowExecution.catch(() => {
00491| 			// We `reject` this promise if the execution fails
00492| 			// but the error is handled already by processError
00493| 			// So we're just preventing crashes here.
00494| 		});
00495| 
00496| 		this.activeExecutions.attachWorkflowExecution(executionId, workflowExecution);
00497| 	}
00498| }
00499| 

(End of file - total 499 lines)
</file>
```
```

---

## Assistant (Explore · big-pickle · 16.6s)

_Thinking:_




Now let me look at the WorkflowExecute class from the core package which is the actual execution engine:

```
Tool: glob

**Input:**
```json
{
  "pattern": "packages/core/**/*.ts"
}
```
**Output:**
```
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/file-system-helper-functions.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/__tests__/file-system-helper-functions.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/requests-response.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/find-start-nodes.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/index.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/__tests__/find-start-nodes.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/__tests__/helpers.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/directed-graph.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/find-trigger-for-partial-execution.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/webhook-context.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/node-execution-context.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/__tests__/local-load-options-context.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/__tests__/supply-data-context.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/__tests__/node-execution-context.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/__tests__/load-options-context.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/__tests__/trigger-context.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/__tests__/shared-tests.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/__tests__/poll-context.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/base-execute-context.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/supply-data-context.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/local-load-options-context.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/request-helper-functions.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/get-input-connection-data.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/binary-helper-functions.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/__tests__/request-helper-functions.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/__tests__/execution-metadata.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/__tests__/binary-helper-functions.test.ts
/home/ab/git-projs/n8n/packages/core/nodes-testing/node-test-harness.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/execution-context-hook-registry.service.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/execution-context.service.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/index.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/workflow-execute.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/workflow-execute-process-process-run-execution-data.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/routing-node.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/requests-response.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/workflow-execute-run-node.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/execution-context.service.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/execution-context.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/execution-context-hook-service.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/execution-context.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/__tests__/execute-context.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/__tests__/hook-context.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/mock-node-types.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/data-table-helper-functions.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/routing-node.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/ssh-clients-manager.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/recreate-node-execution-stack.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/get-incoming-data.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/get-source-data-groups.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/run-data-utils.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/__tests__/get-source-data-groups.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/__tests__/run-data-utils.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/__tests__/to-iconnections.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/__tests__/rewire-graph.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/__tests__/handle-cycles.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/__tests__/to-itask-data.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/__tests__/recreate-node-execution-stack.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/__tests__/find-trigger-for-partial-execution.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/__tests__/find-subgraph.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/find-subgraph.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/handle-cycles.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/filter-disabled-nodes.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/rewire-graph.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/clean-run-data.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/triggers-and-pollers.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/__tests__/directed-graph.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/__tests__/clean-run-data.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/partial-execution-utils/__tests__/filter-disabled-nodes.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/trigger-context.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/hook-context.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/poll-context.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/index.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/__tests__/webhook-context.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/credentials-test-context.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/workflow-node-context.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/execute-single-context.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/execution-metadata.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/construct-execution-metadata.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/scheduling-helper-functions.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/create-node-as-tool.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/__tests__/parse-incoming-message.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/__tests__/cleanup-parameter-data.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/__tests__/scheduling-helper-functions.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/__tests__/create-node-as-tool.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/utils/__tests__/ssh-tunnel-helper-functions.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/external-secrets-proxy.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/active-workflows.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/ssh-clients-manager.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/external-secrets-proxy.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/execution-lifecycle-hooks.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/scheduled-task-manager.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/active-workflows.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/triggers-and-pollers.test.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/execution-lifecycle-hooks.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/interfaces.ts
/home/ab/git-projs/n8n/packages/core/src/execution-engine/node-execution-context/__tests__/execute-single-context.test.ts
/home/ab/git-projs/n8n/packages/core/nodes-testing/credentials-helper.ts
/home/ab/git-projs/n8n/packages/core/nodes-testing/credential-types.ts
/home/ab/git-projs/n8n/packages/core/nodes-testing/node-types.ts
/home/ab/git-projs/n8n/packages/core/nodes-testing/load-nodes-and-credentials.ts

(Results are truncated. Consider using a more specific path or pattern.)
```
```

---

## Assistant (Explore · big-pickle · 4.5s)

_Thinking:_





```
Tool: glob

**Input:**
```json
{
  "pattern": "packages/core/src/execution-engine/workflow-execute.ts"
}
```
**Output:**
```
/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts
```
```

---

## Assistant (Explore · big-pickle · 3.4s)

_Thinking:_





```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts",
  "limit": 200
}
```
**Output:**
```
<file>
00001| /* eslint-disable @typescript-eslint/prefer-optional-chain */
00002| /* eslint-disable @typescript-eslint/no-unsafe-member-access */
00003| /* eslint-disable @typescript-eslint/no-unsafe-assignment */
00004| /* eslint-disable @typescript-eslint/prefer-nullish-coalescing */
00005| import { GlobalConfig } from '@n8n/config';
00006| import { TOOL_EXECUTOR_NODE_NAME } from '@n8n/constants';
00007| import { Container } from '@n8n/di';
00008| import * as assert from 'assert/strict';
00009| import { setMaxListeners } from 'events';
00010| import get from 'lodash/get';
00011| import type {
00012| 	ExecutionBaseError,
00013| 	ExecutionStatus,
00014| 	GenericValue,
00015| 	IConnection,
00016| 	IDataObject,
00017| 	IExecuteData,
00018| 	INode,
00019| 	INodeExecutionData,
00020| 	IPairedItemData,
00021| 	IPinData,
00022| 	IRun,
00023| 	IRunData,
00024| 	ITaskData,
00025| 	ITaskDataConnections,
00026| 	ITaskMetadata,
00027| 	NodeApiError,
00028| 	NodeOperationError,
00029| 	Workflow,
00030| 	IRunExecutionData,
00031| 	IWorkflowExecuteAdditionalData,
00032| 	WorkflowExecuteMode,
00033| 	CloseFunction,
00034| 	IRunNodeResponse,
00035| 	IWorkflowIssues,
00036| 	INodeIssues,
00037| 	INodeType,
00038| 	ITaskStartedData,
00039| 	AiAgentRequest,
00040| 	IWorkflowExecutionDataProcess,
00041| 	EngineRequest,
00042| 	EngineResponse,
00043| 	IDestinationNode,
00044| } from 'n8n-workflow';
00045| import {
00046| 	LoggerProxy as Logger,
00047| 	NodeHelpers,
00048| 	NodeConnectionTypes,
00049| 	ApplicationError,
00050| 	sleep,
00051| 	Node,
00052| 	UnexpectedError,
00053| 	UserError,
00054| 	OperationalError,
00055| 	TimeoutExecutionCancelledError,
00056| 	ManualExecutionCancelledError,
00057| 	createRunExecutionData,
00058| } from 'n8n-workflow';
00059| import PCancelable from 'p-cancelable';
00060| 
00061| import { ErrorReporter } from '@/errors/error-reporter';
00062| import { WorkflowHasIssuesError } from '@/errors/workflow-has-issues.error';
00063| import * as NodeExecuteFunctions from '@/node-execute-functions';
00064| import { assertExecutionDataExists } from '@/utils/assertions';
00065| import { isJsonCompatible } from '@/utils/is-json-compatible';
00066| 
00067| import { establishExecutionContext } from './execution-context';
00068| import type { ExecutionLifecycleHooks } from './execution-lifecycle-hooks';
00069| import { ExecuteContext, PollContext } from './node-execution-context';
00070| import {
00071| 	DirectedGraph,
00072| 	findStartNodes,
00073| 	findSubgraph,
00074| 	findTriggerForPartialExecution,
00075| 	cleanRunData,
00076| 	recreateNodeExecutionStack,
00077| 	handleCycles,
00078| 	filterDisabledNodes,
00079| 	rewireGraph,
00080| 	getNextExecutionIndex,
00081| } from './partial-execution-utils';
00082| import { handleRequest, isEngineRequest, makeEngineResponse } from './requests-response';
00083| import { RoutingNode } from './routing-node';
00084| import { TriggersAndPollers } from './triggers-and-pollers';
00085| 
00086| export class WorkflowExecute {
00087| 	private status: ExecutionStatus = 'new';
00088| 
00089| 	private readonly abortController = new AbortController();
00090| 	timedOut: boolean = false;
00091| 
00092| 	constructor(
00093| 		private readonly additionalData: IWorkflowExecuteAdditionalData,
00094| 		private readonly mode: WorkflowExecuteMode,
00095| 		private runExecutionData: IRunExecutionData = createRunExecutionData(),
00096| 	) {}
00097| 
00098| 	/**
00099| 	 * Executes the given workflow.
00100| 	 *
00101| 	 * @param {Workflow} workflow The workflow to execute
00102| 	 * @param {INode[]} [startNode] Node to start execution from
00103| 	 * @param {string} [destinationNode] Node to stop execution at
00104| 	 */
00105| 	// IMPORTANT: Do not add "async" to this function, it will then convert the
00106| 	//            PCancelable to a regular Promise and does so not allow canceling
00107| 	//            active executions anymore
00108| 	// eslint-disable-next-line @typescript-eslint/promise-function-async
00109| 	run(
00110| 		workflow: Workflow,
00111| 		startNode?: INode,
00112| 		destinationNode?: IDestinationNode,
00113| 		pinData?: IPinData,
00114| 		triggerToStartFrom?: IWorkflowExecutionDataProcess['triggerToStartFrom'],
00115| 	): PCancelable<IRun> {
00116| 		this.status = 'running';
00117| 
00118| 		// Get the nodes to start workflow execution from
00119| 		startNode = startNode || workflow.getStartNode(destinationNode?.nodeName);
00120| 
00121| 		if (startNode === undefined) {
00122| 			throw new ApplicationError('No node to start the workflow from could be found');
00123| 		}
00124| 
00125| 		// If a destination node is given we only run the direct parent nodes and no others
00126| 		let runNodeFilter: string[] | undefined;
00127| 		if (destinationNode) {
00128| 			runNodeFilter = workflow.getParentNodes(destinationNode.nodeName);
00129| 			if (destinationNode.mode === 'inclusive') {
00130| 				runNodeFilter.push(destinationNode.nodeName);
00131| 			}
00132| 		}
00133| 
00134| 		// Initialize the data of the start nodes
00135| 		const nodeExecutionStack: IExecuteData[] = [
00136| 			{
00137| 				node: startNode,
00138| 				data: triggerToStartFrom?.data?.data ?? {
00139| 					main: [
00140| 						[
00141| 							{
00142| 								json: {},
00143| 							},
00144| 						],
00145| 					],
00146| 				},
00147| 				source: null,
00148| 			},
00149| 		];
00150| 
00151| 		this.runExecutionData = createRunExecutionData({
00152| 			startData: {
00153| 				destinationNode,
00154| 				runNodeFilter,
00155| 			},
00156| 			executionData: {
00157| 				nodeExecutionStack,
00158| 			},
00159| 			resultData: {
00160| 				pinData,
00161| 			},
00162| 		});
00163| 
00164| 		return this.processRunExecutionData(workflow);
00165| 	}
00166| 
00167| 	isLegacyExecutionOrder(workflow: Workflow): boolean {
00168| 		return workflow.settings.executionOrder !== 'v1';
00169| 	}
00170| 
00171| 	// IMPORTANT: Do not add "async" to this function, it will then convert the
00172| 	//            PCancelable to a regular Promise and does so not allow canceling
00173| 	//            active executions anymore
00174| 	// eslint-disable-next-line @typescript-eslint/promise-function-async
00175| 	runPartialWorkflow2(
00176| 		workflow: Workflow,
00177| 		runData: IRunData,
00178| 		pinData: IPinData = {},
00179| 		dirtyNodeNames: string[] = [],
00180| 		destinationNode: IDestinationNode,
00181| 		agentRequest?: AiAgentRequest,
00182| 	): PCancelable<IRun> {
00183| 		const originalDestination = { ...destinationNode };
00184| 
00185| 		let destination = workflow.getNode(destinationNode.nodeName);
00186| 		assert.ok(
00187| 			destination,
00188| 			`Could not find a node with the name ${destinationNode.nodeName} in the workflow.`,
00189| 		);
00190| 
00191| 		let graph = DirectedGraph.fromWorkflow(workflow);
00192| 
00193| 		const destinationNodeType = workflow.nodeTypes.getByNameAndVersion(
00194| 			destination.type,
00195| 			destination.typeVersion,
00196| 		);
00197| 		// Partial execution of nodes as tools
00198| 		if (NodeHelpers.isTool(destinationNodeType.description, destination.parameters)) {
00199| 			graph = rewireGraph(destination, graph, agentRequest);
00200| 			workflow = graph.toWorkflow({ ...workflow });

(File has more lines. Use 'offset' parameter to read beyond line 200)
</file>
```
```

---

## Assistant (Explore · big-pickle · 4.1s)

_Thinking:_





```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts",
  "limit": 100,
  "offset": 200
}
```
**Output:**
```
<file>
00201| 			// Rewire destination node to the virtual agent
00202| 			const toolExecutorNode = workflow.getNode(TOOL_EXECUTOR_NODE_NAME);
00203| 			if (!toolExecutorNode) {
00204| 				throw new OperationalError('ToolExecutor can not be found');
00205| 			}
00206| 			destination = toolExecutorNode;
00207| 			// TODO(CAT-1265): Verify that this functionality works as expected.
00208| 			destinationNode = { nodeName: toolExecutorNode.name, mode: 'inclusive' };
00209| 		}
00210| 
00211| 		// 1. Find the Trigger
00212| 		let trigger = findTriggerForPartialExecution(workflow, destinationNode.nodeName, runData);
00213| 		if (trigger === undefined) {
00214| 			// destination has parents but none of them are triggers, so find the closest
00215| 			// parent node that has run data, and treat that parent as starting point
00216| 
00217| 			let startNode;
00218| 
00219| 			const parentNodes = workflow.getParentNodes(destinationNode.nodeName);
00220| 
00221| 			for (const nodeName of parentNodes) {
00222| 				if (runData[nodeName]) {
00223| 					startNode = workflow.getNode(nodeName);
00224| 					break;
00225| 				}
00226| 			}
00227| 
00228| 			if (!startNode) {
00229| 				throw new UserError('Connect a trigger to run this node');
00230| 			}
00231| 
00232| 			trigger = startNode;
00233| 		}
00234| 
00235| 		// 2. Find the Subgraph
00236| 		graph = findSubgraph({ graph: filterDisabledNodes(graph), destination, trigger });
00237| 		const filteredNodes = graph.getNodes();
00238| 
00239| 		// 3. Find the Start Nodes
00240| 		const dirtyNodes = graph.getNodesByNames(dirtyNodeNames);
00241| 		runData = cleanRunData(runData, graph, dirtyNodes);
00242| 		let startNodes = findStartNodes({ graph, trigger, destination, runData, pinData });
00243| 
00244| 		// 4. Detect Cycles
00245| 		// 5. Handle Cycles
00246| 		startNodes = handleCycles(graph, startNodes, trigger);
00247| 
00248| 		// 6. Clean Run Data
00249| 		runData = cleanRunData(runData, graph, startNodes);
00250| 
00251| 		// 7. Recreate Execution Stack
00252| 		const { nodeExecutionStack, waitingExecution, waitingExecutionSource } =
00253| 			recreateNodeExecutionStack(graph, startNodes, runData, pinData ?? {});
00254| 
00255| 		// 8. Execute
00256| 
00257| 		// Increment currentExecutionIndex based on previous run
00258| 		this.additionalData.currentNodeExecutionIndex = getNextExecutionIndex(runData);
00259| 
00260| 		this.status = 'running';
00261| 		this.runExecutionData = createRunExecutionData({
00262| 			startData: {
00263| 				destinationNode,
00264| 				originalDestinationNode: originalDestination,
00265| 				runNodeFilter: Array.from(filteredNodes.values()).map((node) => node.name),
00266| 			},
00267| 			resultData: {
00268| 				runData,
00269| 				pinData,
00270| 			},
00271| 			executionData: {
00272| 				nodeExecutionStack,
00273| 				waitingExecution,
00274| 				waitingExecutionSource,
00275| 			},
00276| 		});
00277| 
00278| 		// Still passing the original workflow here, because the WorkflowDataProxy
00279| 		// needs it to create more useful error messages, e.g. differentiate
00280| 		// between a node not being connected to the node referencing it or a node
00281| 		// not existing in the workflow.
00282| 		return this.processRunExecutionData(workflow);
00283| 	}
00284| 
00285| 	/**
00286| 	 * Merges temporary execution metadata into the final runData structure.
00287| 	 * During workflow execution, metadata is collected in a temporary location
00288| 	 * (executionData.metadata). This method moves that metadata to its final
00289| 	 * location in the resultData.runData for each node.
00290| 	 *
00291| 	 * @remarks
00292| 	 * - Metadata from multiple runs is preserved using run indices
00293| 	 * - Existing metadata in runData is preserved and merged with new metadata
00294| 	 * - If no metadata exists, the operation is a no-op
00295| 	 */
00296| 	moveNodeMetadata(): void {
00297| 		const metadata = get(this.runExecutionData, 'executionData.metadata');
00298| 
00299| 		if (metadata) {
00300| 			const runData = get(this.runExecutionData, 'resultData.runData');

(File has more lines. Use 'offset' parameter to read beyond line 300)
</file>
```
```

---

## Assistant (Explore · big-pickle · 4.3s)

_Thinking:_





```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts",
  "limit": 100,
  "offset": 400
}
```
**Output:**
```
<file>
00401| 			workflow.connectionsByDestinationNode[connectionData.node]?.main?.length ?? 0;
00402| 		if (numberOfInputs > 1) {
00403| 			// Node has multiple inputs
00404| 			let nodeWasWaiting = true;
00405| 
00406| 			if (!this.runExecutionData.executionData!.waitingExecutionSource) {
00407| 				this.runExecutionData.executionData!.waitingExecutionSource = {};
00408| 			}
00409| 
00410| 			// Check if there is already data for the node
00411| 			if (
00412| 				this.runExecutionData.executionData!.waitingExecution[connectionData.node] === undefined
00413| 			) {
00414| 				// Node does not have data yet so create a new empty one
00415| 				this.runExecutionData.executionData!.waitingExecution[connectionData.node] = {};
00416| 				this.runExecutionData.executionData!.waitingExecutionSource[connectionData.node] = {};
00417| 				nodeWasWaiting = false;
00418| 			}
00419| 
00420| 			// Figure out if the node is already waiting with partial data to which to add the
00421| 			// data to or if a new entry has to get created
00422| 			let createNewWaitingEntry = true;
00423| 
00424| 			if (
00425| 				Object.keys(this.runExecutionData.executionData!.waitingExecution[connectionData.node])
00426| 					.length > 0
00427| 			) {
00428| 				// Check if there is already data for the input on all of the waiting nodes
00429| 				for (const index of Object.keys(
00430| 					this.runExecutionData.executionData!.waitingExecution[connectionData.node],
00431| 				)) {
00432| 					if (
00433| 						!this.runExecutionData.executionData!.waitingExecution[connectionData.node][
00434| 							parseInt(index)
00435| 						].main[connectionData.index]
00436| 					) {
00437| 						// Data for the input is missing so we can add it to the existing entry
00438| 						createNewWaitingEntry = false;
00439| 						waitingNodeIndex = parseInt(index);
00440| 						break;
00441| 					}
00442| 				}
00443| 			}
00444| 
00445| 			if (waitingNodeIndex === undefined) {
00446| 				waitingNodeIndex = Object.values(
00447| 					this.runExecutionData.executionData!.waitingExecution[connectionData.node],
00448| 				).length;
00449| 			}
00450| 
00451| 			if (createNewWaitingEntry) {
00452| 				// There is currently no node waiting that does not already have data for
00453| 				// the given input, so create a new entry
00454| 
00455| 				this.prepareWaitingToExecution(
00456| 					connectionData.node,
00457| 					workflow.connectionsByDestinationNode[connectionData.node].main.length,
00458| 					waitingNodeIndex,
00459| 				);
00460| 			}
00461| 
00462| 			// Add the new data
00463| 			if (nodeSuccessData === null) {
00464| 				this.runExecutionData.executionData!.waitingExecution[connectionData.node][
00465| 					waitingNodeIndex
00466| 				].main[connectionData.index] = null;
00467| 				this.runExecutionData.executionData!.waitingExecutionSource[connectionData.node][
00468| 					waitingNodeIndex
00469| 				].main[connectionData.index] = null;
00470| 			} else {
00471| 				this.runExecutionData.executionData!.waitingExecution[connectionData.node][
00472| 					waitingNodeIndex
00473| 				].main[connectionData.index] = nodeSuccessData[outputIndex];
00474| 
00475| 				this.runExecutionData.executionData!.waitingExecutionSource[connectionData.node][
00476| 					waitingNodeIndex
00477| 				].main[connectionData.index] = {
00478| 					previousNode: parentNodeName,
00479| 					previousNodeOutput: outputIndex || undefined,
00480| 					previousNodeRun: runIndex || undefined,
00481| 				};
00482| 			}
00483| 
00484| 			// Check if all data exists now
00485| 			let thisExecutionData: INodeExecutionData[] | null;
00486| 			let allDataFound = true;
00487| 			for (
00488| 				let i = 0;
00489| 				i <
00490| 				this.runExecutionData.executionData!.waitingExecution[connectionData.node][waitingNodeIndex]
00491| 					.main.length;
00492| 				i++
00493| 			) {
00494| 				thisExecutionData =
00495| 					this.runExecutionData.executionData!.waitingExecution[connectionData.node][
00496| 						waitingNodeIndex
00497| 					].main[i];
00498| 				if (thisExecutionData === null) {
00499| 					allDataFound = false;
00500| 					break;

(File has more lines. Use 'offset' parameter to read beyond line 500)
</file>
```
```

---

## Assistant (Explore · big-pickle · 3.5s)

_Thinking:_




Let me look at the main execution processing method:

```
Tool: grep

**Input:**
```json
{
  "path": "/home/ab/git-projs/n8n/packages/core/src/execution-engine",
  "pattern": "processRunExecutionData"
}
```
**Output:**
```
Found 41 matches
/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts:
  Line 164: 		return this.processRunExecutionData(workflow);
  Line 282: 		return this.processRunExecutionData(workflow);
  Line 1404: 	processRunExecutionData(workflow: Workflow): PCancelable<IRun> {

/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/workflow-execute.test.ts:
  Line 543: 			jest.spyOn(workflowExecute, 'processRunExecutionData').mockImplementationOnce(jest.fn());
  Line 573: 			jest.spyOn(workflowExecute, 'processRunExecutionData').mockImplementationOnce(jest.fn());
  Line 651: 			const processRunExecutionDataSpy = jest
  Line 652: 				.spyOn(workflowExecute, 'processRunExecutionData')
  Line 671: 			expect(processRunExecutionDataSpy).toHaveBeenCalledTimes(1);
  Line 672: 			const nodes = Object.keys(processRunExecutionDataSpy.mock.calls[0][0].nodes);
  Line 716: 			jest.spyOn(workflowExecute, 'processRunExecutionData').mockImplementationOnce(jest.fn());
  Line 769: 			jest.spyOn(workflowExecute, 'processRunExecutionData').mockImplementationOnce(jest.fn());
  Line 822: 			jest.spyOn(workflowExecute, 'processRunExecutionData').mockImplementationOnce(jest.fn());
  Line 875: 			const processRunExecutionDataSpy = jest
  Line 876: 				.spyOn(workflowExecute, 'processRunExecutionData')
  Line 914: 			expect(processRunExecutionDataSpy).toHaveBeenCalledTimes(1);
  Line 915: 			expect(processRunExecutionDataSpy).toHaveBeenCalledWith(expectedGraph);
  Line 950: 			const processRunExecutionDataSpy = jest.spyOn(workflowExecute, 'processRunExecutionData');
  Line 959: 			expect(processRunExecutionDataSpy).toHaveBeenCalledTimes(1);
  Line 996: 			const processRunExecutionDataSpy = jest.spyOn(workflowExecute, 'processRunExecutionData');
  Line 1005: 			expect(processRunExecutionDataSpy).toHaveBeenCalledTimes(1);
  Line 1036: 			const processRunExecutionDataSpy = jest
  Line 1037: 				.spyOn(workflowExecute, 'processRunExecutionData')
  Line 1047: 			expect(processRunExecutionDataSpy).toHaveBeenCalledTimes(1);
  Line 2668: 			const promise = workflowExecute.processRunExecutionData(workflow);
  Line 2764: 			const promise = workflowExecute.processRunExecutionData(workflow);

/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/workflow-execute-process-process-run-execution-data.test.ts:
  Line 27: describe('processRunExecutionData', () => {
  Line 56: 		expect(() => workflowExecute.processRunExecutionData(workflow)).toThrowError(
  Line 77: 		const result = await workflowExecute.processRunExecutionData(workflow);
  Line 103: 		await workflowExecute.processRunExecutionData(workflow);
  Line 163: 		await workflowExecute.processRunExecutionData(workflowInstance);
  Line 207: 			const result = await workflowExecute.processRunExecutionData(workflow);
  Line 240: 			expect(() => workflowExecute.processRunExecutionData(workflow)).toThrowError(
  Line 272: 			expect(() => workflowExecute.processRunExecutionData(workflow)).not.toThrowError();
  Line 360: 			const result = await workflowExecute.processRunExecutionData(workflow);
  Line 510: 			const result = await workflowExecute.processRunExecutionData(workflow);
  Line 621: 			const result = await workflowExecute.processRunExecutionData(workflow);
  Line 703: 			const result = await workflowExecute.processRunExecutionData(workflow);
  Line 757: 			const result = await workflowExecute.processRunExecutionData(workflow);
  Line 790: 			const result = await workflowExecute.processRunExecutionData(workflow);
  Line 895: 			const result = await workflowExecute.processRunExecutionData(workflow);
  Line 1009: 			await expect(workflowExecute.processRunExecutionData(workflow)).resolves.toBeTruthy();
```
```

---

## Assistant (Explore · big-pickle · 5.5s)

_Thinking:_





```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts",
  "limit": 100,
  "offset": 1400
}
```
**Output:**
```
<file>
01401| 	//            PCancelable to a regular Promise and does so not allow canceling
01402| 	//            active executions anymore
01403| 	// eslint-disable-next-line @typescript-eslint/promise-function-async
01404| 	processRunExecutionData(workflow: Workflow): PCancelable<IRun> {
01405| 		Logger.debug('Workflow execution started', { workflowId: workflow.id });
01406| 		const { startedAt, hooks } = this.setupExecution();
01407| 		this.checkForWorkflowIssues(workflow);
01408| 		this.handleWaitingState(workflow);
01409| 
01410| 		// Variables which hold temporary data for each node-execution
01411| 		let executionData: IExecuteData;
01412| 		let subNodeExecutionResults: EngineResponse = makeEngineResponse();
01413| 		let executionError: ExecutionBaseError | undefined;
01414| 		let executionNode: INode;
01415| 		let runIndex: number;
01416| 		let currentExecutionTry = '';
01417| 		let lastExecutionTry = '';
01418| 		let closeFunction: Promise<void> | undefined;
01419| 
01420| 		return new PCancelable(async (resolve, _reject, onCancel) => {
01421| 			// Let as many nodes listen to the abort signal, without getting the MaxListenersExceededWarning
01422| 			setMaxListeners(Infinity, this.abortController.signal);
01423| 
01424| 			onCancel.shouldReject = false;
01425| 			onCancel(() => {
01426| 				this.status = 'canceled';
01427| 				this.updateTaskStatusesToCancelled();
01428| 				this.abortController.abort();
01429| 				const fullRunData = this.getFullRunData(startedAt);
01430| 				void hooks.runHook('workflowExecuteAfter', [fullRunData]);
01431| 			});
01432| 
01433| 			// eslint-disable-next-line complexity
01434| 			const returnPromise = (async () => {
01435| 				try {
01436| 					// Establish the execution context
01437| 					await establishExecutionContext(
01438| 						workflow,
01439| 						this.runExecutionData,
01440| 						this.additionalData,
01441| 						this.mode,
01442| 					);
01443| 
01444| 					if (!this.additionalData.restartExecutionId) {
01445| 						await hooks.runHook('workflowExecuteBefore', [workflow, this.runExecutionData]);
01446| 					}
01447| 				} catch (error) {
01448| 					const e = error as unknown as ExecutionBaseError;
01449| 
01450| 					// Set the error that it can be saved correctly
01451| 					executionError = {
01452| 						...e,
01453| 						message: e.message,
01454| 						stack: e.stack,
01455| 					};
01456| 
01457| 					// Set the incoming data of the node that it can be saved correctly
01458| 
01459| 					executionData = this.runExecutionData.executionData!.nodeExecutionStack[0];
01460| 					const taskData: ITaskData = {
01461| 						startTime: Date.now(),
01462| 						executionIndex: 0,
01463| 						executionTime: 0,
01464| 						data: {
01465| 							main: executionData.data.main,
01466| 						},
01467| 						source: [],
01468| 						executionStatus: 'error',
01469| 						hints: [],
01470| 					};
01471| 					this.runExecutionData.resultData = {
01472| 						runData: {
01473| 							[executionData.node.name]: [taskData],
01474| 						},
01475| 						lastNodeExecuted: executionData.node.name,
01476| 						error: executionError,
01477| 					};
01478| 
01479| 					throw error;
01480| 				}
01481| 
01482| 				executionLoop: while (
01483| 					this.runExecutionData.executionData!.nodeExecutionStack.length !== 0
01484| 				) {
01485| 					if (
01486| 						this.additionalData.executionTimeoutTimestamp !== undefined &&
01487| 						Date.now() >= this.additionalData.executionTimeoutTimestamp
01488| 					) {
01489| 						this.status = 'canceled';
01490| 						this.timedOut = true;
01491| 					}
01492| 
01493| 					if (this.status === 'canceled') {
01494| 						return;
01495| 					}
01496| 
01497| 					subNodeExecutionResults = makeEngineResponse();
01498| 
01499| 					let nodeSuccessData: INodeExecutionData[][] | null | undefined = null;
01500| 					executionError = undefined;

(File has more lines. Use 'offset' parameter to read beyond line 1500)
</file>
```
```

---

## Assistant (Explore · big-pickle · 4.7s)

_Thinking:_





```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts",
  "limit": 100,
  "offset": 1500
}
```
**Output:**
```
<file>
01501| 					executionData =
01502| 						this.runExecutionData.executionData!.nodeExecutionStack.shift() as IExecuteData;
01503| 					executionNode = executionData.node;
01504| 
01505| 					const taskStartedData: ITaskStartedData = {
01506| 						startTime: Date.now(),
01507| 						executionIndex: this.additionalData.currentNodeExecutionIndex++,
01508| 						source: !executionData.source ? [] : executionData.source.main,
01509| 						hints: [],
01510| 					};
01511| 
01512| 					// Update the pairedItem information on items
01513| 					const newTaskDataConnections: ITaskDataConnections = {};
01514| 					for (const connectionType of Object.keys(executionData.data)) {
01515| 						newTaskDataConnections[connectionType] = executionData.data[connectionType].map(
01516| 							(input, inputIndex) => {
01517| 								if (input === null) {
01518| 									return input;
01519| 								}
01520| 
01521| 								return input.map((item, itemIndex) => {
01522| 									// Preserve any existing sourceOverwrite from the pairedItem
01523| 									// for tool executions. Tool calls don't have a main
01524| 									// connection to the agent's input, so the data proxy needs
01525| 									// the sourceOverwrite information to know where to look up
01526| 									// paired items. This is necessary because the workflow data
01527| 									// proxy works on input data which normally scrubs paired
01528| 									// item information before executing the node.
01529| 									const isToolExecution = !!executionData.metadata?.preserveSourceOverwrite;
01530| 									if (
01531| 										isToolExecution &&
01532| 										typeof item.pairedItem === 'object' &&
01533| 										'sourceOverwrite' in item.pairedItem
01534| 									) {
01535| 										return {
01536| 											...item,
01537| 											pairedItem: {
01538| 												item: itemIndex,
01539| 												input: inputIndex || undefined,
01540| 												sourceOverwrite: item.pairedItem.sourceOverwrite,
01541| 											},
01542| 										};
01543| 									}
01544| 
01545| 									return {
01546| 										...item,
01547| 										pairedItem: {
01548| 											item: itemIndex,
01549| 											input: inputIndex || undefined,
01550| 										},
01551| 									};
01552| 								});
01553| 							},
01554| 						);
01555| 					}
01556| 					executionData.data = newTaskDataConnections;
01557| 
01558| 					// Get the index of the current run
01559| 					runIndex = 0;
01560| 					if (executionData.runIndex !== undefined) {
01561| 						runIndex = executionData.runIndex;
01562| 					} else if (Object.hasOwn(this.runExecutionData.resultData.runData, executionNode.name)) {
01563| 						runIndex = this.runExecutionData.resultData.runData[executionNode.name].length;
01564| 					}
01565| 
01566| 					currentExecutionTry = `${executionNode.name}:${runIndex}`;
01567| 					if (currentExecutionTry === lastExecutionTry) {
01568| 						throw new ApplicationError(
01569| 							'Stopped execution because it seems to be in an endless loop',
01570| 						);
01571| 					}
01572| 
01573| 					if (
01574| 						this.runExecutionData.startData!.runNodeFilter !== undefined &&
01575| 						this.runExecutionData.startData!.runNodeFilter.indexOf(executionNode.name) === -1
01576| 					) {
01577| 						// If filter is set and node is not on filter skip it, that avoids the problem that it executes
01578| 						// leaves that are parallel to a selected destinationNode. Normally it would execute them because
01579| 						// they have the same parent and it executes all child nodes.
01580| 						continue;
01581| 					}
01582| 
01583| 					const hasInputData = this.ensureInputData(workflow, executionNode, executionData);
01584| 					if (!hasInputData) {
01585| 						lastExecutionTry = currentExecutionTry;
01586| 						continue executionLoop;
01587| 					}
01588| 
01589| 					Logger.debug(`Start executing node "${executionNode.name}"`, {
01590| 						node: executionNode.name,
01591| 						workflowId: workflow.id,
01592| 					});
01593| 					// Skip nodeExecuteBefore for resumed agent nodes to prevent duplicate event emission.
01594| 					// Context: AI agents pause execution to run tools, then resume with tool results.
01595| 					// Without this check, the agent would emit nodeExecuteBefore twice (initial + resume)
01596| 					// but only one nodeExecuteAfter, causing frontend spinner state to become stuck.
01597| 					// See: AI-1414
01598| 					// Future: May introduce dedicated nodeExecutionPaused/nodeExecutionResumed events
01599| 					// if we need finer-grained visibility into the pause/resume cycle.
01600| 					if (!executionData.metadata?.nodeWasResumed) {

(File has more lines. Use 'offset' parameter to read beyond line 1600)
</file>
```
```

---

## Assistant (Explore · big-pickle · 3.5s)

_Thinking:_





```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts",
  "limit": 100,
  "offset": 1600
}
```
**Output:**
```
<file>
01601| 						await hooks.runHook('nodeExecuteBefore', [executionNode.name, taskStartedData]);
01602| 					}
01603| 					let maxTries = 1;
01604| 					if (executionData.node.retryOnFail === true) {
01605| 						// TODO: Remove the hardcoded default-values here and also in NodeSettings.vue
01606| 						maxTries = Math.min(5, Math.max(2, executionData.node.maxTries || 3));
01607| 					}
01608| 
01609| 					let waitBetweenTries = 0;
01610| 					if (executionData.node.retryOnFail === true) {
01611| 						// TODO: Remove the hardcoded default-values here and also in NodeSettings.vue
01612| 						waitBetweenTries = Math.min(
01613| 							5000,
01614| 							Math.max(0, executionData.node.waitBetweenTries || 1000),
01615| 						);
01616| 					}
01617| 
01618| 					for (let tryIndex = 0; tryIndex < maxTries; tryIndex++) {
01619| 						try {
01620| 							if (tryIndex !== 0) {
01621| 								// Reset executionError from previous error try
01622| 								executionError = undefined;
01623| 								if (waitBetweenTries !== 0) {
01624| 									// TODO: Improve that in the future and check if other nodes can
01625| 									//       be executed in the meantime
01626| 
01627| 									await new Promise((resolve) => {
01628| 										setTimeout(() => {
01629| 											resolve(undefined);
01630| 										}, waitBetweenTries);
01631| 									});
01632| 								}
01633| 							}
01634| 
01635| 							const { pinData } = this.runExecutionData.resultData;
01636| 
01637| 							if (pinData && !executionNode.disabled && pinData[executionNode.name] !== undefined) {
01638| 								const nodePinData = pinData[executionNode.name];
01639| 
01640| 								nodeSuccessData = [nodePinData]; // always zeroth runIndex
01641| 							} else {
01642| 								if (executionData.metadata?.subNodeExecutionData) {
01643| 									subNodeExecutionResults.metadata =
01644| 										executionData.metadata.subNodeExecutionData.metadata;
01645| 									for (const subNode of executionData.metadata.subNodeExecutionData.actions) {
01646| 										const nodeRunData = this.runExecutionData.resultData.runData[subNode.nodeName];
01647| 										if (nodeRunData && nodeRunData[subNode.runIndex]) {
01648| 											const data = nodeRunData[subNode.runIndex];
01649| 											subNodeExecutionResults.actionResponses.push({
01650| 												data,
01651| 												action: subNode.action,
01652| 											});
01653| 										}
01654| 									}
01655| 								}
01656| 
01657| 								Logger.debug(`Running node "${executionNode.name}" started`, {
01658| 									node: executionNode.name,
01659| 									workflowId: workflow.id,
01660| 								});
01661| 
01662| 								let runNodeData = await this.runNode(
01663| 									workflow,
01664| 									executionData,
01665| 									this.runExecutionData,
01666| 									runIndex,
01667| 									this.additionalData,
01668| 									this.mode,
01669| 									this.abortController.signal,
01670| 									subNodeExecutionResults,
01671| 								);
01672| 
01673| 								let nodeFailed =
01674| 									!isEngineRequest(runNodeData) &&
01675| 									runNodeData.data?.[0]?.[0]?.json?.error !== undefined;
01676| 
01677| 								while (nodeFailed && tryIndex !== maxTries - 1) {
01678| 									await sleep(waitBetweenTries);
01679| 
01680| 									runNodeData = await this.runNode(
01681| 										workflow,
01682| 										executionData,
01683| 										this.runExecutionData,
01684| 										runIndex,
01685| 										this.additionalData,
01686| 										this.mode,
01687| 										this.abortController.signal,
01688| 									);
01689| 
01690| 									nodeFailed =
01691| 										!isEngineRequest(runNodeData) &&
01692| 										runNodeData.data?.[0]?.[0]?.json?.error !== undefined;
01693| 									tryIndex++;
01694| 								}
01695| 
01696| 								// if runNodeData is Request
01697| 								if (isEngineRequest(runNodeData)) {
01698| 									this.handleEngineRequest({
01699| 										workflow,
01700| 										currentNode: executionNode,

(File has more lines. Use 'offset' parameter to read beyond line 1700)
</file>
```
```

---

## Assistant (Explore · big-pickle · 4.9s)

_Thinking:_




Now let me look at the runNode method where individual nodes are executed:

```
Tool: grep

**Input:**
```json
{
  "path": "/home/ab/git-projs/n8n/packages/core/src/execution-engine",
  "pattern": "runNode.*\\("
}
```
**Output:**
```
Found 54 matches
/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts:
  Line 128: 			runNodeFilter = workflow.getParentNodes(destinationNode.nodeName);
  Line 130: 				runNodeFilter.push(destinationNode.nodeName);
  Line 265: 				runNodeFilter: Array.from(filteredNodes.values()).map((node) => node.name),
  Line 1182: 		const data = await routingNode.runNode();
  Line 1190: 	async runNode(
  Line 1575: 						this.runExecutionData.startData!.runNodeFilter.indexOf(executionNode.name) === -1
  Line 1662: 								let runNodeData = await this.runNode(
  Line 1680: 									runNodeData = await this.runNode(
  Line 1723: 									closeFunction = runNodeData.closeFunction();

/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/workflow-execute.test.ts:
  Line 629: 		test('removes disabled nodes from the runNodeFilter, but not the graph', async () => {
  Line 666: 			const runNodeFilter: string[] = (workflowExecute as any).runExecutionData.startData
  Line 668: 			expect(runNodeFilter).toContain(trigger.name);
  Line 669: 			expect(runNodeFilter).toContain(node2.name);
  Line 670: 			expect(runNodeFilter).not.toContain(node1.name);
  Line 1195: 	describe('runNode', () => {
  Line 1233: 			const runPromise = workflowExecute.runNode(
  Line 2273: 				const runPromise = workflowExecute.runNode(

/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/routing-node.test.ts:
  Line 778: 	describe('runNode', () => {
  Line 2173: 				const result = await routingNode.runNode();

/home/ab/git-projs/n8n/packages/core/src/execution-engine/__tests__/workflow-execute-run-node.test.ts:
  Line 50: 		runNode: jest.fn().mockResolvedValue([[{ json: { routed: 'result' } }]]),
  Line 84: describe('WorkflowExecute.runNode - Real Implementation', () => {
  Line 171: 			const result = await workflowExecute.runNode(
  Line 191: 			const result = await workflowExecute.runNode(
  Line 212: 			const result = await workflowExecute.runNode(
  Line 238: 				workflowExecute.runNode(
  Line 261: 				workflowExecute.runNode(
  Line 284: 				workflowExecute.runNode(
  Line 311: 				workflowExecute.runNode(
  Line 323: 				await workflowExecute.runNode(
  Line 374: 			const result = await workflowExecute.runNode(
  Line 397: 			const result = await workflowExecute.runNode(
  Line 433: 			const result = await workflowExecute.runNode(
  Line 457: 			const result = await workflowExecute.runNode(
  Line 511: 			const result = await workflowExecute.runNode(
  Line 571: 				workflowExecute.runNode(
  Line 617: 				workflowExecute.runNode(
  Line 641: 			const result = await workflowExecute.runNode(
  Line 665: 			const result = await workflowExecute.runNode(
  Line 707: 			const result = await workflowExecute.runNode(
  Line 742: 			const result = await workflowExecute.runNode(
  Line 783: 			const result = await workflowExecute.runNode(
  Line 827: 			const result = await workflowExecute.runNode(
  Line 847: 			const result = await workflowExecute.runNode(
  Line 868: 			const result = await workflowExecute.runNode(
  Line 889: 				runNode: jest.fn().mockResolvedValue(mockData),
  Line 896: 			const result = await workflowExecute.runNode(
  Line 906: 			expect(mockRoutingNodeInstance.runNode).toHaveBeenCalled();
  Line 921: 				runNode: jest.fn().mockResolvedValue(mockData),
  Line 928: 			const result = await workflowExecute.runNode(
  Line 938: 			expect(mockRoutingNodeInstance.runNode).toHaveBeenCalled();
  Line 985: 			await workflowExecute.runNode(
  Line 1029: 			const result = await workflowExecute.runNode(
  Line 1056: 			const result = await workflowExecute.runNode(

/home/ab/git-projs/n8n/packages/core/src/execution-engine/routing-node.ts:
  Line 52: 	async runNode(): Promise<INodeExecutionData[][] | undefined> {
```
```

---

## Assistant (Explore · big-pickle · 9.9s)

_Thinking:_





```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts",
  "limit": 100,
  "offset": 1190
}
```
**Output:**
```
<file>
01191| 		workflow: Workflow,
01192| 		executionData: IExecuteData,
01193| 		runExecutionData: IRunExecutionData,
01194| 		runIndex: number,
01195| 		additionalData: IWorkflowExecuteAdditionalData,
01196| 		mode: WorkflowExecuteMode,
01197| 		abortSignal?: AbortSignal,
01198| 		subNodeExecutionResults?: EngineResponse,
01199| 	): Promise<IRunNodeResponse | EngineRequest> {
01200| 		const { node } = executionData;
01201| 		let inputData = executionData.data;
01202| 
01203| 		if (node.disabled === true) {
01204| 			return this.handleDisabledNode(inputData);
01205| 		}
01206| 
01207| 		const nodeType = workflow.nodeTypes.getByNameAndVersion(node.type, node.typeVersion);
01208| 		const customOperation = this.getCustomOperation(node, nodeType);
01209| 
01210| 		const connectionInputData = this.prepareConnectionInputData(
01211| 			workflow,
01212| 			nodeType,
01213| 			customOperation,
01214| 			inputData,
01215| 		);
01216| 
01217| 		if (connectionInputData === null) {
01218| 			return { data: undefined };
01219| 		}
01220| 
01221| 		this.rethrowLastNodeError(runExecutionData, node);
01222| 
01223| 		inputData = this.handleExecuteOnce(node, inputData);
01224| 
01225| 		if (nodeType.execute || customOperation) {
01226| 			return await this.executeNode(
01227| 				workflow,
01228| 				node,
01229| 				nodeType,
01230| 				customOperation,
01231| 				additionalData,
01232| 				mode,
01233| 				runExecutionData,
01234| 				runIndex,
01235| 				connectionInputData,
01236| 				inputData,
01237| 				executionData,
01238| 				abortSignal,
01239| 				subNodeExecutionResults,
01240| 			);
01241| 		}
01242| 
01243| 		if (nodeType.poll) {
01244| 			return await this.executePollNode(workflow, node, nodeType, additionalData, mode, inputData);
01245| 		}
01246| 
01247| 		if (nodeType.trigger) {
01248| 			return await this.executeTriggerNode(
01249| 				workflow,
01250| 				node,
01251| 				additionalData,
01252| 				mode,
01253| 				inputData,
01254| 				abortSignal,
01255| 			);
01256| 		}
01257| 
01258| 		const isDeclarativeNode = nodeType.description.requestDefaults !== undefined;
01259| 		if (nodeType.webhook && !isDeclarativeNode) {
01260| 			// Check if the node have requestDefaults(Declarative Node),
01261| 			// else for webhook nodes always simply pass the data through
01262| 			// as webhook method would be called by WebhookService
01263| 			return { data: inputData.main as INodeExecutionData[][] };
01264| 		}
01265| 
01266| 		return await this.executeDeclarativeNodeInTest(
01267| 			workflow,
01268| 			node,
01269| 			nodeType,
01270| 			additionalData,
01271| 			mode,
01272| 			runExecutionData,
01273| 			runIndex,
01274| 			connectionInputData,
01275| 			inputData,
01276| 			executionData,
01277| 		);
01278| 	}
01279| 
01280| 	/**
01281| 	 * Handles executions that have been waiting by
01282| 	 * 1. unsetting the `waitTill`
01283| 	 * 2. disabling the currently executing node (which should be the node that
01284| 	 *    put the execution into waiting) making sure it won't be executed again
01285| 	 * 3. Removing the last run for the last executed node (which also should be
01286| 	 *    the node that put the execution into waiting) to make sure the node
01287| 	 *    does not show up as having run twice
01288| 	 */
01289| 	private handleWaitingState(workflow: Workflow) {
01290| 		if (this.runExecutionData.waitTill) {

(File has more lines. Use 'offset' parameter to read beyond line 1290)
</file>
```
```

---

## Assistant (Explore · big-pickle · 10.2s)

_Thinking:_




Now let me find the executeNode method:

```
Tool: grep

**Input:**
```json
{
  "path": "/home/ab/git-projs/n8n/packages/core/src/execution-engine",
  "pattern": "executeNode.*\\("
}
```
**Output:**
```
Found 2 matches
/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts:
  Line 1006: 	private async executeNode(
  Line 1226: 			return await this.executeNode(
```
```

---

## Assistant (Explore · big-pickle · 6.1s)

_Thinking:_





```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts",
  "limit": 100,
  "offset": 1006
}
```
**Output:**
```
<file>
01007| 		workflow: Workflow,
01008| 		node: INode,
01009| 		nodeType: INodeType,
01010| 		customOperation: ReturnType<WorkflowExecute['getCustomOperation']>,
01011| 		additionalData: IWorkflowExecuteAdditionalData,
01012| 		mode: WorkflowExecuteMode,
01013| 		runExecutionData: IRunExecutionData,
01014| 		runIndex: number,
01015| 		connectionInputData: INodeExecutionData[],
01016| 		inputData: ITaskDataConnections,
01017| 		executionData: IExecuteData,
01018| 		abortSignal?: AbortSignal,
01019| 		subNodeExecutionResults?: EngineResponse,
01020| 	): Promise<IRunNodeResponse | EngineRequest> {
01021| 		const closeFunctions: CloseFunction[] = [];
01022| 		const context = new ExecuteContext(
01023| 			workflow,
01024| 			node,
01025| 			additionalData,
01026| 			mode,
01027| 			runExecutionData,
01028| 			runIndex,
01029| 			connectionInputData,
01030| 			inputData,
01031| 			executionData,
01032| 			closeFunctions,
01033| 			abortSignal,
01034| 			subNodeExecutionResults,
01035| 		);
01036| 
01037| 		let data: INodeExecutionData[][] | EngineRequest | null;
01038| 
01039| 		if (customOperation) {
01040| 			data = await customOperation.call(context);
01041| 		} else if (nodeType.execute) {
01042| 			data =
01043| 				nodeType instanceof Node
01044| 					? await nodeType.execute(context, subNodeExecutionResults)
01045| 					: await nodeType.execute.call(context, subNodeExecutionResults);
01046| 		} else {
01047| 			throw new UnexpectedError(
01048| 				"Can't execute node. There is no custom operation and the node has not execute function.",
01049| 			);
01050| 		}
01051| 
01052| 		if (isEngineRequest(data)) {
01053| 			return data;
01054| 		}
01055| 
01056| 		this.reportJsonIncompatibleOutput(data, workflow, node);
01057| 
01058| 		const closeFunctionsResults = await Promise.allSettled(
01059| 			closeFunctions.map(async (fn) => await fn()),
01060| 		);
01061| 
01062| 		const closingErrors = closeFunctionsResults
01063| 			.filter((result): result is PromiseRejectedResult => result.status === 'rejected')
01064| 			// eslint-disable-next-line @typescript-eslint/no-unsafe-return
01065| 			.map((result) => result.reason);
01066| 
01067| 		if (closingErrors.length > 0) {
01068| 			if (closingErrors[0] instanceof Error) throw closingErrors[0];
01069| 			throw new ApplicationError("Error on execution node's close function(s)", {
01070| 				extra: { nodeName: node.name },
01071| 				tags: { nodeType: node.type },
01072| 				cause: closingErrors,
01073| 			});
01074| 		}
01075| 
01076| 		return { data, hints: context.hints };
01077| 	}
01078| 
01079| 	/**
01080| 	 * Executes a poll node
01081| 	 */
01082| 	private async executePollNode(
01083| 		workflow: Workflow,
01084| 		node: INode,
01085| 		nodeType: INodeType,
01086| 		additionalData: IWorkflowExecuteAdditionalData,
01087| 		mode: WorkflowExecuteMode,
01088| 		inputData: ITaskDataConnections,
01089| 	): Promise<IRunNodeResponse> {
01090| 		if (mode === 'manual') {
01091| 			// In manual mode run the poll function
01092| 			const context = new PollContext(workflow, node, additionalData, mode, 'manual');
01093| 			return { data: await nodeType.poll!.call(context) };
01094| 		}
01095| 		// In any other mode pass data through as it already contains the result of the poll
01096| 		return { data: inputData.main as INodeExecutionData[][] };
01097| 	}
01098| 
01099| 	/**
01100| 	 * Executes a trigger node
01101| 	 */
01102| 	private async executeTriggerNode(
01103| 		workflow: Workflow,
01104| 		node: INode,
01105| 		additionalData: IWorkflowExecuteAdditionalData,
01106| 		mode: WorkflowExecuteMode,

(File has more lines. Use 'offset' parameter to read beyond line 1106)
</file>
```
```

---

## Assistant (Explore · big-pickle · 4.5s)

_Thinking:_




Now let me also look at the node execution functions:

```
Tool: glob

**Input:**
```json
{
  "pattern": "packages/core/src/node-execute-functions.ts"
}
```
**Output:**
```
/home/ab/git-projs/n8n/packages/core/src/node-execute-functions.ts
```
```

---

## Assistant (Explore · big-pickle · 3.6s)

_Thinking:_





```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/core/src/node-execute-functions.ts",
  "limit": 100
}
```
**Output:**
```
<file>
00001| import type {
00002| 	INode,
00003| 	IPollFunctions,
00004| 	ITriggerFunctions,
00005| 	IWorkflowExecuteAdditionalData,
00006| 	Workflow,
00007| 	WorkflowActivateMode,
00008| 	WorkflowExecuteMode,
00009| } from 'n8n-workflow';
00010| 
00011| import { PollContext, TriggerContext } from './execution-engine/node-execution-context';
00012| 
00013| /**
00014|  * Returns the execute functions the poll nodes have access to.
00015|  */
00016| // TODO: Check if I can get rid of: additionalData, and so then maybe also at ActiveWorkflowManager.add
00017| export function getExecutePollFunctions(
00018| 	workflow: Workflow,
00019| 	node: INode,
00020| 	additionalData: IWorkflowExecuteAdditionalData,
00021| 	mode: WorkflowExecuteMode,
00022| 	activation: WorkflowActivateMode,
00023| ): IPollFunctions {
00024| 	return new PollContext(workflow, node, additionalData, mode, activation);
00025| }
00026| 
00027| /**
00028|  * Returns the execute functions the trigger nodes have access to.
00029|  */
00030| // TODO: Check if I can get rid of: additionalData, and so then maybe also at ActiveWorkflowManager.add
00031| export function getExecuteTriggerFunctions(
00032| 	workflow: Workflow,
00033| 	node: INode,
00034| 	additionalData: IWorkflowExecuteAdditionalData,
00035| 	mode: WorkflowExecuteMode,
00036| 	activation: WorkflowActivateMode,
00037| ): ITriggerFunctions {
00038| 	return new TriggerContext(workflow, node, additionalData, mode, activation);
00039| }
00040| 

(End of file - total 40 lines)
</file>
```
```

---

## Assistant (Explore · big-pickle · 4.2s)

_Thinking:_




Now let me check for webhooks and the request handling workflow:

```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhooks.controller.ts",
  "limit": 100
}
```
**Output:**
```
<file>
00001| import { Post, RestController } from '@n8n/decorators';
00002| import { Request } from 'express';
00003| import get from 'lodash/get';
00004| 
00005| import { WebhookService } from './webhook.service';
00006| import type { Method } from './webhook.types';
00007| 
00008| @RestController('/webhooks')
00009| export class WebhooksController {
00010| 	constructor(private readonly webhookService: WebhookService) {}
00011| 
00012| 	@Post('/find')
00013| 	async findWebhook(req: Request) {
00014| 		const body = get(req, 'body', {}) as { path: string; method: Method };
00015| 
00016| 		try {
00017| 			const webhook = await this.webhookService.findWebhook(body.method, body.path);
00018| 			return webhook;
00019| 		} catch (error) {
00020| 			return null;
00021| 		}
00022| 	}
00023| }
00024| 

(End of file - total 24 lines)
</file>
```
```

---

## Assistant (Explore · big-pickle · 3.4s)

_Thinking:_





```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook.service.ts",
  "limit": 150
}
```
**Output:**
```
<file>
00001| import { Logger } from '@n8n/backend-common';
00002| import type { WebhookEntity } from '@n8n/db';
00003| import { WebhookRepository } from '@n8n/db';
00004| import { Service } from '@n8n/di';
00005| import { HookContext, WebhookContext } from 'n8n-core';
00006| import { ensureError, Node, NodeHelpers, UnexpectedError } from 'n8n-workflow';
00007| import type {
00008| 	IHttpRequestMethods,
00009| 	INode,
00010| 	IRunExecutionData,
00011| 	IWebhookData,
00012| 	IWebhookResponseData,
00013| 	IWorkflowExecuteAdditionalData,
00014| 	WebhookSetupMethodNames,
00015| 	Workflow,
00016| 	WorkflowActivateMode,
00017| 	WorkflowExecuteMode,
00018| } from 'n8n-workflow';
00019| 
00020| import { NodeTypes } from '@/node-types';
00021| import { CacheService } from '@/services/cache/cache.service';
00022| 
00023| import type { Method } from './webhook.types';
00024| 
00025| @Service()
00026| export class WebhookService {
00027| 	constructor(
00028| 		private readonly logger: Logger,
00029| 		private readonly webhookRepository: WebhookRepository,
00030| 		private readonly cacheService: CacheService,
00031| 		private readonly nodeTypes: NodeTypes,
00032| 	) {}
00033| 
00034| 	async populateCache() {
00035| 		const staticWebhooks = await this.webhookRepository.getStaticWebhooks();
00036| 
00037| 		if (staticWebhooks.length === 0) return;
00038| 
00039| 		void this.cacheService.setMany(staticWebhooks.map((w) => [w.cacheKey, w]));
00040| 	}
00041| 
00042| 	async findAll() {
00043| 		return await this.webhookRepository.find();
00044| 	}
00045| 
00046| 	private async findCached(method: Method, path: string) {
00047| 		const cacheKey = `webhook:${method}-${path}`;
00048| 
00049| 		let cachedStaticWebhook;
00050| 		try {
00051| 			cachedStaticWebhook = await this.cacheService.get(cacheKey);
00052| 		} catch (error) {
00053| 			this.logger.warn('Failed to query webhook cache', {
00054| 				error: ensureError(error).message,
00055| 			});
00056| 			cachedStaticWebhook = undefined;
00057| 		}
00058| 
00059| 		if (cachedStaticWebhook) return this.webhookRepository.create(cachedStaticWebhook);
00060| 
00061| 		const dbStaticWebhook = await this.findStaticWebhook(method, path);
00062| 
00063| 		if (dbStaticWebhook) {
00064| 			try {
00065| 				await this.cacheService.set(cacheKey, dbStaticWebhook);
00066| 			} catch (error) {
00067| 				this.logger.warn('Failed to cache webhook', {
00068| 					error: ensureError(error).message,
00069| 				});
00070| 			}
00071| 			return dbStaticWebhook;
00072| 		}
00073| 
00074| 		return await this.findDynamicWebhook(path, method);
00075| 	}
00076| 
00077| 	/**
00078| 	 * Find a matching webhook with zero dynamic path segments, e.g. `<uuid>` or `user/profile`.
00079| 	 */
00080| 	private async findStaticWebhook(method: Method, path: string) {
00081| 		return await this.webhookRepository.findOneBy({ webhookPath: path, method });
00082| 	}
00083| 
00084| 	/**
00085| 	 * Find a matching webhook with one or more dynamic path segments, e.g. `<uuid>/user/:id/posts`.
00086| 	 * It is mandatory for dynamic webhooks to have `<uuid>/` at the base.
00087| 	 */
00088| 	private async findDynamicWebhook(path: string, method?: Method) {
00089| 		const [uuidSegment, ...otherSegments] = path.split('/');
00090| 
00091| 		const dynamicWebhooks = await this.webhookRepository.findBy({
00092| 			webhookId: uuidSegment,
00093| 			method,
00094| 			pathLength: otherSegments.length,
00095| 		});
00096| 
00097| 		if (dynamicWebhooks.length === 0) return null;
00098| 
00099| 		const requestSegments = new Set(otherSegments);
00100| 
00101| 		const { webhook } = dynamicWebhooks.reduce<{
00102| 			webhook: WebhookEntity | null;
00103| 			maxMatches: number;
00104| 		}>(
00105| 			(acc, dw) => {
00106| 				const allStaticSegmentsMatch = dw.staticSegments.every((s) => requestSegments.has(s));
00107| 
00108| 				if (allStaticSegmentsMatch && dw.staticSegments.length > acc.maxMatches) {
00109| 					acc.maxMatches = dw.staticSegments.length;
00110| 					acc.webhook = dw;
00111| 					return acc;
00112| 				} else if (dw.staticSegments.length === 0 && !acc.webhook) {
00113| 					acc.webhook = dw; // edge case: if path is `:var`, match on anything
00114| 				}
00115| 
00116| 				return acc;
00117| 			},
00118| 			{ webhook: null, maxMatches: 0 },
00119| 		);
00120| 
00121| 		return webhook;
00122| 	}
00123| 
00124| 	async findWebhook(method: Method, path: string) {
00125| 		return await this.findCached(method, path);
00126| 	}
00127| 
00128| 	async storeWebhook(webhook: WebhookEntity) {
00129| 		try {
00130| 			await this.cacheService.set(webhook.cacheKey, webhook);
00131| 		} catch (error) {
00132| 			this.logger.warn('Failed to cache webhook', {
00133| 				error: ensureError(error).message,
00134| 			});
00135| 		}
00136| 
00137| 		await this.webhookRepository.upsert(webhook, ['method', 'webhookPath']);
00138| 	}
00139| 
00140| 	createWebhook(data: Partial<WebhookEntity>) {
00141| 		return this.webhookRepository.create(data);
00142| 	}
00143| 
00144| 	async deleteWorkflowWebhooks(workflowId: string) {
00145| 		const webhooks = await this.webhookRepository.findBy({ workflowId });
00146| 
00147| 		return await this.deleteWebhooks(webhooks);
00148| 	}
00149| 
00150| 	private async deleteWebhooks(webhooks: WebhookEntity[]) {

(File has more lines. Use 'offset' parameter to read beyond line 150)
</file>
```
```

---

## Assistant (Explore · big-pickle · 3.2s)

_Thinking:_




Now let me look at the webhook execution logic:

```
Tool: glob

**Input:**
```json
{
  "pattern": "packages/cli/**/webhook*"
}
```
**Output:**
```
/home/ab/git-projs/n8n/packages/cli/test/integration/webhooks.api.test.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/__tests__/webhook-helpers.test.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook.service.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook-request-handler.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook-helpers.ts
/home/ab/git-projs/n8n/packages/cli/src/modules/mcp/__tests__/webhook-utils.test.ts
/home/ab/git-projs/n8n/packages/cli/src/modules/mcp/tools/webhook-utils.ts
/home/ab/git-projs/n8n/packages/cli/src/commands/__tests__/webhook.test.ts
/home/ab/git-projs/n8n/packages/cli/src/commands/webhook.ts
/home/ab/git-projs/n8n/packages/cli/test/integration/webhooks.test.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook-on-received-response-extractor.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook-response.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook-server.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook.types.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhooks.controller.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook-request-sanitizer.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook-last-node-response-extractor.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook-execution-context.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/__tests__/webhook.service.test.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/__tests__/webhook-request-handler.test.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/__tests__/webhook-on-received-response-extractor.test.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/__tests__/webhook-form-data.test.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/__tests__/webhook-last-node-response-extractor.test.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/__tests__/webhook-request-sanitizer.test.ts
/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook-form-data.ts
/home/ab/git-projs/n8n/packages/cli/src/errors/response-errors/webhook-not-found.error.ts
/home/ab/git-projs/n8n/packages/cli/src/errors/response-errors/__tests__/webhook-not-found.error.test.ts
```
```

---

## Assistant (Explore · big-pickle · 2.7s)

_Thinking:_





```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook-request-handler.ts",
  "limit": 100
}
```
**Output:**
```
<file>
00001| import { Logger } from '@n8n/backend-common';
00002| import { Container } from '@n8n/di';
00003| import type express from 'express';
00004| import {
00005| 	isWebhookHtmlSandboxingDisabled,
00006| 	getWebhookSandboxCSP,
00007| 	isHtmlRenderedContentType,
00008| } from 'n8n-core';
00009| import { ensureError, type IHttpRequestMethods } from 'n8n-workflow';
00010| import { Readable } from 'stream';
00011| import { finished } from 'stream/promises';
00012| 
00013| import { WebhookNotFoundError } from '@/errors/response-errors/webhook-not-found.error';
00014| import * as ResponseHelper from '@/response-helper';
00015| import type {
00016| 	WebhookStaticResponse,
00017| 	WebhookResponse,
00018| 	WebhookResponseStream,
00019| } from '@/webhooks/webhook-response';
00020| import {
00021| 	isWebhookNoResponse,
00022| 	isWebhookStaticResponse,
00023| 	isWebhookResponse,
00024| 	isWebhookStreamResponse,
00025| } from '@/webhooks/webhook-response';
00026| import type {
00027| 	IWebhookManager,
00028| 	WebhookOptionsRequest,
00029| 	WebhookRequest,
00030| 	WebhookResponseHeaders,
00031| } from '@/webhooks/webhook.types';
00032| 
00033| const WEBHOOK_METHODS: IHttpRequestMethods[] = ['DELETE', 'GET', 'HEAD', 'PATCH', 'POST', 'PUT'];
00034| 
00035| class WebhookRequestHandler {
00036| 	constructor(private readonly webhookManager: IWebhookManager) {}
00037| 
00038| 	/**
00039| 	 * Handles an incoming webhook request. Handles CORS and delegates the
00040| 	 * request to the webhook manager to execute the webhook.
00041| 	 */
00042| 	async handleRequest(req: WebhookRequest | WebhookOptionsRequest, res: express.Response) {
00043| 		const method = req.method;
00044| 
00045| 		if (method !== 'OPTIONS' && !WEBHOOK_METHODS.includes(method)) {
00046| 			return ResponseHelper.sendErrorResponse(
00047| 				res,
00048| 				new Error(`The method ${method} is not supported.`),
00049| 			);
00050| 		}
00051| 
00052| 		// Setup CORS headers only if the incoming request has an `origin` header
00053| 		if ('origin' in req.headers) {
00054| 			const corsSetupError = await this.setupCorsHeaders(req, res);
00055| 			if (corsSetupError) {
00056| 				return ResponseHelper.sendErrorResponse(res, corsSetupError);
00057| 			}
00058| 		}
00059| 
00060| 		if (method === 'OPTIONS') {
00061| 			return ResponseHelper.sendSuccessResponse(res, {}, true, 204);
00062| 		}
00063| 
00064| 		try {
00065| 			const response = await this.webhookManager.executeWebhook(req, res);
00066| 
00067| 			// Modern way of responding to webhooks
00068| 			if (isWebhookResponse(response)) {
00069| 				await this.sendWebhookResponse(res, response);
00070| 			} else if (response.noWebhookResponse !== true) {
00071| 				// Legacy way of responding to webhooks. `WebhookResponse` should be used to
00072| 				// pass the response from the webhookManager. However, we still have code
00073| 				// that doesn't use that yet. We need to keep this here until all codepaths
00074| 				// return a `WebhookResponse` instead.
00075| 				this.sendLegacyResponse(res, response.data, true, response.responseCode, response.headers);
00076| 			}
00077| 		} catch (e) {
00078| 			const error = ensureError(e);
00079| 
00080| 			const logger = Container.get(Logger);
00081| 
00082| 			if (e instanceof WebhookNotFoundError) {
00083| 				logger.error(`Received request for unknown webhook: ${e.message}`);
00084| 			} else {
00085| 				logger.error(
00086| 					`Error in handling webhook request ${req.method} ${req.path}: ${error.message}`,
00087| 					{ stacktrace: error.stack },
00088| 				);
00089| 			}
00090| 
00091| 			return ResponseHelper.sendErrorResponse(res, error);
00092| 		}
00093| 	}
00094| 
00095| 	private async sendWebhookResponse(res: express.Response, webhookResponse: WebhookResponse) {
00096| 		if (isWebhookNoResponse(webhookResponse)) {
00097| 			return;
00098| 		}
00099| 
00100| 		if (isWebhookStaticResponse(webhookResponse)) {

(File has more lines. Use 'offset' parameter to read beyond line 100)
</file>
```
```

---

## Assistant (Explore · big-pickle · 3.1s)

_Thinking:_





```
Tool: glob

**Input:**
```json
{
  "pattern": "packages/cli/**/webhook-manager*"
}
```
**Output:**
```
No files found
```
```

---

## Assistant (Explore · big-pickle · 4.6s)

_Thinking:_





```
Tool: grep

**Input:**
```json
{
  "path": "/home/ab/git-projs/n8n/packages/cli/src/webhooks",
  "pattern": "executeWebhook"
}
```
**Output:**
```
Found 41 matches
/home/ab/git-projs/n8n/packages/cli/src/webhooks/waiting-forms.ts:
  Line 73: 	async executeWebhook(

/home/ab/git-projs/n8n/packages/cli/src/webhooks/__tests__/waiting-forms.test.ts:
  Line 225: 			const result = await waitingForms.executeWebhook(req, res);
  Line 247: 			await waitingForms.executeWebhook(req, res);
  Line 270: 			await waitingForms.executeWebhook(req, res);
  Line 290: 			await waitingForms.executeWebhook(req, res);
  Line 340: 			await waitingForms.executeWebhook(req, res);
  Line 437: 	describe('executeWebhook - default completion page', () => {
  Line 483: 			const result = await waitingForms.executeWebhook(req, res);
  Line 539: 			await waitingForms.executeWebhook(req, res);

/home/ab/git-projs/n8n/packages/cli/src/webhooks/waiting-webhooks.ts:
  Line 121: 	async executeWebhook(
  Line 264: 			void WebhookHelpers.executeWebhook(

/home/ab/git-projs/n8n/packages/cli/src/webhooks/__tests__/live-webhooks.test.ts:
  Line 51: 	describe('executeWebhook', () => {
  Line 119: 			(WebhookHelpers.executeWebhook as jest.Mock).mockImplementation(
  Line 132: 			await liveWebhooks.executeWebhook(request, mock<Response>());
  Line 137: 		it('should pass workflowData with activeVersion nodes/connections to executeWebhook', async () => {
  Line 232: 			(WebhookHelpers.executeWebhook as jest.Mock).mockImplementation(
  Line 250: 			await liveWebhooks.executeWebhook(request, mock<Response>());
  Line 252: 			// Verify that workflowData passed to executeWebhook has activeVersion nodes/connections

/home/ab/git-projs/n8n/packages/cli/src/webhooks/__tests__/test-webhooks.test.ts:
  Line 220: 	describe('executeWebhook()', () => {
  Line 225: 			const promise = testWebhooks.executeWebhook(
  Line 244: 			const promise = testWebhooks.executeWebhook(

/home/ab/git-projs/n8n/packages/cli/src/webhooks/__tests__/waiting-webhooks.test.ts:
  Line 46: 		const promise = waitingWebhooks.executeWebhook(
  Line 68: 		const promise = waitingWebhooks.executeWebhook(
  Line 90: 		const promise = waitingWebhooks.executeWebhook(

/home/ab/git-projs/n8n/packages/cli/src/webhooks/live-webhooks.ts:
  Line 71: 	async executeWebhook(
  Line 160: 			void WebhookHelpers.executeWebhook(

/home/ab/git-projs/n8n/packages/cli/src/webhooks/test-webhooks.ts:
  Line 67: 	async executeWebhook(
  Line 134: 				const executionId = await WebhookHelpers.executeWebhook(

/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook-request-handler.ts:
  Line 65: 			const response = await this.webhookManager.executeWebhook(req, res);

/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook-helpers.ts:
  Line 366: export async function executeWebhook(

/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook.types.ts:
  Line 29: 	executeWebhook(req: WebhookRequest, res: Response): Promise<IWebhookResponseCallbackData>;

/home/ab/git-projs/n8n/packages/cli/src/webhooks/__tests__/webhook-request-handler.test.ts:
  Line 153: 			const executeWebhookResponse: IWebhookResponseCallbackData = {
  Line 160: 			webhookManager.executeWebhook.mockResolvedValueOnce(executeWebhookResponse);
  Line 164: 			expect(webhookManager.executeWebhook).toHaveBeenCalledWith(req, res);
  Line 167: 			expect(res.json).toHaveBeenCalledWith(executeWebhookResponse.data);
  Line 180: 			webhookManager.executeWebhook.mockRejectedValueOnce(
  Line 186: 			expect(webhookManager.executeWebhook).toHaveBeenCalledWith(req, res);
  Line 205: 				const executeWebhookResponse: IWebhookResponseCallbackData = {
  Line 208: 				webhookManager.executeWebhook.mockResolvedValueOnce(executeWebhookResponse);
  Line 212: 				expect(webhookManager.executeWebhook).toHaveBeenCalledWith(req, res);
  Line 214: 				expect(res.json).toHaveBeenCalledWith(executeWebhookResponse.data);
```
```

---

## Assistant (Explore · big-pickle · 3.9s)

_Thinking:_





```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook-helpers.ts",
  "limit": 100,
  "offset": 366
}
```
**Output:**
```
<file>
00367| 	workflow: Workflow,
00368| 	webhookData: IWebhookData,
00369| 	workflowData: IWorkflowBase,
00370| 	workflowStartNode: INode,
00371| 	executionMode: WorkflowExecuteMode,
00372| 	pushRef: string | undefined,
00373| 	runExecutionData: IRunExecutionData | undefined,
00374| 	executionId: string | undefined,
00375| 	req: WebhookRequest,
00376| 	res: express.Response,
00377| 	responseCallback: (
00378| 		error: Error | null,
00379| 		data: IWebhookResponseCallbackData | WebhookResponse,
00380| 	) => void,
00381| 	destinationNode?: IDestinationNode,
00382| ): Promise<string | undefined> {
00383| 	// Get the nodeType to know which responseMode is set
00384| 	const nodeType = workflow.nodeTypes.getByNameAndVersion(
00385| 		workflowStartNode.type,
00386| 		workflowStartNode.typeVersion,
00387| 	);
00388| 
00389| 	const additionalKeys: IWorkflowDataProxyAdditionalKeys = {
00390| 		$executionId: executionId,
00391| 	};
00392| 
00393| 	const context = new WebhookExecutionContext(
00394| 		workflow,
00395| 		workflowStartNode,
00396| 		webhookData,
00397| 		executionMode,
00398| 		additionalKeys,
00399| 	);
00400| 
00401| 	let project: Project | undefined = undefined;
00402| 	try {
00403| 		project = await Container.get(OwnershipService).getWorkflowProjectCached(workflowData.id);
00404| 	} catch (error) {
00405| 		throw new NotFoundError('Cannot find workflow');
00406| 	}
00407| 
00408| 	// Prepare everything that is needed to run the workflow
00409| 	const additionalData = await WorkflowExecuteAdditionalData.getBase({
00410| 		projectId: project?.id,
00411| 	});
00412| 
00413| 	if (executionId) {
00414| 		additionalData.executionId = executionId;
00415| 	}
00416| 
00417| 	const { responseMode, responseCode, responseData, checkAllMainOutputs } = evaluateResponseOptions(
00418| 		workflowStartNode,
00419| 		workflow,
00420| 		req,
00421| 		webhookData,
00422| 		executionMode,
00423| 		additionalKeys,
00424| 	);
00425| 
00426| 	if (
00427| 		!['onReceived', 'lastNode', 'responseNode', 'formPage', 'streaming', 'hostedChat'].includes(
00428| 			responseMode,
00429| 		)
00430| 	) {
00431| 		// If the mode is not known we error. Is probably best like that instead of using
00432| 		// the default that people know as early as possible (probably already testing phase)
00433| 		// that something does not resolve properly.
00434| 		const errorMessage = `The response mode '${responseMode}' is not valid!`;
00435| 		responseCallback(new UnexpectedError(errorMessage), {});
00436| 		throw new InternalServerError(errorMessage);
00437| 	}
00438| 
00439| 	// Add the Response and Request so that this data can be accessed in the node
00440| 	additionalData.httpRequest = req;
00441| 	additionalData.httpResponse = res;
00442| 
00443| 	let didSendResponse = false;
00444| 	let runExecutionDataMerge = {};
00445| 	try {
00446| 		// Run the webhook function to see what should be returned and if
00447| 		// the workflow should be executed or not
00448| 		let webhookResultData: IWebhookResponseData;
00449| 
00450| 		await parseRequestBody(req, workflowStartNode, workflow, executionMode, additionalKeys);
00451| 
00452| 		// TODO: remove this hack, and make sure that execution data is properly created before the MCP trigger is executed
00453| 		if (workflowStartNode.type === MCP_TRIGGER_NODE_TYPE) {
00454| 			// Initialize the data of the webhook node
00455| 			const nodeExecutionStack: IExecuteData[] = [];
00456| 			nodeExecutionStack.push({
00457| 				node: workflowStartNode,
00458| 				data: {
00459| 					main: [],
00460| 				},
00461| 				source: null,
00462| 			});
00463| 			runExecutionData =
00464| 				runExecutionData ??
00465| 				createRunExecutionData({
00466| 					executionData: {

(File has more lines. Use 'offset' parameter to read beyond line 466)
</file>
```
```

---

## Assistant (Explore · big-pickle · 3.8s)

_Thinking:_





```
Tool: read

**Input:**
```json
{
  "filePath": "/home/ab/git-projs/n8n/packages/cli/src/webhooks/webhook-helpers.ts",
  "limit": 100,
  "offset": 466
}
```
**Output:**
```
<file>
00467| 						nodeExecutionStack,
00468| 					},
00469| 				});
00470| 		}
00471| 
00472| 		try {
00473| 			webhookResultData = await Container.get(WebhookService).runWebhook(
00474| 				workflow,
00475| 				webhookData,
00476| 				workflowStartNode,
00477| 				additionalData,
00478| 				executionMode,
00479| 				runExecutionData ?? null,
00480| 			);
00481| 			Container.get(WorkflowStatisticsService).emit('nodeFetchedData', {
00482| 				workflowId: workflow.id,
00483| 				node: workflowStartNode,
00484| 			});
00485| 		} catch (err) {
00486| 			// Send error response to webhook caller
00487| 			const webhookType = ['formTrigger', 'form'].includes(nodeType.description.name)
00488| 				? 'Form'
00489| 				: 'Webhook';
00490| 			const errorMessage = _privateGetWebhookErrorMessage(err, webhookType);
00491| 
00492| 			Container.get(ErrorReporter).error(err, {
00493| 				extra: {
00494| 					nodeName: workflowStartNode.name,
00495| 					nodeType: workflowStartNode.type,
00496| 					nodeVersion: workflowStartNode.typeVersion,
00497| 					workflowId: workflow.id,
00498| 				},
00499| 			});
00500| 
00501| 			responseCallback(new UnexpectedError(errorMessage), {});
00502| 			didSendResponse = true;
00503| 
00504| 			// Add error to execution data that it can be logged and send to Editor-UI
00505| 			runExecutionDataMerge = {
00506| 				resultData: {
00507| 					runData: {},
00508| 					lastNodeExecuted: workflowStartNode.name,
00509| 					error: {
00510| 						...err,
00511| 						message: err.message,
00512| 						stack: err.stack,
00513| 					},
00514| 				},
00515| 			};
00516| 
00517| 			webhookResultData = {
00518| 				noWebhookResponse: true,
00519| 				// Add empty data that it at least tries to "execute" the webhook
00520| 				// which then so gets the chance to throw the error.
00521| 				workflowData: [[{ json: {} }]],
00522| 			};
00523| 		}
00524| 
00525| 		const responseHeaders = evaluateResponseHeaders(context);
00526| 
00527| 		if (!res.headersSent && responseHeaders) {
00528| 			// Only set given headers if they haven't been sent yet, e.g. for streaming
00529| 			for (const [name, value] of responseHeaders.entries()) {
00530| 				res.setHeader(name, value);
00531| 			}
00532| 		}
00533| 
00534| 		if (webhookResultData.noWebhookResponse === true && !didSendResponse) {
00535| 			// The response got already send
00536| 			responseCallback(null, {
00537| 				noWebhookResponse: true,
00538| 			});
00539| 			didSendResponse = true;
00540| 		}
00541| 
00542| 		if (webhookResultData.workflowData === undefined) {
00543| 			// Workflow should not run
00544| 			if (webhookResultData.webhookResponse !== undefined) {
00545| 				// Data to respond with is given
00546| 				if (!didSendResponse) {
00547| 					responseCallback(null, {
00548| 						data: webhookResultData.webhookResponse,
00549| 						responseCode,
00550| 					});
00551| 					didSendResponse = true;
00552| 				}
00553| 			} else {
00554| 				// Send default response
00555| 
00556| 				if (!didSendResponse) {
00557| 					responseCallback(null, {
00558| 						data: {
00559| 							message: 'Webhook call received',
00560| 						},
00561| 						responseCode,
00562| 					});
00563| 					didSendResponse = true;
00564| 				}
00565| 			}
00566| 			return;

(File has more lines. Use 'offset' parameter to read beyond line 566)
</file>
```
```

---

## Assistant (Explore · big-pickle · 49.5s)

_Thinking:_




Based on my comprehensive analysis of the n8n codebase, I can now trace the complete flow of how a workflow JSON object sent from the frontend gets processed and executed. Let me provide you with a detailed breakdown:

## Workflow Execution Flow Analysis

### 1. API Endpoint that Receives Workflow JSON

**Primary Endpoint**: `POST /workflows/:workflowId/run`
- **Location**: `/home/ab/git-projs/n8n/packages/cli/src/workflows/workflows.controller.ts` (lines 584-611)
- **Method**: `runManually()` in the `WorkflowsController`
- **Purpose**: Handles manual workflow execution triggered from the frontend

### 2. JSON Processing and Validation

**First Processing Layer**:
```typescript
// WorkflowsController.runManually()
@Post('/:workflowId/run')
@ProjectScope('workflow:execute')
async runManually(req: WorkflowRequest.ManualRun, _res: unknown) {
```

**Validation Steps**:
1. **ID Validation**: Ensures `workflowData.id` exists and matches URL parameter
2. **Security Check**: In enterprise mode, calls `enterpriseWorkflowService.preventTampering()` to validate user permissions
3. **Structure Validation**: Basic validation through request DTOs

### 3. Workflow Execution Service

**Next Layer**: `WorkflowExecutionService.executeManually()`
- **Location**: `/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-execution.service.ts` (lines 99-249)
- **Key Logic**: Determines execution type (partial vs full) based on payload

**Execution Types**:
1. **Partial Execution**: When `destinationNode` and `runData` are present
2. **Full Execution**: When starting from a known trigger (`triggerToStartFrom`)
3. **Unknown Trigger**: When trigger needs to be auto-detected

### 4. Workflow Runner - Core Execution Engine

**Main Entry Point**: `WorkflowRunner.run()`
- **Location**: `/home/ab/git-projs/n8n/packages/cli/src/workflow-runner.ts` (lines 135-202)
- **Key Decision**: Queue mode vs inline execution

**Execution Path**:
```typescript
// Check if should enqueue to worker queue
if (shouldEnqueue) {
    await this.enqueueExecution(executionId, workflowId, data, loadStaticData, realtime);
} else {
    await this.runMainProcess(executionId, data, loadStaticData, restartExecutionId);
}
```

### 5. Core Workflow Execution Logic

**WorkflowExecute.processRunExecutionData()**
- **Location**: `/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts` (lines 1404-1404)
- **Core Loop**: Processes `nodeExecutionStack` until empty

**Execution Loop**:
```typescript
executionLoop: while (
    this.runExecutionData.executionData!.nodeExecutionStack.length !== 0
) {
    // Extract next node to execute
    executionData = this.runExecutionData.executionData!.nodeExecutionStack.shift() as IExecuteData;
    executionNode = executionData.node;
    
    // Execute the node
    let runNodeData = await this.runNode(/*...*/);
}
```

### 6. Individual Node Execution

**Node Execution Entry**: `WorkflowExecute.runNode()`
- **Location**: `/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts` (lines 1191-1278)
- **Node Type Detection**: Determines if it's a regular execute, poll, trigger, or webhook node

**Execution Logic**:
```typescript
const nodeType = workflow.nodeTypes.getByNameAndVersion(node.type, node.typeVersion);

if (nodeType.execute) {
    return await this.executeNode(/*...*/);
} else if (nodeType.poll) {
    return await this.executePollNode(/*...*/);
} else if (nodeType.trigger) {
    return await this.executeTriggerNode(/*...*/);
}
```

### 7. Actual Node Function Execution

**Final Layer**: `WorkflowExecute.executeNode()`
- **Location**: `/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts` (lines 1007-1077)
- **Context Creation**: Creates `ExecuteContext` with all necessary data
- **Function Call**: Actually calls the node's execute method

```typescript
const context = new ExecuteContext(/*...*/);

let data: INodeExecutionData[][] | EngineRequest | null;

if (customOperation) {
    data = await customOperation.call(context);
} else if (nodeType.execute) {
    data = nodeType instanceof Node
        ? await nodeType.execute(context, subNodeExecutionResults)
        : await nodeType.execute.call(context, subNodeExecutionResults);
}
```

## Key Transition Points

### 1. HTTP Request to Service Layer
```
Frontend POST /workflows/:workflowId/run
↓
WorkflowsController.runManually()
↓
WorkflowExecutionService.executeManually()
```

### 2. Service Layer to Execution Engine
```
WorkflowExecutionService.executeManually()
↓
WorkflowRunner.run()
↓
WorkflowExecute.processRunExecutionData()
```

### 3. Execution Engine to Node Execution
```
WorkflowExecute.processRunExecutionData()
↓
WorkflowExecute.runNode() [for each node]
↓
WorkflowExecute.executeNode()
↓
Actual node.execute() method
```

### 4. Webhook Special Path
For webhook-triggered workflows:
```
HTTP Request → WebhookRequestHandler
↓
WebhookManager.executeWebhook()
↓
WebhookHelpers.executeWebhook()
↓
WorkflowRunner.run()
```

## Additional Key Components

- **Validation**: Workflow validation happens in `WorkflowValidationService`
- **Permissions**: Checked via `CredentialsPermissionChecker` and `SubworkflowPolicyChecker`
- **Error Handling**: Comprehensive error handling at each layer
- **Queue Mode**: Optional distributed execution via Bull queues
- **Lifecycle Hooks**: Pre/post execution hooks for extensibility

This architecture provides a clean separation of concerns with the CLI package handling HTTP/api concerns and the Core package containing the actual workflow execution engine.

---


