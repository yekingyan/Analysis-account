from flask import (
    jsonify,
    render_template,
)


def template_or_json(request, template, data, **kwargs):
    if request.headers.get('Accept') == 'application/json':
        return jsonify(data)
    else:
        return render_template(template, data=data, **kwargs)
