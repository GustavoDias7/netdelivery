import * as vue from "../vendor/vue";
import { mainMixin } from "../mixins";
const { createApp } = vue;

const app = createApp({
  mixins: [mainMixin],
  delimiters: ["[[", "]]"],
  setup() {
    return {};
  },
  data() {
    return {
      fields: {
        first_name: "",
        last_name: "",
        phone: "",
        email: "",
        password: "",
        confirm_password: "",
      },
      passwords: {
        main: false,
        confirm: false,
      },
    };
  },
  methods: {
    togglePassword(name = "") {
      this.passwords[name] = !this.passwords[name];
    },
  },
});

app.mount("#app");
