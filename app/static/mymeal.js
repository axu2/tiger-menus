const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

let date = new Date();
if (window.location.pathname.split('/')[2] !== undefined) {
  const nextDate = date.getDate() + parseInt(window.location.pathname.split('/')[2]);
  date.setDate(nextDate);
}
const dateString = date.toLocaleDateString('en-US', options);
document.getElementById("date").textContent = `Menus for ${dateString}`;

function openNav() {
  document.getElementById("mySidenav").style.width = "15%";
  document.getElementById("bg").style.marginRight = "15%";
  document.getElementById("bg").style.width = "85%";
  document.getElementById("navbar").style.width = "85%";
  document.getElementsByClassName("container")[0].style.width = "99%";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("bg").style.marginRight = "0";
  document.getElementById("bg").style.width = "100%";
  document.getElementById("navbar").style.width = "100%";
  document.getElementsByClassName("container")[0].style.width = "95%";
}