# Module Closure Prompts for Humans

## Purpose
Exact prompts for humans to use with Claude Code at the end of each module to ensure proper framework updates.

## When to Use This Guide
- After Claude Code completes a module implementation
- Before starting the next module  
- When you need to close out a development session properly

---

## Step 1: Framework Discovery Update

### Prompt for Claude Code:
```
Based on the [MODULE_NAME] module you just completed, update the framework with your discoveries.

Follow the framework evolution process defined in meta/framework_evolution_guide.md:

1. **Validate module success**: Ensure all tests pass and module works correctly

2. **Technology Discoveries**: Review the module for any new API usage, syntax patterns, or solutions discovered for technologies used (Airflow, Spark, Great Expectations, etc.). Update or create appropriate technology guides when discoveries were made.

3. **System Updates**: Update context/system_context.yaml with any new database tables, services, or configuration components created.

4. **Framework Changelog**: Update the framework changelog with what technology guides were updated or created.

Please review the module implementation and identify what should be documented for future modules. Follow the established documentation standards from meta/framework_evolution_guide.md.
```

**Expected Output**: Claude Code will create/update technology guides, patterns, and changelog

---

## Step 2: Progress Tracking Update

### Prompt for Claude Code:
```
Update the project progress tracking files to close out the [MODULE_NAME] module:

1. **Module Status**: Update the module status tracking file to mark [MODULE_NAME] as completed with completion date and any important notes.

2. **System Context**: Update the system configuration file with any new components created during this module:
   - Database tables or schemas
   - Configuration files added  
   - New dependencies introduced
   - Infrastructure components

3. **Project Status**: Update the project status documentation with:
   - Lessons learned from this module
   - Current overall project status
   - Any blockers or issues identified
   - Key achievements and milestones reached

4. **Execution Documentation**: Create documentation in the executed prompts folder for this module including:
   - The prompts used for this module
   - What was delivered
   - Any challenges encountered
   - Framework improvements made

Make sure all updates accurately reflect the current state.
```

**Expected Output**: Updated tracking files and execution documentation

---

## Step 3: Quality Validation

### Prompt for Claude Code:
```
Perform a quality validation of the [MODULE_NAME] module completion:

1. **Success Criteria Review**: Check the original module task specification and confirm all success criteria are met. List any that are incomplete.

2. **Deliverables Check**: Verify all required deliverables were created and are in the correct locations.

3. **Integration Validation**: Confirm the module integrates properly with existing components and doesn't break previous functionality.

4. **Documentation Review**: Ensure all code includes proper documentation, error handling, and follows established patterns.

5. **Framework Compliance**: Verify the module follows the development standards and uses existing patterns appropriately.

Provide a summary of validation results and flag any issues that need attention before moving to the next module.
```

**Expected Output**: Quality validation report with any issues identified

---

## Step 4: Next Module Preparation

### Prompt for Claude Code:
```
Prepare for the next module development:

1. **Dependencies Analysis**: Based on the current phase plan, identify what the next logical module should be and what dependencies it has.

2. **Context Preparation**: Review what context files, patterns, and examples the next module will need. Identify any gaps in the framework that should be addressed.

3. **Integration Planning**: Consider how the next module will integrate with what we just completed and what interfaces or data flows need to be planned.

4. **Risk Assessment**: Identify potential challenges or blockers for the next module based on what you learned in this module.

Provide recommendations for the next module and any preparatory work needed.
```

**Expected Output**: Analysis and recommendations for next module

---

## Quick Reference Commands

### For Standard Module Completion:
```bash
# Step 1: Framework Updates
"Update framework with discoveries from [MODULE_NAME] module following the framework evolution guide"

# Step 2: Progress Tracking  
"Update progress tracking files to close [MODULE_NAME] module: module status, system context, project status, and create executed prompts documentation"

# Step 3: Quality Check
"Validate [MODULE_NAME] module completion against original success criteria and framework standards"

# Step 4: Next Module Prep
"Analyze next module requirements and prepare recommendations based on current progress"
```

### For Rushed Closure (Minimum Required):
```bash
# Essential Updates Only
"Update module status to mark [MODULE_NAME] complete, add key discoveries to framework changelog, and update system context with any new components created"
```

---

## Expected Timeframe

### Full Module Closure: **15-20 minutes**
- Step 1 (Framework Updates): 5-8 minutes
- Step 2 (Progress Tracking): 3-5 minutes  
- Step 3 (Quality Validation): 5-7 minutes
- Step 4 (Next Module Prep): 2-3 minutes

### Quick Closure: **5-8 minutes**
- Essential updates only
- Use when time is limited but framework integrity must be maintained

---

## Validation Checklist

After running the closure prompts, verify:

### Framework Updates:
- [ ] Technology discoveries documented in appropriate context files
- [ ] Reusable patterns added to patterns folder
- [ ] Framework changelog updated with discoveries
- [ ] All new files follow naming conventions

### Progress Tracking:
- [ ] Module marked complete in module status file
- [ ] System context reflects current state
- [ ] Lessons learned documented
- [ ] Execution prompt saved in executed prompts folder

### Quality Assurance:
- [ ] All success criteria met
- [ ] Integration validated
- [ ] Documentation complete
- [ ] Standards compliance verified

### Next Module Readiness:
- [ ] Dependencies identified
- [ ] Context gaps addressed
- [ ] Integration points planned
- [ ] Risks assessed

---

## Troubleshooting

### If Claude Code doesn't update framework files:
**Re-prompt with**: "Review the [MODULE_NAME] implementation and identify specific technology insights, code patterns, or process improvements that should be documented. Use the available templates to create appropriate documentation."

### If progress tracking is incomplete:
**Re-prompt with**: "Ensure all progress files accurately reflect the current state after [MODULE_NAME] completion. Check that module status, system context, and project status all contain current information."

### If validation finds issues:
**Address immediately**: Don't proceed to next module until validation issues are resolved. Use Claude Code to fix identified problems.

### If next module prep is unclear:
**Re-prompt with**: "Based on the overall project plan and what we just completed, provide specific recommendations for the next module including exact deliverables, dependencies, and integration requirements."

---

## Module Closure Success Indicators

You've successfully closed a module when:

1. **Framework is Enhanced**: New discoveries are documented and reusable
2. **Progress is Tracked**: Current state is accurately reflected in all tracking files
3. **Quality is Assured**: Module meets standards and integrates properly
4. **Next Steps are Clear**: You know exactly what to build next and how

**Remember**: Taking 15-20 minutes to properly close a module saves hours of confusion and rework later.