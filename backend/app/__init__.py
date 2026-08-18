from flask import Flask, jsonify

def create_app(config_name):
	app = Flask(__name__)

	@app.route("/api/health")
	def health():
		return jsonify({"status": "ok"})

	if config_name == "development":
		app.config["DATABASE_URL"] = "development database"
	
	elif config_name == "testing":
		app.config["DATABASE_URL"] = "testing database"
	
	elif config_name == "production":
		app.config["DATABASE_URL"] = "production database"
	else:
		raise ValueError("Invalid config_name")
	
	return app