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
        methods: {
            doExit() {
                console.log("Exit button clicked");
            },
            doAdjust() {
                console.log("Adjust button clicked");
            },
            doMenu() {
                console.log("Menu button clicked");
            },
            mounted() {
                console.log('Vue instance mounted');
            }
        }
    });
});