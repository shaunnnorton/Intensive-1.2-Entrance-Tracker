let building_select = document.getElementById('BLD')
let date_select = document.getElementById('DTE')
let download_button = document.getElementById('DWN')
let next_button = document.getElementById('NXT')

if(date_select.style.display == 'none'){
   download_button.style.display = 'none'
   next_button.innerHTML = "Next"
}

building_select.addEventListener('change', function() {
    date_select.style.display = 'none'
    date_select.value = "None"
    download_button.style.display = 'none'
    next_button.textContent = "Next"
 })
 
 date_select.addEventListener('change', function() {
    download_button.style.display = 'initial'
 })