// ==UserScript==
// @name         NVDA Stock Data Popout
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Add a popout to show NVDA stock data chart
// @author       Riya Nair
// @match        https://elite.finviz.com/quote.ashx?t=NVDA&ty=c&ta=1&p=h
// @icon         https://www.finviz.com/favicon.ico
// @grant        GM_addStyle
// ==/UserScript==

(function() {
    'use strict';

    // Add the popout HTML structure
    const popoutHTML = `
        <button id="showPopout" style="position:fixed; bottom:20px; right:20px; z-index:1000;">Show Stock Data</button>
        <div id="popout" class="popout">
            <span class="close">&times;</span>
            <img src="https://i.imgur.com/APlpOMa.png" alt="NVDA Stock Data">
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', popoutHTML);

    // Add the styles for the popout
    GM_addStyle(`
        .popout {
            display: none;
            position: fixed;
            z-index: 1001;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.8);
            padding-top: 60px;
        }
        .popout img {
            display: block;
            margin: 5% auto;
            width: 80%;
            max-width: 700px;
        }
        .close {
            position: absolute;
            top: 15px;
            right: 35px;
            color: #fff;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
        }
    `);

    // Add the JavaScript functionality
    document.getElementById('showPopout').onclick = function() {
        document.getElementById('popout').style.display = "block";
    }

    document.querySelector('.close').onclick = function() {
        document.getElementById('popout').style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == document.getElementById('popout')) {
            document.getElementById('popout').style.display = "none";
        }
    }
})();
