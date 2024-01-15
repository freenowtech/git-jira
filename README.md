
![](out.gif)

## Installation

```bash
brew tap free-now/cli "git@gitlab.free-now.com:free-now/android/supply/core/homebrew-cli.git"
brew install free-now/cli/git-jira
```

Create a Personal Access Token (PAT) in **JIRA** (not Confluence ⚠️) as per [instruction](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html#UsingPersonalAccessTokens-CreatingPATsintheapplication).

Add `$JIRA_PAT` to your favorite shell:

```
echo -n 'export JIRA_PAT=YOUR_PAT' >> ~/.zshrc
source ~/.zshrc
```

## Usage

Run with `git-jira` or `git jira`.

### Prefixing behavior

1. **Default:** `feature/SUP-1344-bla`

2. `--no-prefix`  ➡️  `SUP-1344-bla`

3. `--prefix blubb` ➡️ `blubb/SUP-1344-bla`
