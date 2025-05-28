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
    return {};
  },
  methods: {
    handleMaximum(option_id, variant_id) {
      const not_checked = this.cart.getOption(option_id) === null;
      const is_maximum = variant.option_group.maximum === this.cart.getOptions(variant_id).length;

      console.log(this.cart.getOptions(variant_id).length);
      console.log(variant.option_group.maximum);
      
      console.log(is_maximum);
      
      return not_checked && is_maximum;
    },
    handleOption(e, itemId) {
      const checkbox = e.target;
      const option_id = checkbox.id.split("_")[1];
      
      if (checkbox.checked) {
        const hasItem = this.cart.hasItem(itemId);
        if (hasItem) {
          this.cart.addOption(
            itemId, 
            option_id, 
            checkbox.dataset.name, 
            checkbox.dataset.price
          );
        } else {
          this.cart.addItem(
            variant.id,
            variant.name,
            variant.price,
            variant.img,
            variant.discount,
            variant.link,
            this.checkboxes_filter
          );
        }
      } else {
        this.cart.removeOption(itemId, option_id);
      }
    },
    isChecked(optionId) {
      return this.cart.getOption(optionId);
    },
  },
  computed: {
    disable_check() {
      return this.check_fields.length === maximum_options;
    },
    checkboxes_filter() {
      const $fields = document.querySelectorAll("#option_group input");
      const fields = Array.from($fields)
      .filter($field => {
        return $field.checked;
      })
      .map($field => {
        const obj = {};

        obj["id"] = $field.id.split("_")[1];
        obj["name"] = $field.dataset.name;
        obj["price"] = Number($field.dataset.price);
        
        return obj;
      });
      
      return fields;
    },
  },
  mounted() {}
});

app.mount("#app");
