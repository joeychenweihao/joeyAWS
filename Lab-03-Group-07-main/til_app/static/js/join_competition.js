
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





document.addEventListener('DOMContentLoaded', function () {
    var errorModal = document.getElementById("error");
    var signupModal = document.getElementById("signupModal");
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

   
    document.querySelectorAll('.card').forEach(function(card) {
        card.addEventListener('click', function() {
            // var gameTitle = card.querySelector('figcaption').textContent; 
            var competitionDate = card.getAttribute('data-competition-date'); 
            var competitionPk = card.getAttribute('data-competition-pk');
            document.getElementById('competition-pk').value = competitionPk;
            const competitionNameInput = document.getElementById("competition-name");
            const competitionStartDateInput = document.getElementById("competition-start-date");
            
           
            var modalTitle = document.getElementById("modalTitle"); 
            var errormodalTitle = document.getElementById("errormodalTitle");
            
            const competitionName = card.getAttribute('data-competition-name');
            const competitionStartDate = card.getAttribute('data-competition-date');

            

            
            const today = new Date();
            const competitionDateObj = new Date(competitionDate);
            today.setHours(0, 0, 0, 0);

            console.log("click card");

            if (competitionDateObj < today) {
                
                errormodalTitle.textContent = "This competition has ended and cannot be joined.";
                toggleModal(errorModal, true); 
            } else if (!isUserLoggedIn) {
        
                errormodalTitle.textContent = "Please log in to join this competition.";
                toggleModal(errorModal, true); 
            }
            else {
             
                modalTitle.textContent = "Join " + competitionName;
                competitionNameInput.value = competitionName;
                competitionStartDateInput.value = competitionStartDate;
                toggleModal(signupModal, true); 
            }
        });
    });


    document.querySelectorAll('.close').forEach(function(closeButton) {
        closeButton.addEventListener('click', function() {
            toggleModal(signupModal, false); 
       
            toggleModal(errorModal, false); 
        });
    });


});



function validateForm() {
    var phoneField = document.getElementById("competitor-phone");
    var emailField = document.getElementById("competitor-email");
    var nameField = document.getElementById("competitor-name");
    var categoryField = document.getElementById("competition-category");
    var dateField = document.getElementById("competition-date");


    var phonePattern = /^\d{10,15}$/;
    if (!phonePattern.test(phoneField.value)) {
        alert("Please enter a valid phone number with 10 to 15 digits.");
        return false;
    }


    var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailPattern.test(emailField.value)) {
        alert("Please enter a valid email address.");
        return false;
    }


    var namePattern = /^[A-Za-z\s]+$/;
    if (!namePattern.test(nameField.value.trim())) {
        alert("Name can only contain letters and spaces.");
        return false;
    }


    if (categoryField.value === "") {
        alert("Please select a competition category.");
        return false;
    }

  
    if (dateField.value === "") {
        alert("Please select a competition date.");
        return false;
    }

    return true; 
}




