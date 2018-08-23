class Config(object):
	"""
	Common Configurations
	"""
	UPLOAD_FOLDER="/uploads"
	MAIL_SERVER='smtp.gmail.com'
	MAIL_PORT=465
	#MAIL_PORT=587
	MAIL_USERNAME="ccc"
	MAIL_PASSWORD="ccc"
	MAIL_USE_TLS=False
	MAIL_USE_SSL=True
	MAIL_DEFAULT_SENDER="gregoriusairlangga@gmail.com"

class DevelopmentConfig(Config):
	DEBUG=True
	SQLALCHEMY_ECHO=True
	SQLALCHEMY_TRACK_MODIFICATIONS=True

class ProductionConfig(Config):
	DEBUG=False

app_config={
	"development":DevelopmentConfig,
	"production":ProductionConfig
}
