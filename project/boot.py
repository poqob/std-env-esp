from home.main import main
from home.setup import Setup

def loop():
    pass


if __name__=='__main__':
    setup = Setup(callback=main, config_path="/config.json",loop=loop)
    setup.setup_all()
    setup.run_callback()
    
    