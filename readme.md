# GithubWatcher

Ever thought it would be cool and/or wanted to get the activity of a repository but you were restricted due to having to ask the repository owner? Or perhaps it was already at its cap of 20 webhooks? Well heres githubwatcher. 

Githubwatcher is a discord bot that imitates github webhooks through the [github events api](https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28), bringing you issue, pull request, release, starring, committing, and forking events of the repository.

Your able to watch as many repositories as you want, potentially only limited by your github rate limit and how active the repositories are. Having a github token is highly prefered as it raises the limit to 5000 from 60 requests( and in fact only requests to the events api that return the http code 200 affect your limit)

# Setup

## Using a IDE such as Visual Studio:
1. To get started clone the repository or download the source zip file
2. In ```variables.env```: you will need to fill a valid discord bot token into 'TOKEN' and a github personal access token([fine grained](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#types-of-personal-access-tokens) is recomended) in 'git_token'

In ```main.py```:

3. In the ```on_ready``` function: initialize as many githubwatcher classes as wanted
4. In ```GithubWatcher.checkgithub``` function: fill in a channel id of a server the bot is in

5. A requirements.txt is provided, use pip to install dependencies
6. run ```py run main.py``` in cmd or powershell within the IDE



## Using replit

[replit.com](https://replit.com/) is another option, most useful being it is possible to keep the bot running even while your own device is off. 

1. create your own replit on your account or go to a existing bot if you have one
2. move/migrate the code from the downloaded zip or from this repository to your repl
3. do steps 2 to 4 above
4. click the ```run``` button, repl will handle the dependencies for you

# GithubWatcher vs normal webhooks

GithubWatcher is a little more limited than webhooks noting it cant alert about workflows, projects, or deployments. Neither is it full proof on posting every event that occurs, either because of being offline or some other reason. However I think its certainly a great alternative while its checking and hope that anyone that uses it feels as satisfied as I have with it. 

# License

The code is under the MIT license and you are able to modify it as you like