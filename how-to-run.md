# How To Run The Project

1. Ensure you have Python 3 installed. You can check with the following command:

    ```powershell
    python --version
    ```

    or if you're on a Unix system:

    ```bash
    python3 --version
    ```

2. Install the required packages by running the following command:

    ```bash
    pip install -r requirements.txt
    ```

## Running The Web Server

Run the following command to start the server:

```powershell
python run_app.py
```

or if you're on a Unix system:

```bash
python3 run_app.py
```

## Running The Test Suite

Run the following command to start run the unit tests:

```powershell
python -m unittest discover -s tests
```

or if you're on a Unix system:

```bash
python3 -m unittest discover -s tests
```
