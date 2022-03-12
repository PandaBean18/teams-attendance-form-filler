### Attendance form filler (ms forms)
Originally it was supposed to be a program where you could enter some basic details into the shell and it would do the rest for you.
However, due to reasons such as admin consent for reading channel messages and microsoft not having an API for their forms, it became impossible to 
do that. I did end up making something that works, but it is VERY personalized.

I have created a step by step guide on how you can do this too.

# Step 1: Azure AD
You will need to log in to [azure](https://portal.azure.com/#home) with your school id and then navigate to azure active directory. There, [register a new app](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredApps) with whatever
name you want. Then go to API permissions tab of your app and add these permissions. 

![image](https://user-images.githubusercontent.com/69561650/158028005-87bce29f-1054-4840-a5fc-60d5ae23fd7a.png)

## Authentication for graph API 
The code was taken from [Microsoft authentication library for python](https://github.com/AzureAD/microsoft-authentication-library-for-python) (this [example](https://github.com/AzureAD/microsoft-authentication-library-for-python/blob/dev/sample/username_password_sample.py) in particular

install microsoft authentication library using ```pip install msal```

Firstly, you will need to create a file called parameters.json with such format: 
```json
{
    "authority": "https://login.microsoftonline.com/organizations",
    "client_id": "your_client_id",
    "username": "your_username@your_tenant.com",
    "password": "This is a sample only. You better NOT persist your password.",
    "scope": ["Add all the permissions in the image seperated by comas"],
    "endpoint": "https://graph.microsoft.com/v1.0/me/messages"
}
```
Now you can copy the code from my [ms graph auth](https://github.com/PandaBean18/teams-attendance-form-filler/blob/main/ms_graph_auth.py) file or from [here](https://github.com/AzureAD/microsoft-authentication-library-for-python/blob/dev/sample/username_password_sample.py)

**Note:** The first time that you will try running this, the program will print a url and exit, you will need to go to the url and authorize your application. After you have            authorized it, you might get something that says 'something went wrong, no redirect url provided' (I dont remember this was a month ago.), it is alright and your app has        been authorized, there was just no redirect url (duh). 

# Step 2: Creating a flow with microsoft power automate
Create a flow that sends messages to your outlook account when a new message is added to the channel with [Ms power automate](https://powerautomate.microsoft.com) (use school acc lol)
You can use [this template](https://india.flow.microsoft.com/en-us/galleries/public/templates/4289ec53edec430b8b760234bcc87267/send-an-email-when-a-new-message-is-added-in-microsoft-teams/)

Now, everytime your teacher adds a message in a channel, you will receive a mail on outlook, the mail can then be fetched with the API. You **WILL** need to look through the 
data and figure out how to extract the form url. In my code I even added checks to make sure that the mail was from the correct teacher.

Once you have the form link with you, now we need to fill the form

# Step 3: Selenium
Since microsoft does not have an API for ms forms, we will need to use selenium for running an actual browser.
However, working with selenium can be a pain (it was for me) so i recommend following a tutorial. i used [this one for wsl](https://cloudbytes.dev/snippets/run-selenium-and-chrome-on-wsl2)

Once you have done that, you can copy the steps in [form filler](https://github.com/PandaBean18/teams-attendance-form-filler/blob/main/form_filler.py)
Basic idea is to directly try to open the form link, get redirected as we are not signed in, sign-in in 3 steps, get redirected back to the form, click on whatever option
you need to to mark yourself present, and then submit the form.

**Note:** The FormFiller class has a fav_option param, this is the option that you have to click to mark yourself present. If your teacher does something where you have to type your name
        then you can modify the code and use element.send_keys method of selenium to type.

# Step 4: Putting it all together
Now all you have to do is write a simple script that fetches the url using graph api, then fills the form with selenium. In my [main](https://github.com/PandaBean18/teams-attendance-form-filler/blob/main/main.py)
file, i have created a function to deal with this, and a while true loop so that it keeps running in the background

**Note:** ensure that you are only calling the function when needed, it would be unwise to spam the API and it will end up taking more processing than required. i have created
        my loop in a way so that it only checks for new mails when i know that teacher will upload the link, that too has a 10 second cool down to avoid spamming.
        
# Resources
[Microsoft azure AD usage](https://github.com/AzureAD/microsoft-authentication-library-for-python)

[Setting up selenium for wsl](https://cloudbytes.dev/snippets/run-selenium-and-chrome-on-wsl2)
