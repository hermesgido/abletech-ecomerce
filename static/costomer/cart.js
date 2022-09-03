
let timeValue = document.querySelector('#timesValue')
let totalAmount = document.querySelector('#total-amount')
var plusOrder = document.getElementsByClassName('plus-order')
var minusOrder = document.getElementsByClassName('minus-order')
var currentValue = document.getElementsByClassName('current-value')
 
for (var i = 0; i < plusOrder.length; i++) {
    plusOrder[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action  = this.dataset.action 
        if (user =="AnonymousUser") {
            console.log("User not login")
        }
        else{

            updateUserOrder (productId, action)
        }
    })
    
}


function updateUserOrder (productId, action) {
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'X-Requested-Width': 'XMLHttpRequest',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({'productId': productId, 'action':action })
    })
.then((response)=>{ 
    return response.json()
})

.then((data)=>{
    console.log('data:', data)
    location.reload()
})
}

/* 
for (var i = 0; i < minusOrder.length; i++) {
    minusOrder[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action  = this.dataset.action 
       
        if (user =="AnonymousUser") {
            console.log("User not login")
        }
        else{

            updateUserOrder (productId, action)
        }
    })
    
}

function updateUserOrder (productId, action) {
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({'productId': productId, 'action':action })
    })

.then((response)=>{ 
    return response.json()
})

.then((data)=>{
    console.log('data:', data)
    location.reload
    
})
}
 */