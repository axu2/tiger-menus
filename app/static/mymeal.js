var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
var phone = window.matchMedia('(min-width: 320px) and (max-width: 480px)');
var tablet = window.matchMedia('(min-width: 768px) and (max-width: 1024px)');
var landscape = window.matchMedia('(min-width: 500px) and (max-height: 600px)');

var mySideNav = document.getElementById("mySidenav");
var myBackground = document.getElementById("bg");
var myNavbar = document.getElementById("navbar");
var myMealContainer = document.getElementsByClassName("container")[0];

var date = new Date();
if (window.location.pathname.split('/')[2] !== undefined) {
  const nextDate = date.getDate() + parseInt(window.location.pathname.split('/')[2]);
  date.setDate(nextDate);
}
var dateString = date.toLocaleDateString('en-US', options);
document.getElementById("date").textContent = `Menus for ${dateString}`;

if (phone.matches) {
  function openNav() {
    console.log("test");
    mySideNav.style.width = "100%";
  }
  function closeNav() {
    mySideNav.style.width = "0";
  }
} else if (tablet.matches) {
  function openNav() {
    mySideNav.style.width = "25%";
  }
  function closeNav() {
    mySideNav.style.width = "0";
  }
} else if (landscape.matches) {
  function openNav() {
    mySideNav.style.width = "30%";
  }
  function closeNav() {
    mySideNav.style.width = "0";
  }
} else {

  function openNav() {
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
  myMealContainer.style.width = "95%";
}