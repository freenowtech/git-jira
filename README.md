
![](out.gif)

# git-jira

A simple CLI to switch to git branches based on one's JIRA tickets, only supports Jira Cloud.

## Installation

```bash
brew tap freenowtech/cli
brew install freenowtech/cli/git-jira
```

Create a Personal Access Token (PAT) in **JIRA** as per [instruction](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/).

Add `$JIRA_USER`, `$JIRA_API_TOKEN` and `$JIRA_INSTANCE` to your favorite shell:

**Important**: `$JIRA_INSTANCE` needs to be pointed at the `atlassian.net` domain, for example `htts://x.atlassian.net`. 

```
echo -n 'export JIRA_USER=YOUR_USER' >> ~/.zshrc
echo -n 'export JIRA_API_TOKEN=YOUR_API_TOKEN' >> ~/.zshrc
echo -n 'export JIRA_INSTANCE=YOUR_INSTANCE' >> ~/.zshrc
source ~/.zshrc
```

## Usage

Run with `git-jira` or `git jira`.

### Prefixing behavior

1. **Default:** `feature/SUP-1344-bla`

2. `--no-prefix`  ➡️  `SUP-1344-bla`

3. `--prefix blubb` ➡️ `blubb/SUP-1344-bla`
