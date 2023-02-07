/*const Vue = require('vue');
const App = require('./App.vue');
document.addEventListener('DOMContentLoaded', function () {
    new Vue({
        render: h => h(App)
    }).$mount('#app');
});*/


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
            mounted() {
                console.log('Vue instance mounted');
            }
        }
    });
});