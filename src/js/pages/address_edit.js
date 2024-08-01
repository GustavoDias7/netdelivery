import * as vue from "../vendor/vue";
import VueMask from "@devindex/vue-mask";
import { mainMixin } from "../utils/mixins";
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
        cep: "",
        district: "",
        address: "",
        number: "",
        complement: "",
      },
    };
  },
  methods: {},
  mounted() {
    const fields = getInputValues([
      "cep",
      "district",
      "address",
      "number",
      "complement",
    ]);
    this.fields = { ...this.fields, ...fields };
  },
});

app.use(VueMask);
app.mount("#app");
