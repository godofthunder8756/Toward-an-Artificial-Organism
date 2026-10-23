# Preregistration materials

Prepared for Jonathan D Faeth, Independent Researcher. Not yet registered.

Read protocol.md for the scientific plan and registration-fields.md for submission text. The original exploratory reports are included for disclosure; their older designs do not override this protocol. The manifest hashes every included file except itself. No confirmatory study data are in this package.

## Reproduction

Tested on Windows, Python 3.14.0, CPU. Create an isolated Python environment, install requirements.txt, clone the upstream repository named in protocol.md, and check out its pinned commit. Install that checkout with `python -m pip install --no-deps -e PATH_TO_CHECKOUT`. Its reproduce.py applies the documented pymdp compatibility patch when imported. Keep the checkout clean.

Run a development preflight with `python main_study_runner.py --repo PATH_TO_CHECKOUT --out NEW_PREFLIGHT_FOLDER --mode preflight`. Analyze with `python analyze_main_study.py NEW_PREFLIGHT_FOLDER`. Preflight uses seed 301 and cannot be treated as confirmation.

After public registration is verified, create registration-record.json with the actual public HTTPS `url` and timezone-aware ISO `registered_utc` timestamp. Do not invent these values. Run `python main_study_runner.py --repo PATH_TO_CHECKOUT --out NEW_MAIN_FOLDER --mode main --registration registration-record.json`. Analyze the completed folder with `python analyze_main_study.py NEW_MAIN_FOLDER`. Identical invocation resumes checkpoints; it refuses to combine changed designs or environments. Keep the original attempts log.

The registration metadata gate checks format, not authenticity; independently verify the public record before running. Source and package checksums are recorded again in the run manifest. No paid API or cloud compute is required.
