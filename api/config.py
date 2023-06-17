from os import getenv

GITHUB_API_KEY = getenv("GITHUB_API_KEY")


github_headers = {
    "Authorization": f"Bearer {GITHUB_API_KEY}",
}


github_query = """
query($userName:String!) {
  user(login: $userName){
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
  }
}
"""

github_url = "https://api.github.com/graphql"