function openNav() {
    document.getElementById("mySidenav").style.width = "15%";
    document.getElementById("bg").style.marginRight = "15%";
    document.getElementById("bg").style.width = "85%";
    document.getElementById("navbar").style.width = "85%";
    document.getElementById("landing").style.padding = "26rem 21rem 26rem 21rem";
  }
  
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("bg").style.marginRight = "0";
    document.getElementById("bg").style.width = "100%";
    document.getElementById("navbar").style.width = "100%";
    document.getElementById("landing").style.padding = "26rem 29rem 26rem 29rem";
  }