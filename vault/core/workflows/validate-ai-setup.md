# Workflow: Validate AI Setup

Check that the AI layer is correctly installed in this vault.

## Usage

> "validate AI setup", "check AI setup", "is the AI layer installed correctly"

## Steps

1. Run from the root of the vault:

```bash
bash _AI/core/scripts/validate-ai-setup.sh
```

2. Present the output to the user as-is.

3. If any required checks fail, stop — do not proceed with other workflows until the setup is valid. Optional items (marked `!`) are safe to skip.
