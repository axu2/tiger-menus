function openNav() {
    document.getElementById("mySidenav").style.width = "15%";
    document.getElementById("bg").style.marginRight = "15%";
    document.getElementById("bg").style.width = "85%";
    document.getElementById("navbar").style.width = "85%";
    document.getElementsByClassName("container")[0].style.width = "97%";
  }
  
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("bg").style.marginRight = "0";
    document.getElementById("bg").style.width = "100%";
    document.getElementById("navbar").style.width = "100%";
    document.getElementsByClassName("container")[0].style.width = "95%";
  }