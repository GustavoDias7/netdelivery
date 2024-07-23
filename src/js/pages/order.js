import * as vue from "../vendor/vue";
import { mainMixin } from "../mixins";
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
    };
  },
  methods: {},
  computed: {},
});

app.mount("#app");
