from quote_gen import create_app

# Function defined in __init__.py
app = create_app()

if __name__ == '__main__':
    print('launching app')
    app.run(debug=False)
