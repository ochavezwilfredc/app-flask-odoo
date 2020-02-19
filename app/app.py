from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from module.OdooFencri import Fencri

app = Flask(__name__)

CORS(app, resources={r"/odoo/*": {"origins": "*"}})
fe = Fencri()


# END POINTS
@app.route('/odoo/v1/authenticate', methods=['POST'])
def login():
    # limpiar la session
    if not request.json:
        abort(400)
    login_ = request.json.get('login') or request.json.get('username')
    password_ = request.json.get('password')
    rememberMe_ = request.json.get('rememberMe', True)

    if not login_ or not password_:
        abort(400)

    logindata = {
        'login': login_,
        'password': password_,
        'rememberMe': rememberMe_
    }
    user = fe.odoo.env['res.external.user']
    token = user.login(logindata)
    if token:
        return jsonify({
            "token_id": token['token_id']
        })
    else:
        return jsonify({
            "status": False,
            "message": "No se encuentra registrado!"
        })


@app.route('/odoo/v1/ludopaths/q/check', methods=['POST'])
def validation():
    if not request.json or not ('document' in request.json):
        abort(400)
    re_ = request.environ.get('HTTP_AUTHORIZATION', False)
    if re_:
        token_ = re_.split(' ')[1]
        if token_validate(token_):
            document = request.json.get('document')
            partner_ = fe.get_ludopata(document)
            if partner_:
                return jsonify({
                    "result": "found"
                })
            else:
                return jsonify({
                    "result": "not_found"
                })
        else:
            return jsonify({
                "state": False,
                "message": "Token incorrecto!"
            })

    else:
        return jsonify({
            "state": False,
            "message": "Verificar el tocken de acceso"
        })


def token_validate(token_):
    model = fe.odoo.env['utils.security.jwt']
    values = model.jwt_validate_access(token_)
    return values


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
