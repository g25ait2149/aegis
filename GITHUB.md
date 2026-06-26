# Run Aegis from GitHub (no Kaggle datasets)

Push this repo to GitHub once, then every notebook clones/pulls it on each run — so
refreshing all of P1–P4 becomes a single `git push` on your machine and a re-run on
Kaggle. No more dataset versions to juggle.

---

## 1. Publish the repo to GitHub (one time)

> ⚠️ **Push the UNZIPPED contents, not `Aegis_repo.zip`.** Git does not unzip — if the
> repo contains only the zip, a `git clone` on Kaggle just downloads that one file and
> there is no `aegis/` or `eval/` package to import (`ModuleNotFoundError: No module
> named 'eval'`). First **unzip** `Aegis_repo.zip`, then publish the folder that contains
> `aegis/`, `eval/`, `notebooks/` — the repo's top level must show those folders, **not** a `.zip`.

**Option A — GitHub website (no git CLI):**
1. Create a new repo at https://github.com/new — name it `aegis`, Public (simplest), **don't** add a README (this repo has one).
2. On the empty repo page click **uploading an existing file**, then drag in the **contents** of this folder (the `aegis/`, `eval/`, `notebooks/`, `docs/` folders + `README.md` etc. — i.e. the folder that contains `aegis/__init__.py` one level down).
3. **Commit**.

**Option B — git CLI:**
```bash
cd aegis                                   # the folder containing aegis/  eval/  notebooks/
git init -b main                           # older git: git init && git branch -M main
git add -A
git commit -m "Aegis P1-P4"
git remote add origin https://github.com/YOUR_USERNAME/aegis.git
git push -u origin main
```

> The big binaries (trained guard adapter, joblib, zips) are excluded via `.gitignore`,
> so the repo stays small and code-only.

---

## 2. Point each Kaggle notebook at GitHub

In **each** of your four notebooks, replace the dataset-finder setup cell with the
clone-setup cell (also saved at `notebooks/_github_setup_cell.py`). Set `REPO_URL` once:

```python
import sys, os, glob, subprocess
REPO_URL = "https://github.com/YOUR_USERNAME/aegis.git"     # <-- set this
DEST = "/kaggle/working/aegis_src"
if os.path.isdir(os.path.join(DEST, ".git")):
    subprocess.run(["git", "-C", DEST, "pull", "--ff-only"], check=False)
else:
    subprocess.run(["git", "clone", "--depth", "1", REPO_URL, DEST], check=False)
hits = glob.glob(DEST + "/**/aegis/__init__.py", recursive=True)
root = os.path.dirname(os.path.dirname(hits[0])) if hits else DEST
sys.path.insert(0, root)
for m in [m for m in sys.modules if m == "aegis" or m.startswith(("aegis.", "eval"))]:
    del sys.modules[m]
!pip -q install datasets transformers torch peft bitsandbytes accelerate sentence-transformers wandb langdetect 2>/dev/null
print("aegis repo at:", root)
```

Then **remove the old `aegis_pX_repo` dataset input** from each notebook (Input panel),
and turn **Settings → Internet: ON** (required for `git clone`). You can delete the four
per-phase datasets afterwards.

---

## 3. The new workflow

- **Edit code** → `git push` (or upload via the website).
- **In Kaggle** → just **Run All**. The setup cell `git pull`s the latest and reloads it.
- All four notebooks stay in sync automatically — there is nothing to update per-notebook.

**Private repo?** Add a GitHub **Personal Access Token** (repo scope) as a Kaggle Secret
named `GITHUB_TOKEN`, and build the URL with it:
```python
from kaggle_secrets import UserSecretsClient
REPO_URL = f"https://{UserSecretsClient().get_secret('GITHUB_TOKEN')}@github.com/YOUR_USERNAME/aegis.git"
```

**Pin a version for reproducibility?** Clone a tag/commit instead of latest:
`git clone --depth 1 --branch v0.4 REPO_URL DEST`.

---

## Windows — VS Code PowerShell (publish to `g25ait2149`)

Open the unzipped repo folder in VS Code (the folder that contains `aegis\`, `eval\`, `notebooks\`).
**Terminal → New Terminal** (PowerShell), then run:

```powershell
# 0) one-time tools — skip any you already have, then RESTART the terminal so PATH updates
winget install --id Git.Git -e
winget install --id GitHub.cli -e

# 1) git identity (use the email on your GitHub account)
git config --global user.name  "U E Sai Pavan Vamshi Krishna"
git config --global user.email "you@example.com"

# 2) make sure you're in the repo root (contains aegis\  eval\  notebooks\)
cd "C:\path\to\aegis"

# 3) sign in to GitHub (opens a browser)
gh auth login            # choose: GitHub.com  ->  HTTPS  ->  Login with a web browser

# 4) init, commit, create the repo under g25ait2149, and push — one shot
git init -b main
git add -A
git commit -m "Aegis P1-P4: layered LLM jailbreak/prompt-injection defense"
gh repo create g25ait2149/aegis --public --source=. --remote=origin --push
```

Your clone URL is then **`https://github.com/g25ait2149/aegis.git`** — put that in each notebook's `REPO_URL`.

**Verify:**
```powershell
git remote -v
git log --oneline -1
Start-Process "https://github.com/g25ait2149/aegis"
```

**Without GitHub CLI** — create an empty repo at https://github.com/new (owner `g25ait2149`, name `aegis`), then:
```powershell
cd "C:\path\to\aegis"
git init -b main
git add -A
git commit -m "Aegis P1-P4"
git remote add origin 