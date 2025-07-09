# Project Structure Standard v2.0

## Purpose
Standard template for creating new projects using the agentic development framework.

## Development Phases

### Phase 0: Framework Design (Pre-existing)
Framework governance documents maintained separately from projects.

### Phase 1: Discovery & Requirements  
Business requirements analysis, technical assessment, data profiling.

### Phase 2: Solution Design (Two-Step Process)
**Step 2A:** Module decomposition optimized for agentic development  
**Step 2B:** Complete architecture design, data modeling, security planning.

### Phase 3: Development Environment Setup
Project structure creation, configuration, and initial context.
Identify and include applicable initial examples and standards.

### Phase 4: Iterative Development
Module-by-module implementation using Claude Code.

## Standard Project Structure

```
project-root/
├── agent-prompts/                    # Agentic framework (separate IP)
│   ├── requirements/                 # [Phase 1] Requirements analysis
│   │   ├── business_requirements.md  # [Phase 1] Business objectives and success criteria
│   │   ├── technical_assessment.md   # [Phase 1] Infrastructure and technical evaluation
│   │   └── data_discovery.md         # [Phase 1] Data profiling and source analysis
│   ├── design/                       # System design documents
│   │   ├── module_structure.yaml     # [Phase 2A] Module decomposition for agentic development
│   │   ├── architecture_rationale.md # [Phase 2A] Justification for module design decisions
│   │   ├── architecture.md           # [Phase 2B] System components and technology stack
│   │   ├── data_flows.md             # [Phase 2B] Data processing flows and diagrams
│   │   ├── design_decisions.md       # [Phase 2B] Architecture Decision Records
│   │   └── implementation_plan.md    # [Phase 2B] Complete system modules and implementation steps
│   ├── context/                      # Project context
│   │   ├── system_context.yaml       # [Phase 3] Machine-readable config
│   │   ├── data_context.md           # [Phase 3] Data specifications
│   │   └── technology/               # [Phase 3,4] Technology guidance
│   ├── meta/                         # [Phase 0] Framework governance
│   │   ├── framework_evolution_guide.md # [Phase 0] How Claude Code evolves framework
│   │   ├── revised_prompt_strategy.md   # [Phase 0] Prompt engineering guidelines
│   │   ├── context_file_standards.md    # [Phase 0] Documentation format standards
│   │   ├── discovery_templates.md       # [Phase 0] Templates for documenting discoveries
│   │   ├── framework_changelog.md       # [Phase 0] Framework change tracking
│   │   ├── module_closure_prompts.md    # [Phase 0] Human prompts for module closure
│   │   └── project_structure_standard.md # [Phase 0] Project creation template
│   ├── tasks/                        # [Phase 4] Module task specifications
│   ├── progress/                     # [Phase 4] Development tracking
│   │   ├── current_module_status.md  # Real-time module progress
│   │   ├── project_status.md         # Overall project status and learnings
│   │   ├── decisions_log.md          # Architecture decisions with evolution
│   │   ├── next_module_guide.md      # Human workflow for next module
│   │   └── executed_prompts/         # Audit trail of AI interactions
│   ├── examples/                     # [Phase 3] Code templates
│   └── standards/                    # [Phase 3] Development procedures
│       ├── development_patterns.md   # CB-Core specific patterns and conventions
│       └── [other standards files]
├── setup-scripts/                   # [Phase 3] Environment setup automation
├── configs/                         # [Phase 3] Application configuration files
├── src/                             # [Phase 4] Main codebase
│   └── common/                      # Shared utilities
├── great-expectations/              # [Phase 4] Quality framework
├── tests/                          # [Phase 4] Test suite
├── scripts/                        # [Phase 4] Utility scripts
└── logs/                           # [Phase 4] Application logs
```

## Files Required Before Phase 4 (Iterative Development)

### Phase 1 Completion:
- `requirements/business_requirements.md` - Business objectives and success criteria
- `requirements/technical_assessment.md` - Infrastructure and technical evaluation  
- `requirements/data_discovery.md` - Data profiling and source analysis

### Phase 2 Completion (Two-Step Process):

#### Step 2A: Solution Decomposition
- `design/module_structure.yaml` - Module decomposition optimized for agentic development
- `design/architecture_rationale.md` - Justification for module design decisions

#### Step 2B: Complete Architecture Design
- `design/architecture.md` - Complete system design
- `design/data_flows.md` - All data processing flows documented  
- `design/design_decisions.md` - Key architectural decisions recorded
- `design/implementation_plan.md` - Complete module roadmap

### Phase 3 Completion:
- `context/system_context.yaml` - Machine-readable project configuration
- `context/data_context.md` - Data specifications and processing requirements
- `meta/` - All framework governance documents (copied from Phase 0 template)
- `examples/` - Code templates for the technology stack
- `standards/` - Development procedures, quality guidelines, and core development patterns for Claude Code
- `setup-scripts/` - Environment automation ready
- `configs/` - Application configuration prepared

## Phase 4 File Creation (During Development)

### Created by Human Supervisor:
- `tasks/` initial specifications - First module task definitions
- `progress/executed_prompts/` - Audit trail of development

