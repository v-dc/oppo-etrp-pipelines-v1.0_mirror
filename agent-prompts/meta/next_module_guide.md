# Next Module Development Guide

## Step 1: Close Current Module

### Update Progress Files
Ask Claude-Code:
```
Update these files to close the [current_module]:
- progress/module_status.yaml → mark [current_module] as completed
- context/system_context.yaml → add new tables/configs created
- progress/project_status.md → add what we learned
```

### Document Module Completion
Save executed prompt in: `progress/executed_prompts/YYYY-MM-DD_[module_name].md`

## Step 2: Plan Next Module

### Get Next Module Strategy
Ask Claude (chat):
```
Based on:
- progress/module_status.yaml (what's done)
- progress/phase4a_historical_plan.md (what's next)
- standards/prompt_engineering.md (how to prompt)

Create a Claude-Code prompt for the next module.
Include specific context files and clear success criteria.
```

## Step 3: Execute Next Module

### Human Review
- Check the prompt makes sense
- Verify context files exist
- Run the prompt with Claude-Code

### Track Execution
Document the prompt and results in `progress/executed_prompts/`

## Quick Checklist
- [ ] Current module complete
- [ ] Progress files updated
- [ ] Next prompt created and reviewed
- [ ] New module executed
- [ ] Results documented

## The Pattern
**Close → Plan → Execute → Document → Repeat**

Each module builds on the previous work and improves the framework.