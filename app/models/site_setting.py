from app.extensions import db



class SiteSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)  # e.g., 'website_name', 'website_logo'
    value = db.Column(db.Text, nullable=True)  # Value of the setting

    def __repr__(self):
        return f"<SiteSetting {self.key}>"