# AsterixDB-CRUD

A basic Python CRUD application to interact with an AsterixDB database.

Python version 3.12.X

## Installation

Create venv

```bash
python -m venv venv
source venv/bin/activate
```

Install dependance

```bash
pip install -r requirements.txt
```

## Configuration

Create .env file and complete your information

```txt
DATABASE_HOST=localhost
DATABASE_PORT=19002
DATAVERSE=your_dataverse
```

**Note:**

- `DATABASE_HOST`: Your AsterixDB server address (e.g., localhost or an IP address)
- `DATABASE_PORT`: Your AsterixDB server port (must be a number, default: 19002)
- `DATAVERSE`: The name of the dataverse to use or create
