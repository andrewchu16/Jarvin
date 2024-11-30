TRAIN_DATA = [
    # Repository Examples
    ("Merge pull requests for repoX.", {"entities": [(24, 30, "REPOSITORY")]}),
    ("Check the status of repoY.", {"entities": [(20, 26, "REPOSITORY")]}),
    ("Deploy changes to repoZ.", {"entities": [(18, 24, "REPOSITORY")]}),
    ("What's the status of repo123?", {"entities": [(21, 28, "REPOSITORY")]}),

    # Branch Examples
    ("Run tests on the main branch.", {"entities": [(17, 21, "BRANCH")]}),
    ("Switch to the develop branch.", {"entities": [(14, 21, "BRANCH")]}),
    ("Merge PRs into the feature/new-feature branch.", {"entities": [(19, 38, "BRANCH")]}),
    ("Merge PRs into the feature/new-feature branch.", {"entities": [(19, 38, "BRANCH")]}),
    ("Check the changes on the hotfix branch.", {"entities": [(25, 31, "BRANCH")]}),

    # Slack Examples
    ("Read Slack mentions from the #general channel.", {"entities": [(29, 37, "SLACK_CHANNEL")]}),
    ("Check the messages in the #development channel.", {"entities": [(26, 38, "SLACK_CHANNEL")]}),
    ("Are there any updates on #marketing?", {"entities": [(25, 35, "SLACK_CHANNEL")]}),
    ("Send a message to #team-leads.", {"entities": [(18, 29, "SLACK_CHANNEL")]}),

    # Pull Request Examples
    ("Merge the open pull requests for repoX.", {"entities": [(15, 28, "PULL_REQUEST"), (33, 39, "REPOSITORY")]}),
    ("Approve PR #123 on repoY.", {"entities": [(8, 15, "PULL_REQUEST"), (19, 25, "REPOSITORY")]}),
    ("Are there any PRs on repoZ?", {"entities": [(14, 17, "PULL_REQUEST"), (21, 26, "REPOSITORY")]}),
    ("Close all PRs for the hotfix branch.", {"entities": [(10, 13, "PULL_REQUEST"), (22, 28, "BRANCH")]}),
]
