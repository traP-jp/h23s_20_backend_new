from os import getenv

GITHUB_API_KEY = getenv("GITHUB_API_KEY")


github_headers = {
    "Authorization": "Bearer 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",
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

github_url = "https://api.github.com/graphql",