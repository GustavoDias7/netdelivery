import * as vue from "vue/dist/vue.esm-bundler.js";
// import { Money3Directive } from 'v-money3'
const { createApp } = vue;

const app = createApp({
  delimiters: ["[[", "]]"],
  setup() {
    return {};
  },
  data() {
    return {};
  },
  methods: {},
});

// app.directive('money', Money3Directive)
app.mount("#content-start");
