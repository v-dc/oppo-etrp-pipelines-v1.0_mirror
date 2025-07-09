# Prompt Strategy Guide v2.0

## 1. TASK Section (Primary Instruction First)

**Design Decision**: Place the core task as a single, clear sentence at the very top.

**Sources & Reasoning**:
- AWS/Anthropic documentation specifies the recommended order: "Task context: Assign the LLM a role or persona and broadly define the task it is expected to perform" should come first
- Anthropic's "Be clear and direct" guide emphasizes: "The more precisely you explain what you want, the better Claude's response will be"
- Claude Code best practices show task-first examples: "migrate foo.py from React to Vue. When you are done, you MUST return the string OK"

**Chain of Thought**: Claude Code is agentic, so it needs to understand the primary objective immediately. A scattered or buried task description leads to confused implementation.

**Typical Elements**: Primary objective, main deliverable, target outcome

## 2. SUCCESS CRITERIA Section (Measurable Outcomes)

**Design Decision**: Use checkboxes with specific, measurable behaviors before diving into technical details.

**Sources & Reasoning**:
- Anthropic's prompt engineering process emphasizes: "Define the task and success criteria: The first and most crucial step is to clearly define the specific task you want Claude to perform"
- Claude 4 best practices state: "Be specific about desired behavior: Consider describing exactly what you'd like to see in the output"

**Chain of Thought**: Success criteria prevent scope creep and provide Claude with clear validation targets. Checkboxes make it scannable and actionable.

**Typical Elements**: Validation checkpoints, functional requirements, completion indicators

## 3. CONTEXT FILES Section (Dependencies Before Implementation)

**Design Decision**: Reference external files immediately after task definition but before technical specifications.

**Sources & Reasoning**:
- Long context prompting tips: "Put longform data at the top: Place your long documents and inputs (~20K+ tokens) near the top of your prompt, above your query, instructions, and examples"
- Context guidance states: "Give Claude contextual information: Just like you might be able to better perform on a task if you knew more context, Claude will perform better if it has more contextual information"

**Chain of Thought**: Claude Code needs to understand existing schemas, patterns, and constraints before architecting new solutions. Context files provide the "rules of the game."

**Typical Elements**: Dependencies, schemas, module interfaces, shared utilities

## 4. TECHNICAL SPECIFICATIONS (Implementation Details)

**Design Decision**: Break down into data flow, infrastructure, and quality requirements as separate subsections.

**Sources & Reasoning**:
- Chain prompts documentation: "Use prompt chaining for multi-step tasks like research synthesis, document analysis, or iterative content creation"
- Sequential instructions guidance: "Provide instructions as sequential steps: Use numbered lists or bullet points to better ensure that Claude carries out the task the exact way you want it to"

**Chain of Thought**: Complex development tasks have multiple dimensions (data, infrastructure, quality). Separating these prevents Claude from missing critical aspects.

**Typical Elements**: Data flow, processing logic, integration points, technology stack

## 5. DELIVERABLES (Concrete Outputs)

**Design Decision**: Specify exact filenames and purposes rather than vague descriptions.

**Sources & Reasoning**:
- Claude 4 best practices: "Being specific about your desired output can help enhance results"
- Claude Code examples demonstrate specific success indicators: "you MUST return the string OK if you succeeded, or FAIL if the task failed"

**Chain of Thought**: Vague deliverables like "documentation" lead to inconsistent outputs. Specific filenames with purposes provide clear targets.

**Typical Elements**: Source files, test files, documentation, configuration files

## 6. CONSTRAINTS & STANDARDS (Boundaries and Quality)

**Design Decision**: Include security, compatibility, and scalability considerations as explicit constraints.

**Sources & Reasoning**:
- Contextual information examples include: "What the task results will be used for, What audience the output is meant for, What workflow the task is a part of"
- System prompts guide: "Improved focus: By setting the role context, Claude stays more within the bounds of your task's specific requirements"

