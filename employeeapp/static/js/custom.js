"use strict";
$(document).ready(function() {
    $("select").niceSelect();

    /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        AOS Animation Activation
    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
    AOS.init();
    window.addEventListener("load", AOS.refresh);


    if (jQuery(".category-one").length > 0) {
        $('.category-one').slick({
            centerPadding: '25%',
            centerMode: true,
            slidesToShow: 3,
            slidesToScroll: 1,
            autoplay: true,
            swipe: true,
            infinite: true,
            autoplaySpeed: 2000,
            appendArrows: '.l1-category-slider',
            prevArrow: '<button class="slick-prev"><i class="icon icon-small-left"></i></button>',
            nextArrow: '<button class="slick-next"><i class="icon icon-small-right"></i></button>',
            responsive: [{
                    breakpoint: 1595,
                    settings: {
                        centerPadding: '10%',
                        slidesToShow: 4
                    }
                },
                {
                    breakpoint: 1488,
                    settings: {
                        centerPadding: '30px',
                        slidesToShow: 4
                    }
                },
                {
                    breakpoint: 1135,
                    settings: {
                        centerPadding: '40px',
                        slidesToShow: 3
                    }
                },
                {
                    breakpoint: 900,
                    settings: {
                        centerPadding: '10%',
                        slidesToShow: 2
                    }
                },
                {
                    breakpoint: 660,
                    settings: {
                        centerPadding: '20px',
                        slidesToShow: 2
                    }
                },
                {
                    breakpoint: 590,
                    settings: {
                        centerPadding: '15%',
                        slidesToShow: 1
                    }
                },
                {
                    breakpoint: 380,
                    settings: {
                        centerPadding: '0px',
                        slidesToShow: 1
                    }
                }
            ]
        });
    }
    if (jQuery(".testimonial-one").length > 0) {
        $('.testimonial-one').slick({
            autoplay: true,
            slidesToShow: 4,
            arrows: true,
            swipe: true,
            infinite: true,
            appendArrows: '.testimonial-one-button',
            prevArrow: '<button type="button" class="slick-prev"><i class="icon icon-minimal-left"></i></button>',
            nextArrow: '<button type="button" class="slick-next"><i class="icon icon-minimal-right"></i></button>',
            dots: true,
            responsive: [{
                    breakpoint: 1200,
                    settings: {
                        slidesToShow: 3
                    }
                },
                {
                    breakpoint: 992,
                    settings: {
                        slidesToShow: 2
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 1
                    }
                },
                {
                    breakpoint: 468,
                    settings: {
                        slidesToShow: 1
                    }
                }
            ]
        });
    }
    if (jQuery(".l4-review-slider").length > 0) {
        $('.l4-review-slider').slick({
            slidesToShow: 1,
            arrows: false,
            autoplay: true,
            fade: true,
            cssEase: 'linear',
            asNavFor: '.l4-tab-slider'
        });
        $('.l4-tab-slider').slick({
            slidesToShow: 6,
            asNavFor: '.l4-review-slider',
            dots: false,
            arrows: false,
            focusOnSelect: true,
            centerPadding: "60px",
            cssEase: 'ease-in-out',
            swipe: false,
            responsive: [{
                    breakpoint: 1180,
                    settings: {
                        slidesToShow: 5
                    }
                },
                {
                    breakpoint: 991,
                    settings: {
                        slidesToShow: 4
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 3
                    }
                },
                {
                    breakpoint: 530,
                    settings: {
                        slidesToShow: 2
                    }
                },
                {
                    breakpoint: 320,
                    settings: {
                        slidesToShow: 2
                    }
                }
            ]
        });
    }
    if (jQuery(".l5-review-slider").length > 0) {
        $('.l5-review-slider').slick({
            slidesToShow: 1,
            autoplay: true,
            asNavFor: '.l5-slider-dots',
            fade: true,
            cssEase: 'linear',
            arrows: false
        });
        $(".l5-slider-dots").slick({
            slidesToShow: 4,
            slidesToScroll: 1,
            asNavFor: ".l5-review-slider",
            dots: false,
            arrows: false,
            autoplay: true,
            focusOnSelect: true,
            centerPadding: "20px",
            swipe: false,
            responsive: [{
                breakpoint: 320,
                settings: {
                    slidesToShow: 3,
                },
            }, ],
        });
    }

    if (jQuery(".screenshot-slider").length > 0) {

        $('.screenshot-slider').slick({
            infinite: true,
            slidesToShow: 5,
            slidesToScroll: 1,
            dots: true,
            arrows: false,
            centerMode: true,
            centerPadding: '130px',
            autoplay: true,
            autoplaySpeed: 3000,
            infinite: true,
            easing: 'linear',
            speed: 800,
            appendDots: ".screenshots-dots",
            responsive: [{
                    breakpoint: 1800,
                    settings: {
                        slidesToShow: 5,
                        centerPadding: '100px',

                    }
                },
                {
                    breakpoint: 1750,
                    settings: {
                        slidesToShow: 5,
                        centerPadding: '20px',

                    }
                },
                {
                    breakpoint: 1670,
                    settings: {
                        slidesToShow: 4,
                        centerPadding: '60px',

                    }
                },
                {
                    breakpoint: 1640,
                    settings: {
                        slidesToShow: 3,
                        centerPadding: '20px',

                    }
                },
                {
                    breakpoint: 1550,
                    settings: {
                        slidesToShow: 3,
                        centerPadding: '30px',

                    }
                },
                {
                    breakpoint: 1450,
                    settings: {
                        slidesToShow: 3,
                        centerPadding: '10px',

                    }
                },
                {
                    breakpoint: 1350,
                    settings: {
                        slidesToShow: 3,
                        centerPadding: '20px',

                    }
                },
                {
                    breakpoint: 1250,
                    settings: {
                        slidesToShow: 3,
                        centerPadding: '10px',

                    }
                },
                {
                    breakpoint: 1150,
                    settings: {
                        slidesToShow: 3,
                        centerPadding: '0px',

                    }
                },
                {
                    breakpoint: 1050,
                    settings: {
                        slidesToShow: 1,
                        centerPadding: '10px',

                    }
                },
                {
                    breakpoint: 950,
                    settings: {
                        slidesToShow: 1,
                        centerPadding: '0',

                    }
                },
                {
                    breakpoint: 850,
                    settings: {
                        slidesToShow: 1,
                        centerPadding: '20px',
                    }
                },
                {
                    breakpoint: 750,
                    settings: {
                        slidesToShow: 1,
                        centerPadding: '20px',
                    }
                },
                {
                    breakpoint: 650,
                    settings: {
                        slidesToShow: 1,
                        centerPadding: '10px',
                    }
                },
                {
                    breakpoint: 515,
                    settings: {
                        slidesToShow: 1,
                        autoplay: true,
                        centerPadding: '0px',
                    }
                },
                {
                    breakpoint: 480,
                    settings: {
                        slidesToShow: 1,
                        autoplay: true,
                        centerPadding: '0px',
                        arrows: false,
                    }
                }

            ]
        });



    }
    if (jQuery(".l6-testimonial").length > 0) {
        $('.l6-testimonial').slick({
            dots: true,
            infinite: true,
            speed: 500,
            slidesToShow: 2,
            slidesToScroll: 1,
            autoplay: false,
            autoplaySpeed: 2000,
            centerMode: false,
            arrows: false,
            responsive: [{
                    breakpoint: 991,
                    settings: {
                        centerPadding: '20%',
                        slidesToShow: 1,
                    }
                },
                {
                    breakpoint: 769,
                    settings: {
                        centerPadding: '0',
                        slidesToShow: 1,
                    }
                }

            ]
        })
    }


    // Feature Section
    if (jQuery(".l3-feature-slider").length > 0) {
        $('.l3-feature-slider').slick({
            autoplay: true,
            autoplaySpeed: '3000',
            centerMode: true,
            centerPadding: '17%',
            slidesToShow: 3,
            arrows: false,
            touchMove: true,
            infinite: true,
            slidesToScroll: 1,
            responsive: [{
                    breakpoint: 1507,
                    settings: {
                        centerPadding: '8%',
                        slidesToShow: 3,
                    }
                },
                {
                    breakpoint: 1366,
                    settings: {
                        centerPadding: '10px',
                        slidesToShow: 3,
                    }
                },
                {
                    breakpoint: 1100,
                    settings: {
                        centerPadding: '80px',
                        slidesToShow: 2
                    }
                },
                {
                    breakpoint: 1099,
                    settings: {
                        centerPadding: '180px',
                        slidesToShow: 2
                    }
                },
                {
                    breakpoint: 1029,
                    settings: {
                        centerPadding: '80px',
                        slidesToShow: 2
                    }
                },
                {
                    breakpoint: 849,
                    settings: {
                        centerPadding: '30%',
                        slidesToShow: 1
                    }
                },
                {
                    breakpoint: 830,
                    settings: {
                        centerPadding: '25%',
                        slidesToShow: 1
                    }
                },
                {
                    breakpoint: 719,
                    settings: {
                        centerPadding: '20%',
                        slidesToShow: 1
                    }
                },
                {
                    breakpoint: 570,
                    settings: {
                        centerPadding: '30px',
                        slidesToShow: 1
                    }
                },
                {
                    breakpoint: 480,
                    settings: {
                        centerPadding: '0px',
                        slidesToShow: 1
                    }
                }
            ]
        });
    }

    /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
        Fancybox Support
    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/

    $("a.video-btn").fancybox({
        'transitionIn': 'elastic',
        'transitionOut': 'elastic',
        'speedIn': 600,
        'speedOut': 200,
        'overlayShow': false
    });

    /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
        Bootstrap Mobile Megamenu Support
    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/

    $(".dropdown-menu a.dropdown-toggle").on("click", function(e) {
        if (!$(this).next().hasClass("show")) {
            $(this)
                .parents(".dropdown-menu")
                .first()
                .find(".show")
                .removeClass("show");
        }
        var $subMenu = $(this).next(".dropdown-menu");
        $subMenu.toggleClass("show");

        $(this)
            .parents("li.nav-item.dropdown.show")
            .on("hidden.bs.dropdown", function(e) {
                $(".dropdown-submenu .show").removeClass("show");
            });

        return false;
    });

    /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
           Sticky Header
    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
    window.onscroll = function() {
        scrollFunction();
    };

    function scrollFunction() {
        if (
            document.body.scrollTop > 20 ||
            document.documentElement.scrollTop > 20
        ) {
            $(".site-header--sticky").addClass("scrolling");
        } else {
            $(".site-header--sticky").removeClass("scrolling");
        }
        if (
            document.body.scrollTop > 300 ||
            document.documentElement.scrollTop > 300
        ) {
            $(".site-header--sticky.scrolling").addClass("reveal-header");
        } else {
            $(".site-header--sticky.scrolling").removeClass("reveal-header");
        }
    }

    /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
           Input Count Up Button
    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
    $(".count-btn").on("click", function() {
        var $button = $(this);
        var oldValue = $button
            .parent(".count-input-btns")
            .parent()
            .find("input")
            .val();
        if ($button.hasClass("inc-ammount")) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            // Don't allow decrementing below zero
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        $button.parent(".count-input-btns").parent().find("input").val(newVal);
    });

    /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
           Prcing Dynamic Script
    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
    $("[data-pricing-trigger]").on("click", function(e) {
        $(e.target).addClass("active").siblings().removeClass("active");
        var valueAttr = $(e.target).attr('data-value');
        var target = $(e.target).attr("data-target");

        // For some browsers, attr is undefined; for others,
        // attr is false.  Check for both.
        if (typeof valueAttr !== typeof undefined && valueAttr !== false) {

            $(target).attr("data-value-active", valueAttr);

            // if ($(target).attr("data-value-active") == "monthly" && valueAttr == "monthly") {
            //   $(target).attr("data-value-active", "yearly");
            // } else {
            //   $(target).attr("data-value-active", "monthly");
            // }
        }
        // else {
        //   if ($(target).attr("data-value-active") == "monthly") {
        //     $(target).attr("data-value-active", "yearly");
        //   } else {
        //     $(target).attr("data-value-active", "monthly");
        //   }
        // }

    });

    /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
           Smooth Scroll
    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/

    $(".goto").on("click", function(event) {
        if (this.hash !== "") {
            event.preventDefault();
            var hash = this.hash;
            $("html, body").animate({
                    scrollTop: $(hash).offset().top,
                },
                2000,
                function() {
                    window.location.hash = hash;
                }
            );
        } // End if
    });
});


/*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
      Counter Up Activation
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
$('.counter').counterUp({
    delay: 10,
    time: 1000
});
/*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      
      Preloader Activation
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/

$(window).load(function() {
    setTimeout(function() {
        $("#loading").fadeOut(500);
    }, 1000);
    setTimeout(function() {
        $("#loading").remove();
    }, 2000);
});