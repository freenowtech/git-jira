#!/usr/bin/env python
import json
import os
import re
import subprocess
from urllib import request

import typer
from simple_term_menu import TerminalMenu
from typing_extensions import Annotated
from typing import Optional

MAX_RESULT = 5


def load_branches():
    instance = os.environ.get("JIRA_INSTANCE")
    token = os.environ.get("JIRA_PAT")
    if not instance:
        raise Exception("Please disclose your jira instance as $JIRA_INSTANCE")
    if not token:
        raise Exception("Please disclose your jira token as $JIRA_PAT")
    req = request.Request(
        instance + '/rest/api/2/search?'
        'jql=assignee=currentUser()+order+by+updated&fields=id,key,summary,issuetype,assignee',
        method="GET")
    req.add_header('Authorization', f'Bearer {token}')
    response = request.urlopen(req).read().decode('utf-8')
    response = json.loads(response)

    formatted_branches = []

    for issue in response['issues']:
        formatted = issue['key'] + " " + issue['fields']['summary']
        formatted_branches.append(re.sub(r"[^a-zA-Z0-9]+", ' ', formatted))
    return formatted_branches[:MAX_RESULT]


def main(prefix: Annotated[str, typer.Option(help="Prefix that is being used for the new branch.")] = "feature",
         no_prefix: Annotated[bool, typer.Option("--no-prefix", help="Will not use a prefix")] = False):
    """
   CLI to switch to git branches based on one's JIRA tickets.

   If --prefix is used, it will add a specific prefix to the branch (e.g. feature -> "feature/")
   --no-prefix will omit the default "feature/" prefix.
   """
    tasks = load_branches()
    terminal_menu = TerminalMenu(tasks)
    menu_entry_index = terminal_menu.show()
    selected_task = tasks[menu_entry_index]
    prefix = None if no_prefix else prefix
    formatted_branch = format_branch(selected_task, prefix)
    print(f"Switching to branch: {formatted_branch}")
    process = subprocess.Popen(['git', 'switch', '-c', formatted_branch],
                               stdout=subprocess.PIPE)
    process.communicate()


def format_branch(selected_task: str, prefix: Optional[str]):
    print(f"Using prefix: {prefix}")
    selected_task = re.sub(r'\s', '-',
                           selected_task).lower()
    jira_key = re.match(r'[A-Za-z]{2,}-\d+', selected_task).group()
    selected_task = selected_task.replace(jira_key, jira_key.upper())
    formatted_branch = (f"{prefix}/" if prefix else '') + selected_task
    return formatted_branch


if __name__ == "__main__":
    typer.run(main)