**Chain of Thought**: Production systems have implicit requirements (security, scalability) that Claude might not consider without explicit prompting.

**Typical Elements**: Coding standards, security requirements, established patterns, error handling conventions

## 7. SECTION ORDERING BY PROJECT TYPE (Context-Dependent Structure)

**Design Decision**: Adapt section ordering based on project characteristics rather than using a rigid template.

**Sources & Reasoning**:
- Anthropic's guidance on prompt templates: "Adapt templates to your specific use case" and "Consider the nature of your task when structuring prompts"
- Claude Code examples show variation in structure based on task complexity

**Chain of Thought**: Different project types have different cognitive requirements. A data migration needs context files upfront, while a greenfield project benefits from deliverables-first thinking.

### Recommended Orders by Project Type:

**Implementation/Development Tasks** (building something new):
```
1. TASK
2. DELIVERABLES (concrete outputs provide immediate clarity)
3. SUCCESS CRITERIA (validation of those deliverables)
4. CONTEXT FILES (existing code/patterns to follow)
5. TECHNICAL SPECIFICATIONS
6. CONSTRAINTS & STANDARDS
```
*Rationale*: Claude needs to understand what it's building before diving into how to build it.

**Integration/Migration Tasks** (working within existing systems):
```
1. TASK
2. CONTEXT FILES (critical to understand existing environment)
3. TECHNICAL SPECIFICATIONS (how to work within constraints)
4. SUCCESS CRITERIA
5. DELIVERABLES
6. CONSTRAINTS & STANDARDS
```
*Rationale*: Context dominates - Claude must understand the existing system before planning changes.

**Research/Analysis Tasks** (discovery and recommendations):
```
1. TASK
2. SUCCESS CRITERIA (define what good analysis looks like)
3. CONTEXT FILES (data sources and references)
4. TECHNICAL SPECIFICATIONS (analysis methodology)
5. DELIVERABLES (reports/findings format)
6. CONSTRAINTS & STANDARDS
```
*Rationale*: Success criteria guide the research direction before diving into specifics.

**Bug Fix/Debugging Tasks** (solving specific problems):
```
1. TASK (including problem description)
2. CONTEXT FILES (relevant code and logs)
3. SUCCESS CRITERIA (definition of "fixed")
4. TECHNICAL SPECIFICATIONS (approach/tools)
5. DELIVERABLES (fixed code/patches)
6. CONSTRAINTS & STANDARDS
```
*Rationale*: Understanding the problem context is paramount before proposing solutions.

**Phase 1: Discovery & Requirements Analysis** (business and technical assessment):
```
1. TASK
2. SUCCESS CRITERIA (what constitutes complete discovery)
3. CONTEXT FILES (existing documentation, stakeholder inputs)
4. TECHNICAL SPECIFICATIONS (analysis methodologies)
5. DELIVERABLES (requirements documents)
6. CONSTRAINTS & STANDARDS (compliance, governance)
```
*Rationale*: Success criteria define the thoroughness of discovery before diving into methodologies.

**Phase 2: Solution Design & Architecture** (two-step process):

**Step 2A: Solution Decomposition**
```
1. TASK
2. SUCCESS CRITERIA (optimal module structure for agentic development)
3. CONTEXT FILES (Phase 1 requirements, data sources)
4. TECHNICAL SPECIFICATIONS (decomposition methodology)
5. DELIVERABLES (module structure and rationale)
6. CONSTRAINTS & STANDARDS (Claude Code optimization)
```
*Rationale*: Focus purely on module boundaries without implementation complexity.

**Step 2B: Complete Architecture Design**
```
1. TASK
2. CONTEXT FILES (module structure from 2A, Phase 1 requirements)
3. SUCCESS CRITERIA (design completeness and validation)
4. TECHNICAL SPECIFICATIONS (architecture patterns, technology decisions)
5. DELIVERABLES (design documents, diagrams)
6. CONSTRAINTS & STANDARDS (architectural principles, compliance)
```
*Rationale*: Context from module decomposition and Phase 1 requirements drives detailed architecture decisions.

