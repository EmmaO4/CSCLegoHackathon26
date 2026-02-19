from flask import Flask, render_template, request, redirect, url_for, session
import msal
import uuid

app = Flask(__name__)

# will add scrt key, clientID, clientScrt, tenantID


AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/callback"
SCOPE = ["User.Read"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    session["state"] = str(uuid.uuid4())
    auth_url = _build_msal_app().get_authorization_request_url(
        SCOPE,
        state=session["state"],
        redirect_uri=url_for("callback", _external=True)
    )
    return redirect(auth_url)

@app.route(REDIRECT_PATH)
def callback():
    if request.args.get("state") != session.get("state"):
        return "State mismatch"

    code = request.args.get("code")
    result = _build_msal_app().acquire_token_by_authorization_code(
        code,
        scopes=SCOPE,
        redirect_uri=url_for("callback", _external=True)
    )

    if "id_token_claims" in result:
        session["user"] = result["id_token_claims"]
        return redirect("/dashboard")

    return "Login failed"

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return f"Welcome {session['user']['name']}"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

def _build_msal_app():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential= #scrt here
    )
if __name__ == "__main__":
    app.run(debug=True)