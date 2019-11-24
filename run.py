#This is for starting up the server
from voting_system.VotingSystem import app


if __name__== "__main__":
    app.run(port=2222, debug=True)