### Selection Criteria:
- **High context dependency** → Context files early
- **Clear output requirements** → Deliverables early  
- **Complex validation needs** → Success criteria early
- **Greenfield project** → Technical specifications can come later
- **Legacy system work** → Context and constraints upfront
- **Discovery phase** → Success criteria define thoroughness
- **Design phase** → Module decomposition first, then requirements context drives architecture decisions

**Key Principle**: The optimal order maximizes Claude's understanding at each step, preventing backtracking and confusion. Consider what Claude needs to know first to avoid making incorrect assumptions.

## 8. FRAMEWORK PHASE PROMPT EXAMPLES

### Phase 1: Discovery & Requirements Prompt Template

```bash
claude "TASK: Conduct comprehensive discovery and requirements analysis for [project_name] data solution.

SUCCESS CRITERIA: Complete requirements documentation that enables Phase 2 design
- [ ] Business objectives clearly defined with measurable success metrics
- [ ] All data sources identified with access patterns and volumes
- [ ] Technical infrastructure capacity and constraints documented
- [ ] Stakeholder needs and data consumer requirements mapped
- [ ] Compliance and security requirements identified
- [ ] Data quality issues and patterns profiled
- [ ] SLA and performance requirements specified

CONTEXT FILES: Review existing documentation and inputs
- Project charter or initial requirements (if available)
- Existing system documentation
- Stakeholder interview notes
- Data source inventory
- Infrastructure documentation

TECHNICAL SPECIFICATIONS: Discovery methodology
- Conduct stakeholder interviews using structured templates
- Perform data profiling on all identified sources
- Assess current infrastructure capacity and performance
- Review regulatory and compliance requirements
- Analyze existing data flows and integration points
- Document data quality patterns and anomalies

DELIVERABLES: Create Phase 1 requirements package
- requirements/business_requirements.md - Business objectives, KPIs, success criteria
- requirements/technical_assessment.md - Infrastructure evaluation, capacity analysis
- requirements/data_discovery.md - Data profiling results, quality assessment

CONSTRAINTS & STANDARDS: Follow discovery best practices
- Use standardized templates for consistency
- Ensure all stakeholder groups are represented
- Document assumptions and risks explicitly
- Validate findings with business stakeholders
- Follow data privacy and security protocols during profiling"
```

### Phase 2: Solution Design & Architecture (Two-Step Process)

#### Step 2A: Solution Decomposition Prompt Template

```bash
claude "TASK: Design module decomposition for [project_name] optimized for agentic code generation.

SUCCESS CRITERIA: Optimal module structure for Claude Code development
- [ ] Each module has clear, single responsibility  
- [ ] Module boundaries enable isolated testing
- [ ] Module size balances maintainability with AI generation limits (200-400 lines optimal)
- [ ] No over-decomposition (prefer fewer, larger modules where safe)
- [ ] Dependencies between modules are minimal and explicit
- [ ] Output format is scannable and actionable for scaffolding

CONTEXT FILES: Base decomposition on Phase 1 discoveries
- requirements/business_requirements.md - Business logic complexity
- requirements/data_discovery.md - Data processing requirements  
- requirements/technical_assessment.md - System constraints
- [project-specific schema/data files as applicable]

TECHNICAL SPECIFICATIONS: Decomposition methodology
- Analyze data flow complexity and processing steps
- Group related functionality into cohesive modules
- Consider Claude Code generation limits (prefer 200-400 line modules)
- Design for testability and modularity
- Plan for common utilities and shared components
- Optimize for independent module development

DELIVERABLES: Module structure foundation
- design/module_structure.yaml - Complete module listing with classes and responsibilities
- design/architecture_rationale.md - Justification for each design decision

CONSTRAINTS & STANDARDS: Agentic development optimization
- Optimize for Claude Code generation patterns
- Ensure modules can be developed independently
- Design for clear testing boundaries
- Follow established framework patterns
- Consider Spark 3.5.x processing patterns"
```

