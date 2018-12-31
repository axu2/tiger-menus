const phone = window.matchMedia('(min-width: 320px) and (max-width: 480px)');
const tablet = window.matchMedia('(min-width: 768px) and (max-width: 1024px)');
const landscape = window.matchMedia('(min-width: 500px) and (max-height: 600px)');

if(phone.matches) {
  function openNav() {
    document.getElementById("mySidenav").style.width = "100%";
  }
 } else if(tablet.matches) {
  function openNav() {
    document.getElementById("mySidenav").style.width = "25%";
  }
 } else if(landscape.matches){
  function openNav() {
    document.getElementById("mySidenav").style.width = "30%";
  }
 } else {
function openNav() {
  document.getElementById("mySidenav").style.width = "15%";
  }
}
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";

}