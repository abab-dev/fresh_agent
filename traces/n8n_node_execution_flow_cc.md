❯  I need to trace the flow of how a workflow JSON object sent from the frontend gets unmarshaled/unrolled and executed in the n8n
  codebase.

● I'll explore the codebase to trace the workflow execution flow from frontend JSON to backend execution.               01:00 PM  glm-4.7

● Explore(Trace workflow execution flow)
  ⎿  Prompt:
       Trace and document the complete flow of how a workflow JSON object sent from the frontend gets unmarshaled/unrolled and executed in
       the n8n codebase.

       I need to understand:
       1. Where the frontend sends the workflow JSON (API endpoint)
       2. How the workflow JSON is received and validated in the backend
       3. The unmarshaling/unrolling process - how the JSON is converted into executable workflow objects
       4. The execution flow - how the workflow is actually executed

       Focus on:
       - The API controller that receives workflow execution requests
       - The service layer that processes the workflow
       - The workflow execution engine in packages/core
       - How connections between nodes are resolved
       - The data structures used to represent workflows during execution

       Look at packages/cli (Express server, REST API), packages/core (workflow execution engine), packages/workflow (workflow interfaces),
       and packages/editor-ui (Vue frontend).

       Provide specific file paths and line numbers for key components in this flow.
  ⎿  ❯ Trace and document the complete flow of how a workflow JSON object sent from the frontend gets unmarshaled/unrolled and executed in the
       n8n codebase.

       I need to understand:
       1. Where the frontend sends the workflow JSON (API endpoint)
       2. How the workflow JSON is received and validated in the backend
       3. The unmarshaling/unrolling process - how the JSON is converted into executable workflow objects
       4. The execution flow - how the workflow is actually executed

       Focus on:
       - The API controller that receives workflow execution requests
       - The service layer that processes the workflow
       - The workflow execution engine in packages/core
       - How connections between nodes are resolved
       - The data structures used to represent workflows during execution

       Look at packages/cli (Express server, REST API), packages/core (workflow execution engine), packages/workflow (workflow interfaces), and
       packages/editor-ui (Vue frontend).

       Provide specific file paths and line numbers for key components in this flow.
  ⎿  Search(pattern: "POST.*\/executions|executeWorkflow", path: "/home/ab/git-projs/n8n/packages/cli")

  ⎿  Search(pattern: "app\.post.*executions", path: "/home/ab/git-projs/n8n/packages/cli")

  ⎿  Search(pattern: "**/execution*controller*.ts", path: "/home/ab/git-projs/n8n/packages/cli")

  ⎿  Search(pattern: "**/routes/executions*.ts", path: "/home/ab/git-projs/n8n/packages/cli")

  ⎿  Search(pattern: "execute.*workflow|run.*workflow", path: "/home/ab/git-projs/n8n/packages/editor-ui", glob: "*.ts")

  ⎿  Error: Path does not exist: /home/ab/git-projs/n8n/packages/editor-ui

  ⎿  Search(pattern: "packages/editor-ui/src/**/*execution*.ts", path: "/home/ab/git-projs/n8n")

  ⎿  Search(pattern: "packages/frontend/src/**/*execution*.ts", path: "/home/ab/git-projs/n8n")

  ⎿  Read(/home/ab/git-projs/n8n/packages/cli/src/executions/executions.controller.ts)

  ⎿  Search(pattern: "class.*ExecutionService", path: "/home/ab/git-projs/n8n/packages/cli/src", glob: "*.ts")


  ⎿  Read(/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-execution.service.ts)

  ⎿  Read(/home/ab/git-projs/n8n/packages/cli/src/manual-execution.service.ts)

  ⎿  Search(pattern: "@Post.*webhook|@Post.*execute|@Post.*run", path: "/home/ab/git-projs/n8n/packages/cli/src")

  ⎿  Search(pattern: "**/workflows*.controller.ts", path: "/home/ab/git-projs/n8n/packages/cli/src")

  ⎿

  ⎿  Read(/home/ab/git-projs/n8n/packages/cli/src/workflows/workflows.controller.ts)

  ⎿  Search(pattern: "class WorkflowRunner", path: "/home/ab/git-projs/n8n/packages/cli/src")

  ⎿  Search(pattern: "class.*WorkflowExecute", path: "/home/ab/git-projs/n8n/packages/cli/src")

  ⎿  Search(pattern: "**/workflow-runner*.ts", path: "/home/ab/git-projs/n8n/packages/cli/src")

  ⎿

  ⎿

  ⎿

  ⎿

  ⎿  Read(/home/ab/git-projs/n8n/packages/cli/src/workflow-runner.ts)

  ⎿  Search(pattern: "**/workflow-execute*.ts", path: "/home/ab/git-projs/n8n/packages/core")

  ⎿  Search(pattern: "**/workflow.ts", path: "/home/ab/git-projs/n8n/packages/workflow")

  ⎿  Search(pattern: "export class Workflow", path: "/home/ab/git-projs/n8n/packages/workflow")

  ⎿

  ⎿

  ⎿

  ⎿

  ⎿  Read(/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts)

  ⎿  Read(/home/ab/git-projs/n8n/packages/workflow/src/workflow.ts)

  ⎿  Search(pattern: "export interface.*WorkflowBase|export interface.*IWorkflowBase", path: "/home/ab/git-projs/n8n/packages/workflow/src")

  ⎿  Search(pattern: "export interface.*IWorkflowExecutionDataProcess", path: "/home/ab/git-projs/n8n/packages/workflow/src")

  ⎿

  ⎿

  ⎿

  ⎿

  ⎿  Read(/home/ab/git-projs/n8n/packages/workflow/src/interfaces.ts · lines 0-199)

  ⎿  Read(/home/ab/git-projs/n8n/packages/workflow/src/interfaces.ts · lines 700-849)

  ⎿  Search(pattern: "interface.*ManualRunPayload|type.*ManualRunPayload", path: "/home/ab/git-projs/n8n/packages/cli/src")

  ⎿  Read(/home/ab/git-projs/n8n/packages/cli/src/workflows/workflow.request.ts)

  ⎿

  ⎿

  ⎿

  ⎿

  ⎿  Read(/home/ab/git-projs/n8n/packages/workflow/src/interfaces.ts · lines 2800-2899)

  ⎿  Search(pattern: "export interface IWorkflowExecutionDataProcess", path: "/home/ab/git-projs/n8n/packages/workflow/src")

  ⎿  Read(/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts · lines 0-199)

  ⎿

  ⎿

  ⎿

  ⎿  Search(pattern: "IWorkflowExecutionDataProcess", path: "/home/ab/git-projs/n8n/packages/workflow/src", output_mode: "content",
           head_limit: 50)
  ⎿  Read(/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts · lines 450-599)

  ⎿  Search(pattern: "processRunExecutionData", path: "/home/ab/git-projs/n8n/packages/core/src/execution-engine", output_mode: "content",
           head_limit: 30)
  ⎿

  ⎿

  ⎿

  ⎿  Read(/home/ab/git-projs/n8n/packages/workflow/src/interfaces.ts · lines 2700-2779)

  ⎿  Read(/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts · lines 1400-1599)

  ⎿  Search(pattern: "runNode|executeNode", path: "/home/ab/git-projs/n8n/packages/core/src/execution-engine", output_mode: "content",
           head_limit: 20)
  ⎿

  ⎿

  ⎿

  ⎿  Read(/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts · lines 1600-1799)

  ⎿  Read(/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts · lines 1200-1449)

  ⎿

  ⎿

  ⎿  Search(pattern: "export interface IWorkflowBase", path: "/home/ab/git-projs/n8n/packages/workflow/src", output_mode: "content",
           head_limit: 50)
  ⎿  Search(pattern: "export interface IConnections", path: "/home/ab/git-projs/n8n/packages/workflow/src", output_mode: "content",
           head_limit: 30)
  ⎿  Read(/home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts · lines 1000-1149)

  ⎿

  ⎿

  ⎿

  ⎿  Read(/home/ab/git-projs/n8n/packages/workflow/src/interfaces.ts · lines 2650-2729)

  ⎿  Read(/home/ab/git-projs/n8n/packages/workflow/src/interfaces.ts · lines 410-469)

  ⎿  Read(/home/ab/git-projs/n8n/packages/workflow/src/common.ts · lines 1-100)

  ⎿  Error: File does not exist. Did you mean common?

  ⎿

  ⎿

  ⎿  Search(pattern: "**/common*.ts", path: "/home/ab/git-projs/n8n/packages/workflow/src")

  ⎿

  ⎿  Bash(find /home/ab/git-projs/n8n/packages/workflow/src -name "*.ts" | head -30)
     Waiting…
  ⎿  Search(pattern: "export.*mapConnectionsByDestination", path: "/home/ab/git-projs/n8n/packages/workflow/src", output_mode: "content",
           head_limit: 20)
  ⎿

  ⎿

  ⎿  Read(/home/ab/git-projs/n8n/packages/workflow/src/common/map-connections-by-destination.ts)

  ⎿  Bash(ls /home/ab/git-projs/n8n/packages/workflow/src/common/)
     Waiting…
  ⎿

  ⎿

  ⎿  Read(/home/ab/git-projs/n8n/packages/workflow/src/common/index.ts)

  ⎿  Read(/home/ab/git-projs/n8n/packages/workflow/src/common/get-parent-nodes.ts)

  ⎿  Read(/home/ab/git-projs/n8n/packages/workflow/src/common/get-child-nodes.ts)

  ⎿

  ⎿

  ⎿

  ⎿  Response:
       Now I have enough information to provide a comprehensive documentation. Let me compile the findings:

       Complete Flow of Workflow JSON Execution in n8n

       Based on my analysis of the n8n codebase, here's the complete flow of how a workflow JSON object sent from the frontend gets
       unmarshaled/unrolled and executed:

       1. API Endpoint - Frontend to Backend Communication

       Location: /home/ab/git-projs/n8n/packages/cli/src/workflows/workflows.controller.ts

       Line Numbers: Lines 615-660

       The workflow execution starts when the frontend sends a POST request to the /workflows/:workflowId/run endpoint:

       @Post('/:workflowId/run')
       @ProjectScope('workflow:execute')
       async runManually(req: WorkflowRequest.ManualRun, _res: unknown) {
           // ... validation code ...

           const result = await this.workflowExecutionService.executeManually(
               req.body,
               req.user,
               req.headers['push-ref'],
           );

           return result;
       }

       Request Payload Structure (WorkflowRequest.ManualRunPayload):
       - File: /home/ab/git-projs/n8n/packages/cli/src/workflows/workflow.request.ts (Lines 36-66)
       - Three types of payloads:
         a. FullManualExecutionFromKnownTriggerPayload - User selected a specific trigger
         b. FullManualExecutionFromUnknownTriggerPayload - System determines trigger
         c. PartialManualExecutionToDestinationPayload - Execute to specific node with existing run data

       The payload contains:
       {
           workflowData: IWorkflowBase,  // The workflow JSON
           destinationNode?: IDestinationNode,  // Target node for partial execution
           triggerToStartFrom?: { name: string; data?: ITaskData },
           runData?: IRunData,  // Previous execution data
           dirtyNodeNames?: string[],  // Nodes to re-execute
           agentRequest?: AiAgentRequest
       }

       2. Service Layer - Workflow Execution Service

       Location: /home/ab/git-projs/n8n/packages/cli/src/workflows/workflow-execution.service.ts

       Line Numbers: Lines 101-251 (executeManually method)

       The WorkflowExecutionService.executeManually() method processes the request:

       async executeManually(
           payload: WorkflowRequest.ManualRunPayload,
           user: User,
           pushRef?: string,
       ): Promise<{ executionId: string } | { waitingForWebhook: boolean }>

       Key Processing Steps:

       1. Workflow Validation (Lines 107-111): Check if workflow is active, set to inactive for manual execution
       2. Determine Execution Type (Lines 121-207):
         - Partial Execution (Lines 121-136): If destination node and runData provided, execute only to that node
         - Full Execution from Known Trigger (Lines 140-170): User specified trigger node
         - Full Execution from Unknown Trigger (Lines 173-207): System finds trigger from pinned data
       3. Prepare Execution Data (Lines 123-246):
       const data: IWorkflowExecutionDataProcess = {
           executionMode: 'manual',
           workflowData: payload.workflowData,
           userId: user.id,
           destinationNode: payload.destinationNode,
           triggerToStartFrom: payload.triggerToStartFrom,
           pinData: payload.workflowData.pinData,
           runData: payload.runData,
           dirtyNodeNames: payload.dirtyNodeNames
       };
       4. Execute via WorkflowRunner (Line 244):
       const executionId = await this.workflowRunner.run(data);

       3. Workflow Runner - Execution Orchestration

       Location: /home/ab/git-projs/n8n/packages/cli/src/workflow-runner.ts

       Line Numbers: Lines 135-202 (run method), 206-366 (runMainProcess method)

       The WorkflowRunner.run() method orchestrates the execution:

       async run(
           data: IWorkflowExecutionDataProcess,
           loadStaticData?: boolean,
           realtime?: boolean,
           restartExecutionId?: string,
           responsePromise?: IDeferredPromise<IExecuteResponsePromiseData>,
       ): Promise<string>

       Key Steps:

       1. Register Execution (Line 143):
       const executionId = await this.activeExecutions.add(data, restartExecutionId);
       2. Check Permissions (Lines 147-161): Validate credentials permissions
       3. Determine Execution Mode (Lines 168-177):
         - Queue mode (for production): Enqueue to worker
         - Main process (for manual): Execute directly
       4. Main Process Execution (runMainProcess, Lines 206-366):

       4. a. Create Workflow Instance (Lines 234-244):
       const workflow = new Workflow({
           id: workflowId,
           name: data.workflowData.name,
           nodes: data.workflowData.nodes,
           connections: data.workflowData.connections,
           active: data.workflowData.activeVersionId !== null,
           nodeTypes: this.nodeTypes,
           staticData: data.workflowData.staticData,
           settings: workflowSettings,
           pinData,
       });

       4. b. Prepare Additional Data (Lines 246-257): Add execution context, hooks, timeouts

       4. c. Create WorkflowExecute Instance (Lines 293-298):
       const workflowExecute = new WorkflowExecute(
           additionalData,
           data.executionMode,
           data.executionData,
       );

       4. d. Execute (Lines 298 or 300-306):
         - With execution data: workflowExecute.processRunExecutionData(workflow)
         - Without execution data: manualExecutionService.runManually(...)

       4. Workflow Class - Data Structure Transformation

       Location: /home/ab/git-projs/n8n/packages/workflow/src/workflow.ts

       Line Numbers: Lines 59-135 (constructor), 138-148 (setNodes, setConnections)

       Key Transformation - Unmarshaling/Unrolling:

       The Workflow class constructor transforms the JSON into executable objects:

       constructor(parameters: WorkflowParameters) {
           // 1. Store basic metadata
           this.id = parameters.id;
           this.name = parameters.name;
           this.nodeTypes = parameters.nodeTypes;

           // 2. Process nodes - add default values
           for (const node of parameters.nodes) {
               nodeType = this.nodeTypes.getByNameAndVersion(node.type, node.typeVersion);
               const nodeParameters = NodeHelpers.getNodeParameters(
                   nodeType.description.properties,
                   node.parameters,
                   true,  // returnDefaults
                   false, // ignoreHidden
                   node,
                   nodeType.description,
               );
               node.parameters = nodeParameters !== null ? nodeParameters : {};
           }

           // 3. Transform nodes array to object for O(1) lookup
           this.setNodes(parameters.nodes);  // Lines 138-143
           // nodes: { "nodeName": nodeObject, ... }

           // 4. Transform connections - create dual indexes
           this.setConnections(parameters.connections);  // Lines 145-148
           // connectionsBySourceNode: Original format (source -> destination)
           // connectionsByDestinationNode: Inverted format (destination -> source)
       }

       Connection Resolution:

       File: /home/ab/git-projs/n8n/packages/workflow/src/common/map-connections-by-destination.ts

       The mapConnectionsByDestination() function inverts the connection graph:

       // Original structure (from JSON):
       connectionsBySourceNode = {
           "NodeA": {
               "main": [
                   [{ node: "NodeB", index: 0, type: "main" }]
               ]
           }
       }

       // Transformed to:
       connectionsByDestinationNode = {
           "NodeB": {
               "main": [
                   [{ node: "NodeA", index: 0, type: "main" }]
               ]
           }
       }

       This dual indexing allows efficient traversal in both directions:
       - Forward traversal (finding children): Use connectionsBySourceNode
       - Backward traversal (finding parents): Use connectionsByDestinationNode

       Traversal Utilities:

       Files:
       - /home/ab/git-projs/n8n/packages/workflow/src/common/get-parent-nodes.ts (Lines 11-18)
       - /home/ab/git-projs/n8n/packages/workflow/src/common/get-child-nodes.ts (Lines 5-12)

       // Get parent nodes (predecessors)
       getParentNodes(this.connectionsByDestinationNode, nodeName, 'main', depth)

       // Get child nodes (successors)
       getChildNodes(this.connectionsBySourceNode, nodeName, 'main', depth)

       5. WorkflowExecute - Core Execution Engine

       Location: /home/ab/git-projs/n8n/packages/core/src/execution-engine/workflow-execute.ts

       Line Numbers:
       - Lines 122-182 (run method)
       - Lines 1431-1950+ (processRunExecutionData method)
       - Lines 1214-1302 (runNode method)
       - Lines 1030-1101 (executeNode method)

       Main Execution Flow:

       A. Initial Setup (run method, Lines 122-182):

       run({
           workflow,
           startNode,
           destinationNode,
           pinData,
           triggerToStartFrom,
           additionalRunFilterNodes,
       }): PCancelable<IRun>

       1. Determine Start Node (Line 133):
       startNode = startNode || workflow.getStartNode(destinationNode?.nodeName);
       2. Create Node Filter for Partial Execution (Lines 140-149):
       if (destinationNode) {
           runNodeFilter = workflow.getParentNodes(destinationNode.nodeName);
           if (destinationNode.mode === 'inclusive') {
               runNodeFilter.push(destinationNode.nodeName);
           }
       }
       3. Initialize Execution Stack (Lines 152-167):
       const nodeExecutionStack: IExecuteData[] = [{
           node: startNode,
           data: triggerToStartFrom?.data ?? { main: [[{ json: {} }]] },
           source: null,
       }];

       B. Process Execution Loop (processRunExecutionData, Lines 1431+):

       processRunExecutionData(workflow: Workflow): PCancelable<IRun> {
           // Main execution loop
           executionLoop: while (nodeExecutionStack.length !== 0) {
               // 1. Pop next node from stack
               executionData = nodeExecutionStack.shift();
               executionNode = executionData.node;

               // 2. Check if node should be executed (filter, disabled, etc.)
               if (runNodeFilter && !runNodeFilter.includes(executionNode.name)) {
                   continue;
               }

               // 3. Execute the node
               let runNodeData = await this.runNode(
                   workflow,
                   executionData,
                   runExecutionData,
                   runIndex,
                   additionalData,
                   mode,
                   abortSignal,
               );

               // 4. Process results and add child nodes to stack
               if (nodeSuccessData) {
                   // Add connected nodes to execution stack
                   this.addNodeToBeExecuted(...);
               }
           }
       }

       C. Node Execution (runNode, Lines 1214-1302):

       async runNode(
           workflow: Workflow,
           executionData: IExecuteData,
           runExecutionData: IRunExecutionData,
           runIndex: number,
           additionalData: IWorkflowExecuteAdditionalData,
           mode: WorkflowExecuteMode,
           abortSignal?: AbortSignal,
       ): Promise<IRunNodeResponse | EngineRequest>

       1. Get Node Type (Line 1231):
       const nodeType = workflow.nodeTypes.getByNameAndVersion(
           node.type,
           node.typeVersion
       );
       2. Route to Appropriate Executor (Lines 1249-1301):
         - Regular nodes with execute: → executeNode() (Line 1250)
         - Poll nodes: → executePollNode() (Line 1268)
         - Trigger nodes: → executeTriggerNode() (Line 1272)
         - Webhook nodes: Pass through data (Line 1287)

       D. Execute Node (executeNode, Lines 1030-1101):

       private async executeNode(
           workflow, node, nodeType, customOperation,
           additionalData, mode, runExecutionData, runIndex,
           connectionInputData, inputData, executionData, abortSignal
       ): Promise<IRunNodeResponse>

       1. Create Execution Context (Lines 1046-1059):
       const context = new ExecuteContext(
           workflow, node, additionalData, mode, runExecutionData,
           runIndex, connectionInputData, inputData, executionData,
           closeFunctions, abortSignal, subNodeExecutionResults
       );
       2. Call Node's Execute Method (Lines 1063-1074):
       if (customOperation) {
           data = await customOperation.call(context);
       } else if (nodeType.execute) {
           data = await nodeType.execute.call(context);
       }
       3. Return Results (Line 1100):
       return { data, hints: context.hints };

       6. Data Structures Summary

       IWorkflowBase Interface

       File: /home/ab/git-projs/n8n/packages/workflow/src/interfaces.ts (Lines 2658-2677)

       export interface IWorkflowBase {
           id: string;
           name: string;
           nodes: INode[];
           connections: IConnections;
           settings?: IWorkflowSettings;
           staticData?: IDataObject;
           pinData?: IPinData;
           active: boolean;
           activeVersionId: string | null;
           // ... other fields
       }

       IConnections Structure

       File: /home/ab/git-projs/n8n/packages/workflow/src/interfaces.ts (Lines 414-417)

       export interface IConnections {
           [nodeName: string]: {  // Source node name
               [connectionType: string]: {  // "main", "ai_agent", etc.
                   [outputIndex: string]: IConnection[]  // Array of connections
               }
           }
       }

       export interface IConnection {
           node: string;      // Destination node name
           type: string;      // Connection type
           index: number;     // Input index on destination
       }

       IWorkflowExecutionDataProcess Interface

       File: /home/ab/git-projs/n8n/packages/workflow/src/interfaces.ts (Lines 2707-2733)

       export interface IWorkflowExecutionDataProcess {
           destinationNode?: IDestinationNode;
           executionMode: WorkflowExecuteMode;  // 'manual', 'trigger', 'webhook', etc.
           executionData?: IRunExecutionData;
           runData?: IRunData;
           pinData?: IPinData;
           workflowData: IWorkflowBase;
           userId?: string;
           triggerToStartFrom?: { name: string; data?: ITaskData };
           dirtyNodeNames?: string[];
           agentRequest?: AiAgentRequest;
           // ... other fields
       }

       IExecuteData Interface (Execution Stack Item)

       File: /home/ab/git-projs/n8n/packages/workflow/src/interfaces.ts (Lines 447-453)

       export interface IExecuteData {
           node: INode;                      // Node to execute
           data: ITaskDataConnections;       // Input data for the node
           source: ITaskDataConnectionsSource | null;  // Where data came from
           runIndex?: number;                // Execution attempt number
           metadata?: ITaskMetadata;
       }

       7. Complete Execution Flow Summary

       1. Frontend → POST /workflows/:id/run
          ↓
       2. WorkflowsController.runManually()
          File: packages/cli/src/workflows/workflows.controller.ts:615-660
          ↓
       3. WorkflowExecutionService.executeManually()
          File: packages/cli/src/workflows/workflow-execution.service.ts:101-251
          - Validates workflow
          - Determines execution type (full/partial)
          - Creates IWorkflowExecutionDataProcess
          ↓
       4. WorkflowRunner.run()
          File: packages/cli/src/workflow-runner.ts:135-202
          - Registers execution
          - Checks permissions
          - Routes to queue or main process
          ↓
       5. WorkflowRunner.runMainProcess()
          File: packages/cli/src/workflow-runner.ts:206-366
          - Creates Workflow instance (JSON → Object transformation)
          - Prepares additional data
          - Creates WorkflowExecute instance
          ↓
       6. Workflow Constructor
          File: packages/workflow/src/workflow.ts:59-135
          - Transforms nodes array to object (O(1) lookup)
          - Transforms connections (creates dual index)
          - Adds default parameter values
          ↓
       7. WorkflowExecute.run() or processRunExecutionData()
          File: packages/core/src/execution-engine/workflow-execute.ts:122-182, 1431+
          - Determines start node
          - Creates execution stack
          - Processes nodes in loop
          ↓
       8. WorkflowExecute.runNode()
          File: packages/core/src/execution-engine/workflow-execute.ts:1214-1302
          - Gets node type
          - Routes to appropriate executor
          ↓
       9. WorkflowExecute.executeNode()
          File: packages/core/src/execution-engine/workflow-execute.ts:1030-1101
          - Creates execution context
          - Calls node's execute() method
          - Returns results
          ↓
       10. Add Child Nodes to Stack
           - Uses connections to find next nodes
           - Pushes to execution stack
           - Continues loop until stack empty

       Key Architectural Patterns

       1. Dual-Indexed Connections: Both source→destination and destination→source mappings for efficient traversal
       2. Execution Stack: Nodes are added to a stack as they become ready to execute
       3. Waiting Execution: Nodes with multiple inputs wait until all inputs are available
       4. Partial Execution: Can execute only a portion of the workflow based on destination node and run data
       5. Node Filters: Only nodes in the filter (parents of destination) are executed in partial mode
       6. Lifecycle Hooks: Pre/post execution hooks for extensibility
  ⎿  Done (54 tool uses · 0 tokens · 2m 32s)

