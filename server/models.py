from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name.strip():
            raise ValueError("Author's name can't be empty string")
        # elif author and author.id !=self.id:
        elif Author.query.filter(Author.name==name).first():
            
            raise ValueError("Author's name must be unique")
        return name

    # author phone numbers are exactly 10 digits
    @validates('phone_number')
    def validate_number(self, key, phone_number):
        try:
            if len(phone_number) == 10:
                int(phone_number)
            else: 
                raise ValueError("number must be 10 digits")
        except (ValueError):
            raise ValueError("Number must be digits only")
                    # ValueError("Number must be 10 digits"))
        return phone_number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("content must be at least 250 characters")
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be less than 250 characters")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category == "Fiction" or category == "Non-Fiction":
            return category
        else:
            raise ValueError("Post category is either `Fiction` or `Non-Fiction`")
    
    @validates('title')
    def validate_title(self, key, title):
        word_present = False
        words = ["Won't Believe","Secret","Top","Guess"]
        for word in words:
            if word in title:
                word_present = True
        if word_present == False:
            raise ValueError("incorrect title, must be click-bait")
    


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
