# Discovery Templates for Claude Code

## Purpose
Standardized templates for Claude Code to document discoveries during module development.

## When to Use Templates

### Technology Guide Template
**Use when**: You discover technology-specific syntax, patterns, or common mistakes
**Location**: `context/technology/{technology}_{version}_{type}.md`

### Pattern Template  
**Use when**: You create reusable code that other modules can benefit from
**Location**: `patterns/{domain}_{purpose}_pattern.py`

### Integration Pattern Template
**Use when**: You discover how to integrate multiple technologies effectively
**Location**: `patterns/{tech1}_{tech2}_integration_pattern.py`

### Mistake Prevention Template
**Use when**: You encounter and solve common errors that others should avoid
**Location**: `context/technology/{technology}_{version}_mistakes.md`

---

## Technology Guide Template

```markdown
# {Technology} {Version} Guide

---
title: {Technology} {Version} Guide for Claude Code
purpose: Guide Claude Code to use {technology} correctly and efficiently
audience: [claude-code]
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
version: 1.0
related_files: [patterns/{related_pattern}.py, examples/{related_example}.py]
---

## Purpose
Guide Claude Code to use {technology} {version} correctly and avoid common mistakes.

## Summary
Brief 2-3 sentence overview of key points and why this guide matters.

## Key Changes from Previous Version
- **Change 1**: Description of what changed and impact
- **Change 2**: Description of what changed and impact
- **Breaking Change**: Any breaking changes that affect existing code

## Best Practices

### Practice 1: Descriptive Name
Explanation of the practice and why it's important.

**Example**:
```{language}
// Working code example showing the practice
function exampleFunction() {
    // Implementation following best practice
    return result;
}
```

### Practice 2: Descriptive Name
Explanation of the practice and why it's important.

**Example**:
```{language}
// Another working code example
```

## Common Mistakes to Avoid

### Mistake 1: Brief Description
**Problem**: What goes wrong when you do this
**Symptoms**: How to recognize this mistake
**Solution**: Correct approach with code example

```{language}
// ❌ Wrong way
function wrongApproach() {
    // Code that causes problems
}

// ✅ Correct way  
function correctApproach() {
    // Code that works properly
    return success;
}
```

### Mistake 2: Brief Description
**Problem**: What goes wrong
**Solution**: How to fix it

## CB-Core Integration
How this technology integrates with CB-Core framework patterns:
- Connection to existing patterns
- Configuration requirements
- Resource considerations

## Performance Notes
Any performance considerations specific to this technology version.

## References
- Official documentation links
- Related framework files
- Version migration guides
```

---

## Code Pattern Template

```python
"""
{Pattern Name} - CB-Core Framework Pattern

---
file: {filename}
purpose: {One sentence describing what this pattern solves}
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
version: 1.0
dependencies: [list, of, required, packages]
related: [other, pattern, files]
discovered_in: {module_name}
---

Purpose: What this pattern solves (detailed)
Usage: How to import and use this pattern
Dependencies: Required packages, configurations, or setup
Example: Brief usage example

Created by: Claude Code during {module_name} development
Date: {YYYY-MM-DD}
Framework Version: 1.0
"""

import logging
from typing import Dict, Any, Optional, Union
from pathlib import Path

class {PatternName}:
    """
    {Brief description of what this pattern does}
    
    This pattern was discovered during {module_name} development when
    {brief description of the problem this solves}.
    
    Args:
        config (Dict[str, Any]): Configuration parameters
        logger (Optional[logging.Logger]): Logger instance
        
    Example:
        >>> pattern = {PatternName}({"param": "value"})
        >>> result = pattern.execute()
        >>> print(result["success"])
        True
    """
    
    def __init__(self, config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        """Initialize the pattern with configuration."""
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate required configuration parameters."""
        required_params = ["param1", "param2"]  # Update with actual requirements
        for param in required_params:
            if param not in self.config:
                raise ValueError(f"Required parameter '{param}' missing from config")
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the pattern logic.
        
        Returns:
            Dict containing:
                - success (bool): Whether execution succeeded
                - data (Any): Result data if successful
                - error (str): Error message if failed
                
        Raises:
            {SpecificException}: When specific conditions occur
        """
        try:
            self.logger.info(f"Executing {self.__class__.__name__} pattern")
            
            # Main pattern logic here
            result = self._perform_main_logic()
            
            self.logger.info("Pattern execution completed successfully")
            return {
                "success": True,
                "data": result,
                "pattern": self.__class__.__name__
            }
            
        except Exception as e:
            self.logger.error(f"Pattern execution failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "pattern": self.__class__.__name__
            }
    
    def _perform_main_logic(self) -> Any:
        """
        Implement the core pattern logic.
        
        Returns:
            The result of the pattern execution
        """
        # Implement actual pattern logic here
        # This is where the pattern's value is delivered
        pass

# Utility functions related to this pattern
def helper_function(param: str) -> str:
    """
    Helper function for {PatternName}.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
    """
    return f"processed_{param}"

# Usage example and testing
if __name__ == "__main__":
    # Example usage
    config = {
        "param1": "value1",
        "param2": "value2"
    }
    
    pattern = {PatternName}(config)
    result = pattern.execute()
    
    print(f"Pattern execution result: {result}")
    
    # Simple test
    assert result["success"] == True
    print("Pattern test passed!")
```

