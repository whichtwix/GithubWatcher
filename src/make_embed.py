import discord

def MakeEmbed(json):
  embed = discord.Embed()
  user = json["actor"]["login"]
  userlink = f'https://github.com/{user}'
  repo = json["repo"]["name"]
  embed.set_thumbnail(url=json["actor"]["avatar_url"])
  embed.color = discord.Colour.from_str("#43f770")

  if json["type"] == "WatchEvent":
    embed.title = '' # so it isnt None on the length check and raises a error
    embed.description = f'[{user}]({userlink}) starred {repo}!'
  elif json["type"] == "IssueCommentEvent" and json["payload"]["action"] == "created":
    embed.url = json["payload"]["issue"]["html_url"]
    embed.title = f'{user} commented on {json["repo"]["name"]}#{json["payload"]["issue"]["number"]}'
    embed.description = json["payload"]["comment"]["body"]
  elif json["type"] == "IssuesEvent":
    link = json["payload"]["issue"]["html_url"]
    issue = f'{json["repo"]["name"]}#{json["payload"]["issue"]["number"]}'
    embed.url = link
    if json["payload"]["action"] == "opened":
      embed.title = f'{user} opened issue: {issue} {json["payload"]["issue"]["title"]}'
      embed.description = json["payload"]["issue"]["body"]
    elif json["payload"]["action"] == "closed":
      embed.title = f'{user} closed issue: {issue}'
      embed.description = f'reason: {json["payload"]["issue"]["state_reason"]}'
  elif json["type"] == "PullRequestEvent":
    link = json["payload"]["pull_request"]["html_url"]
    embed.url = link
    pr = f'{json["repo"]["name"]}#{json["payload"]["number"]}'
    if json["payload"]["action"] == "opened":
      embed.title = f'{user} opened pull request: {pr} {json["payload"]["pull_request"]["title"]}'
      embed.description = json["payload"]["pull_request"]["body"]
    elif json["payload"]["action"] == "closed":
      embed.title = f'{user} closed pull request: {pr}'
      embed.description = f'merged: {json["payload"]["pull_request"]["merged"]}'
  elif json["type"] == "ForkEvent":
     link = f'https://github.com/{json["payload"]["forkee"]["full_name"]}'
     embed.url = link
     embed.title = f'{user} forked {repo}'
     embed.description = '' # so it isnt None on the length check and raises a error
  elif json["type"] == "ReleaseEvent":
     link = json["payload"]["release"]["html_url"]
     embed.url = link
     embed.title = f'{user} published a release for {repo}: {json["payload"]["release"]["tag_name"]}'
     embed.description = json["payload"]["release"]["body"]
  elif json["type"] == "PushEvent":
     link = f'https://github.com/{repo}/compare/{json["payload"]["before"]}..{json["payload"]["head"]}'
     embed.url = link
     embed.title = f'{user} pushed {json["payload"]["size"]} commit(s) to {repo}'
     embed.description = ''
     for i in json["payload"]["commits"]:
       embed.description += f'[{i["sha"][0:6]}]({trimlink(i["url"])}) - {i["message"]} - {i["author"]["name"]} \n'
  else:
     return None

  if len(embed.description) > 4096:
    embed.description = "[body was too long, please visit the link]"

  if len(embed.title) > 256:
    embed.title = "[title was too long, click here]"
    
  return embed

def trimlink(api_link: str):
  link = api_link.replace("api.", "")
  link = link.replace("repos/", "")
  link = link.replace("commits", "commit")
  return link
