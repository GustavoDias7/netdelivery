import * as vue from "../vendor/vue";
const { createApp } = vue;

const app = createApp({
    delimiters: ["[[", "]]"],
    data() {
        return { 
            modal: {
                menu: false,
                logout: false
            } 
        }
    },
    methods: {
        openModal(name = "") {
            this.modal[name] = true
        },
        closeModal(name = "") {
            this.modal[name] = false
        },
        openLogout() {
            this.closeModal("menu")
            this.modal.logout = true
        },
        closeLogout() {
            this.modal.logout = false
        }
    },
});

app.mount("#app");
