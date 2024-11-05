from app.app import create_app

"""
This script is the entry point used to launch the web app.
Run it with python to start the web app.
On most systems this can be done by running the following in a terminal
python run_app.py
Check out 'how-to-run.md' for more details
"""
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)