from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests

user_bp = Blueprint("user", __name__, template_folder="templates")

# =====================
# CONFIG
# =====================
BACKEND_API = "http://localhost:8000/api"

# =====================
# LOGIN
# =====================
@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    payload = {
        "email": email,
        "password": password
    }

    try:
        res = requests.post(f"{BACKEND_API}/auth/login", json=payload)
        data = res.json()

        if res.status_code != 200:
            flash(data.get("message", "Đăng nhập thất bại"), "error")
            return redirect(url_for("user.login"))

        # Lưu token vào session (frontend quản lý)
        session["access_token"] = data["access_token"]
        session["role"] = data.get("role")

        return redirect(url_for("user.profile"))

    except Exception:
        flash("Không kết nối được server", "error")
        return redirect(url_for("user.login"))

# =====================
# PROFILE
# =====================
@user_bp.route("/profile")
def profile():
    token = session.get("access_token")

    if not token:
        return redirect(url_for("user.login"))

    headers = {
        "Authorization": f"Bearer {token}"
    }

    res = requests.get(f"{BACKEND_API}/users/me", headers=headers)

    if res.status_code != 200:
        session.clear()
        return redirect(url_for("user.login"))

    user_data = res.json()

    return render_template("profile.html", user=user_data)

# =====================
# LOGOUT
# =====================
@user_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("user.login"))
