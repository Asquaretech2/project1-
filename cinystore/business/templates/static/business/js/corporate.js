const businessNavbar = document.getElementById('corporate-business-navbar');
const businessNavbarHeading = document.getElementById('businessLogoNameDescription')
const businessNavbarSubHeading = document.getElementById('businessLogoSubDescription')

window.onscroll = () => {
    if (window.scrollY > 60) {
        businessNavbar.classList.add('business-nav-container-active');
        businessNavbarHeading.style.color = "black"
        businessNavbarSubHeading.style.color = "black"
    } else {
        businessNavbar.classList.remove('business-nav-container-active');
        businessNavbarHeading.classList.remove('logo-name-description-active')
        businessNavbarHeading.style.color = "white"
        businessNavbarSubHeading.style.color = "white"
    }
};


/*................connecting page ...................*/

function registerBtn() {
  document.getElementById("dotsLine1").style.color = "green";
  document.getElementById("number1").style.backgroundColor = "green";
}