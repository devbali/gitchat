# Trendsetter University
Chatting based on git

## Dependencies
* Python version 3.0
* GitPython library, to install execute `pip install GitPython`
* An Internet Connection

## Instructions and Setup
* Clone the repository, make sure you satisfy the dependencies
* Make sure that you have SSH key passwords stored in keychain so git can be pulled and pushed automatically
* Run the `trendsetter.py` python file
* View desired chat in the `trendsetter.log` file
* Edit nicknames in `nicknames.json` to view desired names instead of user ids

## How to Use it
* Every user writes to their own `cache/[userid]` and pushes to a central repository
* This is how merge conflicts are avoided
* The `main.log` file is generated by the `main.py` file and it is completely unique to the user
* The `main.log` file can be deleted and regenerated after running the `regen.py` and then `main.py`
* Edit the `nicknames.json` file to add names for each user id, to have names displayed in `main.log` instead of user ids