from factory_app import create_app

app = create_app()


@app.route('/ping/')
def ping():
    return '200 ok'


if __name__ == '__main__':
    app.run()
