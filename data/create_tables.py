import os
from models.bill import BILL
from app import app

if __name__ == '__main__':
    with app.app_context():
        # 运行时路径与app.py保持一致
        os.chdir('..')
        BILL.create_bill()
