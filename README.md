# GET_SCM_PULL_SAILPOINT


This code retrieves pull requests from a GitHub repository, formats the data, and sends it as an email summary.

# Dependencies
The following dependencies are required to run this code:

**requests**: To send HTTP requests to the GitHub API.

**datetime**: To manipulate dates and times.

**smtplib**: To establish an SMTP connection and send emails.

**email.mime.text**: To create the email message with MIME content.

You can install these dependencies using the following command:

**_pip install requests datetime smtplib_**



# Functions
This code defines several functions:

**get_pull_requests(repo_owner, repo_name, token)**
This function retrieves all pull requests from the given GitHub repository. It returns the JSON response containing pull request information.


**get_pull_request_details(pull_request, token)**
This function retrieves details of a specific pull request. The function returns the JSON response containing the pull request details.


**format_pr_details(pr, token)**
This function formats the details of a pull request into a readable format. It returns a formatted multi-line string containing the pull request details.


**format_data(repo_owner, repo_name, token)**
This function formats the pull request data for email. It composes the subject and body of the email and returns them as a tuple.


**send_email(sender, recipient, subject, body)**
This function sends an email with the pull request summary. 



# Usage
To use this code, you need to provide the required information and execute the code. Modify the following variables according to your needs:

**repo_owner**: The owner of the GitHub repository.

**repo_name**: The name of the GitHub repository.

**github_token**: Your GitHub token for authentication.

**email_sender**: The email address of the sender.

**email_recipient**: The email address of the recipient.

Once you have set the required variables, execute the code. It retrieves pull requests, formats the data, and sends an email with the pull request summary. If the execution is successful, it will display a success message. If any exceptions occur, it will print an error message.

**Make sure to install the required dependencies before running the code.**
