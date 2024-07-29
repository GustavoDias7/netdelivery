import * as vue from "../vendor/vue";
import VueMask from "@devindex/vue-mask";
import { mainMixin } from "../mixins";
import getInputValues from "../utils/getInputValues";
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
  mounted() {
    const fields = getInputValues([
      "first_name",
      "last_name",
      "email",
      "password",
      "confirm_password",
      "phone"
    ]);
    this.fields = { ...this.fields, ...fields };
  },
});

app.use(VueMask);
app.mount("#app");
