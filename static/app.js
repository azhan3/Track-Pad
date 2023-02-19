document.addEventListener('DOMContentLoaded', function () {
  var app = new Vue({
    el: '#app',
    data: {
      popoverHeight: 500,
      showSlider: false,
      slider1Value: 50,
      slider2Value: 50,
      showMenu: false,
      checkState: false,
      activeButton: null,
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
      gestures: {},
      translate: {
        "DoubleIndexFinger": "Double Index Finger",
        "IndexFinger": "Index Finger",
        "OpenPalm": "Open Palm",
        "Fist": "Fist",
        "NoAction": "No Action",
        "Spider-Man": "Spider-Man",
        "OK": "OK",
        "Telephone": "Telephone"
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
      doMenu(event) {
        console.log("Menu button clicked");
        this.showMenu = !this.showMenu;
        var submit_btn = event.target.parentElement.parentElement.querySelector(".popover").querySelector(".content").querySelector(".button-apply").querySelector("p");
        console.log(submit_btn.innerHTML);
        submit_btn.innerHTML = "Apply Changes";
        $.getJSON('config.json', function (data) {
          // Store the JSON data in a variable for easier access
          var jsonData = data;
          $.each(jsonData.gestures, function (key, value) {
            //this.gestures[key] = value;
            $('#' + key.replace(/\s/g, '')).prev().find('span').text(value);
          });
        });

        $.getJSON('config.json', (data) => {
          $.each(data.gestures, (key, value) => {
            this.gestures[key] = value;
          });
  
        });
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
      onChg(e) {
        console.log(this.slider1Value)
      },
      IncreaseLen(event) {
        var submit_btn = event.target.parentElement.parentElement.parentElement.parentElement.querySelector(".button-apply").querySelector("p");
        console.log(submit_btn);
        submit_btn.innerHTML = "Apply Changes";
        const id = Number(event.target.getAttribute("data-id"));
        if (id <= 4) {
          if (this.menus[id] && this.menus[id + 4]) {
            this.menus[id] = false;
          } else if (!this.menus[id] && !this.menus[id + 4]) {
            this.menus[id] = true;
            this.popoverHeight += 250;
          } else if (!this.menus[id]) {
            this.menus[id] = true;
          } else {
            this.menus[id] = false;
            this.popoverHeight -= 250;
          }
        } else {
          if (this.menus[id] && this.menus[id - 4]) {
            this.menus[id] = false;
          } else if (!this.menus[id] && !this.menus[id - 4]) {
            this.menus[id] = true;
            this.popoverHeight += 250;
          } else if (!this.menus[id]) {
            this.menus[id] = true;
          } else {
            this.menus[id] = false;
            this.popoverHeight -= 250;
          }
        }

        console.log(id);
      },
      logParentContainer(event) {
        const parentContainer = event.target.parentElement;
        // update the span text to the clicked button's label
        const span = parentContainer.parentElement.querySelector(`label[for="${parentContainer.getAttribute("for")}"]`);
        const checkbox = parentContainer.parentElement.querySelector(`input[id=${parentContainer.getAttribute("for")}]`);

        span.innerHTML = `<span>${event.target.textContent}</span>`;
        var ge = this.translate[parentContainer.getAttribute("for")];
        this.gestures[ge] = event.target.textContent;
        checkbox.checked = false;

        var id = Number(parentContainer.parentElement.querySelector(`input[id=${parentContainer.getAttribute("for")}]`).getAttribute("data-id"));

        if (id <= 4) {
          if (this.menus[id] && this.menus[id + 4]) {
            this.menus[id] = false;
          } else if (!this.menus[id]) {
            this.menus[id] = true;
          } else {
            this.menus[id] = false;
            this.popoverHeight -= 250;
          }
        } else {
          if (this.menus[id] && this.menus[id - 4]) {
            this.menus[id] = false;
          } else if (!this.menus[id]) {
            this.menus[id] = true;
          } else {
            this.menus[id] = false;
            this.popoverHeight -= 250;
          }
        }

      },

      applyChanges(event) {
        const btn = event.target;
        
        btnText.innerHTML = "Applied!";
        console.log(this.gestures);


        // Send POST request to Flask with updated gestures

        fetch('/update_gesture', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            gestures: this.gestures
          })
        })
          .then(response => response.json())
          .then(data => {
            console.log('Success:', data);
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      }
    },
    mounted() {
      console.log('Vue instance mounted');
      $.getJSON('config.json', (data) => {
        $.each(data.gestures, (key, value) => {
          this.gestures[key] = value;
        });

      });
    }
  });

});

