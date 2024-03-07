
window.addEventListener("DOMContentLoaded", (event) => {
  let tlacitko = document.getElementById('succes_wrapper');
  if (tlacitko) {
    tlacitko.addEventListener('click', akce);
  }

});


function akce() {
  let tlacitko = document.getElementById('succes_wrapper')
  let hlaska = document.getElementsByClassName("succesmsg");
  tlacitko.style.display = "none";
  hlaska.style.display = "none";
}




