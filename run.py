from app import app
import os

if __name__ == '__main__':
    # Flask-SQLAlchemy will use the DATABASE_URL environment variable loaded via python-dotenv to make the connection.
    
    # host=‘0.0.0.0’ makes the server accessible externally on the network (useful in some environments).
    # port=os.environ.get(‘PORT’, 5000) allows the environment (such as a production server) to set the port, but uses 5000 as the default if not set.
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=True)