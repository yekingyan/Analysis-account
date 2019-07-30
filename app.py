from factory_app import create_app, after_create_app

app = create_app()
after_create_app(app)


@app.route('/ping/')
def ping():
    return '200 ok'


if __name__ == '__main__':
    app.run(app.config['DEBUG'])
