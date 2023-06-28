import requests
import datetime
import smtplib
from email.mime.text import MIMEText

"""
    Use Case :
    Write python code that will use the GitHub API to retrieve a summary of all 
    opened, closed, and in draft pull requests in the last week for a given repository 
    and send a summary email to a configurable email address.
"""

def get_pull_requests(repo_owner, repo_name, token):
    """
    Retrieves all pull requests from the given repository.

    Args:
        repo_owner (str): Owner of the repository.
        repo_name (str): Name of the repository.
        token (str): GitHub access token.

    Returns:
        list: List of pull requests as JSON objects.
    """
    headers = {
        'Authorization': f'Token {token}',
        #'Accept': 'application/vnd.github.v3+json'
        'Accept': 'application/vnd.github+json'
    }

    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)

    params = {
        'state': 'all',
        'sort': 'created',
        'direction': 'desc',
        'since': last_week.isoformat()
    }

    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls'
    response = requests.get(url, headers=headers, params=params)

    response.raise_for_status()  # Raise an exception for non-2xx status codes

    return response.json()


def get_pull_request_details(pull_request, token):
    """
    Retrieves details of a specific pull request.

    Args:
        pull_request (dict): Pull request object.
        token (str): GitHub access token.

    Returns:
        dict: Pull request details as a JSON object.
    """
    headers = {
        'Authorization': f'Token {token}',
        'Accept': 'application/vnd.github+json'
    }

    url = pull_request['url']
    response = requests.get(url, headers=headers)

    response.raise_for_status()  # Raise an exception for non-2xx status codes

    return response.json()


def format_pr_details(pr, token):
    """
    Formats pull request details into a readable format.

    Args:
        pr (dict): Pull request object.
        token (str): GitHub access token.

    Returns:
        str: Formatted pull request details.
    """
    pr_details = get_pull_request_details(pr, token)

    pr_number = pr_details['number']
    pr_title = pr_details['title']
    pr_status = pr_details['state']
    pr_owner = pr_details['user']['login']
    pr_from_branch = pr_details['head']['ref']
    pr_to_branch = pr_details['base']['ref']

    commits_url = pr_details['commits_url'].replace('{/sha}', '')
    commits_response = requests.get(commits_url, headers={'Authorization': f'Token {token}'})
    commits_response.raise_for_status()  # Raise an exception for non-2xx status codes
    commits = commits_response.json()
    commit_messages = [commit['commit']['message'] for commit in commits]

    pr_link = pr_details['html_url']

    formatted_details = f'''
        PR #{pr_number}
        Title: {pr_title}
        Status: {pr_status}
        Owner: {pr_owner}
        PR Branches: {pr_from_branch} --> {pr_to_branch}
        PR Link: {pr_link}
        Commit Messages: {commit_messages}
    '''

    return formatted_details


def format_data(repo_owner, repo_name, token):
    """
    Formats the final data for email and returns email subject and body.

    Args:
        repo_owner (str): Owner of the repository.
        repo_name (str): Name of the repository.
        token (str): GitHub access token.

    Returns:
        tuple: Email subject and body.
    """
    pull_requests = get_pull_requests(repo_owner, repo_name, token)

    opened_prs = [pr for pr in pull_requests if pr['state'] == 'open' and not pr['draft']]
    closed_prs = [pr for pr in pull_requests if pr['state'] == 'closed']
    draft_prs = [pr for pr in pull_requests if pr['draft']]

    opened_pr_count = len(opened_prs)
    closed_pr_count = len(closed_prs)
    draft_pr_count = len(draft_prs)

    opened_pr_details = [format_pr_details(pr, token) for pr in opened_prs]
    closed_pr_details = [format_pr_details(pr, token) for pr in closed_prs]
    draft_pr_details = [format_pr_details(pr, token) for pr in draft_prs]

    subject = f'Pull Request Summary - {repo_owner}/{repo_name}'

    backslash_char = "\\"

    body = f'''
    Pull Request Summary - {repo_owner}/{repo_name}

    Last week's activity:
    - Opened PRs ({opened_pr_count}):
      {"-" * 100}
      {"{backslash_char}n".join(opened_pr_details)}

    - Closed PRs ({closed_pr_count}):
      {"-" * 100}
      {"{backslash_char}n".join(closed_pr_details)}

    - Draft PRs ({draft_pr_count}):
      {"-" * 100}
      {"{backslash_char}n".join(draft_pr_details)}

    Thank you,
    SailPoint DevOps Team
    '''

    return subject, body


def send_email(sender, recipient, subject, body):
    """
    Sends an email with the provided subject and body.

    Args:
        sender (str): Email sender address.
        recipient (str): Email recipient address.
        subject (str): Email subject.
        body (str): Email body.
    """
    message = MIMEText(body)

    message['Subject'] = subject
    message['From'] = sender
    message['To'] = recipient

    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = '**************'  # SMTP Server Username
    smtp_password = '**************'  # SMTP Server Password

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)
        

# Set repository owner, repository name, GitHub token, email sender, and email recipient
repo_owner = 'anshulc55'
repo_name = 'Data_Structure'
github_token = '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'
email_sender = 'anshulc55@gmail.com'
email_recipient = '***************'

try:
    pull_requests = format_data(repo_owner, repo_name, github_token)

    ## Just Printing the Email Subject and Email Content which sent via Sent Email Funcation
    print(pull_requests[0])
    print("****************")
    print(pull_requests[1])
    
    ## Commenting SendEmail Funcation due to unavailability of SMTP Server
    # send_email(email_sender, email_recipient, pull_requests[0], pull_requests[1])
    print('Email sent successfully!')
except Exception as e:
    print(f'Error: {str(e)}')
