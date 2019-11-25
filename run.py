# This is for starting up the server
from voting_system.VotingSystem import app

# set

if __name__ == "__main__":
    app.config.from_object("config.DevelopmentConfig")

    # Can use cfg files by psing as VOTINGSYS_SETTINGS=path/to/Config/file.cfg
    # overrides the the setting from the previous setting
    try:
        app.config.from_envvar('APP_CONFIG_FILE')
    except RuntimeError:
        pass
    except:
        pass
    app.run(port=2222)
