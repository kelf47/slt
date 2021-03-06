// <![CDATA[
$(function() {

  // Slider
  $('#coin-slider').coinslider({width:960,height:450,opacity:1});

  // Radius Box
  $('.menu_nav ul li a, .content .mainbar img.fl, p.infopost a.com, .content p.pages span, .content p.pages a').css({"border-radius":"6px", "-moz-border-radius":"6px", "-webkit-border-radius":"6px"});
  $('.content .sidebar .gadget, .fbg_resize').css({"border-radius":"12px", "-moz-border-radius":"12px", "-webkit-border-radius":"12px"});
  //$('.content p.pages span, .content p.pages a').css({"border-radius":"16px", "-moz-border-radius":"16px", "-webkit-border-radius":"16px"});
  $('.content .sidebar h2').css({"border-top-left-radius":"12px", "border-top-right-radius":"12px", "-moz-border-radius-topleft":"12px", "-moz-border-radius-topright":"12px", "-webkit-border-top-left-radius":"12px", "-webkit-border-top-right-radius":"12px"});

});

// Cufon
Cufon.replace('h1, h2, h3, h4, h5, h6, .menu_nav ul li a', { hover: true });
//Cufon.replace('h1', { color: '-linear-gradient(#fff, #ffaf02)'});
//Cufon.replace('h1 small', { color: '#8a98a5'});

// ]]>

jQuery(document).ready(function($)
{
  // Get the modal
  var modal_productes = document.getElementById('modalProductesPlagues');
  var modal_neteja = document.getElementById('modalProductesNeteja');

  // Get the button that opens the modal
  var div_plagues = document.getElementById("productes-plagues");
  var div_neteja = document.getElementById("productes-neteja");

  // Get the <span> element that closes the modal
  var close_plagues = document.getElementsByClassName("close")[0];
  var close_neteja = document.getElementsByClassName("close")[1]; 
  // When the user clicks the button, open the modal 
  if (div_plagues != null){
    div_plagues.onclick = function() {
        if ($(document).height() > $(window).height()) {
             var scrollTop = ($('html').scrollTop()) ? $('html').scrollTop() : $('body').scrollTop(); // Works for Chrome, Firefox, IE...
             $('html').addClass('noscroll').css('top',-scrollTop);         
        }
        modal_productes.style.display = "block";

    }
  }
  if (div_neteja != null){
    div_neteja.onclick = function() {
        if ($(document).height() > $(window).height()) {
             var scrollTop = ($('html').scrollTop()) ? $('html').scrollTop() : $('body').scrollTop(); // Works for Chrome, Firefox, IE...
             $('html').addClass('noscroll').css('top',-scrollTop);         
        }
        modal_neteja.style.display = "block";

    }
  }
  if (close_plagues != null){
    // When the user clicks on <span> (x), close the modal
    close_plagues.onclick = function() {
      var scrollTop = parseInt($('html').css('top'));
      $('html').removeClass('noscroll');
      $('html,body').scrollTop(-scrollTop);
      modal_productes.style.display = "none";
      modal_neteja.style.display = "none";

    }
  }

  if (close_neteja != null){
    // When the user clicks on <span> (x), close the modal
    close_neteja.onclick = function() {
      var scrollTop = parseInt($('html').css('top'));
      $('html').removeClass('noscroll');
      $('html,body').scrollTop(-scrollTop);
      modal_productes.style.display = "none";
      modal_neteja.style.display = "none";

    }
  }
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
      if (event.target == modal_productes || event.target == modal_neteja) {
          var scrollTop = parseInt($('html').css('top'));
          $('html').removeClass('noscroll');
          $('html,body').scrollTop(-scrollTop);
          modal_productes.style.display = "none";
          modal_neteja.style.display = "none";

      }
  }
 var select_tipus = document.getElementById("tipus-doc");
 if (select_tipus != null){
   select_tipus.onchange = function () { 
        var select = document.getElementById("tipus-doc");
        var tipus = select.options[ select.selectedIndex ].value
        if (tipus != 'tots') {
          $('.table-td').css('display', 'none');
          $('.table-td[doc-type="' + tipus + '"]').fadeIn('slow');
        } else {
          $('.table-td').css('display', 'none').fadeIn('slow');
        }
    }
  }

  /*Select Box js*/
  $('.drop-menu').click(function () {
          $(this).attr('tabindex', 1).focus();
          $(this).toggleClass('active');
          $(this).find('.dropeddown').slideToggle(300);
      });
      $('.drop-menu').focusout(function () {
          $(this).removeClass('active');
          $(this).find('.dropeddown').slideUp(300);
      });
      $('.drop-menu .dropeddown li').click(function () {
          $(this).parents('.drop-menu').find('span').text($(this).text());
          $(this).parents('.drop-menu').find('input').attr('value', $(this).attr('id'));
      });
  /*End Select Box js*/


  $('.dropeddown li').click(function () {
    var input = $(this).parents('.drop-menu').find('input').val();
    var pathname = window.location.pathname
    if (input == "castellano"){
       if (pathname == "/inici" || pathname == "/inicio")window.location.href = 'inicio';
       else if (pathname == "/que_fem" || pathname == "/que_hacemos")window.location.href = 'que_hacemos';
       else if (pathname == "/qui_som" || pathname == "/quienes_somos")window.location.href = 'quienes_somos';
       else if (pathname == "/acces" || pathname == "/acceso")window.location.href = 'acceso';
       else if (pathname == "/contacte" || pathname == "/contacto")window.location.href = 'contacto';
    }
    else{
       if (pathname == "/inici" || pathname == "/inicio")window.location.href = 'inici';
       else if (pathname == "/que_fem" || pathname == "/que_hacemos")window.location.href = 'que_fem';
       else if (pathname == "/qui_som" || pathname == "/quienes_somos")window.location.href = 'qui_som';
       else if (pathname == "/acces" || pathname == "/acceso")window.location.href = 'acces';
       else if (pathname == "/contacte" || pathname == "/contacto")window.location.href = 'contacte';
    }
  }); 

});