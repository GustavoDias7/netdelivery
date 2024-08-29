import * as vue from "../vendor/vue";
import { mainMixin } from "../utils/mixins";
const { createApp, ref } = vue;

const app = createApp({
  mixins: [mainMixin],
  delimiters: ["[[", "]]"],
  setup() {
    const inputField = ref();
    const focusInput = () => {
      inputField.value.focus();
    };
    
    return { focusInput, inputField, notif: hasNotification };
  },
  data({ notif }) {
    return {
      is_delivery: true,
      payment_type: "money",
      notification: notif,
    };
  },
  methods: {
    setNotification() {
      setTimeout(() => {
        this.notification = false;
      }, 3000);
    },
  },
  computed: {},
  watch: {},
  mounted() {
    if (this.notification) this.setNotification()
  }
});

app.mount("#app");
