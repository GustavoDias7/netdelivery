import * as vue from "vue/dist/vue.esm-bundler.js";
import { mainMixin } from "../utils/mixins";
const { createApp } = vue;

const app = createApp({
  mixins: [mainMixin],
  delimiters: ["[[", "]]"],
  setup() {
    return {};
  },
  data() {
    return {
      accordion: {
        state: false,
        index: null,
      },
    };
  },
  methods: {
    handleAccordion(index) {
      if (this.accordion.state == false) {
        this.accordion.state = true;
        this.accordion.index = index;
      } else if (
        this.accordion.state == true &&
        this.accordion.index == index
      ) {
        this.accordion.state = false;
        this.accordion.index = null;
      } else if (
        this.accordion.state == true &&
        this.accordion.index != index
      ) {
        this.accordion.index = index;
      }
    },
  },
});

app.mount("#app");
