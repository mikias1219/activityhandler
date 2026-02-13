# Push LifeOS to GitHub

## Option 1: Use Personal Access Token (Recommended)

1. **Create a PAT**:
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Name: `lifeos-push`
   - Scopes: Check `repo` (includes all repo permissions) and `workflow`
   - Generate and **copy the token** (you won't see it again)

2. **Push using the token**:
   ```bash
   cd /home/mikias/Documents/test/lifeos
   git push https://YOUR_TOKEN@github.com/mikias1219/activityhandler.git main
   ```
   Replace `YOUR_TOKEN` with your actual token.

   Or set it as credential helper:
   ```bash
   git config credential.helper store
   git push -u activityhandler main
   # When prompted: username = mikias1219, password = YOUR_TOKEN
   ```

## Option 2: Use GitHub CLI (gh)

```bash
gh auth login
git push -u activityhandler main
```

## Option 3: Push without workflows first, then add them via web

If you want to push everything except workflows:

```bash
cd /home/mikias/Documents/test/lifeos
git rm --cached .github/workflows/*.yml
git commit -m "Temporarily remove workflows (will add via web)"
git push -u activityhandler main
```

Then add the workflow files via GitHub web UI (Settings → Actions → New workflow).

## After pushing

1. **Set up GitHub Secrets** (Settings → Secrets and variables → Actions):
   - `AZURE_CREDENTIALS`
   - `ACR_USERNAME`
   - `ACR_PASSWORD`
   - Optional: `APP_SECRET_KEY`

2. **Set Variables** (optional):
   - `AZURE_WEBAPP_NAME` (e.g. `lifeos-app-900038`)
   - `AZURE_RESOURCE_GROUP` (default: `lifeos-rg`)

3. **Verify**: Go to Actions tab - CI should run automatically on the next push.
