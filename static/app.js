/*const Vue = require('vue');
const App = require('./App.vue');
document.addEventListener('DOMContentLoaded', function () {
    new Vue({
        render: h => h(App)
    }).$mount('#app');
});*/

/*const fs = require('fs')
fs.readFile('../VirtualMouse/src/config.json', 'utf8', (err, jsonString) => {
    if (err) {
        console.log("File read failed:", err)
        return
    }
    console.log('File data:', jsonString) 
})*/
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