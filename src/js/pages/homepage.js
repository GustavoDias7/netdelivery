import * as vue from "../vendor/vue";
import { mainMixin } from "../mixins";
const { createApp } = vue;

const app = createApp({
  mixins: [mainMixin],
  delimiters: ["[[", "]]"],
  setup() {},
  data() {
    return {};
  },
  methods: {},
});


app.mount("#app");