### Created by Claude Code (development):
- `context/technology/` - Technology-specific guidance (as discoveries made)
- `tasks/` - Module task specifications  
- `src/` - Implementation code
- `great-expectations/` - Quality validation setup
- `tests/` - Test suite
- `scripts/` - Utility scripts

### Created by Claude Code (module closure):
- `progress/current_module_status.md` - Module progress tracking
- `progress/project_status.md` - Project status updates and learnings
- `progress/decisions_log.md` - Architecture decisions and evolution

## Prompt Strategy Integration

The framework includes `meta/revised_prompt_strategy.md` which provides:

### Task Structure Guidelines:
1. **TASK** - Primary instruction first
2. **DELIVERABLES** - Concrete outputs with exact filenames
3. **SUCCESS CRITERIA** - Measurable outcomes with checkboxes
4. **CONTEXT FILES** - Dependencies before implementation
5. **TECHNICAL SPECIFICATIONS** - Implementation details
6. **CONSTRAINTS & STANDARDS** - Boundaries and quality requirements

### Phase 2 Two-Step Process:

#### Step 2A: Solution Decomposition Pattern
```bash
claude "TASK: Design module decomposition for [project_name] optimized for agentic code generation.
SUCCESS CRITERIA: Optimal module structure for Claude Code development
CONTEXT FILES: Phase 1 requirements, project-specific data sources
TECHNICAL SPECIFICATIONS: Decomposition methodology for 200-400 line modules
DELIVERABLES: design/module_structure.yaml, design/architecture_rationale.md
CONSTRAINTS: Agentic development optimization"
```

#### Step 2B: Complete Architecture Design Pattern
```bash
claude "TASK: Design comprehensive solution architecture for [project_name] based on module decomposition.
CONTEXT FILES: design/module_structure.yaml, design/architecture_rationale.md, Phase 1 requirements
SUCCESS CRITERIA: Complete system design ready for implementation
TECHNICAL SPECIFICATIONS: Architecture patterns, technology decisions
DELIVERABLES: design/architecture.md, design/data_flows.md, design/design_decisions.md, design/implementation_plan.md
CONSTRAINTS: Align with approved module decomposition"
```

### Standard Module Prompt Pattern:
```bash
claude-code "Create [module] as defined in agent-prompts/tasks/[module]/[task].md. 
Follow patterns from standards/development_patterns.md and use context/system_context.yaml"
```

### Context Files Always Include:
- `standards/development_patterns.md` - CB-Core specific patterns and conventions
- `context/system_context.yaml` - Technology stack and resource constraints  
- `context/data_context.md` - Data specifications and processing requirements
- `design/architecture.md` - System architecture and integration points
- `design/data_flows.md` - Processing pipeline patterns
- `design/module_structure.yaml` - Approved module boundaries

## Project Initialization Checklist

### Phase 1 Complete:
- [ ] `requirements/business_requirements.md` - Business objectives and success criteria
- [ ] `requirements/technical_assessment.md` - Infrastructure and technical evaluation
- [ ] `requirements/data_discovery.md` - Data profiling and source analysis

### Phase 2 Complete (Two-Step Process):

#### Step 2A Complete:
- [ ] `design/module_structure.yaml` - Module decomposition optimized for agentic development
- [ ] `design/architecture_rationale.md` - Justification for module design decisions

#### Step 2B Complete:
- [ ] `design/architecture.md` - Complete system design
- [ ] `design/data_flows.md` - All data processing flows documented  
- [ ] `design/design_decisions.md` - Key architectural decisions recorded
- [ ] `design/implementation_plan.md` - Complete module roadmap

### Phase 3 Complete:
- [ ] Project folder structure created
- [ ] `context/system_context.yaml` - Project-specific configuration
- [ ] `context/data_context.md` - Data specifications
- [ ] `meta/` - Framework governance documents copied
- [ ] `examples/` - Identify and add applicable code templates for the technology stack
- [ ] `standards/` - Development procedures, quality guidelines, and core development patterns for Claude Code
- [ ] `setup-scripts/` - Environment automation ready
- [ ] `configs/` - Application configuration prepared

### Ready for Phase 4:
- [ ] All required files in place
- [ ] Framework governance available
- [ ] Module decomposition validated and approved
- [ ] First module task specification ready
- [ ] Development environment prepared

## Usage Notes

### For New Projects:
1. Complete Phases 1-3 before any Claude Code engagement
2. Execute Phase 2 as two-step process: decomposition first, then complete architecture
3. Use prompt strategy guidelines for task creation
4. Copy latest framework documents for current best practices
5. Customize system_context.yaml and data_context.md for project specifics

### For Framework Evolution:
- Update meta documents in Phase 0 template
- Maintain backward compatibility for existing projects
- Version framework template for stable project creation

### Phase 2 Two-Step Benefits:
- **Cognitive Load Management**: Separates module thinking from implementation details
- **Context File Creation**: Creates module_structure.yaml for use in subsequent design steps
- **Framework Integration**: Enables validation of module boundaries before detailed design
- **Agentic Optimization**: Ensures modules are sized optimally for Claude Code generation (200-400 lines)

## Framework Template Location
Maintain latest framework template with all Phase 0 meta documents for copying to new projects.