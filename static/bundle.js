(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){

},{}],2:[function(require,module,exports){
/*const Vue = require('vue');
const App = require('./App.vue');
document.addEventListener('DOMContentLoaded', function () {
    new Vue({
        render: h => h(App)
    }).$mount('#app');
});*/

const fs = require('fs')
fs.readFile('./src/config.json', 'utf8', (err, jsonString) => {
    if (err) {
        console.log("File read failed:", err)
        return
    }
    console.log('File data:', jsonString) 
})

document.addEventListener('DOMContentLoaded', function () {
    new Vue({
        el: '#app',
        data: {
            showSlider: false,
            slider1Value: 50,
            slider2Value: 50,
            showMenu: false
          },
        methods: {
            doExit() {
                console.log("Exit button clicked");
            },
            doAdjust() {
                console.log("Adjust button clicked");
                this.showSlider = !this.showSlider;
            },
            doMenu() {
                console.log("Menu button clicked");
                this.showMenu = !this.showMenu;
            },
            onChg (e) {
                console.log(this.slider1Value)
            },
            mounted() {
                console.log('Vue instance mounted');
            }
        }
    });
});
},{"fs":1}]},{},[2]);
