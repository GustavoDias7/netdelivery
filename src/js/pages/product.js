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
      minimum_options: minimum_options,
      maximum_options: maximum_options,
      checkboxes: [],
    };
  },
  methods: {
    handle_check(e) {
      const id = Number(e.target.id);
      const index = this.checkboxes.findIndex((field) => field.id == id);
      if (e.target.checked) this.checkboxes[index].checked = true;
      else this.checkboxes[index].checked = false;
    },
    handle_maximum(id) {
      let result = false
      const index = this.checkboxes.findIndex((field) => field.id == id);
      if (index > -1) (result = this.checkboxes[index].checked);
      return result === false && this.maximum_options == this.check_counter;
    }
  },
  computed: {
    disable_check() {
      return this.check_fields.length === maximum_options;
    },
    check_counter() {
      return this.checkboxes.reduce((acc, crr) => {
        return acc + (crr.checked ? 1 : 0);
      }, 0);
    },
    checkboxes_filter() {
      return this.checkboxes.filter(checkbox => checkbox.checked);
    }
  },
  mounted() {
    const $fields = document.querySelectorAll("#option_group input");
    const fields = [];
    $fields.forEach($field => {
      const obj = {};

      obj["checked"] = false;
      obj["id"] = Number($field.id);
      obj["name"] = $field.name;
      obj["price"] = Number($field.dataset.price);
      
      fields.push(obj);
    });
    this.checkboxes = [ ...this.checkboxes, ...fields ];
  }
  
});

app.mount("#app");
