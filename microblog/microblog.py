from app import app, db
from app.models import User, Post

#have augmented the run command to exclusively point to specific ip and port 
app.run(host="0.0.0.0", port=int("5000"), debug=True)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}