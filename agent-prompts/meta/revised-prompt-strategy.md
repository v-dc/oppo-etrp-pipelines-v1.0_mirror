# Prompt Strategy Guide

## 1. TASK Section (Primary Instruction First)

**Design Decision**: Place the core task as a single, clear sentence at the very top.

**Sources & Reasoning**:
- AWS/Anthropic documentation specifies the recommended order: "Task context: Assign the LLM a role or persona and broadly define the task it is expected to perform" should come first
- Anthropic's "Be clear and direct" guide emphasizes: "The more precisely you explain what you want, the better Claude's response will be"
- Claude Code best practices show task-first examples: "migrate foo.py from React to Vue. When you are done, you MUST return the string OK" Claude 4 prompt engineering best practices - Anthropic

**Chain of Thought**: Claude Code is agentic, so it needs to understand the primary objective immediately. A scattered or buried task description leads to confused implementation.

**Typical Elements**: Primary objective, main deliverable, target outcome

## 2. SUCCESS CRITERIA Section (Measurable Outcomes)

**Design Decision**: Use checkboxes with specific, measurable behaviors before diving into technical details.

**Sources & Reasoning**:
- Anthropic's prompt engineering process emphasizes: "Define the task and success criteria: The first and most crucial step is to clearly define the specific task you want Claude to perform" Use prompt templates and variables - Anthropic
- Claude 4 best practices state: "Be specific about desired behavior: Consider describing exactly what you'd like to see in the output" Chain complex prompts for stronger performance - Anthropic

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
- Claude 4 best practices: "Being specific about your desired output can help enhance results" Chain complex prompts for stronger performance - Anthropic
- Claude Code examples demonstrate specific success indicators: "you MUST return the string OK if you succeeded, or FAIL if the task failed" Claude 4 prompt engineering best practices - Anthropic

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

### Selection Criteria:
- **High context dependency** → Context files early
- **Clear output requirements** → Deliverables early  
- **Complex validation needs** → Success criteria early
- **Greenfield project** → Technical specifications can come later
- **Legacy system work** → Context and constraints upfront

**Key Principle**: The optimal order maximizes Claude's understanding at each step, preventing backtracking and confusion. Consider what Claude needs to know first to avoid making incorrect assumptions.

## Template Strengths vs. Weaknesses

✅ **Strengths (Evidence-based)**:
- Task-first structure aligns with documented best practices
- Hierarchical information flow follows Anthropic's recommended order
- Specific success criteria provide clear validation targets
- Context files prioritization leverages long context capabilities effectively

⚠ **Potential Weaknesses**:
- Length could overwhelm simple tasks - though the template includes usage notes for different complexity levels
- May be too prescriptive for creative tasks - better suited for structured development work
- Doesn't include examples section - Claude 4 documentation notes that "examples align with the behaviors you want to encourage" Chain complex prompts for stronger performance - Anthropic

## Recommendation

The template is well-aligned with Anthropic's documented best practices for structured development tasks. For your PostgreSQL data loading script, this structure should work effectively because it:

- Matches complexity level: Multi-file, production system with specific data processing requirements
- Emphasizes context files: Critical for database schema and existing patterns
- Provides measurable success criteria: Important for data validation and recovery features
- Follows documented prompt structure: Task → Context → Specifications → Constraints