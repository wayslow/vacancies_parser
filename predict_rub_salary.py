def predict_rub_salary(payment_from, payment_to):
    if not not payment_from  and payment_from  and not not payment_to  and payment_to :
        return (payment_from + payment_to) / 2
    elif not not payment_from  and payment_from :
        return payment_from * 1.2
    elif not not payment_to  and payment_to :
        return payment_to * 0.8

