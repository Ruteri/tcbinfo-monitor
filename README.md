## TCB Monitor

Automated intel tcbs tracker.  

Fetches all tcbs daily and compares against the previously seen.  
Diffs are automatically pushed to `diffs/` and compiled into `index.hmtl`.  

Hosted on [ruteri.github.io/tcbinfo-monitor](https://ruteri.github.io/tcbinfo-monitor/)!

### Deep Links

Use the `?fmspc=` URL parameter to link directly to a specific FMSPC search, e.g.:
`https://ruteri.github.io/tcbinfo-monitor/?fmspc=00A06D080000`

### Slack Notifications

You can get Slack alerts when specific FMSPCs are updated. Configure two GitHub Actions secrets in your repo:

- **`SLACK_WEBHOOK_URL`** — a Slack [incoming webhook](https://api.slack.com/messaging/webhooks) URL (`https://hooks.slack.com/services/T.../B.../xxx`)
- **`WATCHED_FMSPCS`** — comma-separated FMSPC list to watch, e.g. `00A06D080000,00906ED10000`

When the daily workflow detects changes to any watched FMSPC, a Slack message is sent with deep links to the affected entries. If the secrets are not set the notification step is silently skipped.

### Signing automated commits

The daily workflow uses
[verified-bot-commit](https://github.com/IAreKyleW00t/verified-bot-commit)
to create GitHub-signed, verified commits as `github-actions[bot]` through the
GitHub API. The action is pinned to the full commit SHA for v2.3.6 and commits
only `tcbs.json`, `index.html`, and files under `diffs/` to `main`.

It uses the automatically provided `GITHUB_TOKEN` with job-level
`contents: write` permission. No machine account, private signing key, additional
secrets, or bot identity variables are needed. The action creates the commit and
updates the remote branch, replacing the manual `git commit` and `git push` steps.

After enabling the workflow, verify that its next update succeeds and the commit
shows **Verified** on GitHub. Other branch restrictions still apply. Pages deployment
and Slack notifications require separate configuration; commits made with
`GITHUB_TOKEN` do not trigger ordinary push workflows or branch-based Pages builds.
