from datetime import datetime
import re

class Receipt:
    category : str
    requestor : str
    amount : float
    date_purchase : datetime
    description : str
    submit_time : datetime
    image_url : str
    id : int
    
    # TODO: more input validation might be needed. Check best practices for type annotation, kinda messy
    def __init__(self, category : str, requestor : str, amount, date_purchase, description : str, submit_time : datetime, image_url = None, id = None):
        self.category = category 
        self.requestor = requestor
        self.description = description

        #TODO: Check for non num or decimal point
        if isinstance(amount, str):
            amount = re.sub(r',', "", amount)
            self.amount = round(float(amount), ndigits = 2)
        else:
            self.amount = amount

        #TODO: Check for date format
        if isinstance(date_purchase, str):
            # If it's a string, convert to datetime object
            self.date_purchase = datetime.strptime(date_purchase, "%Y-%m-%d").date()
        else:
            self.date_purchase = date_purchase

        self.submit_time = submit_time
        self.image_url = image_url
        self.id = id

    def toString(self):
        return f'{self.submit_time}: {self.requestor} requested ${self.amount} from {self.category} for {self.description}'