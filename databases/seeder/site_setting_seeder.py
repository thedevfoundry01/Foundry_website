from app.models.site_setting import SiteSetting
from app.extensions import db

def seed_site_settings():
    """Seed the database with predefined site settings."""
    settings = {
        "website_name": "FlaskBlog",
        "website_logo": "logo.png",
        "website_email": "contact@myawesomewebsite.com",
        "address": "123 Main Street, City, Country",
        "contact_number": "+1234567890",
        "facebook_link": "https://facebook.com/myawesomewebsite",
        "twitter_link": "https://twitter.com/myawesomewebsite",
        "instagram_link": "https://instagram.com/myawesomewebsite",
        "linkedin_link": "https://linkedin.com/company/myawesomewebsite"
    }
    
    for key, value in settings.items():
        existing_setting = SiteSetting.query.filter_by(key=key).first()
        if not existing_setting:
            setting = SiteSetting(key=key, value=value)
            db.session.add(setting)
    
    db.session.commit()
    print("Seeded site settings.")
