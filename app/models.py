class hpr(db.Model):
    __tablename__ = 'hpr'
    objectid = db.Column(db.Integer, primary_key=True)
    propname = db.Column(db.String(64))
    resname = db.Column(db.String(64))
    address = db.Column(db.String(64))
    city = db.Column(db.String(64))
    
