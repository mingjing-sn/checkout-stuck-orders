import requests
import json

def sapCall(worldpayId):
    print(worldpayId)
    url_Il = 'https://cbs-order-service.springernature.app/order?paymentCardAuthorizationReference=' + str(worldpayId)
    url_checkout = 'https://sprcom-checkout-orders.springernature.app/orders?worldpayID=' + str(worldpayId)
    response_IL = requests.get(url_Il)
    response_checkout = requests.get(url_checkout)
    context_Checkout = response_checkout.json()
    orderId = context_Checkout['id']
    print(orderId)
    if response_IL.status_code == 200:
        context = response_IL.json()
        sapOrderId = context[0]['salesOrderNumber']
        resaveWithSapOrderId(orderId, worldpayId, sapOrderId)
    else:
        url_checkout = 'https://sprcom-checkout.springernature.app/api/order/save/' + str(orderId)
        resaveCall = requests.post(url_checkout)
        print(resaveCall.status_code)

def fetchPaymentPendingOrders():
    res = []
    url = 'https://sprcom-checkout-orders.springernature.app/orders?state=paymentPending'
    response = requests.get(url)
    for order in response.json():
        res.append(order['id'])
    return res

def fetchSaveOrderInProgressOrders():
    res = []
    url = 'https://sprcom-checkout-orders.springernature.app/orders?state=saveOrderInProgress'
    response = requests.get(url)
    for i in response.json():
        res.append(i['paymentData']['worldpayId'])
    return res

def resaveWithSapOrderId(checkoutId, worldPayId, sapOrderId):
    url = 'https://sprcom-checkout.springernature.app/api/orders/manually'
    data = [{
        "checkoutId": str(checkoutId),
        "worldPayId": str(worldPayId),
        "sapOrderId": str(sapOrderId)}]
    headers = {'Content-type': 'application/json'}
    manuallyCall = requests.post(url, data=json.dumps(data), headers=headers)
    print(manuallyCall.status_code)

def resaveIndividual(checkoutId):
    url = 'https://sprcom-checkout.springernature.app/api/order/save/' + str(orderId)
    individualCall = requests.post(url)
    print(individualCall.status_code)


paymentPendingOrders = fetchPaymentPendingOrders()
print("PaymentPending List: => => => =>")
print(paymentPendingOrders)
for orderId in paymentPendingOrders:
    print(orderId)
    resaveIndividual(orderId)
    print("-------------------------------------------------------------------------------------")


print("-------------------------------------------------------------------------------------")

saveOrderInProgresslist = fetchSaveOrderInProgressOrders()
print("SaveOrderInProgress List:=> => => =>")
print(saveOrderInProgresslist)
for worldpayId in saveOrderInProgresslist:
    sapCall(worldpayId)


