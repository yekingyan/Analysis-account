from app import app
from models.bill import BILL


if __name__ == '__main__':
    with app.app_context():
        BILL.create_bill()
