from data.connet_db import get_db


class BILL:

    create_bill_text = """
        CREATE TABLE IF NOT EXISTS `bills`(
            `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `create_time` DATETIME NOT NULL, -- 添加时间
            `pay_date` DATE NOT NULL, -- 付款时间
            `transaction_type` TEXT NOT NULL, -- 交易类型
            `transaction_item` TEXT, -- 交易项目
            `amount` DECIMAL(7, 3) NOT NULL, -- 金额
            `payment` TEXT NOT NULL, -- 支付方式
            `pay_type` TEXT NOT NULL, -- 支付类型
            `need` INTEGER NOT NULL -- 需要程度
)"""
    columns = ['id', 'create_time', 'pay_date', 'transaction_type', 'transaction_item', 'amount', 'payment', 'pay_type', 'need']

    @staticmethod
    def create_bill():
        get_db().execute(BILL.create_bill_text)


