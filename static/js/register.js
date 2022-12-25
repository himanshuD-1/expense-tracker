const usernameField = document.querySelector('#userField');
const feedbackArea = document.querySelector('.invalid_feedback');
const emailField = document.querySelector('#emailField');
const emailFeedbackArea = document.querySelector('.email_feedback');
const userOutputSuccess = document.querySelector('.userOutputSuccess');
const passwordField = document.querySelector('#passwordField');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const submitButton = document.querySelector('.submit-btn');


const handleToggleInput = (e) =>{
    if(showPasswordToggle.textContent == "Show"){
        showPasswordToggle.textContent = "Hide";
        passwordField.setAttribute("type", "text");
    }
    else{
        showPasswordToggle.textContent = "Show";
        passwordField.setAttribute("type", "password");
    }
}

showPasswordToggle.addEventListener('click', handleToggleInput);



usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    console.log(usernameVal);
   
       
    
    usernameField.classList.remove('is-invalid');
    feedbackArea.style.display = "none";

    if (usernameVal.length > 0) {
        userOutputSuccess.style.display = "block";
        userOutputSuccess.textContent = `Checking ${usernameVal}`;   
        fetch('/authentication/validate-user/', {
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",

        }).then((res) => res.json()).then((data) => {
            userOutputSuccess.style.display = "none";
            if(data.username_error){
                submitButton.disabled = true;
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display = "block";
                feedbackArea.innerHTML = `<p>${data.username_error}</p>`;
            }
           
            else{
                submitButton.removeAttribute("disabled");
            }
        })
    }
});


emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;
    console.log(emailVal)
    
    emailField.classList.remove('is-invalid');
    emailFeedbackArea.style.display = "none";

    if (emailVal.length > 0) {
        fetch('/authentication/validate-email/', {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",

        }).then((res) => res.json()).then((data) => {
            if(data.email_error){
                submitButton.disabled = true;
                emailField.classList.add('is-invalid');
                emailFeedbackArea.style.display = "block";
                emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
            }
        
            else{
                submitButton.removeAttribute("disabled");
            }
        })
    }
});