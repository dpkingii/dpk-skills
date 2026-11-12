# dpk-skills

Claude Code skills I use for planning features, explaining code and tracking job applications.

## Install in Claude Code

```sh
claude plugin marketplace add dpkingii/dpk-skills
claude plugin install dpk-workflow@dpk-skills
```

Restart Claude Code after installing. The plugin provides:

| Command | What it does |
| --- | --- |
| `/dpk-workflow:applied` | Log job applications to a Google Sheet from links or screenshots, skipping duplicates |
| `/dpk-workflow:apply` | Log an application with `applied`, then tailor a LaTeX resume to the posting and build the PDF |
| `/dpk-workflow:spec` | Interview you about an idea, skipping anything the code already answers, then write a spec to `.plans/` |
| `/dpk-workflow:explain` | Explain a technical idea, or clean up a confusing explanation, for a specific reader |

`spec` and `explain` work as is. `applied` is built around my own setup and needs the configuration below. `apply` also expects my resume folder at `~/Documents/resume`, with its rules in `agent/CONTEXT.md` and checks in `agent/build.sh`. More skills will be added over time.

## Setup

### applied

The skill talks to the sheet through a small Apps Script web app.

1. In your sheet, open Extensions → Apps Script and paste in `skills/applied/Code.gs.template`. Set `SHEET_NAME` to your tab and replace `__SECRET__` with a long random string.
2. Deploy it as a web app (execute as you, access for anyone) and copy the URL.
3. Save both in `~/.config/job-tracker/config.json`:

   ```json
   {"url": "https://script.google.com/macros/s/.../exec", "secret": "your-secret"}
   ```

The skill runs `tracker.py` from `~/.claude/skills/applied/`, so it expects the skill to live there.

## Developing

I keep this repo as the source of truth and symlink each skill into `~/.claude/skills/`, so edits apply right away:

```sh
ln -s "$PWD/skills/applied" ~/.claude/skills/applied
```

To add a skill, create `skills/<name>/SKILL.md`, symlink it the same way, and add a row to the table above.

## Validate locally

```sh
claude plugin validate --strict .claude-plugin/plugin.json
claude plugin validate --strict .claude-plugin/marketplace.json
claude plugin validate skills
```

## Credits

For UI skills, see [jakubkrehel/skills](https://github.com/jakubkrehel/skills). It covers interface polish, typography, color, layout and accessibility.

## License

[MIT](LICENSE)
