import * as vue from "../vendor/vue";
import VueMask from "@devindex/vue-mask";
import { mainMixin } from "../utils/mixins";
import { getAddress } from "../service/address";
const { createApp, ref } = vue;

const app = createApp({
  mixins: [mainMixin],
  delimiters: ["[[", "]]"],
  setup() {
    const inputField = ref();
    const focusInput = () => {
      inputField.value.focus();
    };
    return { focusInput, inputField };
  },
  data() {
    return {
      is_delivery: true,
      payment_type: "money",
      form: {
        cep: "",
        district: "",
        address: "",
        number: "",
        complement: "",
      },
    };
  },
  methods: {},
  computed: {
    cep() {
      return this.form.cep;
    },
  },
  watch: {
    async cep() {
      if (this.cep.length === 9) {
        const data = await getAddress(this.form.cep);
        this.form = {...this.form, ...data}
      }
    },
  },
});

app.use(VueMask);
app.mount("#app");
