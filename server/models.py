from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model):
    __tablename__ = 'customers'
    serialize_rules = ('-reviews.customer',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship('Review', back_populates='customer')

#     #  add an association proxy named items to get a list of items through the customer's reviews relationship.
    items = association_proxy('reviews', 'item',
                                 creator=lambda item_obj: Review(item=item_obj))

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'
    
  
class Item(db.Model):
    __tablename__ = 'items'
    serialize_rules = ('-reviews.item',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    reviews = db.relationship('Review', back_populates='item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model):
    __tablename__ = 'reviews'
    serialize_rules = ('-customer.review','item.reviews',)
    

    # id = db.column(db.Integer,primary_key=True)
    comment = db.Column(db.string)

    # a column named customer_id that is a foreign key to the 'customers' table.
    customer_id  = db.Column(db.Integer, db.ForeignKey('customers.id'))

    # a column named item_id that is a foreign key to the 'items' table.
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # a relationship named customer that establishes a relationship with the Customer model. Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Customer.
    customer = db.relationship('Customer', back_populates='reviews')
    # a relationship named item that establishes a relationship with the Item model. Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Item.
    item = db.relationship('Item', back_populates='reviews')

    

