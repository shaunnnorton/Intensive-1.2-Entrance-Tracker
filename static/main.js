let signin_button = document.getElementById('SIBUTTON')
let signin_form = document.getElementById('signin_form')


signin_form.style.display = 'none'
if(signin_button.value == 'Sign In'){
   signin_button.type = 'button'
   signin_button.addEventListener('click', function() {
   if(signin_form.style.display == 'none'){
      signin_form.style.display = 'initial'
   }else{
      signin_form.style.display = 'none'
   }
 
   })
}else if(signin_button.value == 'Sign Out'){
   signin_button.formaction = '/login'
   signin_button.type = 'submit'
}
