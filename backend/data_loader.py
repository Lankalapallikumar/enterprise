import pandas as pd

def load_all_data():
    workforce = pd.read_csv("data/workforce.csv")
    tasks = pd.read_csv("data/tasks.csv")
    tools = pd.read_csv("data/tools.csv")
    approvals = pd.read_csv("data/approvals.csv")

    return workforce, tasks, tools, approvals