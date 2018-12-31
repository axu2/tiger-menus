if(phone.matches) {
  function openNav() {
    document.getElementById("mySidenav").style.width = "100%";
  }
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }
 } else if(tablet.matches) {
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
 } 
 else {

function openNav() {
  document.getElementById("mySidenav").style.width = "15%";
  document.getElementById("bg").style.marginRight = "15%";
  document.getElementById("bg").style.width = "85%";
  document.getElementById("navbar").style.width = "85%";
  document.getElementById("landing").style.padding = "25rem 21rem 26rem 21rem";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("bg").style.marginRight = "0";
  document.getElementById("bg").style.width = "100%";
  document.getElementById("navbar").style.width = "100%";
  document.getElementById("landing").style.padding = "25rem 29rem 26rem 29rem";
}
}