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

# Mapping of ticket types to branch prefixes
TICKET_TYPE_TO_PREFIX = {
    "Story": "feature",
    "Bug": "bugfix",
    "Refactoring": "refactor"
}

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
        formatted_summary = re.sub(r"[^a-zA-Z0-9]+", ' ', formatted)
        formatted_branches.append({
            'summary': formatted_summary,
            'issuetype': issue['fields']['issuetype']  # Added to retrieve the ticket type
        })
    return formatted_branches[:MAX_RESULT]

def main(prefix: Annotated[str, typer.Option(help="Prefix that is being used for the new branch.")] = "feature",
         no_prefix: Annotated[bool, typer.Option("--no-prefix", help="Will not use a prefix")] = False,
         auto_branch_prefix: Annotated[bool, typer.Option("--auto-branch-prefix", help="Automatically determine branch prefix based on ticket type")] = False):
    """
    CLI to switch to git branches based on one's JIRA tickets.

    If --prefix is used, it will add a specific prefix to the branch (e.g. feature -> "feature/")
    --no-prefix will omit the default "feature/" prefix.
    --auto_branch_prefix will enable the ticket type to set the prefix: feature, bugfix, or refactor
    """
    tasks = load_branches()
    formatted_tasks = [f"{task['summary']}" for task in tasks]  # Display only the summary
    terminal_menu = TerminalMenu(formatted_tasks)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index is not None:
        selected_task = tasks[menu_entry_index]
        prefix = None if no_prefix else prefix
        if auto_branch_prefix:
            auto_prefix = TICKET_TYPE_TO_PREFIX.get(selected_task['issuetype']['name'], None)
            print(f"Ticket Type: {selected_task['issuetype']}")
            formatted_branch = format_branch(selected_task['summary'], auto_prefix)
        else:
            formatted_branch = format_branch(selected_task['summary'], prefix)
        print(f"Switching to branch: {formatted_branch}")
        process = subprocess.Popen(['git', 'switch', '-c', formatted_branch],
                                   stdout=subprocess.PIPE)
        process.communicate()
    else:
        print("No menu entry selected. Exiting.")


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
