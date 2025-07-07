# Framework Evolution Guide

## How Claude Code Should Evolve This Framework

This guide instructs Claude Code on how to improve and extend the agent-prompts framework during development.

## Development Workflow

### During Module Development
1. **Check technology guides**: Review `context/technology/` for correct API usage and existing approaches
2. **Import existing functions**: Use functions from `src/common/` rather than recreating functionality
3. **Create shared utilities during development**: If functionality will be used by multiple modules, create it in `src/common/` during development
4. **Follow existing patterns**: Reference code examples in technology guides for implementation guidance

### During Framework Evolution (Module Closure - After Testing)
1. **Validate module success**: Ensure all tests pass and module works correctly
2. **Update technology guides when discoveries made**: If you discovered new API usage, syntax patterns, or solutions for a technology, update the relevant `context/technology/` file
3. **Create new technology guides when needed**: If you worked with a technology version not yet documented, create a new technology guide
4. **Update system context**: Add any new database tables, services, or configuration components to `context/system_context.yaml`
5. **Update framework changelog**: Record what technology guides were updated or created

## Core Principle
**Every module development should leave the framework better than you found it.**

## When to Update the Framework

### 1. Technology Discoveries
When you encounter:
- New syntax patterns (e.g., Airflow 3.0 vs 2.8)
- Common mistakes or errors
- Performance optimizations
- API changes in libraries

**Action**: Create or update files in `context/technology/`

### 2. Code Pattern Discoveries
When you create:
- Reusable code structures
- Error handling approaches
- Integration patterns
- Performance optimizations

**Action**: Add to `patterns/` folder with documentation

### 3. Process Improvements
When you identify:
- Better development workflows
- Prompt strategies that work well
- Quality assurance approaches
- Testing patterns

**Action**: Update `standards/` files or create new ones

## Documentation Standards

### Technology Guides (`context/technology/`)
**Naming**: `{technology}_{version}_{type}.md`
**Examples**:
- `airflow_3.0_syntax.md`
- `spark_3.5_optimization.md`
- `great_expectations_1.5_api.md`

**Required Sections**:
```markdown
# {Technology} {Version} Guide

## Purpose
Brief description of what this guide helps Claude Code achieve.

## Key Changes from Previous Version
- Change 1: Description
- Change 2: Description

## Common Mistakes to Avoid
- Mistake 1: What not to do and why
- Mistake 2: What not to do and why

## Best Practices
- Practice 1: What to do and example
- Practice 2: What to do and example

## Code Examples
[Working code examples]

## Integration with Framework
How this technology integrates with CB-Core patterns.
```

### Code Patterns (`patterns/`)
**Naming**: `{domain}_{purpose}_pattern.py`
**Examples**:
- `spark_connection_pattern.py`
- `error_handling_pattern.py`
- `data_validation_pattern.py`

**Required Documentation**:
```python
"""
{Pattern Name} - CB-Core Framework Pattern

Purpose: Brief description of what this pattern solves
Usage: How to use this pattern
Dependencies: What this pattern requires
Example: Simple usage example

Created by: Claude Code on YYYY-MM-DD
Module: {module_name}
"""
```

### Process Standards (`standards/`)
**Naming**: `{domain}_{purpose}.md`
**Examples**:
- `error_handling.md`
- `testing_approach.md`
- `integration_patterns.md`

## Framework Update Process

### During Module Development
1. **Use existing framework**: Check technology guides and import from `src/common/`
2. **Document discoveries immediately**: Note new technology patterns or approaches
3. **Follow established patterns**: Use existing utilities rather than creating new ones
4. **Create shared utilities**: If functionality will be used by multiple modules

### Required Updates After Each Module
1. **Technology Guides**: Update or create technology guides only when you made discoveries about API usage, syntax, or approaches
2. **System Context**: Update `context/system_context.yaml` with new components, tables, or services
3. **Framework Changelog**: Record what technology guides were updated/created and why

## Quality Standards

### All Framework Updates Must:
- [ ] Follow naming conventions
- [ ] Include working code examples
- [ ] Explain the "why" not just the "what"
- [ ] Reference related files
- [ ] Be immediately usable by future modules

### Technology Guides Must:
- [ ] Include version numbers
- [ ] Show before/after examples for changes
- [ ] List common mistakes with solutions
- [ ] Provide working code samples

### Code Patterns Must:
- [ ] Be self-contained and importable
- [ ] Include comprehensive docstrings
- [ ] Handle errors gracefully
- [ ] Follow CB-Core conventions

## Framework Changelog Updates

Every framework change should be logged in `meta/framework_changelog.md`:

```markdown
## YYYY-MM-DD - Module: {module_name}

### Added
- `context/technology/new_tech_guide.md` - Discovered new syntax patterns
- `patterns/new_pattern.py` - Reusable error handling approach

### Updated
- `context/system_context.yaml` - Added new database tables
- `standards/error_handling.md` - Enhanced with new patterns

### Discovered
- Technology finding 1
- Process improvement 2
```

## Integration Guidelines

### When Creating New Files
1. **Check existing files first** - Don't duplicate
2. **Use appropriate folder** - Follow folder purpose
3. **Reference related content** - Link to related files
4. **Update index files** - Keep documentation current

### When Updating Existing Files
1. **Preserve working examples** - Don't break existing patterns
2. **Add version notes** - Document what changed and when
3. **Update references** - Check files that reference updated content
4. **Test implications** - Ensure changes don't break other modules

## Framework Governance

### File Ownership
- **`meta/`**: Claude Code maintains with human oversight
- **`standards/`**: Human-defined, Claude Code can suggest updates
- **`patterns/`**: Claude Code creates and maintains
- **`context/technology/`**: Claude Code discovers and documents

### Quality Control
- All technology guides must include working examples
- All patterns must be tested in actual module development
- All process improvements must be validated across multiple modules

## Success Metrics

The framework evolution is successful when:
1. **Subsequent modules develop faster** due to reusable patterns
2. **Fewer repetitive mistakes** due to technology guides
3. **Consistent quality** due to established standards
4. **Knowledge preservation** across development cycles

## Remember
You are not just building modules - you are building a framework that makes future development better, faster, and more reliable.