#### Step 2B: Complete Architecture Design Prompt Template

```bash
claude "TASK: Design comprehensive solution architecture for [project_name] based on module decomposition.

CONTEXT FILES: Build on decomposition and requirements
- design/module_structure.yaml - Approved module boundaries
- design/architecture_rationale.md - Design decision context
- requirements/business_requirements.md - Business objectives and success criteria
- requirements/technical_assessment.md - Infrastructure constraints and capabilities
- requirements/data_discovery.md - Data sources, quality patterns, volumes
- meta/framework_evolution_guide.md - Architecture patterns and principles
- examples/reference_architectures/ - Proven architecture patterns

SUCCESS CRITERIA: Complete system design ready for implementation
- [ ] End-to-end architecture covers all business requirements
- [ ] Data flow diagrams show complete processing pipeline
- [ ] Technology stack selections justified with decision records
- [ ] Integration points and interfaces clearly defined
- [ ] Scalability and performance requirements addressed
- [ ] Security and compliance design integrated
- [ ] Implementation roadmap with module dependencies aligned to decomposition

TECHNICAL SPECIFICATIONS: Architecture design approach
- Apply established patterns from framework examples
- Design for Airflow orchestration, Spark 3.5.x processing, Iceberg storage
- Include data quality framework with Great Expectations
- Plan for monitoring, alerting, and observability
- Design API interfaces and data access patterns
- Consider disaster recovery and backup strategies
- Integrate module structure into overall system design

DELIVERABLES: Create Phase 2 design package
- design/architecture.md - System components, technology stack, integration patterns
- design/data_flows.md - Processing pipelines, data movement, transformation logic
- design/design_decisions.md - Architecture Decision Records with justifications
- design/implementation_plan.md - Module roadmap, dependencies, development sequence

CONSTRAINTS & STANDARDS: Follow architectural principles
- Align with enterprise architecture standards
- Ensure compatibility with existing systems
- Design for maintainability and operational excellence
- Include cost optimization considerations
- Follow security-by-design principles
- Plan for regulatory compliance requirements
- Maintain consistency with approved module decomposition"
```

### Phase 2 Workflow Notes

**Why Two Steps?**
- **Cognitive Load Management**: Solution decomposition requires different thinking than detailed design
- **Context File Creation**: Creates module_structure.yaml and architecture_rationale.md as inputs for Step 2B
- **Framework Integration**: Enables validation and iteration on module boundaries before detailed design
- **Agentic Optimization**: Ensures modules are sized and structured optimally for Claude Code generation

**Execution Sequence**:
1. Execute Step 2A to create module decomposition
2. Review and validate module structure with stakeholders
3. Execute Step 2B using decomposition as foundation context
4. Proceed to Phase 3 with complete design package

## Template Strengths vs. Weaknesses

✅ **Strengths (Evidence-based)**:
- Task-first structure aligns with documented best practices
- Hierarchical information flow follows Anthropic's recommended order
- Specific success criteria provide clear validation targets
- Context files prioritization leverages long context capabilities effectively
- Phase-specific templates ensure framework consistency

⚠ **Potential Weaknesses**:
- Length could overwhelm simple tasks - though the template includes usage notes for different complexity levels
- May be too prescriptive for creative tasks - better suited for structured development work
- Phase templates require framework knowledge to customize effectively

## Recommendation

The updated template is well-aligned with Anthropic's documented best practices and the Agentic Framework Pipelines v1.0 structure. The phase-specific prompts ensure:

- **Consistency**: Standardized approach across projects
- **Completeness**: Comprehensive requirements gathering and design
- **Traceability**: Clear connection between phases
- **Quality**: Built-in validation criteria and constraints
- **Framework Integration**: Aligned with project structure standards