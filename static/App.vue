<template>
  <div>
    <h3>App</h3>
    <button @click="handleExit">Exit</button>
    <button @click="handleAdjust">Adjust</button>
    <button @click="handleMenu">Menu</button>
  </div>
</template>

<script>
export default {
  methods: {
    handleExit() {
      console.log('Exit button clicked');
      // Add your custom logic here
    },
    handleAdjust() {
      console.log('Adjust button clicked');
      // Add your custom logic here
    },
    handleMenu() {
      console.log('Menu button clicked');
      // Add your custom logic here
    }
  }
};
</script>