---

## Integration Pattern Template

```python
"""
{Tech1} + {Tech2} Integration Pattern

---
file: {tech1}_{tech2}_integration_pattern.py
purpose: Integrate {tech1} and {tech2} effectively in CB-Core framework
created: {YYYY-MM-DD}
version: 1.0
dependencies: [{tech1}, {tech2}, logging]
discovered_in: {module_name}
---

Integration pattern for using {tech1} with {tech2} in CB-Core framework.

Discovered during {module_name} development when we needed to
{brief description of integration challenge solved}.
"""

import logging
from typing import Dict, Any, Optional
# Import technology-specific libraries
# import {tech1_library}
# import {tech2_library}

class {Tech1}{Tech2}Integration:
    """
    Manages integration between {Tech1} and {Tech2}.
    
    This pattern handles:
    - Connection management between technologies
    - Data format translation
    - Error handling across technology boundaries
    - Resource cleanup
    
    Example:
        >>> integration = {Tech1}{Tech2}Integration(config)
        >>> result = integration.process_data(data)
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.{tech1}_client = None
        self.{tech2}_client = None
    
    def connect(self) -> bool:
        """
        Establish connections to both technologies.
        
        Returns:
            True if both connections successful, False otherwise
        """
        try:
            # Initialize {tech1} connection
            self.{tech1}_client = self._init_{tech1}()
            
            # Initialize {tech2} connection  
            self.{tech2}_client = self._init_{tech2}()
            
            self.logger.info("Integration connections established")
            return True
            
        except Exception as e:
            self.logger.error(f"Integration connection failed: {e}")
            return False
    
    def _init_{tech1}(self):
        """Initialize {tech1} client."""
        # Technology-specific initialization
        pass
    
    def _init_{tech2}(self):
        """Initialize {tech2} client."""
        # Technology-specific initialization
        pass
    
    def process_data(self, data: Any) -> Dict[str, Any]:
        """
        Process data through both technologies.
        
        Args:
            data: Input data to process
            
        Returns:
            Processing results
        """
        try:
            # Step 1: Process with {tech1}
            {tech1}_result = self._process_with_{tech1}(data)
            
            # Step 2: Transform for {tech2}
            transformed_data = self._transform_data({tech1}_result)
            
            # Step 3: Process with {tech2}
            final_result = self._process_with_{tech2}(transformed_data)
            
            return {
                "success": True,
                "data": final_result,
                "{tech1}_result": {tech1}_result
            }
            
        except Exception as e:
            self.logger.error(f"Data processing failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _process_with_{tech1}(self, data: Any) -> Any:
        """Process data using {tech1}."""
        # {Tech1}-specific processing
        pass
    
    def _transform_data(self, data: Any) -> Any:
        """Transform data between {tech1} and {tech2} formats."""
        # Data transformation logic
        pass
    
    def _process_with_{tech2}(self, data: Any) -> Any:
        """Process data using {tech2}."""
        # {Tech2}-specific processing
        pass
    
    def cleanup(self) -> None:
        """Clean up connections and resources."""
        try:
            if self.{tech1}_client:
                self.{tech1}_client.close()
            if self.{tech2}_client:
                self.{tech2}_client.close()
            self.logger.info("Integration cleanup completed")
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")

# Usage example
if __name__ == "__main__":
    config = {
        "{tech1}_config": {},
        "{tech2}_config": {}
    }
    
    integration = {Tech1}{Tech2}Integration(config)
    
    if integration.connect():
        result = integration.process_data({"test": "data"})
        print(f"Integration result: {result}")
        integration.cleanup()
```

