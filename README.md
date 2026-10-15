# Hands-on Python CI/CD with GitHub Actions and GitHub Pages

This is a tiny, **no-third-party-packages** Python application. You edit code in VS Code, push it to GitHub, watch CI test and build it, and watch CD publish it to a real website.

## Files

- `risk.py` — simple transaction classifier (business logic)
- `data/transactions.json` — sample input data
- `tests/test_risk.py` — automated unit tests
- `build_site.py` — generates `site/index.html` from the sample data
- `.github/workflows/ci-cd.yml` — GitHub Actions automation
- `.gitignore` — ignores Python caches and generated website files
- `requirements.txt` — no external dependencies

## 1. Open and run locally

1. Extract this folder and open it in VS Code (`File` → `Open Folder`).
2. Confirm VS Code has a working Python interpreter. Python 3.11+ is suitable.
3. Open `Terminal` → `New Terminal`, then run from the project root:

   ```powershell
   python -m unittest discover -s tests -v
   python build_site.py
   ```

   If Windows uses `py` for Python, replace `python` with `py`.
4. Open `site/index.html` in your browser (in File Explorer, double-click it). All four tests should pass, and the dashboard should appear.

## 2. Put the files into a GitHub repository

Recommended: use a new **public** GitHub repository named `ci-cd-python-demo` so GitHub Pages works on a GitHub Free account.

If your existing VS Code folder is already linked to an *empty* repository, copy all files from this demo folder into that repository's root, **including the hidden `.github` folder**, and skip creating another repo.

Otherwise, on GitHub create the new repo, then clone it using VS Code's `Git: Clone` or terminal:

```powershell
git clone https://github.com/YOUR_USERNAME/ci-cd-python-demo.git
cd ci-cd-python-demo
```

Copy the project files into this clone, with `.github/workflows/ci-cd.yml` in the repo root. Then:

```powershell
git add .
git commit -m "Add Python CI/CD demo"
git push -u origin main
```

If you created the repository with an initial README, clone it before copying to avoid conflicts. Verify your default branch is named `main`; otherwise rename it or adjust the workflow's branch conditions.

## 3. Turn on GitHub Pages

In the GitHub repository:

1. Select **Settings → Pages**.
2. Under **Build and deployment → Source**, select **GitHub Actions** (NOT 'Deploy from a branch').
3. Select **Actions**, then open **Python CI/CD Demo** to inspect the run. If the first run occurred before Pages was configured and deploy failed, choose **Re-run all jobs**, or push another commit.
4. On successful completion, follow the live site URL in the deployment or under **Settings → Pages**. Expected pattern: `https://YOUR_USERNAME.github.io/ci-cd-python-demo/`.

If Pages is missing or cannot be enabled, check repository visibility and plan. For GitHub Free, use a public repository. If Actions are restricted by repo/org settings, an administrator may need to enable them.

## 4. Observe CI versus CD

On a push to `main`, GitHub automatically executes:

1. `test-and-build` (CI): checkout code, install Python, run tests, build HTML, upload generated site.
2. `deploy` (CD): starts **only if** `test-and-build` succeeds and the run is on `main`. Publishes the site to GitHub Pages.

On pull requests to `main`, only `test-and-build` runs (no production deployment).

## 5. Experiment A: successful change

Edit `data/transactions.json` and append a new transaction inside the JSON array, ensuring the previous last entry has a comma:

```json
{"id": "TX005", "amount": 12000}
```

Or change the threshold in `risk.py` and update tests accordingly. Commit and push:

```powershell
git add .
git commit -m "Add another sample transaction"
git push
```

In **Actions**, the workflow should pass and the published website should show 5 transactions, with 3 High Risk and 2 Low Risk.

## 6. Experiment B: deliberately break CI

Temporarily change `THRESHOLD = 10_000` in `risk.py` to `THRESHOLD = 20_000`. Leave tests unchanged. The high-risk test for 15,000 will now fail, and GitHub will refuse to run the `deploy` job. Your previous website stays published.

To make it a proper branch + pull request exercise:

```powershell
git switch -c experiment/break-test
```

Make the threshold change, then:

```powershell
git add risk.py
git commit -m "Intentionally demonstrate failing CI"
git push -u origin experiment/break-test
```

On GitHub, open **Pull requests → New pull request**, choose base `main` and compare `experiment/break-test`, then create it. CI should show a red failed check. Do **not** merge this broken code.

Fix `risk.py` back to `THRESHOLD = 10_000` and push the fix to the same branch:

```powershell
git add risk.py
git commit -m "Fix failing test"
git push
```

CI should turn green on the PR. Merge the PR into `main` from GitHub. That triggers both CI and deployment to production. Delete the experiment branch if you like.

Note: The starter's `main` push deploys automatically; for strict approvals in a team, configure branch protections and environment reviewers where supported.

## 7. What the automation workflow means

In `.github/workflows/ci-cd.yml`:

- `on`: choose triggers (push, PR, manual).
- `jobs`: separate test/build and deploy jobs.
- `runs-on`: use a hosted Linux computer.
- `uses`: invoke a reusable GitHub Action.
- `run`: execute a command.
- `needs`: wait for the test/build job to pass before deploy.
- `if`: prevent PRs from deploying.
- `permissions`: grant the minimum token privileges necessary to publish.
- `environment`: associate the deployment with the `github-pages` environment.

Production teams add linters, security scans, artifact versioning, integration tests, approvals, rollback plans, and secrets management. The basic workflow here is intentionally small.

## Troubleshooting

- **Tests fail locally:** open a terminal at the repository root, not inside `tests/`.
- **Python not recognized:** use `py` on Windows or select your interpreter in VS Code.
- **No workflow in GitHub Actions:** make sure the hidden `.github/workflows/ci-cd.yml` was copied and pushed.
- **Deploy fails with Pages/404/Not Found:** enable **Settings → Pages → Source: GitHub Actions** and re-run.
- **Permissions error:** check repository Actions policy and make sure `pages: write` and `id-token: write` remain in the deploy job.
- **Site shows old data:** check latest Actions run and refresh the browser after deployment completes.

No API keys, cloud account, Docker, or additional libraries are needed for this tutorial.
