from app import app

if __name__ == "__main__":
    # Render uses PORT environment variable
    import os
    port = int(os.environ.get('PORT', 5050))
    app.run(debug=False, host='0.0.0.0', port=port)