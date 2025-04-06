from home.main import main, once
from home.setup import Setup

if __name__=='__main__':
    setup = Setup(callback=once, config_path="/config.json",loop=main)
    setup.setup_all()
    setup.run_callback()
    setup.run_main_loop()
    
    