var phone = window.matchMedia('(min-width: 320px) and (max-width: 480px)');
var tablet = window.matchMedia('(min-width: 768px) and (max-width: 1024px)');
var landscape = window.matchMedia('(min-width: 500px) and (max-height: 600px)');

var mySideNav = document.getElementById("mySidenav");

if(phone.matches) {
  function openNav() {
    mySideNav.style.width = "100%";
  }
 } else if(tablet.matches) {
  function openNav() {
    mySideNav.style.width = "25%";
  }
 } else if(landscape.matches){
  function openNav() {
    mySideNav.style.width = "30%";
  }
 } else {
function openNav() {
  mySideNav.style.width = "15%";
  }
}
  function closeNav() {
    mySideNav.style.width = "0";
}