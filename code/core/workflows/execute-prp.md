# Workflow: Execute PRP

Implement a feature from a validated PRP file.

## Usage examples

> [!quote] Examples of what the user may say:
> - Execute PRP XYZ
> - Implement PRP ABC

This must be run in a **fresh context**. Do not run in the same session as PRP creation.

## Steps

### 1. Read and internalise the PRP

Read the full PRP, you will find it under the `_AI/PRPs/` folder. Read the full PRP at the path provided. Do not begin implementation until you have read it completely. Pay particular attention to:
- Architecture notes and anti-patterns
- The implementation blueprint (step order matters)
- Validation gates

### 2. Re-read relevant context

Read `_AI/OVERVIEW.md` and any other files referenced in the PRP context section. Do not rely on training knowledge for project-specific patterns — read the actual files.

### 3. Implement in blueprint order

Work through the blueprint steps in sequence. Do not jump ahead.

For each step:
1. Make the change
2. Run the relevant validation gate (see below)
3. Fix any failures before moving to the next step

Never skip a validation gate. Never mark a step done while a gate is failing.

### 4. Validation gates

Run the gates at the points specified in the PRP. The validation commands for this project are defined in `_AI/VALIDATION.md`. Never skip a gate. Never mark a step done while a gate is failing.

### 5. When complete

Report:
- What was implemented (file-by-file summary)
- Which validation gates were run and passed
- Anything that deviated from the PRP blueprint, and why
- Any follow-up work that surfaced but is out of scope for this ticket
