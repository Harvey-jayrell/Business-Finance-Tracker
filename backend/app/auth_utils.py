from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt

def owner_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "owner":
            return jsonify({"error": "Owner access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

def permission_check(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in allowed_roles:
                return jsonify({"error": "Owner or Manager access required"}), 403
                
            return fn(*args, **kwargs)
        return wrapper
    return decorator