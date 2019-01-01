var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

var date = new Date();
if (window.location.pathname.split('/')[2] !== undefined) {
  const nextDate = date.getDate() + parseInt(window.location.pathname.split('/')[2]);
  date.setDate(nextDate);
}
var dateString = date.toLocaleDateString('en-US', options);
document.getElementById("date").textContent = `Menus for ${dateString}`;

if (phone.matches) {
  function openNav() {
    document.getElementById("mySidenav").style.width = "100%";
  }
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }
} else if (tablet.matches) {
  function openNav() {
    document.getElementById("mySidenav").style.width = "25%";
  }
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }
} else if (landscape.matches) {
  function openNav() {
    document.getElementById("mySidenav").style.width = "30%";
  }
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }
} else {

  function openNav() {
    document.getElementById("mySidenav").style.width = "15%";
    document.getElementById("bg").style.marginRight = "15%";
    document.getElementById("bg").style.width = "85%";
    document.getElementById("navbar").style.width = "85%";
    document.getElementsByClassName("container")[0].style.width = "99%";
  }
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("bg").style.marginRight = "0";
  document.getElementById("bg").style.width = "100%";
  document.getElementById("navbar").style.width = "100%";
  document.getElementsByClassName("container")[0].style.width = "95%";
}
