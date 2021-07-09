$(function () {
    /* Preloader */
    $(window).on('load', function () {
        $('pre').addClass('ss-container');
        $('.preloader').delay(100).fadeOut('slow');
    });
    /* Smooth Scroll */
    $('a.smoth-scroll').on("click", function (e) {
        var anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $(anchor.attr('href')).offset().top - 50
        }, 1000);
        e.preventDefault();
    });
    /* Scroll To Top */
    $(window).on('scroll', function () {
        if ($(this).scrollTop() >= 500) {
            $('.scroll-to-top').fadeIn();
        } else {
            $('.scroll-to-top').fadeOut();
        }
    });
    $('.scroll-to-top').on('click', function () {
        $('html, body').animate({
            scrollTop: 0
        }, 800);
        return false;

    });
});


var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    handler: function (direction) {},
    offset: 'bottom-in-view',
    onBeforePageLoad: function () {
        $('.preloader').show();
    },
    onAfterPageLoad: function () {
        $('.preloader').hide();
    }
});

document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll('pre').forEach((block) => {
        hljs.highlightBlock(block);
    });

    document.querySelectorAll('code').forEach((block) => {
        hljs.highlightBlock(block);
    });

});


function displayToggle(id) {
    let x = document.getElementById(id);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}


