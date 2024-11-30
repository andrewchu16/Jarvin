from server import Server

def test_intent():
    server = Server()
    
    assert server.get_intent("What's the database status?") == "get_database_status"
    assert server.get_intent("Merge the PRs to main") == "merge_pr"
    assert server.get_intent("Read my slack mentions in #team-discussion") == "read_slack_mentions"
    assert server.get_intent("Run tests on main") == "run_tests"
    assert server.get_intent("Rebuild the project") == "rebuild_project"