---

## Mistake Prevention Template

```markdown
# {Technology} {Version} Common Mistakes

---
title: {Technology} {Version} Common Mistakes and Prevention
purpose: Help Claude Code avoid frequent errors when using {technology}
audience: [claude-code]
created: {YYYY-MM-DD}
version: 1.0
related_files: [context/technology/{technology}_{version}_syntax.md]
---

## Purpose
Document common mistakes when using {technology} {version} and provide solutions.

## Summary
This guide addresses the most frequent errors encountered during {module_name} development.

## Critical Mistakes

### 1. {Mistake Category}: {Brief Description}

**Problem**: Detailed description of what goes wrong
**Symptoms**: How to recognize this mistake
- Error message patterns
- Unexpected behavior  
- Performance issues

**Root Cause**: Why this happens

**Solution**: Step-by-step fix
```{language}
// ❌ Wrong approach that causes the mistake
function problematicCode() {
    // Code that demonstrates the mistake
}

// ✅ Correct approach  
function correctCode() {
    // Code that avoids the mistake
    // Include comments explaining why this works
}
```

**Prevention**: How to avoid this mistake in the future
- Code review checklist items
- Automated checks to implement
- Pattern to follow

### 2. {Another Mistake Category}: {Brief Description}

[Follow same structure as above]

## Warning Signs

Watch for these indicators that suggest mistakes:
- Warning sign 1: Description
- Warning sign 2: Description  
- Warning sign 3: Description

## Quick Reference

### Before You Code Checklist
- [ ] Check item 1
- [ ] Check item 2
- [ ] Check item 3

### Code Review Checklist  
- [ ] Review item 1
- [ ] Review item 2
- [ ] Review item 3

## Related Patterns

These CB-Core patterns help avoid mistakes:
- `patterns/{pattern1}.py` - Prevents mistake type 1
- `patterns/{pattern2}.py` - Prevents mistake type 2

## Emergency Fixes

### If You Encounter Error X:
1. Step 1: Immediate action
2. Step 2: Diagnosis
3. Step 3: Resolution

### If You Encounter Error Y:
1. Step 1: Immediate action
2. Step 2: Diagnosis  
3. Step 3: Resolution
```

---

## Template Usage Instructions

### For Claude Code:

1. **Choose the appropriate template** based on what you discovered
2. **Copy the entire template** to the appropriate location
3. **Replace all placeholder text** (items in {braces})
4. **Fill in all sections** - don't leave empty sections
5. **Test any code examples** to ensure they work
6. **Update the framework changelog** with your addition

### Required Replacements:

**All Templates**:
- `{YYYY-MM-DD}` → Current date
- `{module_name}` → Name of module where discovered

**Technology Templates**:
- `{Technology}` → Technology name (e.g., "Airflow")
- `{Version}` → Version number (e.g., "3.0")
- `{language}` → Programming language for code blocks

**Pattern Templates**:
- `{PatternName}` → CamelCase pattern name
- `{filename}` → Actual filename
- `{domain}` → Domain area (e.g., "spark", "airflow")
- `{purpose}` → What the pattern accomplishes

### Quality Check Before Saving:
- [ ] All {placeholders} replaced
- [ ] Code examples tested and working
- [ ] Follows naming conventions
- [ ] Serves a clear, unique purpose
- [ ] References related files appropriately