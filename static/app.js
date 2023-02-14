const popover = document.querySelector('.popover');

document.addEventListener('DOMContentLoaded', function () {
    new Vue({
        el: '#app',
        data: {
            popoverHeight: 500,
            showSlider: false,
            slider1Value: 50,
            slider2Value: 50,
            showMenu: false,
            checkState: false,

            menus: {
              1: false,
              2: false,
              3: false,
              4: false,
              5: false,
              6: false,
              7: false,
              8: false
            },

            config: {}
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
            changeState() {
                this.checkState = !this.checkState;
                console.log(this.checkState);
                this.updateCheckState();
            },

            updateCheckState() {
                fetch('/update-checkstate', {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({
                    checkState: this.checkState
                  })
                })
                .then(response => response.json())
                .then(data => {
                  console.log('Success:', data);
                })
                .catch((error) => {
                  console.error('Error:', error);
                });
            },
            onChg (e) {
                console.log(this.slider1Value)
            },
            IncreaseLen1() {
              
            }, 
            IncreaseLen2() {
              
            },
            IncreaseLen3() {
              
            },
            IncreaseLen4() {
              
            },
            IncreaseLen5() {
              
            },
            IncreaseLen6() {
              
            },
            IncreaseLen7() {
              
            },
            IncreaseLen8() {
              
            },

            mounted() {
                console.log('Vue instance mounted');
            }
        },
  });
        
});

