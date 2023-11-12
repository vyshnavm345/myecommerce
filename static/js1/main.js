
$(document).ready(function(){
	"use strict";

	var window_width 	 = $(window).width(),
	window_height 		 = window.innerHeight,
	header_height 		 = $(".default-header").height(),
	header_height_static = $(".site-header.static").outerHeight(),
	fitscreen 			 = window_height - header_height;


	$(".fullscreen").css("height", window_height)
    $(".fitscreen").css("height", fitscreen);

  //------- Active Nice Select --------//

    $('select').niceSelect();


    $('.navbar-nav li.dropdown').hover(function() {
    $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeIn(500);
    }, function() {
    $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeOut(500);
    });

    $('.img-pop-up').magnificPopup({
        type: 'image',
        gallery:{
        enabled:true
        }
    });

    // Search Toggle
    $("#search_input_box").hide();
    $("#search").on("click", function () {
        $("#search_input_box").slideToggle();
        $("#search_input").focus();
    });
    $("#close_search").on("click", function () {
        $('#search_input_box').slideUp(500);
    });

    /*==========================
		javaScript for sticky header
		============================*/
			$(".sticky-header").sticky();

    /*=================================
    Javascript for banner area carousel
    ==================================*/
    $(".active-banner-slider").owlCarousel({
        items:1,
        autoplay:false,
        autoplayTimeout: 5000,
        loop:true,
        nav:true,
        navText:["<img src='static/img/banner/prev.png'>","<img src='static/img/banner/next.png'>"],
        dots:false
    });

    /*=================================
    Javascript for product area carousel
    ==================================*/
    $(".active-product-area").owlCarousel({
        items:1,
        autoplay:false,
        autoplayTimeout: 5000,
        loop:true,
        nav:true,
        navText:["<img src='static/img/product/prev.png'>","<img src='static/img/product/next.png'>"],
        dots:false
    });

    /*=================================
    Javascript for single product area carousel
    ==================================*/
    $(".s_Product_carousel").owlCarousel({
      items:1,
      autoplay:false,
      autoplayTimeout: 5000,
      loop:true,
      nav:false,
      dots:true
    });
    
    /*=================================
    Javascript for exclusive area carousel
    ==================================*/
    $(".active-exclusive-product-slider").owlCarousel({
        items:1,
        autoplay:false,
        autoplayTimeout: 5000,
        loop:true,
        nav:true,
        navText:["<img src='static/img/product/prev.png'>","<img src='static/img/product/next.png'>"],
        dots:false
    });

    //--------- Accordion Icon Change ---------//

    $('.collapse').on('shown.bs.collapse', function(){
        $(this).parent().find(".lnr-arrow-right").removeClass("lnr-arrow-right").addClass("lnr-arrow-left");
    }).on('hidden.bs.collapse', function(){
        $(this).parent().find(".lnr-arrow-left").removeClass("lnr-arrow-left").addClass("lnr-arrow-right");
    });

  // Select all links with hashes
  $('.main-menubar a[href*="#"]')
    // Remove links that don't actually link to anything
    .not('[href="#"]')
    .not('[href="#0"]')
    .click(function(event) {
      // On-page links
      if (
        location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') 
        && 
        location.hostname == this.hostname
      ) {
        // Figure out element to scroll to
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        // Does a scroll target exist?
        if (target.length) {
          // Only prevent default if animation is actually gonna happen
          event.preventDefault();
          $('html, body').animate({
            scrollTop: target.offset().top-70
          }, 1000, function() {
            // Callback after animation
            // Must change focus!
            var $target = $(target);
            $target.focus();
            if ($target.is(":focus")) { // Checking if the target was focused
              return false;
            } else {
              $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
              $target.focus(); // Set focus again
            };
          });
        }
      }
    });



      // -------   Mail Send ajax

         $(document).ready(function() {
            var form = $('#booking'); // contact form
            var submit = $('.submit-btn'); // submit button
            var alert = $('.alert-msg'); // alert div for show alert message

            // form submit event
            form.on('submit', function(e) {
                e.preventDefault(); // prevent default form submit

                $.ajax({
                    url: 'booking.php', // form action url
                    type: 'POST', // form submit method get/post
                    dataType: 'html', // request type html/json/xml
                    data: form.serialize(), // serialize form data
                    beforeSend: function() {
                        alert.fadeOut();
                        submit.html('Sending....'); // change submit button text
                    },
                    success: function(data) {
                        alert.html(data).fadeIn(); // fade in response data
                        form.trigger('reset'); // reset form
                        submit.attr("style", "display: none !important");; // reset submit button text
                    },
                    error: function(e) {
                        console.log(e)
                    }
                });
            });
        });




    $(document).ready(function() {
        $('#mc_embed_signup').find('form').ajaxChimp();
    });   



     if(document.getElementById("js-countdown")){

        var countdown = new Date("October 17, 2018");

        function getRemainingTime(endtime) {
            var milliseconds = Date.parse(endtime) - Date.parse(new Date());
            var seconds = Math.floor(milliseconds / 1000 % 60);
            var minutes = Math.floor(milliseconds / 1000 / 60 % 60);
            var hours = Math.floor(milliseconds / (1000 * 60 * 60) % 24);
            var days = Math.floor(milliseconds / (1000 * 60 * 60 * 24));

        return {
            'total': milliseconds,
            'seconds': seconds,
            'minutes': minutes,
            'hours': hours,
            'days': days
            };
        }

        function initClock(id, endtime) {
            var counter = document.getElementById(id);
            var daysItem = counter.querySelector('.js-countdown-days');
            var hoursItem = counter.querySelector('.js-countdown-hours');
            var minutesItem = counter.querySelector('.js-countdown-minutes');
            var secondsItem = counter.querySelector('.js-countdown-seconds');

        function updateClock() {
            var time = getRemainingTime(endtime);

            daysItem.innerHTML = time.days;
            hoursItem.innerHTML = ('0' + time.hours).slice(-2);
            minutesItem.innerHTML = ('0' + time.minutes).slice(-2);
            secondsItem.innerHTML = ('0' + time.seconds).slice(-2);

            if (time.total <= 0) {
              clearInterval(timeinterval);
            }
            }

            updateClock();
            var timeinterval = setInterval(updateClock, 1000);
        }

        initClock('js-countdown', countdown);

  };



      $('.quick-view-carousel-details').owlCarousel({
          loop: true,
          dots: true,
          items: 1,
      })

// updated filter function

$(document).ready(function () {
  var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

  $('.brand-checkbox, .color-checkbox').on('change', function () {
      updateFormValues();
  });

  if (document.getElementById("price-range")) {
      var nonLinearSlider = document.getElementById('price-range');
      noUiSlider.create(nonLinearSlider, {
          connect: true,
          behaviour: 'tap',
          start: [500, 100000],
          range: {
              'min': [0],
              '10%': [5000, 500],
              '50%': [40000, 1000],
              'max': [100000],
          },
      });

      var nodes = [
          document.getElementById('lower-value'),
          document.getElementById('upper-value'),
      ];

      nonLinearSlider.noUiSlider.on('update', function (values, handle, unencoded, isTap, positions) {
          nodes[handle].innerHTML = values[handle];
      });
  }

  function updateFormValues() {
      var selectedBrands = getSelectedValues("brand");
      var selectedColors = getSelectedValues("color");
      var lowerPrice = parseFloat(document.getElementById('lower-value').innerText);
      var upperPrice = parseFloat(document.getElementById('upper-value').innerText);

      // Create a data object to send to the backend
      var data = {
          'lower_price': lowerPrice,
          'upper_price': upperPrice,
          'brands[]': selectedBrands,
          'colors[]': selectedColors,
          'csrfmiddlewaretoken': csrfToken // Include the CSRF token
            
      };
      

      // Make an AJAX POST request to your server
      $.ajax({
          url: '/update_product_filter/', // Replace with your actual endpoint URL
          type: 'POST',
          data: data,
          success: function (data) {
            // Handle the response data from the backend
            var filteredProductsContainer = $('#filtered-products-container');
            filteredProductsContainer.empty(); // Clear existing content
        
            // Iterate through the filtered products and create HTML elements
            data.filtered_products.forEach(function (product) {
                var productHTML = ` 
                <div class="row">
                <div class="col-lg-4 col-md-6">
                <a href="${product.product_detail_url}">
                    <div class="single-product">
                         <img class="img-fluid" src="${product.image_url}" alt="">
                         
                        <div class="product-details">
                            <h6>${product.product_name}</h6>
                            <div class="price">
                                <h6>₹${product.price}</h6>
                            </div>
                            <div class="prd-bottom">
                                <form action="" method="post">
                                    <a href="{% url 'add_to_cart' 0 %}".replace('0', ${product.id}) class="social-info" type="submit">
                                        <span class="ti-bag"></span>
                                        <p class="hover-text">Cart</p>
                                    </a>
                                    <a href="{% url 'add_to_wishlist' 0 %}".replace('0', ${product.id}) class="social-info" type="submit">
                                        <span class="lnr lnr-heart"></span>
                                        <p class="hover-text">Wishlist</p>
                                    </a>
                                    <a href="" class="social-info">
                                        <span class="lnr lnr-move"></span>
                                        <p class="hover-text">view more</p>
                                    </a>
                                </form>
                            </div>
                        </div>
                    </div>
                </a>
            </div>
            </div>`;
                filteredProductsContainer.append(productHTML);
            });
        },
          error: function (xhr, status, error) {
              // Handle any errors if the request fails
          }
      });
  }

  function getSelectedValues(name) {
      var selectedValues = [];
      $("input[name='" + name + "']:checked").each(function () {
          selectedValues.push($(this).val());
      });
      return selectedValues;
  }
});

  //   //----- Active No ui slider --------//

  //   $(document).ready(function () {

  //     $('.brand-checkbox, .color-checkbox').on('change', function() {
  //       updateFormValues();
  //     });

  //     if (document.getElementById("price-range")) {
  //         var nonLinearSlider = document.getElementById('price-range');
  //         noUiSlider.create(nonLinearSlider, {
  //             connect: true,
  //             behaviour: 'tap',
  //             start: [500, 4000],
  //             range: {
  //                 'min': [0],
  //                 '10%': [5000, 500],
  //                 '50%': [40000, 1000],
  //                 'max': [100000],
  //             },
  //         });
  
  //         var nodes = [
  //             document.getElementById('lower-value'),
  //             document.getElementById('upper-value'),
  //         ];
  
  //         nonLinearSlider.noUiSlider.on('update', function (values, handle, unencoded, isTap, positions) {
  //             nodes[handle].innerHTML = values[handle];
  
  //             // Send an AJAX request to update the product filter
  //             var lowerPrice = values[0];
  //             var upperPrice = values[1];
  //             var selectedBrands = getSelectedValues("brand");
  //             var selectedColors = getSelectedValues("color");
  //             updateProductFilter(lowerPrice, upperPrice, selectedBrands, selectedColors);
  //         });
  //     }
  
  //     function getSelectedValues(name) {
  //         var selectedValues = [];
  //         $("input[name='" + name + "']:checked").each(function () {
  //             selectedValues.push($(this).val());
  //         });
  //         return selectedValues;
  //     }
  //     var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
  //     function updateProductFilter(lowerPrice, upperPrice, selectedBrands, selectedColors) {
  //         // Send an AJAX request to update the product filter
  //         $.ajax({
  //             url: '/update_product_filter/',  // Replace with your actual endpoint URL
  //             type: 'POST',
  //             headers: {
  //               'X-CSRFToken': csrfToken
  //           },
  //             data: {
  //                 'lower_price': lowerPrice,
  //                 'upper_price': upperPrice,
  //                 'brands[]': selectedBrands,
  //                 'colors[]': selectedColors,
  //             },
  //             success: function (data) {
  //                 // Handle the response data and update your product list
  //                 // You can replace the product list content or update it as needed
  //                 // For example: $('#product-list').html(data.filtered_products);
  //             },
  //         });
  //     }
  // });




    // $(function(){

    //     if(document.getElementById("price-range")){
        
    //     var nonLinearSlider = document.getElementById('price-range');
        
    //     noUiSlider.create(nonLinearSlider, {
    //         connect: true,
    //         behaviour: 'tap',
    //         start: [ 500, 4000 ],
    //         range: {
    //             // Starting at 500, step the value by 500,
    //             // until 4000 is reached. From there, step by 1000.
    //             'min': [ 0 ],
    //             '10%': [ 5000, 500 ],
    //             '50%': [ 40000, 1000 ],
    //             'max': [ 100000 ]
    //         }
    //     });


    //     var nodes = [
    //         document.getElementById('lower-value'), // 0
    //         document.getElementById('upper-value')  // 1
    //     ];

    //     // Display the slider value and how far the handle moved
    //     // from the left edge of the slider.
    //     nonLinearSlider.noUiSlider.on('update', function ( values, handle, unencoded, isTap, positions ) {
    //         nodes[handle].innerHTML = values[handle];
    //     });

    //     }

    // });

    
    //-------- Have Cupon Button Text Toggle Change -------//

    $('.have-btn').on('click', function(e){
        e.preventDefault();
        $('.have-btn span').text(function(i, text){
          return text === "Have a Coupon?" ? "Close Coupon" : "Have a Coupon?";
        })
        $('.cupon-code').fadeToggle("slow");
    });

    $('.load-more-btn').on('click', function(e){
        e.preventDefault();
        $('.load-product').fadeIn('slow');
        $(this).fadeOut();
    });
    




  //------- Start Quantity Increase & Decrease Value --------//




    var value,
        quantity = document.getElementsByClassName('quantity-container');

    function createBindings(quantityContainer) {
        var quantityAmount = quantityContainer.getElementsByClassName('quantity-amount')[0];
        var increase = quantityContainer.getElementsByClassName('increase')[0];
        var decrease = quantityContainer.getElementsByClassName('decrease')[0];
        increase.addEventListener('click', function () { increaseValue(quantityAmount); });
        decrease.addEventListener('click', function () { decreaseValue(quantityAmount); });
    }

    function init() {
        for (var i = 0; i < quantity.length; i++ ) {
            createBindings(quantity[i]);
        }
    };

    function increaseValue(quantityAmount) {
        value = parseInt(quantityAmount.value, 10);

        console.log(quantityAmount, quantityAmount.value);

        value = isNaN(value) ? 0 : value;
        value++;
        quantityAmount.value = value;
    }

    function decreaseValue(quantityAmount) {
        value = parseInt(quantityAmount.value, 10);

        value = isNaN(value) ? 0 : value;
        if (value > 0) value--;

        quantityAmount.value = value;
    }

  init();

//------- End Quantity Increase & Decrease Value --------//

  /*----------------------------------------------------*/
  /*  Google map js
    /*----------------------------------------------------*/

    if ($("#mapBox").length) {
        var $lat = $("#mapBox").data("lat");
        var $lon = $("#mapBox").data("lon");
        var $zoom = $("#mapBox").data("zoom");
        var $marker = $("#mapBox").data("marker");
        var $info = $("#mapBox").data("info");
        var $markerLat = $("#mapBox").data("mlat");
        var $markerLon = $("#mapBox").data("mlon");
        var map = new GMaps({
          el: "#mapBox",
          lat: $lat,
          lng: $lon,
          scrollwheel: false,
          scaleControl: true,
          streetViewControl: false,
          panControl: true,
          disableDoubleClickZoom: true,
          mapTypeControl: false,
          zoom: $zoom,
          styles: [
            {
              featureType: "water",
              elementType: "geometry.fill",
              stylers: [
                {
                  color: "#dcdfe6"
                }
              ]
            },
            {
              featureType: "transit",
              stylers: [
                {
                  color: "#808080"
                },
                {
                  visibility: "off"
                }
              ]
            },
            {
              featureType: "road.highway",
              elementType: "geometry.stroke",
              stylers: [
                {
                  visibility: "on"
                },
                {
                  color: "#dcdfe6"
                }
              ]
            },
            {
              featureType: "road.highway",
              elementType: "geometry.fill",
              stylers: [
                {
                  color: "#ffffff"
                }
              ]
            },
            {
              featureType: "road.local",
              elementType: "geometry.fill",
              stylers: [
                {
                  visibility: "on"
                },
                {
                  color: "#ffffff"
                },
                {
                  weight: 1.8
                }
              ]
            },
            {
              featureType: "road.local",
              elementType: "geometry.stroke",
              stylers: [
                {
                  color: "#d7d7d7"
                }
              ]
            },
            {
              featureType: "poi",
              elementType: "geometry.fill",
              stylers: [
                {
                  visibility: "on"
                },
                {
                  color: "#ebebeb"
                }
              ]
            },
            {
              featureType: "administrative",
              elementType: "geometry",
              stylers: [
                {
                  color: "#a7a7a7"
                }
              ]
            },
            {
              featureType: "road.arterial",
              elementType: "geometry.fill",
              stylers: [
                {
                  color: "#ffffff"
                }
              ]
            },
            {
              featureType: "road.arterial",
              elementType: "geometry.fill",
              stylers: [
                {
                  color: "#ffffff"
                }
              ]
            },
            {
              featureType: "landscape",
              elementType: "geometry.fill",
              stylers: [
                {
                  visibility: "on"
                },
                {
                  color: "#efefef"
                }
              ]
            },
            {
              featureType: "road",
              elementType: "labels.text.fill",
              stylers: [
                {
                  color: "#696969"
                }
              ]
            },
            {
              featureType: "administrative",
              elementType: "labels.text.fill",
              stylers: [
                {
                  visibility: "on"
                },
                {
                  color: "#737373"
                }
              ]
            },
            {
              featureType: "poi",
              elementType: "labels.icon",
              stylers: [
                {
                  visibility: "off"
                }
              ]
            },
            {
              featureType: "poi",
              elementType: "labels",
              stylers: [
                {
                  visibility: "off"
                }
              ]
            },
            {
              featureType: "road.arterial",
              elementType: "geometry.stroke",
              stylers: [
                {
                  color: "#d6d6d6"
                }
              ]
            },
            {
              featureType: "road",
              elementType: "labels.icon",
              stylers: [
                {
                  visibility: "off"
                }
              ]
            },
            {},
            {
              featureType: "poi",
              elementType: "geometry.fill",
              stylers: [
                {
                  color: "#dadada"
                }
              ]
            }
          ]
        });
      }


  

 });
