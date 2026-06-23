const pathname = window.location.pathname;

if (pathname === '/') {
    clearCookie(['authState'])
}  

if (pathname !== '/friends/all_friends'){
    clearCookie(['selection'])
}

document.querySelectorAll('.nav-link').forEach(function(link){
    if (pathname.includes(link.id)){
        link.classList.toggle("active-link");
    } else if (pathname === "/" && link.id === "house") {
        link.classList.toggle("active-link");
    };
});