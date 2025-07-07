# Context File Standards

## Purpose
Ensure consistent format and quality across all context files in the agent-prompts framework.

## File Naming Conventions

### Technology Guides (`context/technology/`)
**Format**: `{technology}_{version}_{type}.md`
**Examples**:
- `airflow_3.0_syntax.md`
- `airflow_3.0_mistakes.md`
- `spark_3.5_optimization.md`
- `great_expectations_1.5_api.md`

**Type Suffixes**:
- `syntax` - Language or framework syntax guides
- `mistakes` - Common errors and prevention
- `optimization` - Performance and efficiency patterns
- `api` - API usage and changes
- `integration` - How to integrate with other tools

### Pattern Files (`patterns/`)
**Format**: `{domain}_{purpose}_pattern.py`
**Examples**:
- `spark_connection_pattern.py`
- `airflow_dag_pattern.py`
- `error_handling_pattern.py`
- `data_validation_pattern.py`

### Standards Files (`standards/`)
**Format**: `{domain}_{purpose}.md`
**Examples**:
- `error_handling.md`
- `code_quality.md`
- `testing_approach.md`
- `prompt_engineering.md`

## Required File Structure

### Technology Guide Template
```markdown
# {Technology} {Version} {Type}

## Purpose
One sentence describing what this guide enables Claude Code to do.

## Summary
Brief overview of key points (2-3 sentences).

## Key Changes from Previous Version
- **Change 1**: Description and impact
- **Change 2**: Description and impact

## Best Practices
### Practice Name
Description and rationale.

**Example**:
```{language}
// Working code example
```

## Common Mistakes to Avoid
### Mistake 1: Brief Description
**Problem**: What goes wrong
**Solution**: How to fix it
**Example**: Code showing correct approach

## Integration Notes
How this technology works with CB-Core framework patterns.

## References
- Links to official documentation
- Related framework files
```

### Pattern File Template
```python
"""
{Pattern Name} - CB-Core Framework Pattern

Purpose: What this pattern solves (one sentence)
Usage: How to import and use this pattern
Dependencies: Required packages or setup
Example: Brief usage example

Created by: Claude Code
Date: YYYY-MM-DD
Module: {module_name}
Framework Version: 1.0
"""

# Standard imports
import logging
from typing import Dict, Any, Optional

# Pattern implementation
class PatternTemplate:
    """
    Template class for CB-Core patterns.
    
    Args:
        config: Configuration dictionary
        logger: Optional logger instance
    """
    
    def __init__(self, config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the pattern.
        
        Returns:
            Result dictionary with success status and data
        """
        try:
            # Pattern logic here
            return {"success": True, "data": {}}
        except Exception as e:
            self.logger.error(f"Pattern execution failed: {e}")
            return {"success": False, "error": str(e)}

# Usage example
if __name__ == "__main__":
    # Example usage
    pattern = PatternTemplate({"param": "value"})
    result = pattern.execute()
    print(f"Pattern result: {result}")
```

### Standards File Template
```markdown
# {Domain} {Purpose}

## Purpose
What this standard defines and why it matters.

## Scope
What areas this standard covers.

## Standards

### Standard 1: Name
**Requirement**: What must be done
**Rationale**: Why this is important
**Example**: How to implement

### Standard 2: Name
**Requirement**: What must be done
**Rationale**: Why this is important
**Example**: How to implement

## Validation
How to check compliance with this standard.

## Exceptions
When it's acceptable to deviate from this standard.

## Related Files
- Links to related patterns, examples, or technology guides
```

## Content Quality Standards

### All Context Files Must:
- [ ] Have a clear, single purpose
- [ ] Include working code examples
- [ ] Explain "why" not just "what"
- [ ] Use consistent terminology
- [ ] Reference related framework files
- [ ] Be immediately actionable

### Technology Guides Must:
- [ ] Include version numbers in title and content
- [ ] Show before/after examples for changes
- [ ] List specific common mistakes with solutions
- [ ] Provide complete working code samples
- [ ] Include integration notes for CB-Core

### Pattern Files Must:
- [ ] Be self-contained and importable
- [ ] Include comprehensive docstrings
- [ ] Handle errors gracefully
- [ ] Follow PEP 8 style guidelines
- [ ] Include usage examples

### Standards Files Must:
- [ ] Define clear, measurable requirements
- [ ] Explain rationale for each standard
- [ ] Provide practical implementation guidance
- [ ] Include validation methods
- [ ] Address common exceptions

## File Metadata

### Required Header Information
All `.md` files should include:
```markdown
---
title: {File Title}
purpose: {One sentence purpose}
audience: [claude-code, human-developers, framework-maintenance]
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 1.0
related_files: [list, of, related, files]
---
```

### Pattern File Headers
All `.py` pattern files should include:
```python
"""
File: {filename}
Purpose: {One sentence purpose}
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Version: 1.0
Dependencies: [list, of, dependencies]
Related: [related, pattern, files]
"""
```

## Validation Checklist

Before adding any context file:
- [ ] Follows naming convention
- [ ] Uses appropriate template
- [ ] Includes required sections
- [ ] Has working code examples
- [ ] References related files
- [ ] Serves a clear purpose
- [ ] Doesn't duplicate existing content

## Update Process

### When Updating Existing Files:
1. **Update the metadata** - Change version and update date
2. **Document changes** - Add changelog section if major updates
3. **Verify examples** - Ensure all code examples still work
4. **Check references** - Update any references to changed content
5. **Test integration** - Verify changes don't break other files

### When Creating New Files:
1. **Check for duplicates** - Ensure unique purpose
2. **Use templates** - Follow appropriate template exactly
3. **Add to changelog** - Document in `meta/framework_changelog.md`
4. **Reference appropriately** - Link from related files

## Common Anti-Patterns to Avoid

### ❌ Don't:
- Create files that duplicate existing content
- Use vague or generic titles
- Include outdated code examples
- Mix multiple purposes in one file
- Create files without clear audience
- Skip the required template sections

### ✅ Do:
- Create focused, single-purpose files
- Use specific, descriptive titles
- Include current, working examples
- Follow templates exactly
- Define clear target audience
- Complete all template sections

## Framework Integration

### Cross-References
- Technology guides should reference relevant patterns
- Patterns should reference relevant standards
- Standards should reference implementation examples
- All files should link to related content

### Dependency Management
- Document all dependencies clearly
- Use relative references for framework files
- Avoid external dependencies where possible
- Version pin when external dependencies required