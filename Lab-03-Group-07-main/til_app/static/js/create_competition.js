var errorModal = document.getElementById("error");
var createmodal = document.getElementById("create");
function toggleModal(modal, isOpen) {
    if (isOpen) {
        modal.style.display = "block";
        document.body.style.overflow = "hidden"; 
        document.querySelector('.wrapper').classList.add('blur'); 
    } else {
        modal.style.display = "none";
        document.body.style.overflow = "auto"; 
        document.querySelector('.wrapper').classList.remove('blur'); 
    }
}

toggleModal(createmodal,true)

function validateForm(event) {

    const startDate = document.getElementById("start_date").value;
    const endDate = document.getElementById("end_date").value;
    const name = document.getElementById("name").value;
    const registrationFee = document.getElementById("registration_fee").value;
    const prizePool = document.getElementById("prize_pool").value;
    const image = document.getElementById("image");


    const errorMessage = document.getElementById("error-message");


    errorMessage.textContent = "";


    if (!name || !startDate || !endDate || !registrationFee || !prizePool) {
        errorMessage.textContent = "Please fill in all fields.";
        event.preventDefault();  
        return false;
    }


    if (image.files.length === 0) {
        errorMessage.textContent = "Please upload a competition image.";
        event.preventDefault();  
        return false;
    }


    if (new Date(endDate) < new Date(startDate)) {
        errorMessage.textContent = "End date cannot be earlier than start date.";
        event.preventDefault();  
        return false;
    }

    const xhr = new XMLHttpRequest();
    xhr.open('GET', `/til_app/check-competition-name/?name=${encodeURIComponent(name)}`, true); 
    xhr.onload = function() {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            if (response.exists) {
                errorMessage.textContent = "Competition name already exists.";
                return false;  
            } else {
         
                event.target.submit(); 
                return true
            }
        }
    };
    xhr.send();


    return false;
}
document.querySelectorAll('.close').forEach(function(closeButton) {
    closeButton.addEventListener('click', function() {
        toggleModal(signupModal, false);
   
        toggleModal(errorModal, false); 
    });
});
