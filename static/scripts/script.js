
const btn = document.querySelector('.filter-button');
const filterDiv = document.querySelector('.filter-div');
const filterForm = document.getElementById('filzter-form');



function showFilter() {

    for (const clas of filterDiv.classList) {
       if (clas == 'd-none') {
        filterDiv.classList.remove('d-none')
        filterDiv.classList.add('d-flex')
       }
       if (clas == 'd-flex') {
        filterDiv.classList.remove('d-flex')
        filterDiv.classList.add('d-none')
       }
    }
    
}

btn.addEventListener('click', showFilter);


/*

function onSubmit(e) {
    e.preventDefault()
    console.log("SUbmitegg...")
    data = 
    url = '/all_products'
    fetch(url, {
        hearders: {
            'X-Requested-Width': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        },
        body: JSONStringfy(data)
    })
    
    .then(response=>response.json())
    .then(products => {
        console.log(products)
    })
}
filterForm.addEventListener('submit', onSubmit)
 */