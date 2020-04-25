from flask import Flask, render_template

#call flask constructor
#reference this file __name__
app = Flask(__name__)

#temp data store
all_posts = [
	{
		'title': 'Post 1',
		'content': 'This is the content of post 1',
		'author': 'Vinay'
	},
	{
		'title': 'Post 2',
		'content': 'This is the content of post 2'
	}
]

@app.route('/')
def index():
	return render_template('index.html')



@app.route('/posts')
def posts():
	return render_template('posts.html', posts = all_posts)


#routes
#@ is a decorator
#whatever code follows route is run when we hit route
@app.route('/home/<string:name>')
def hello(name):
	return "Hello " + name

#this route only accepts GET requests
@app.route('/onlyget', methods=['GET'])
def get_req():
	return "You can only get this webpage."





#show errors if we are here
if __name__ == '__main__':
	app.run(debug=True)










