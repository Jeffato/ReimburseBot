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
    
    # TODO: more input validation might be needed
    def __init__(self, category : str, requestor : str, amount : str, date_purchase : datetime, description : str, submit_time : datetime):
        self.category = category 
        self.requestor = requestor
        self.description = description

        #TODO: Check for non num or decimal point
        amount = re.sub(r',', "", amount)
        self.amount = round(float(amount), ndigits = 2)
        
        #TODO: Check for date format
        self.date_purchase = datetime.strptime(date_purchase, "%Y-%m-%d").date()  # Convert to date object
        self.submit_time = submit_time

    def toString(self):
        return f'{self.submit_time}: {self.requestor} requested ${self.amount} from {self.category} for {self.description}'