from backend.app import create_app

app = create_app()

if __name__ == '__main__':
    # Run the server on port 5000 in debug mode for development
    app.run(host='0.0.0.0', port=5000, debug=True)