∴ Thinking…

  The agent provided a comprehensive overview of the workflow execution flow. Let me summarize the key findings for the user in a clear and
  concise way.

● Workflow Execution Flow in n8n                                                                                        01:02 PM  glm-4.7

  Here's the complete flow of how a workflow JSON from the frontend gets executed:

  Summary Flow

  Frontend → API Endpoint → Service Layer → Workflow Runner → Workflow Constructor → Execution Engine

  1. API Entry Point

  packages/cli/src/workflows/workflows.controller.ts:615-660
  - POST /workflows/:workflowId/run receives the workflow JSON
  - Calls WorkflowExecutionService.executeManually()

  2. Service Layer

  packages/cli/src/workflows/workflow-execution.service.ts:101-251
  - Validates workflow state
  - Determines execution type (full/partial)
  - Creates IWorkflowExecutionDataProcess payload
  - Calls WorkflowRunner.run()

  3. Workflow Runner

  packages/cli/src/workflow-runner.ts:135-366
  - Registers the execution
  - Creates Workflow instance (this is where unmarshaling happens)
  - Creates WorkflowExecute instance
  - Initiates execution

  4. Unmarshaling/Unrolling (Key Transformation)

  packages/workflow/src/workflow.ts:59-148

  The Workflow constructor transforms JSON into executable objects:

  // Before: JSON from frontend
  {
    "nodes": [{ "name": "Node1", "type": "...", "parameters": {...} }],
    "connections": { "Node1": { "main": [[{ "node": "Node2" }]] }}
  }

  // After: Executable Workflow object
  workflow.nodes = { "Node1": nodeObject, "Node2": nodeObject, ... }  // O(1) lookup
  workflow.connectionsBySourceNode = { ... }      // Forward traversal
  workflow.connectionsByDestinationNode = { ... } // Backward traversal

  Connection transformation at packages/workflow/src/common/map-connections-by-destination.ts creates dual indexes for
  efficient graph traversal.

  5. Execution Engine

  packages/core/src/execution-engine/workflow-execute.ts

  - run() (122-182): Sets up execution stack with start node
  - processRunExecutionData() (1431+): Main execution loop
    - Pops node from stack
    - Calls runNode()
    - Adds child nodes to stack based on connections
  - runNode() (1214-1302): Routes to appropriate executor
  - executeNode() (1030-1101): Calls the node's execute() method with context

  Key Data Structures
  ┌───────────────────────────────┬───────────────────────────────────┬──────────────────────────────────────────┐
  │           Interface           │              Purpose              │                 Location                 │
  ├───────────────────────────────┼───────────────────────────────────┼──────────────────────────────────────────┤
  │ IWorkflowBase                 │ Raw workflow JSON from frontend   │ packages/workflow/src/interfaces.ts:2658 │
  ├───────────────────────────────┼───────────────────────────────────┼──────────────────────────────────────────┤
  │ IWorkflowExecutionDataProcess │ Execution request payload         │ packages/workflow/src/interfaces.ts:2707 │
  ├───────────────────────────────┼───────────────────────────────────┼──────────────────────────────────────────┤
  │ IExecuteData                  │ Single item on execution stack    │ packages/workflow/src/interfaces.ts:447  │
  ├───────────────────────────────┼───────────────────────────────────┼──────────────────────────────────────────┤
  │ IConnections                  │ Connection graph (source-indexed) │ packages/workflow/src/interfaces.ts:414  │
  └───────────────────────────────┴───────────────────────────────────┴──────────────────────────────────────────┘
  Traversal Utilities

  For navigating the workflow graph:
  - getChildNodes() - packages/workflow/src/common/get-child-nodes.ts:5
  - getParentNodes() - packages/workflow/src/common/get-parent-nodes.ts:11
  - mapConnectionsByDestination() - packages/workflow/src/common/map-connections-by-destination.ts

  Important: The workflow.connections structure is indexed by source node. To find parents, you must invert it first
  using mapConnectionsByDestination().
