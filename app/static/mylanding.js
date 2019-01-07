var phone = window.matchMedia('(min-width: 320px) and (max-width: 480px)');
var tablet = window.matchMedia('(min-width: 768px) and (max-width: 1024px)');
var landscape = window.matchMedia('(min-width: 500px) and (max-device-width : 1024px) and (max-height: 600px) and (orientation: landscape)');

var mySideNav = document.getElementById("mySidenav");
var myBackground = document.getElementById("bg");
var myNavbar = document.getElementById("navbar");

function openNav() {
  if (phone.matches) {
    mySideNav.style.width = "100%";
  } else if (tablet.matches) {
    mySideNav.style.width = "25%";
  } else if (landscape.matches) {
    mySideNav.style.width = "30%";
  } else {
    mySideNav.style.width = "15%";
    myBackground.style.marginRight = "15%";
    myBackground.style.width = "85%";
    myNavbar.style.width = "85%";
    myMealContainer.style.width = "99%";
  }
}

  function closeNav() {
    mySideNav.style.width = "0";
    myBackground.style.marginRight = "0";
    myBackground.style.width = "100%";
    myNavbar.style.width = "100%";
  }