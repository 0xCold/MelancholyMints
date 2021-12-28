const mintDate = new Date("Dec 25, 2021 00:00:00").getTime();

var days;
var hrs;
var mins;
var secs;

window.onload = function() {onLoad()};


async function onLoad() {
    if ("solana" in window) {
        const provider = window.solana;
        if (provider.isPhantom) {
          console.log(provider);
        }
    }

    //days = document.getElementById("days-countdown");
    //hrs = document.getElementById("hrs-countdown");
    //mins = document.getElementById("mins-countdown");
    //secs = document.getElementById("secs-countdown");

    //var x = setInterval(function() {
    //    updateCountdown();
    //}, 1000);

    var allMods = $(".slider");
    allMods.each(function(i, el) {
        var el = $(el);
        if (el.visible(true)) {
            el.addClass("already-visible");
        }
    });

    var acc = document.getElementsByClassName("accordion");
    var i;

    for (i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var panel = this.getElementsByClassName("panel")[0];
            var plusminus = this.getElementsByClassName("plusminus")[0];
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null;
                plusminus.innerHTML = "+"
            }
            else {
                panel.style.maxHeight = panel.scrollHeight + "px";
                plusminus.innerHTML = "-"
            }
        });
    }
}


async function connectWallet() {
    try {
        const resp = await window.solana.connect();
        var wallet_button = document.getElementById("wallet-button");
        wallet_button.innerHTML = resp.publicKey.toString().slice(0, 4).toUpperCase() + "..." + resp.publicKey.toString().slice(-4).toUpperCase();
    }
    catch {
        console.log("User rejected the request");
    }
}

function updateCountdown() {
    var now = new Date().getTime();
    var delta = mintDate - now;

    days.innerHTML = Math.floor(delta / (1000 * 60 * 60 * 24));
    hrs.innerHTML = Math.floor((delta % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    mins.innerHTML = Math.floor((delta % (1000 * 60 * 60)) / (1000 * 60));
    secs.innerHTML = Math.floor((delta % (1000 * 60)) / 1000);

}

function scrollToElem(element) {
    element_pos = document.getElementById(element).getBoundingClientRect().top - 10;
    window.scrollTo(0, element_pos);
}

(function($) {

  /**
   * Copyright 2012, Digital Fusion
   * Licensed under the MIT license.
   * http://teamdf.com/jquery-plugins/license/
   *
   * @author Sam Sehnert
   * @desc A small plugin that checks whether elements are within
   *     the user visible viewport of a web browser.
   *     only accounts for vertical position, not horizontal.
   */

  $.fn.visible = function(partial) {

      var $t            = $(this),
          $w            = $(window),
          viewTop       = $w.scrollTop(),
          viewBottom    = viewTop + $w.height(),
          _top          = $t.offset().top,
          _bottom       = _top + $t.height(),
          compareTop    = partial === true ? _bottom : _top,
          compareBottom = partial === true ? _top : _bottom;

    return ((compareBottom <= viewBottom) && (compareTop >= viewTop));

  };

})(jQuery);


function testScroll() {
    var allMods = $(".slider");
    allMods.each(function(i, el) {
        var el = $(el);
        if (el.visible(true)) {
            if (el.hasClass("slide-l")) {
                el.addClass("slide-in-l");
            }
            else if (el.hasClass("slide-r")) {
                el.addClass("slide-in-r");
            }
            else {
                el.addClass("come-in");
            }
        }
    });
}