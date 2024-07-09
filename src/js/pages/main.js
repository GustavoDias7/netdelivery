import * as vue from "../vendor/vue";
const { createApp } = vue;

const app = createApp({
  data() {
    return {
      count: 0,
    };
  },
});

app.mount("#app");
