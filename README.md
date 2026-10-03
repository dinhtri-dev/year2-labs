# Year2 Labs

Year2 source archive by dinhtri-dev. Original workspace files are unchanged.

## Contents and status

embedded contains button/GPIO examples; diffusion uses a pretrained DDPM model; gui is a PySide6 login/UI prototype. GUI login is a local demonstration, not an authentication service. Slides are catalogued but excluded until authorship is confirmed.

## Run / inspect

GUI: python "gui/# main.py". Diffusion: python "diffusion/import os.py"; it downloads a model and runs generation, so this is not executed by archive QA. YEAR2_DATA_ROOT configures external data paths.

Install only this project's listed dependencies in a separate virtual environment. Model binaries, large datasets, private configuration and generated output are excluded. Check DATA_AND_MODELS.md when present.

## Archive validation

See ARCHIVE_STATUS.md and SECURITY_REVIEW.md for the exact publication scope, tests and remaining limitations. A successful source-archive check does not certify production deployment, firmware flashing, model accuracy or CAD geometry.

## Future work

The consolidated Google document records project-specific fixes, missing functions and suggested features. This commit focuses on reproducible archiving, not implementing that roadmap.

## Directory guide

- `diffusion`
- `embedded`
- `gui`

## Python environment

Use Python 3.12 on Windows, from the repository root:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

`constraints.txt` pins the complete dependency resolution checked by OSV. Training dependencies are separate when `training/requirements.txt` is present. No model training is performed by archive checks. Other operating systems need their own dependency resolution and audit.

## Tests actually run

Python source compiled without executing model training. 1 complete firmware targets compiled with PlatformIO (build only, never upload).
