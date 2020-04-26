from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#call flask constructor
#reference this file __name__
app = Flask(__name__)
#sqlalchemy lets us use any database we like
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

#database models
class BlogPost(db.Model):
	id = db.Column(db.Integer, primary_key=True) #unique
	title = db.Column(db.String(100), nullable=False) #required field
	content = db.Column(db.Text, nullable=False)
	author = db.Column(db.String(20), nullable=False, default='N/A')
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return 'Blog post' + str(self.id)


@app.route('/')
def index():
	return render_template('index.html')


#to delete:
#db.session.delete(BlogPost.query.get(<put id here>))
@app.route('/posts', methods=['GET', 'POST'])
def posts():
	#Q: where is this request coming from?
	#A: From import on top
	if(request.method == 'POST'):
		post_title = request.form['title']
		post_content = request.form['content']
		post_author = request.form['author']
		new_post = BlogPost(title=post_title, content=post_content, author=post_author)
		db.session.add(new_post)
		db.session.commit() #persist out of session
		return redirect('/posts')
	else: #if we are GETting
		all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
		return render_template('posts.html', posts = all_posts)

#if we get to this URL
#then use the id in the URL to delete the post with that id
@app.route('/posts/delete/<int:id>')
def delete(id):
	post = BlogPost.query.get_or_404(id)
	db.session.delete(post)
	db.session.commit()
	return redirect('/posts')



@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

	post = BlogPost.query.get_or_404(id)

	if(request.method == 'POST'):
		post.title = request.form['title']
		post.content = request.form['content']
		post.author = request.form['author']
		db.session.commit()
		return redirect('/posts')
	else:
		return render_template('edit.html', post=post)

#show errors if we are here
if __name__ == '__main__':
	app.run(debug=True)










