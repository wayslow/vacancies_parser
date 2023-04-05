def predict_rub_salary(payment_from, payment_to):
    if payment_from != 0 and payment_from is not None and payment_to != 0 and payment_to is not None:
        return (payment_from + payment_to) / 2
    elif payment_from != 0 and payment_from is not None:
        return payment_from * 1.2
    elif payment_to != 0 and payment_to is not None:
        return payment_to * 0.8
