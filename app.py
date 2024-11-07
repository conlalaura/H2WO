from app import create_app  # function from __init__.py

app = create_app()  # Initialize the Flask application

if __name__ == "__main__":
    app.run(debug=True)
