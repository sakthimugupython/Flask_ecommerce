from __init__ import create_app

app = create_app()

if __name__ == '__main__':
    from extensions import db
    with app.app_context():
        db.create_all()
        print('Database tables created.')
    app.run(debug=True)
