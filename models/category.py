from config import db

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Use lazy='dynamic' for query evaluation only when accessed
    products = db.relationship('Product', backref='category', lazy=True)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }